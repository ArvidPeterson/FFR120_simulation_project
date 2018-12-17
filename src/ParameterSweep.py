from matplotlib import pyplot as plt
from Lattice import Lattice

# which vars should be fixed?
# lattice_size, n_sim_steps,
# increase both pops
# mixed increase/decrease
class ParamSweep:

    def __init__(self, lattice_size, n_sim_steps,
                 n_birds_range, n_rats_range,
                 hatch_prob, hatch_time):
        self.plot_title = ""

        self.lattice_size = lattice_size
        self.n_sim_steps = n_sim_steps
        self.n_birds_range = n_birds_range
        self.n_rats_range = n_rats_range


        pass

    def run_simulation(self):
        for nrats in self.n_rats_range:
            for nbirds in self.n_birds_range:
                self.lattice = Lattice(self.size, nrats, nbirds,
                                       self.n_sim_steps, self.hatch_time,
                                       self.nest_placement_delay, self.rat_energy,
                                       self.nutritional_value, plot_environment=False,
                                       plot_populations=False)
                self.save_plot()

    def save_plot(self, name):
        dir = 'save_data/' + str(name)
        plt.savefig(dir)
# todo: verify that save_plots works
# todo:

if __name__ == '__main__':
    lattice_size = 200
    n_birds = 100
    n_rats = 50
    n_sim_steps = int(1e4)
    nest_placement_delay = 200
    hatch_time = 200
    hatch_prob = .5
    ylim = 200
    rat_initial_energy = 1000
    nutritional_value_of_nests = 10000

    sim = Lattice(lattice_size, n_rats, n_birds,
                  n_sim_steps, hatch_time, hatch_prob, nest_placement_delay,
                  rat_initial_energy, nutritional_value_of_nests,
                  ylim=ylim, plot_environment=True, plot_populations=True)
    sim.start()
    plt.show()
