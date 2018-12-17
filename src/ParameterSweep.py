import numpy as np
from matplotlib import pyplot as plt
from Lattice import Lattice

# which vars should be fixed?
# lattice_size, n_sim_steps,
# increase both pops
# mixed increase/decrease
class ParamSweep:

    def __init__(self, lattice_size, n_sim_steps,
                 n_birds_range, n_rats_range,
                 hatch_time, rat_initial_energy,
                 nest_nutritonal_value, nest_placement_delay):


        self.size = lattice_size
        self.n_sim_steps = n_sim_steps
        self.n_birds_range = n_birds_range
        self.n_rats_range = n_rats_range
        self.nest_placement_delay = nest_placement_delay
        self.nutritional_value = nest_nutritonal_value
        self.nest_placement_delay = nest_placement_delay
        self.hatch_time = hatch_time
        self.rat_energy = rat_initial_energy
        self.run_simulation()


    def run_simulation(self):
        for nrats in self.n_rats_range:
            for nbirds in self.n_birds_range:
                self.sim = Lattice(self.size, nrats, nbirds,
                                       self.n_sim_steps, self.hatch_time,
                                       self.nest_placement_delay, self.rat_energy,
                                       self.nutritional_value, plot_environment=False,
                                       plot_populations=False)
                self.sim.start()
                bird_pop, rat_pop, nest_pop, time = self.sim.join()
                fig, ax = plt.subplots()
                plt.plot(time, bird_pop, color='blue', label='Bird population')
                plt.plot(time, nest_pop, color='green', label='Nest population')
                plt.plot(time, rat_pop, color='red', label='Rat population')
                plt.legend()
                ax.set_xlabel('Time steps')
                ax.set_ylabel('Populations')
                ax.set_title('initial bird population: {}, initial rat population: {}\n'
                             'nest placement delay: {}, nest nutritional value: {}'.format(
                    nbirds, nrats, self.nest_placement_delay, self.nutritional_value
                ))
                fname = 'nbirds{}nrats{}'.format(nbirds, nrats)
                self.save_plot(fig, fname)

                #plt.close(fig)

    def save_plot(self, fig, name):
        dir = 'save_data/' + str(name) + '.png'
        fig.savefig(dir)


if __name__ == '__main__':
    lattice_size = 200
    hatch_time = 200
    nutritional_value = 10
    rat_initial_energy = 100
    nest_placement_delay = 100
    n_sim_steps = int(1e2)
    n_rats_range = [5]
    n_birds_range = [20]
    sweep = ParamSweep(lattice_size, n_sim_steps, n_birds_range,
                       n_rats_range, hatch_time, rat_initial_energy,
                       nutritional_value, nest_placement_delay)