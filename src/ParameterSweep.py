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
                sim = Lattice(self.size, nrats, nbirds,
                                       self.n_sim_steps, self.hatch_time,
                                       self.nest_placement_delay, self.rat_energy,
                                       self.nutritional_value, plot_environment=False,
                                       plot_populations=True)
                sim.start()
                sim.join()
                self.save_plot('test_plot')

    def save_plot(self, name):
        dir = 'save_data/' + str(name) + '.png'
        plt.savefig(dir)


if __name__ == '__main__':
    lattice_size = 200
    hatch_time = 200
    nutritional_value = 100
    rat_initial_energy = 100
    nest_placement_delay = 100
    n_sim_steps = int(1e3)
    n_rats_range = [5, 10]
    n_birds_range = [100, 200]
    sweep = ParamSweep(lattice_size, n_sim_steps, n_birds_range,
                       n_rats_range, hatch_time, rat_initial_energy,
                       nutritional_value, nest_placement_delay)