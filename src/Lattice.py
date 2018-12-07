import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as Animation
import matplotlib.colors as clr
from Bird import *
from Rat import *

class Lattice:


    def __init__(self, size, n_rats, n_birds):
        self.size = size
        self.shape = (size, size)
        self.topological_map = np.zeros(self.shape)
        self.island_radius = .45 * self.size
        self.island_center = .5 * self.size
        self.maximum_peak_height = 100
        self.location_matrix = [[[] for _ in range(size)] for _ in range(size)]
        self.n_birds = n_birds
        self.n_rats = n_rats
        self.rat_lifetime = 100
        self.bird_lifetime = 100
        self.bird_list = []
        self.rat_list = []
        self.nest_list = []
        self.step_count = 0


        # --- plotting variables --- #
        self.water_color_index = 0
        self.land_color_index = 1
        self.rat_color_index = 2
        self.bird_color_index = 3
        self.nest_color_index = 4

        self.plot_matrix = np.zeros(self.shape)
        self.cmap = clr.ListedColormap(['blue', 'green', 'peru', 'yellow', 'black'])
        self.fig, self.environment_ax = plt.subplots(1, 1)
        self.anim = Animation.FuncAnimation(self.fig,
                                       self.update_plot,
                                       blit=False,
                                        interval=500)


<<<<<<< HEAD
    def init_topology(self):
=======

    def init_topology(self):
        padding_percentage = .2
        island_bounds = (padding_percentage, self.size - padding_percentage)
        possible_topological_values =  np.linspace(1, self.maximum_peak_height, self.maximum_peak_height, dtype=int)
        island_topology = np.random.choice(possible_topological_values, size=island_bounds)
        # todo: fix the topological implementation
        # save this implementation for later versions though!


    def run_simulation(self):
        for i in range(int(1e3)):
            self.plot_matrix = np.random.rand(*self.shape)
        #for i_step in range(self.n_steps):
         #   self.step()

        island_radius = .45 * self.size
        island_center = .5 * self.size
>>>>>>> 599dee42e1a4128c4b3573a3c2475ce207d3eac2
        self.plot_matrix = np.zeros(self.shape)
        self.topological_map = np.zeros(self.shape)
        for x in range(self.size):
            for y in range(self.size):
                if math.sqrt((x - self.island_center) ** 2 + (y - self.island_center) ** 2)  < self.island_radius:
                    self.plot_matrix[x, y] = self.land_color_index
                    self.topological_map[x, y] = 1

        # possible_topological_values =  np.linspace(1, self.maximum_peak_height, self.maximum_peak_height, dtype=int)
        # island_topology = np.random.choice(possible_topological_values, size=island_bounds)


    def run_simulation(self):
        self.init_topology()
        self.init_agents()
        #for i_step in range(self.n_sim_steps):
        #    self.step(i_step)
        #    self.step_count = i_step

    def init_agents(self):
        '''
        for i_bird in range(self.n_birds):
            x, y = self.gen_starting_pos()
            bird = Bird(x, y)
            nest = bird.place_nest()
            self.bird_list.append(bird)
            self.nest_list.append(nest)
        '''

        for i_rat in range(self.n_rats):
            x_start, y_start = self.gen_starting_pos()
            rat = Rat(x_start, y_start, self.topological_map, self.rat_lifetime)
            self.plot_matrix[x_start, y_start] = self.rat_color_index
            print('finished initializing rat {}'.format(i_rat))
            self.rat_list.append(rat)


    def step(self):
        self.step_rats()
        #self.step_birds()
        #self.kill_birds_and_nests()
        #self.build_nests()
        #self.hatch()
        self.update_plot_matrix
        self.step_count += 1

    def hatch(self):
        for nest in self.nest_list:
            if nest.counter > nest.hatch_time:
                x, y = nest.hatch()
                # --- spawn a bird ! --- #
                x, y = self.gen_starting_pos()
                bird = Bird(x,y)
                self.bird_list.append(bird)
                self.location_matrix[x][y].append(bird)

    def gen_starting_pos(self):
        x, y = np.random.randint(0, self.size, 2)
        while math.sqrt((x - self.island_center) ** 2 + (y - self.island_center) ** 2) > self.island_radius:
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

            x, y =  rat.move()

            self.location_matrix[rat.x][rat.y].remove(rat)
            x, y = rat.move()
            self.location_matrix[x][y].append(rat)
            self.plot_matrix[x][y] = self.rat_color_index

    def move_birds(self):
        for bird in self.bird_list:
            bird.step()

    def kill_birds_and_nests(self):
        for i_nest, nest in enumerate(self.nest_list):
            x, y = nest.x, nest.y
            # --- check if there is a rat at the nest site --- #
            if any(filter(lambda x: isinstance(x, Rat), self.location_matrix[x][y])):
                for item in self.location_matrix[x][y]:
                    # --- remove all the birds on the site --- #
                    if isinstance(item, Bird):
                        self.bird_list.remove(item)

                # --- finish by removing the nest --- #
                self.nest_list.remove(nest)

    def build_nests(self):
        for bird in self.bird_list:
            if not bird.has_nest:
                nest = bird.place_nest(self.nest_list)
                self.nest_list.append(nest)

    def update_plot(self, i):
        # --- we probably want to use trisurf here! --- #
        self.plot_matrix = np.random.randint(0, 4, size=self.shape)
        self.environment_ax.pcolorfast(self.plot_matrix, vmin=0, vmax=4, cmap=self.cmap)


if __name__ == '__main__':
    lattice_size = 200
    n_birds = 10
<<<<<<< HEAD
    n_rats = 200
    n_sim_steps = int(1e3)
    lattice = Lattice(lattice_size, n_rats, n_birds, n_sim_steps)
    lattice.run_simulation()
    plt.show()
=======
    n_rats = 10
    lattice = Lattice(lattice_size, n_rats, n_birds)
>>>>>>> 599dee42e1a4128c4b3573a3c2475ce207d3eac2
