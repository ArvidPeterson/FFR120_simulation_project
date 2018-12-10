import logging
import math
import numpy as np
import matplotlib
matplotlib.use('qt4agg')
import matplotlib.pyplot as plt
import matplotlib.animation as Animation
import matplotlib.colors as clr
from threading import Thread
from Bird import *
from Rat import *

class Lattice(Thread):


    def __init__(self, size, n_rats, n_birds, n_sim_steps, *,
                 plot_environment=True, plot_populations=False):
        Thread.__init__(self)
        # --- environment and general sim variables --- #
        self.size = size
        self.shape = (size, size)
        self.topological_map = np.zeros(self.shape)
        self.island_radius = .45 * self.size
        self.island_center = .5 * self.size
        self.maximum_peak_height = 100
        self.location_matrix = [[[] for _ in range(size)] for _ in range(size)]
        self.step_count = 0
        self.n_sim_steps = n_sim_steps

        # --- agent variables --- #
        self.n_birds = n_birds
        self.n_rats = n_rats
        self.rat_lifetime = 100
        self.bird_lifetime = 100
        self.bird_list = []
        self.rat_list = []
        self.nest_list = []
        self.bird_population_record = []
        self.rat_population_record = []
        self.nest_population_record = []
        self.time_record = []

        # --- plotting variables --- #
        self.water_color_index = 0
        self.land_color_index = 1
        self.rat_color_index = 2
        self.bird_color_index = 3
        self.nest_color_index = 4
        self.plot_matrix = np.zeros(self.shape)
        self.cmap = clr.ListedColormap(['blue', 'green', 'peru', 'yellow', 'black'])
        self.fig = plt.figure()
        self.environment_ax = self.fig.add_subplot(121)
        self.population_dynamics_ax = self.fig.add_subplot(122)
        self.init_topology()
        #self.im = plt.imshow(self.plot_matrix, animated=True, cmap=self.cmap, vmin=0, vmax=5)
        self.frames = [self.plot_matrix]

        # --- plot ---

        self.anim = Animation.FuncAnimation(self.fig,
                                            self.update_plot,
                                            frames=range(0, self.n_sim_steps),
                                            blit=False,
                                            interval=50)

    def init_topology(self):
        self.topological_map = np.zeros(self.shape)
        for x in range(self.size):
            for y in range(self.size):
                if math.sqrt((x - self.island_center) ** 2 + (y - self.island_center) ** 2)  < self.island_radius:
                    self.plot_matrix[x, y] = self.land_color_index
                    self.topological_map[x, y] = 1

    def run(self):
        self.init_agents()
        for i_step in range(self.n_sim_steps):
            # --- perform current simulation step --- #
            self.step(i_step)
            self.step_count = i_step

            # --- save data so that it can be visualized async --- #
            self.frames.append(np.copy(self.plot_matrix))
            self.bird_population_record.append(len(self.bird_list))
            self.rat_population_record.append(len(self.rat_list))
            self.nest_population_record.append(len(self.nest_list))
            self.time_record.append(i_step)

    def step(self, i_step):
        self.step_count += 1
        self.move_rats()
        self.move_birds()
        self.kill_birds_and_nests()
        self.build_nests()
        self.hatch()

    def init_agents(self):

        # --- init rats --- #
        for i_rat in range(self.n_rats):
            x_start, y_start = self.gen_starting_pos()
            rat = Rat(self.size, x_start, y_start, self.topological_map, self.rat_lifetime)
            self.location_matrix[x_start][y_start].append(rat)
            self.plot_matrix[x_start, y_start] = self.rat_color_index
            self.rat_list.append(rat)

        # --- init birds and nests --- #
        for i_bird in range(self.n_birds):
            x_start, y_start = self.gen_starting_pos()
            bird = Bird(self.size, x_start, y_start, self.topological_map)
            self.location_matrix[x_start][y_start].append(bird)
            self.plot_matrix[x_start, y_start] = self.bird_color_index
            nest = bird.place_nest(self.nest_list)
            self.nest_list.append(nest)
            self.bird_list.append(bird)



    def hatch(self):
        for nest in self.nest_list:
            if nest.counter > nest.hatch_time:
                x, y = nest.hatch()
                # --- spawn a bird ! --- #
                x, y = self.gen_starting_pos()
                bird = Bird(x, y)
                self.bird_list.append(bird)
                self.location_matrix[x][y].append(bird)

    # -- for generating independent starting positions --- #
    def gen_starting_pos(self):
        x, y = np.random.randint(0, self.size, 2)
        while math.sqrt((x - self.island_center) ** 2 + (y - self.island_center) ** 2) > self.island_radius:
            while not self.location_matrix[x][y]: # make sure site is empy
                x, y = np.random.randint(0, self.size, 2)
        return x, y

    def move_rats(self):
        for rat in self.rat_list:
            x, y = rat.x, rat.y
            self.location_matrix[x][y].remove(rat)

            # if there are no rats left on the old location
            # color the location green!
            for agent in self.location_matrix[x][y]:
                if isinstance(agent, Rat):
                    break
            else:
                self.plot_matrix[x][y] = self.land_color_index

            x, y = rat.move()
            self.location_matrix[x][y].append(rat)
            self.plot_matrix[x][y] = self.rat_color_index

    def move_birds(self):
        for bird in self.bird_list:
            bird.move()  # sets the bird in or out of nest
            x, y = bird.x, bird.y
            if bird.is_in_nest:
                self.plot_matrix[x][y] = self.bird_color_index
            else:
                self.plot_matrix[x][y] = self.nest_color_index

    def kill_birds_and_nests(self):
        for i_nest, nest in enumerate(self.nest_list):
            x, y = nest.x, nest.y

            # --- list all agents on the site with the nest --- #
            bird_list = []
            rat_list = []
            for agent_on_site in self.location_matrix[x][y]:
                if isinstance(agent_on_site, Rat):
                    rat_list.append(agent_on_site)
                    tmp_bird_list = self.get_birds_on_neighbouring_positions(agent_on_site.x, agent_on_site.y)
                    bird_list.append(tmp_bird_list)
                if isinstance(agent_on_site, Bird):
                    bird_list.append(agent_on_site)

            # if there's a rat on the current site
            if rat_list:  # TODO: implement removing birds from neighbouring positions
                    for bird in bird_list:
                        if bird.is_in_nest:
                            self.bird_list.remove(bird)
                            self.nest_list.remove(nest)
                        else:
                            bird.has_nest = False
                            self.nest_list.remove(nest)
                        self.location_matrix[x][y].remove(bird)
                        try:
                            self.location_matrix[x][y].remove(nest)
                        except ValueError:
                            logging.exception("something wrong with the nest removal")

    def get_birds_on_neighbouring_positions(self, x, y):

        position_list = np.array([[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]])

        position_list[position_list < 0] = 0

        position_list[position_list > self.size - 1] = self.size
        bird_list = []

        for pos in position_list:  # loop over neighbouring birds
            for agent in self.location_matrix[pos[0]][pos[1]]:
                if isinstance(agent, Bird):
                    bird_list.append(agent)

        return bird_list

    def build_nests(self):
        for bird in self.bird_list:
            if not bird.has_nest:
                x, y = bird.x, bird.y
                nest = bird.place_nest(self.nest_list)
                self.nest_list.append(nest)
                self.location_matrix[x][y].append(nest)

    def update_plot(self, i):
        self.environment_ax.pcolorfast(self.plot_matrix, vmin=0, vmax=5, cmap= self.cmap)
        self.environment_ax.set_title("time: {}".format(self.step_count))
        self.population_dynamics_ax.plot(self.time_record, self.bird_population_record)
        self.population_dynamics_ax.plot(self.time_record, self.rat_population_record)
        self.population_dynamics_ax.plot(self.time_record, self.nest_population_record)


if __name__ == '__main__':
    lattice_size = 200
    n_birds = 100
    n_rats = 1000
    n_sim_steps = int(1e4)
    sim = Lattice(lattice_size, n_rats, n_birds, n_sim_steps)
    sim.start()
    plt.show()
