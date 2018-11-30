import numpy as np
import SuperAgentClass as SuperAgent
import matplotlib.pyplot as plt
import matplotlib.animation as Animation
from Bird import *
from Rat import *




# todo: visualize the random walk of the rats
# todo: visualize the topological environmenth
class Lattice:


    def __init__(self, size, n_agents):
        self.size = size
        self.shape = (size, size)
        self.topological_matrix = np.zeros(self.shape)
        self.maximum_peak_height = 100
        self.location_matrix = [[[] for _ in range(size)] for _ in range(size)]
        self.n_birds = 100
        self.n_rats = 100
        self.bird_list = []
        self.rat_list = []
        self.nest_list = []
        self.step_count = 0
        self.plot_matrix = np.zeros(self.shape)
        self.fig, self.environment_ax, self.anim = self.init_plot()


    def init_topology(self):
        padding_percentage = .2
        island_bounds = (padding_percentage, self.size - padding_percentage)
        possible_topological_values = list(map(int, np.linspace(1, self.maximum_peak_height, self.maximum_peak_height)))
        island_topology = np.random.choice(possible_topological_values, size=island_bounds)
        # todo: fix the topological implementation
        # save this implementation for later versions though!


    def run_simulation(self):
        for i_step in range(self.n_steps):
            self.step()

    def init_agents(self):
        for i_bird in range(self.n_birds):
            x, y = gen_starting_pos()
            bird = Bird(x, y)
            nest = bird.place_nest()
            self.bird_list.append(bird)
            self.nest_list.append(nest)

        for i_rat in range(self.n_rats):
            x, y = self.gen_starting_pos()
            rat = Rat()
            self.rat_list.append(rat)


    def step(self):
        self.step_rats()
        #self.step_birds()
        #self.kill_birds_and_nests()
        #self.build_nests()
        #self.hatch()
        self.plot_matrix
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
        return np.random.randint(0, self.size, 2)

    def move_rats(self):
        for rat in self.rat_list:
            self.location_matrix[rat.x][rat.y].remove(rat)
            x, y =  rat.move()
            self.location_matrix[x][y].append(rat)


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

    def init_plot(self):
        fig = plt.figure()
        environment_ax = fig.add_subplot(111)
        anim = Animation.FuncAnimation(environment_ax, self.update_plot())
        return fig, environment_ax, anim

    def update_plot(self, i):
        self.environment_ax.pcolor(self.plot_matrix)
        pass



