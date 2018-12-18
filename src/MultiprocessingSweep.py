import multiprocessing as mp
from os import getpid
from Lattice import Lattice

def func(procnum):
    return str(procnum) + " " + str(getpid())

def run_simulation(params):
    # parameters for the simulation
    size = 200
    nest_placement_delay = 100
    rat_energy = 100
    n_sim_steps = int(1e2)

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
    with mp.Pool(4) as p: # I have checked, will only start 4 processes in tandem!
        r_vals = p.map(run_simulation, params)
        print(r_vals)

def gen_params():

    # parameters to sweep over
    rats_initial_populations = [5, 20, 30, 40, 50, 60, 100]
    bird_initial_populations =  [int(1e4)]
    hatch_times = [200]
    nutritional_values = [10]

    # generate a list of parameter comibinations to run in the sim!
    params = []
    for nrats in rats_initial_populations:
        for nbirds in bird_initial_populations:
            for hatch_time in hatch_times:
                for nval in nutritional_values:
                    params.append([nrats, nbirds, hatch_time, nval])

    return params

if __name__ == '__main__':
    # works - but creating new processes has quite a bit of overhead
    # --> instantiation is slow as fuck
    main()
