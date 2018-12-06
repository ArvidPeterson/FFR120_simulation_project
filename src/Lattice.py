import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as Animation
import matplotlib.colors as clr
from Bird import *
from Rat import *

def gen_colormap():
    cdict = {'red': ((0,0,0), (1,0,0)),
             'green': ((0,0,0),(0,1,0)),
             'blue': ((0,0,0),(0,1,0)),
             'brown': ((0,0,0),(210/255, 180/255, 140/255)),
             'yellow': ((0,0,0), (0, 1, 1))}
    return clr.LinearSegmentedColormap.from_list('main_color', cdict)

# todo: visualize the random walk of the rats
# todo: visualize the topological environment
class Lattice:


    def __init__(self, size, n_rats, n_birds):
        self.size = size
        self.shape = (size, size)
        self.topological_matrix = np.zeros(self.shape)
        self.maximum_peak_height = 100
        self.location_matrix = [[[] for _ in range(size)] for _ in range(size)]
        self.n_birds = n_birds
        self.n_rats = n_rats
        self.bird_list = []
        self.rat_list = []
        self.nest_list = []
        self.step_count = 0
        self.plot_matrix = np.zeros(self.shape)
        self.cmap = gen_colormap()
        self.fig, self.environment_ax = plt.subplots(1, 1)
        self.anim = Animation.FuncAnimation(self.fig,
                                       self.update_plot,
                                       blit=False,
                                        interval=500)



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

    def init_agents(self):
        for i_bird in range(self.n_birds):
            x, y = self.gen_starting_pos()
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

    def update_plot(self, i):
        # --- we probably want to use trisurf here! --- #
        self.plot_matrix = np.random.randint(0, 4, size=self.shape)
        self.environment_ax.pcolorfast(self.plot_matrix, vmin=0, vmax=4, cmap=self.cmap)


if __name__ == '__main__':
    lattice_size = 1000
    n_birds = 10
    n_rats = 10
    #lattice = Lattice(lattice_size, n_rats, n_birds)
    fig, ax = plt.subplots()
    ax.pcolorfast(np.random.randint(0, 4, size=(3,3)), vmin=0, vmax=4,cmap=gen_colormap())

    plt.show()
    #lattice.run_simulation()
