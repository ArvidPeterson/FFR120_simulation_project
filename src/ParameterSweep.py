import numpy as np
from matplotlib import pyplot as plt
from Lattice import Lattice

# which vars should be fixed?
# lattice_size, n_sim_steps,
# increase both pops
# mixed increase/decrease
class ParamSweep:

    def __init__(self, lattice_size, n_sim_steps, bird_initial_populations,
                rats_initial_populations,
                hatch_times, rat_initial_energy,
                nutritional_values, nest_placement_delay):


        self.size = lattice_size
        self.n_sim_steps = n_sim_steps
        self.n_birds_range = bird_initial_populations
        self.n_rats_range = rats_initial_populations
        self.nest_placement_delay = nest_placement_delay
        self.nutritional_values = nutritional_values
        self.nest_placement_delay = nest_placement_delay
        self.hatch_times = hatch_times
        self.rat_energy = rat_initial_energy
        self.run_simulation()


    def run_simulation(self):
        for hatch_time in self.hatch_times:
            for nutritional_value in self.nutritional_values:
                for nrats in self.n_rats_range:
                    for nbirds in self.n_birds_range:
                        sim = Lattice(self.size, nrats, nbirds,
                                    self.n_sim_steps, hatch_time,
                                    self.nest_placement_delay, self.rat_energy,
                                    nutritional_value, plot_environment=False,
                                    plot_populations=False)
                        bird_pop, rat_pop, nest_pop, time = sim.run()
                        max_bird_pop = max(bird_pop)
                        max_rat_pop = max(rat_pop)
                        min_bird_pop = min(bird_pop)
                        min_rat_pop = min(rat_pop)
                        fig, ax = plt.subplots()
                        plt.plot(time, bird_pop, color='blue', label='Bird population')
                        plt.plot(time, nest_pop, color='green', label='Nest population')
                        plt.plot(time, rat_pop, color='red', label='Rat population')
                        handles, labels = ax.get_legend_handles_labels()
                        plt.legend(handles, labels)
                        ax.set_xlabel('Time steps')
                        ax.set_ylabel('Populations')
                        ax.set_title('initial bird population: {}, initial rat population: {}\n'
                                     'hatch time: {}, nest nutritional value: {}'.format(
                            nbirds, nrats, hatch_time, nutritional_value
                        ))
                        fname = 'nbirds{}nrats{}nutrition{}hatchtime{}'.format(nbirds, nrats, nutritional_value, hatch_time)
                        self.save_data(fig, fname)
                        plt.close(fig)

    def save_data(self, fig, name):
        img_dir = 'save_data/img/' + str(name) + '.png'
        fig.savefig(img_dir)


if __name__ == '__main__':
    # fixed values
    lattice_size = 200
    hatch_time = 200
    rat_initial_energy = 100
    nest_placement_delay = 100
    n_sim_steps = int(1e4)

    # sweeping values
    rats_initial_populations = [5, 10, 20, ]
    bird_initial_populations = [20, 50, 100, 500]
    hatch_times = [30, 100, 200, 500]
    nutritional_values = [10, 20, 50, 100]
    sweep = ParamSweep(lattice_size, n_sim_steps, bird_initial_populations,
                       rats_initial_populations,
                       hatch_times, rat_initial_energy,
                       nutritional_values, nest_placement_delay)