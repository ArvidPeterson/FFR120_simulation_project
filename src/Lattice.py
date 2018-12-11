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
import datetime

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
        self.bird_lifetime = 5000
        self.hatch_time = 1000
        self.hatch_prob = 1/3
        self.nest_placement_delay = 200
        self.bird_list = []
        self.rat_list = []
        self.nest_list = []
        self.bird_population_record = []
        self.rat_population_record = []
        self.nest_population_record = []
        self.time_record = []

        # --- booleans for testing purposes --- #
        self.age_birds = False

        # --- plotting variables --- #
        self.water_color_index = 0
        self.land_color_index = 1
        self.rat_color_index = 2
        self.bird_color_index = 3
        self.nest_color_index = 4
        self.plot_matrix = np.zeros(self.shape)
        self.cmap = clr.ListedColormap(['steelblue', 'limegreen', 'red', 'yellow', 'black'])
        self.fig = plt.figure()
        self.environment_ax = self.fig.add_subplot(121)
        self.init_topology()
        self.population_dynamics_ax = self.fig.add_subplot(122)

        # ----- create plots for population dynamics
        self.rat_popu_plot, = self.population_dynamics_ax.plot([], [], color='red', label='Rat population')
        self.bird_popu_plot, = self.population_dynamics_ax.plot([], [], color='blue', label='Bird population')
        self.nest_popu_plot, = self.population_dynamics_ax.plot([], [], color='green', label='Nest population')
        self.population_dynamics_ax.set_ylim(0, max(self.n_rats, self.n_birds))

        plt.legend()
        plt.grid = True

        # ----- init the plotting
        self.anim = Animation.FuncAnimation(self.fig,
                                            self.update_plot,
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
            if i_step % 100 == 0:
                self.bird_population_record.append(len(self.bird_list))
                self.rat_population_record.append(len(self.rat_list))
                self.nest_population_record.append(len(self.nest_list))
                self.time_record.append(i_step)

    def step(self, i_step):
        self.step_count += 1
        self.move_and_age_rats()
        self.move_and_age_birds()
        self.kill_birds_and_nests()
        self.build_nests()
        self.age_and_hatch_nests()

    def init_agents(self):
        # spawn rat agents
        for i_rat in range(self.n_rats):
            x, y= self.gen_starting_pos()
            rat = Rat(self.size, x, y, self.topological_map, self.rat_lifetime)
            self.location_matrix[x][y].append(rat)
            self.plot_matrix[x,y] = self.rat_color_index
            self.rat_list.append(rat)

        for i_bird in range(self.n_birds):
            self.spawn_bird_and_nest()

    def age_and_hatch_nests(self):
        for nest in self.nest_list:
            nest.tick()
            if nest.counter > nest.hatch_time:
                if np.random.rand() < self.hatch_prob:
                    nest.hatch()
                    self.spawn_bird_and_nest()
                else:
                    nest.counter = 0
                
    def spawn_bird_and_nest(self):
        x, y = self.gen_unique_starting_pos()
        bird = Bird(self.size, x, y, self.topological_map, self.bird_lifetime)
        nest = Nest(self.size, x, y, self.topological_map, self.hatch_time, bird)
        bird.has_nest = True
        bird.nest = nest

        # --- keeping tabs of the agents! --- #
        self.nest_list.append(nest)
        self.bird_list.append(bird)
        self.location_matrix[x][y].append(bird)
        self.location_matrix[x][y].append(nest)
        # --- make it beautiful! --- #
        self.plot_matrix[x, y] = self.bird_color_index

    def gen_starting_pos(self):
        # generate a random x within island bounds
        x = np.random.randint((self.island_center - self.island_radius), (self.island_center + self.island_radius))

        # use trig to find y within island bounds as well!
        x_rel_to_circle = abs(self.island_center - x)
        y_rel_to_circle = math.sqrt(self.island_radius ** 2 - x_rel_to_circle ** 2)
        ymax = max((self.island_center + y_rel_to_circle), (self.island_center - y_rel_to_circle))
        ymin = min((self.island_center + y_rel_to_circle), (self.island_center - y_rel_to_circle))

        # if we're in the outskirts of the island
        if ymax == ymin:
            y = int(ymax) - 1 # todo: make sure that they're not placed on perimiter
        else:
            y = np.random.randint(ymin, ymax)

        return x, y

    def gen_unique_starting_pos(self):
        x, y = self.gen_starting_pos()
        while self.location_matrix[x][y]:
            x, y = self.gen_starting_pos()
        return x, y


    def move_and_age_rats(self):
        for rat in self.rat_list:
            rat.age += 1
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

    def move_and_age_birds(self):
        for bird in self.bird_list:
            bird.age += 1
            bird.move()  # sets the bird in or out of nest
            x, y = bird.x, bird.y
            if bird.is_in_nest:
                self.plot_matrix[x][y] = self.bird_color_index
            else:
                self.plot_matrix[x][y] = self.nest_color_index

            if self.age_birds:
                if bird.age > bird.life_time:
                    self.kill_agent(bird)

    def kill_agent(self, agent):  # used primarely when agents die from age
        x, y = agent.x, agent.y
        self.location_matrix[x][y].remove(agent)

        if isinstance(agent, Rat):
            self.rat_list.remove(agent)

        if isinstance(agent, Bird):
            self.bird_list.remove(agent)  # remove the bird
            if agent.has_nest:  # also remove nest which otherwise is left dangling
                self.nest_list.remove(agent.nest)
                self.location_matrix[x][y].remove(agent.nest)

        if not self.location_matrix[x][y]:
            self.plot_matrix[x][y] = self.land_color_index


    def kill_birds_and_nests(self):
        self.range_vision_kill_function()

    def range_vision_kill_function(self):  # kills nest neighbouring to a rat
        for rat in self.rat_list:
            position_list = np.array([[rat.x - 1, rat.y], [rat.x + 1, rat.y], [rat.x, rat.y - 1], [rat.x, rat.y + 1]])

            position_list[position_list < 0] = 0  # limit the indices to be within grid
            position_list[position_list > self.size - 1] = self.size

            for pos in position_list:
                x = pos[0]
                y = pos[1]
                for agent in self.location_matrix[pos[0]][pos[1]]:

                    if isinstance(agent, Nest):  # TODO: check for nestless birds as well
                        try:
                            if agent.parent.is_in_nest:  # if bird in nest, kill the bird
                                self.location_matrix[x][y].remove(agent.parent)
                                self.bird_list.remove(agent.parent)
                            else:
                                agent.parent.has_nest = False  # if parent bird not in nest let it continue
                        except ValueError:
                            print('Missing agent')
                        self.location_matrix[x][y].remove(agent)  # anyway kill the nest
                        self.nest_list.remove(agent)

        # --- reset the color if successful kill! --- #
                if not self.location_matrix[x][y]:
                    self.plot_matrix[x][y] = self.land_color_index

    def build_nests(self):
        for bird in self.bird_list:
            if not bird.has_nest:

                #count the delay for the bird
                if bird.nest_placement_timer < self.nest_placement_delay:
                    bird.nest_placement_timer += 1
                else:
                    x, y = bird.x, bird.y

                    # this moves the bird as by defalut!
                    self.location_matrix[x][y].remove(bird)
                    nest = bird.place_nest(self.nest_list)
                    x, y = bird.x, bird.y
                    self.nest_list.append(nest)
                    self.location_matrix[x][y].append(nest)
                    self.location_matrix[x][y].append(bird)

    def update_plot(self, i):
        #self.environment_ax.pcolorfast(self.plot_matrix, vmin=0, vmax=5, cmap=self.cmap)
        self.environment_ax.set_title("time: {}".format(self.step_count))

        self.rat_popu_plot.set_xdata(self.time_record)
        self.rat_popu_plot.set_ydata(self.rat_population_record)

        self.bird_popu_plot.set_xdata(self.time_record)
        self.bird_popu_plot.set_ydata(self.bird_population_record)

        self.nest_popu_plot.set_xdata(self.time_record)
        self.nest_popu_plot.set_ydata(self.nest_population_record)

        tmp_m = max(self.time_record + [10])
        self.population_dynamics_ax.set_xlim(0, tmp_m)

        title_str = 'n_rats: ' + str(len(self.rat_list)) + ', n_birds: ' + str(len(self.bird_list)) + ', n_nests: ' \
                    + str(len(self.nest_list))

        self.population_dynamics_ax.set(title=title_str)

        plt.draw()
        plt.pause(1e-17)


if __name__ == '__main__':
    print(datetime.datetime.now())
    lattice_size = 500
    n_birds = 100
    n_rats = 100
    n_sim_steps = int(1e5)
    sim = Lattice(lattice_size, n_rats, n_birds, n_sim_steps)
    sim.start()
    plt.show()

