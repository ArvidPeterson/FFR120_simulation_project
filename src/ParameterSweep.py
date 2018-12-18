import time
import numpy as np
from matplotlib import pyplot as plt
from Lattice import Lattice
import numpy as np

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
        self.n_birds_range = bird_initial_populations  # all these are lists with different settings
        self.n_rats_range = rats_initial_populations
        self.nest_placement_delay = nest_placement_delay
        self.nutritional_values = nutritional_values
        self.nest_placement_delay = nest_placement_delay
        self.hatch_times = hatch_times
        self.rat_energy = rat_initial_energy
        self.run_simulation()
        self.simulation_idx = 1


    def run_simulation(self):

        self.simulation_idx = 1
        print('Simulation start')

        n_simulations = len(self.hatch_times) * len(self.nutritional_values) * len(self.n_rats_range) * len(self.n_birds_range)

        for hatch_time in self.hatch_times:
            for nutritional_value in self.nutritional_values:
                for nrats in self.n_rats_range:
                    for nbirds in self.n_birds_range:
                        start = time.process_time()
                        sim = Lattice(self.size, nrats, nbirds,
                                    self.n_sim_steps, hatch_time,
                                    self.nest_placement_delay, self.rat_energy,
                                    nutritional_value, plot_environment=False,
                                    plot_populations=False)
                        sim.start()
                        bird_pop, rat_pop, nest_pop, time_record = sim.join()
                        max_bird_pop = max(bird_pop)
                        max_rat_pop = max(rat_pop)
                        min_bird_pop = min(bird_pop)
                        min_rat_pop = min(rat_pop)
                        fig, ax = plt.subplots()
                        plt.plot(time_record, bird_pop, color='blue', label='Bird population')
                        plt.plot(time_record, nest_pop, color='green', label='Nest population')
                        plt.plot(time_record, rat_pop, color='red', label='Rat population')
                        handles, labels = ax.get_legend_handles_labels()
                        plt.legend(handles, labels)
                        ax.set_xlabel('Time steps')
                        ax.set_ylabel('Populations')
                        ax.set_title('initial bird population: {}, initial rat population: {}\n'
                                     'hatch time: {}, nest nutritional value: {}'.format(
                            nbirds, nrats, hatch_time, nutritional_value
                        ))
                        fname = 'nbirds_{}_nrats_{}_nutrition_{}_hatchtime_{}'.format(nbirds, nrats, nutritional_value, hatch_time)
                        self.save_data(fig, fname, bird_pop=bird_pop, rat_pop=rat_pop,nest_pop=nest_pop, time=time)
                        plt.close(fig)
                        
                        print('simulation ' + str(self.simulation_idx) + '/' + str(n_simulations))
                        self.simulation_idx += 1
                        stop = time.process_time()
                        print('time taken to generate 1 plot: {}'.format(stop-start))

    def save_data(self, fig, name, bird_pop=[], rat_pop=[], nest_pop=[], time=[]):
        img_dir = 'save_data/img/' + str(name) + '.png'
        fig.savefig(img_dir)

        data_name_v = ['bird_pop', 'rat_pop', 'nest_pop', 'time']
        pop_v = [bird_pop, rat_pop, nest_pop, time]

        num_data_dir = 'save_data/num/'

        for ii in range(len(pop_v)):
            pop = pop_v[ii]
            if pop:
                file_name = num_data_dir + name + '_' + data_name_v[ii] + '_' + str(self.simulation_idx)
                np_data = np.array(pop)
                np.save(file_name, np_data)


if __name__ == '__main__':
    # fixed values
    lattice_size = 200
    hatch_time = 200
    rat_initial_energy = 4
    nest_placement_delay = 100
    n_sim_steps = int(1e3)

    # sweeping values
    rats_initial_populations = [10]
    bird_initial_populations = [100]
    hatch_times = [100]
    nutritional_values = [10]

    sweep = ParamSweep(lattice_size, n_sim_steps, bird_initial_populations,
                       rats_initial_populations,
                       hatch_times, rat_initial_energy,
                       nutritional_values, nest_placement_delay)