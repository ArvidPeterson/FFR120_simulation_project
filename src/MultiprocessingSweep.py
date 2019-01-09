import multiprocessing as mp
from os import getpid
from Lattice import Lattice
import matplotlib.pyplot as plt
import numpy as np

def func(procnum):
    return str(procnum) + " " + str(getpid())

def run_simulation(params):
    # parameters for the simulation
    size = 200
    nest_placement_delay = 100
    rat_energy = 100 # should be 100
    n_sim_steps = int(3e4)

    # parameters which vary are passed in 'params'
    nrats, nbirds, hatch_time, nutritional_value = params

    # init and run simulation
    sim = Lattice(size, nrats, nbirds,
                  n_sim_steps, hatch_time,
                  nest_placement_delay, rat_energy,
                  nutritional_value, plot_environment=False,
                  plot_populations=False)
    sim.start()
    return sim.join()

def main():
    # start processes in a thread pool (workaround for threading blocking each other)
    params = gen_params()
    r_vals = []
    with mp.Pool(2) as p: # I have checked, will only start 4 processes in tandem!
        populations = p.map(run_simulation, params)
        r_vals.append(populations)

    plot_and_save(params, r_vals)

def gen_params():

    # parameters to sweep over
    rats_initial_populations = [20]
    bird_initial_populations =  [int(1e3)]
    hatch_times = [500]
    nutritional_values = [10]

    # generate a list of parameter comibinations to run in the sim!
    params = []
    for nrats in rats_initial_populations:
        for nbirds in bird_initial_populations:
            for hatch_time in hatch_times:
                for nval in nutritional_values:
                    params.append([nrats, nbirds, hatch_time, nval])

    return params

def plot_and_save(params, data):
    # r_vals on the form t[wrapper][all lists (bird, nest etc)][data_acess]
    for i, time_series in enumerate(data[0]):
        bird_pop, rat_pop, nest_pop, time_record = time_series
        nrats, nbirds, hatch_time, nutritional_value = params[i]

        # maximum population measures for the plotting!
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
        #ax.set_title('
        ax.set_title('Oscillatory population behavior')
        fname = 'nbirds_{}_nrats_{}_nutrition_{}_hatchtime_{}_maxbird_{}_maxrat_{}_minbird_{}_minrat_{}'\
            .format(nbirds, nrats, nutritional_value, hatch_time, max_bird_pop, max_rat_pop, min_bird_pop, min_rat_pop)
        ratio = 0.3
        xleft, xright = ax.get_xlim()
        ybottom, ytop = ax.get_ylim()
        ax.set_aspect(abs((xright - xleft) / (ybottom - ytop)) * ratio)
        #plt.axis('off')
        plt.gca().set_position([0,0,1,1])
        save_data(fig, fname, bird_pop=bird_pop, rat_pop=rat_pop, nest_pop=nest_pop, time=time_record)
        plt.close(fig)

def save_data(fig, name, bird_pop=[], rat_pop=[], nest_pop=[], time=[]):
    img_dir = 'save_data/img/' + str(name) + '.svg'
    fig.savefig(img_dir, dpi = 1000, bbox_inches='tight')

    data_name_v = ['bird_pop', 'rat_pop', 'nest_pop', 'time']
    pop_v = [bird_pop, rat_pop, nest_pop, time]

    num_data_dir = 'save_data/num/'

    for ii in range(len(pop_v)):
        pop = pop_v[ii]
        if pop:
            file_name = num_data_dir + name + '_' + data_name_v[ii]
            np_data = np.array(pop)
            np.save(file_name, np_data)


if __name__ == '__main__':
    # works - but creating new processes has quite a bit of overhead
    # --> instantiation is slow as fuck
    t = main()
    print('test')
