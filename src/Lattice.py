import time
import math
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as Animation
import matplotlib.colors as clr
from threading import Thread
from Bird import *
from Rat import *
import datetime
import random


class Lattice(Thread):

    def __init__(self, size, n_rats, n_birds, n_sim_steps,
                 hatch_time, nest_placement_delay,
                 rat_initial_energy, nutritional_value_of_nests,  *,
                 plot_environment=False, plot_populations=True,
                 population_plot_title='population'):
        Thread.__init__(self)
        # --- environment and general sim variables --- #
        self.size = size
        self.shape = (size, size)
        self.topological_map = np.zeros(self.shape)
        self.island_radius = .45 * self.size
        self.island_center = .5 * self.size
        self.maximum_peak_height = 100
        self.location_matrix = [[[] for _ in range(size)] for _ in range(size)]
        self.step_count = 0  # time step
        self.n_sim_steps = n_sim_steps

        # --- agent variables --- #
        self.n_birds = n_birds
        self.n_rats = n_rats
        self.rat_lifetime = 100
        self.initial_rat_energy = 100
        self.nest_nutritional_value = nutritional_value_of_nests
        self.bird_lifetime = 5000
        self.hatch_time = hatch_time #1000
        self.nest_placement_delay = nest_placement_delay #200
        self.bird_list = []
        self.rat_list = []
        self.nest_list = []
        self.bird_population_record = []
        self.rat_population_record = []
        self.nest_population_record = []
        self.time_record = []
        self.available_nesting_sites = set()
        self.island_positions = set()

        # --- booleans for testing purposes --- #
        self.age_birds = False

        # --- plotting variables --- #
        self.plot_environment = plot_environment
        self.plot_populations = plot_populations

        self.water_color_index = 0
        self.land_color_index = 1
        self.rat_color_index = 2
        self.bird_color_index = 3
        self.nest_color_index = 4
        self.max_ever_population = 1

        self.plot_matrix = np.zeros(self.shape)
        self.cmap = clr.ListedColormap(['aqua', 'g','red', 'yellow', 'black'])

        if self.plot_populations or self.plot_environment:
            self.fig = plt.figure()

        if self.plot_environment and self.plot_populations:
            self.environment_ax = self.fig.add_subplot(121)
            self.population_dynamics_ax = self.fig.add_subplot(122)
        elif self.plot_environment:
            self.environment_ax = self.fig.add_subplot(111)
        elif self.plot_populations:
            self.population_dynamics_ax = self.fig.add_subplot(111)

        self.init_topology()

        # ----- create plots for population dynamics
        if self.plot_populations:
            self.rat_popu_plot, = self.population_dynamics_ax.plot([], [], color='red', label='Rat population')
            self.bird_popu_plot, = self.population_dynamics_ax.plot([], [], color='blue', label='Bird population')
            self.nest_popu_plot, = self.population_dynamics_ax.plot([], [], color='green', label='Nest population')
            plt.legend()
            plt.grid = True

        # ----- init the plotting
        if self.plot_environment or self.plot_populations:
            plt.legend()
            plt.grid = True
            self.anim = Animation.FuncAnimation(self.fig,
                                                self.update_plot,
                                                blit=False,
                                                interval=50)

    def init_topology(self):
        self.topological_map = np.zeros(self.shape)
        for x in range(self.size):
            for y in range(self.size):
                if math.sqrt((x - self.island_center) ** 2 + (y - self.island_center) ** 2) < self.island_radius:
                    # color
                    self.plot_matrix[x, y] = self.land_color_index
                    self.topological_map[x, y] = 1
                    # keep the books
                    self.island_positions.add((x, y))
                    self.available_nesting_sites.add((x, y))


    def run(self):  # since Lattice inherits Thread this is called when doing Lattice.start()
        self.init_agents()
        for i_step in range(self.n_sim_steps):
            # --- perform current simulation step --- #
            start = time.process_time()
            self.step(i_step)
            self.step_count = i_step  # why is this changed in two  places ?

            # --- save data so that it can be visualized async --- #
            if i_step % 10 == 0:
                self.bird_population_record.append(len(self.bird_list))
                self.rat_population_record.append(len(self.rat_list))
                self.nest_population_record.append(len(self.nest_list))
                self.time_record.append(i_step)
                stop = time.process_time()
                #print('iteration: {} took: {}'.format(i_step, stop - start))
            if i_step % 500 == 0:
                print('done with {} iteration'.format(i_step))
            # if rats or birds are extinct the simulation stops
            n_alive_birds = len(self.bird_list)
            n_alive_rats = len(self.rat_list)

            if n_alive_birds * n_alive_rats == 0:
                # self.anim.event_source.stop()  # find a way to stop updating in the other thread
                break  # quit simulation

            stop = time.process_time()
            # print('time_elapsed {} for iteration {}'.format(stop - start, i_step))

        self.bird_population_record.append(len(self.bird_list))
        self.rat_population_record.append(len(self.rat_list))
        self.nest_population_record.append(len(self.nest_list))
        self.time_record.append(i_step)

        return self.bird_population_record,\
                self.rat_population_record,\
                self.nest_population_record,\
                self.time_record# Returns to make statistics

    def join(self):
        Thread.join(self)
        return self.bird_population_record, self.rat_population_record, self.nest_population_record, self.time_record

    def step(self, i_step):
        self.move_and_age_rats()
        self.move_and_age_birds()
        self.range_vision_kill_function()
        self.build_nests()
        self.age_and_hatch_nests()
        print(self.step_count)

    def init_agents(self):
        for i_rat in range(self.n_rats):
            self.spawn_rat()

        for i_bird in range(self.n_birds):
            self.spawn_bird_and_nest()

    def spawn_rat(self):
        x, y = self.gen_rat_starting_pos()
        rat = Rat(self.size, x, y, self.topological_map, self.rat_lifetime, self.initial_rat_energy)
        self.location_matrix[x][y].append(rat)
        self.plot_matrix[x, y] = self.rat_color_index
        self.rat_list.append(rat)

    def age_and_hatch_nests(self):
        for nest in self.nest_list:
            nest.tick()
            if nest.counter > nest.hatch_time:
                nest.hatch()
                self.spawn_bird_and_nest()
                nest.counter = 0
                
    def spawn_bird_and_nest(self):
        x, y = self.gen_bird_starting_pos()
        if x > 0 and y > 0:
            bird = Bird(self.size, x, y, self.topological_map, self.bird_lifetime)
            nest = Nest(self.size, x, y, self.topological_map, self.hatch_time, bird)
            bird.has_nest = True
            bird.nest = nest

            # keep tabs of the book-keeping data
            self.nest_list.append(nest)
            self.bird_list.append(bird)
            self.location_matrix[x][y].append(bird)
            self.location_matrix[x][y].append(nest)
            self.recolor(x, y)

    def gen_rat_starting_pos(self):
        pos = random.sample(self.island_positions, 1)
        return pos[0]

    def gen_bird_starting_pos(self):

        if not self.available_nesting_sites:
            return -1, -1

        pos = random.sample(self.available_nesting_sites, 1)
        self.available_nesting_sites.discard(pos[0])

        return pos[0] # need this here as the tuple is wrapped in list for some reason

    def move_and_age_rats(self):
        for rat in self.rat_list:
            rat.age += 1
            rat.energy -= 1
            x, y = rat.x, rat.y
            self.location_matrix[x][y].remove(rat)
            self.recolor(x, y)  # recolor the old rat location
            x, y = rat.move()
            self.recolor(x, y)  # color the new rat location
            self.location_matrix[x][y].append(rat)
            self.plot_matrix[x][y] = self.rat_color_index
            if rat.energy < 0:  # TODO: Seems like there is a bug, no killing of rats
                self.kill_agent(rat)

            if rat.should_spawn_new_rat:
                self.spawn_rat()
                rat.has_spawned()

    def move_and_age_birds(self):
        for bird in self.bird_list:
            bird.age += 1
            bird.move()  # sets the bird in or out of nest
            x, y = bird.x, bird.y
            self.recolor(x, y)
            if self.age_birds:
                if bird.age > bird.life_time:
                    self.kill_agent(bird)

    def kill_agent(self, agent):  # used primarely when agents die from age
        x, y = agent.x, agent.y
        self.location_matrix[x][y].remove(agent)

        if isinstance(agent, Rat):
            self.rat_list.remove(agent)

        if isinstance(agent, Bird):
            self.available_nesting_sites.add((x, y))
            self.bird_list.remove(agent)  # remove the bird
            if agent.has_nest:  # also remove nest which otherwise is left dangling
                self.nest_list.remove(agent.nest)
                self.location_matrix[x][y].remove(agent.nest)

        self.recolor(x, y)

    def range_vision_kill_function(self):  # kills nest neighbouring to a rat
        for rat in self.rat_list:
            position_list = np.array([[rat.x - 1, rat.y],
                                      [rat.x + 1, rat.y],
                                      [rat.x, rat.y - 1],
                                      [rat.x, rat.y + 1]])

            position_list[position_list < 0] = 0  # limit the indices to be within grid
            position_list[position_list > self.size - 1] = self.size

            for pos in position_list:
                x = pos[0]
                y = pos[1]
                for agent in self.location_matrix[pos[0]][pos[1]]:

                    if isinstance(agent, Nest):  # rats kill birds that are in nests not 'free' birds who fly away..
                        rat.energy += self.nest_nutritional_value
                        if agent.parent.is_in_nest:  # if bird in nest, kill the bird
                            self.location_matrix[x][y].remove(agent.parent)
                            self.bird_list.remove(agent.parent)
                        else:
                            agent.parent.has_nest = False  # if parent bird not in nest let it continue
                        self.location_matrix[x][y].remove(agent)  # anyway kill the nest
                        self.nest_list.remove(agent)

                self.recolor(x, y)

    def build_nests(self):
        for bird in self.bird_list:
            if not bird.has_nest:

                # count the delay for the bird
                if bird.nest_placement_timer < np.random.normal(self.nest_placement_delay, 1):
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

        if self.plot_environment:
            self.environment_ax.pcolorfast(self.plot_matrix, vmin=0, vmax=5, cmap=self.cmap)
            self.environment_ax.set_title("time: {} (days)".format(self.step_count))
            self.environment_ax.set_xlabel('x')
            self.environment_ax.set_ylabel('y')
            self.environment_ax.set_aspect('equal')

        if self.plot_populations:
            self.rat_popu_plot.set_xdata(self.time_record)
            self.rat_popu_plot.set_ydata(self.rat_population_record)
            self.bird_popu_plot.set_xdata(self.time_record)
            self.bird_popu_plot.set_ydata(self.bird_population_record)
            self.nest_popu_plot.set_xdata(self.time_record)
            self.nest_popu_plot.set_ydata(self.nest_population_record)

            tmp_m = max(self.time_record + [10])
            self.population_dynamics_ax.set_xlim(0, tmp_m)

            n_nests = len(self.nest_list)
            n_birds = len(self.bird_list)
            n_rats = len(self.rat_list)

            title_str = 'Time: ' + str(self.step_count) + ' n_rats: ' + str(n_rats) + ', n_birds: ' + str(n_birds) + ', n_nests: ' \
                        + str(n_nests)

            self.population_dynamics_ax.set(title=title_str)
            self.population_dynamics_ax.set_xlabel('Time steps')
            self.population_dynamics_ax.set_ylabel('Population sizes')
            self.rat_popu_plot.set_xdata(self.time_record)
            self.rat_popu_plot.set_ydata(self.rat_population_record)

            # --- set the y limit properly
            max_pop = max([n_birds, n_rats, n_nests])

            if max_pop > self.max_ever_population:
                self.max_ever_population = max_pop

            self.population_dynamics_ax.set_ylim(0, self.max_ever_population + 100)

        plt.draw()
        plt.pause(1e-17)

    def recolor(self, x, y):
        if Rat in map(type, self.location_matrix[x][y]):
            self.plot_matrix[x][y] = self.rat_color_index
        elif Bird in map(type, self.location_matrix[x][y]):
            self.plot_matrix[x][y] = self.bird_color_index
        elif Nest in map(type, self.location_matrix[x][y]):
            self.plot_matrix[x][y] = self.nest_color_index
        else:
            self.plot_matrix[x][y] = self.land_color_index


if __name__ == '__main__':
    print(datetime.datetime.now())
    lattice_size = 200
    n_birds = 500
    n_rats = 10
    n_sim_steps = int(1e4)
    nest_placement_delay = 25
    hatch_time = 20

    rat_initial_energy = 5

    nutritional_value_of_nests = 5

    sim = Lattice(lattice_size, n_rats, n_birds,
                  n_sim_steps, hatch_time, nest_placement_delay,
                  rat_initial_energy, nutritional_value_of_nests,
                  plot_environment=False,  plot_populations=True)
    start = time.process_time()
    sim.start()
    #_, _, _, time_record = sim.join()
    #stop = time.process_time()
    #print('entire time: {}'.format(stop - start))
    #print('time-record-len: {}'.format(len(time_record)))

    plt.show()

# todo: rats die if they don't have food   ---  DONE!
# todo: larger blobs for the agents so that they're better visualized  ---  njaaaaaaaeh
# todo: fun for recoloring  --- DONE!
