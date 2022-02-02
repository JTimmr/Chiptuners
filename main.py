"""
main.py

Authors: Auriella, Jasper en Rick

This program tries to find a good as posible solution to the shortest path problem on a grid between points.
It optimizes the routes/ nets between gates on a grid with respect to costs.

rules:
    - Each wire segment has a cost of 1
    - Intersection of wire costs 300 and is highly undesireable
    - NO wires may ever share the same segment called "collition"

Our structure of solving this problem is as follows:
    - Sort netlist by a specific rule
    - Find a base solution that is as close to the global optimum as possible
    - Improve that base solution by use of an itterative algorithm in order to obtain the global/local optimum

Findings: the best results were obtained by using sorting by length ascending, using A* as base algortihm and optimizing with a hillclimber.

Usage: python3 main.py netlistnummer (-h) (-c naam algoritme) (-i naam algoritme) (-vis) (-leg) (-plotly) (-iter N) (-n N) (-m N verbeteringen) (-file bestandsnaam) (-pop indexnummer) (-gs lagen) (-random netlistnummer)

Powered by Chiptuners
"""

from copy import deepcopy
import csv
import code.classes.grid as grid
from code.algorithms import baseline as base
from code.algorithms import hillclimber as climber
from code.algorithms import A_star as star
from code.visualize import *
from code.algorithms import simulated_annealing as sim
from code.algorithms.sorting import *
import argparse
import sys


def log_simulation(N, netlist, constructive_algorithm, sorting_method, randomized, pop, gate_space):
    """
    Takes the amount of runs, netlist number, type of algorithm and sorting algorithm as input.
    Runs the given algorithm a number of times, creating a set of solutions. Set N to 1 if a single solution suffices.
    Saves the results in a CSV file, where each row represents the results of a single run,
    and each columns stores the costs. The algorithms to choose from are baseline and A*. A* can be combined
    with one of the following sorting algorithms:
    - Random
    - Decreasing path length
    - Increading path length
    - From inside to outside
    - From outside to inside
    - Number of connections gate descending
    - Number of connections gate ascending
    - Increading estimated number of intersections
    - Decreasing estimated number of intersections
    See baseline.py, a_star.py and sorting.py for further explanation of the algorithms.
    """

    # Calculate chip number from netlist number
    chip_nr = int((netlist - 1) / 3)

    if randomized:
        add = "random_"
    else:
        add = ""

    # Open file where results will be stored
    with open(f"results/{add}netlist_{netlist}_{N}x.csv", "w", newline="") as csvfile:

        # Set up fieldnames
        fieldnames = ["simulation", "cost"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        costs = []

        # Run N simulations and log each run in a new row
        for n in range(1, N + 1):

            # Make grid
            chip = grid.Grid(chip_nr, netlist, randomized=randomized)

            # Run desired algorithm
            if constructive_algorithm == "baseline":
                baseline = base.Baseline(chip, sorting_method)
                baseline.run()
            elif constructive_algorithm == "a_star":
                solver = star.A_Star(chip, sorting_method, pop, gate_space, display=True)
                if not solver.run():
                    print(f"Netlist {netlist} cannot be solved using A* with the current combination of sorting algorithm, gate_space and pop.")
                    return

            # Compute costs of the grid
            chip.compute_costs()

            # Save path data to csv
            chip.to_csv(name=n)

            # Save row in CSV
            costs.append(chip.cost)
            writer.writerow({
                    "simulation": n, "cost": chip.cost
                    })

            print(f"Completed run {n}: C = {chip.cost}")

        # Make row with average results
        average_costs = sum(costs)/N
        writer.writerow({
            "simulation": "Avg costs", "cost": average_costs
        })


def improve(netlist, specific_file, algorithm, update_csv_paths, make_csv_improvements, make_iterative_plot, iterations, N, N_improvements, sorting_method, randomized):
    """
    Loads N previously generated solutions, and tries to make improvements during a given number of iterations.
    There is also the option to start over after the algorithm is finished, since the algorithm could
    be stuck in a local optimum. The number of runs per solution is given by N_improvements.
    If update_csv_paths is set to True, every new solution will be saved into a CSV file.
    If make_csv_improvements is set to True, a CSV file will be created for all runs, storing the costs
    against the iteration so the development of the costs over time can be investigated.
    The algorithms to choose from are Hillclimber and Simulated Annealing,
    which both can use one of the following sorting algorithms:
    - Random
    - Decreasing path length
    - Increading path length
    - From inside to outside
    - From outside to inside
    - Number of connections gate descending
    - Number of connections gate ascending
    - Increading estimated number of intersections
    - Decreasing estimated number of intersections
    For further explanation of the algorithms, see simulated_annealing.py, hillclimber.py and sorting.py.
    Returns a list of costs.
    """

    if randomized:
        add = "random_"
    else:
        add = ""

    for i in range(1, N+1):

        for j in range(1, N_improvements + 1):

            # Open specific set of paths if desired
            add_string = ""
            try:
                int(specific_file)
                add_string = f"_{specific_file}"
            except ValueError:
                if N > 1:
                    add_string = f"_{i}"
                else:
                    add_string = f"_{specific_file}"

            # Open file
            inputfile = f"results/{add}paths_netlist_{netlist}{add_string}.csv"
            chip_nr = int((netlist - 1) / 3)

            # Load paths into grid
            chip = grid.Grid(chip_nr, netlist, infile=inputfile, randomized=randomized)

            # Run hillclimber algorithm with a number of iterations
            if algorithm == "hillclimber":
                hillclimber = climber.Hillclimber(chip, iterations, update_csv_paths, make_csv_improvements, make_iterative_plot, i, j, sorting_method)
                hillclimber.run()

            elif algorithm == "simulated_annealing":

                chip.compute_costs()

                temperature = 10000
                start_cost = deepcopy(chip.cost)
                simanneal = sim.SimulatedAnnealing(chip, iterations, update_csv_paths, make_csv_improvements, make_iterative_plot, i, j, temperature, sorting_method)

                simanneal.run()
                print(f"{start_cost}")


def visualize_three_dimensional(netlist, specific_file, legend, randomized, matplotlib, plotly):
    """
    Takes a csv file containing previously generates paths of a given netlist,
    and create a 3-dimensional plot to visualize them.
    """

    if randomized:
        add = "random_"
    else:
        add = ""

    # Open file
    inputfile = f"results/{add}paths_netlist_{netlist}_{specific_file}.csv"
    chip_nr = int((netlist - 1) / 3)

    # Load paths into grid
    chip = grid.Grid(chip_nr, netlist, inputfile, randomized)

    # Make visualization
    if matplotlib is True:
        visualize_matplotlib(chip, legend)

    if plotly is True:
        visualize_plotly(chip)


if __name__ == "__main__":

    # Make it possible to accept closely related arguments with dictionaries
    # Calls sorting function based on args given
    function_map = {
        'random': [random_sort, None], "r": [random_sort, None], "rand": [random_sort, None], 
	 "willekeurig": [random_sort, None],

        'length_d': [sort_length, True], 'length d': [sort_length, True], 'd length': [sort_length, True], 
	 'length descending': [sort_length, True], 'descending length': [sort_length, True], 
        'length_descending': [sort_length, True], "descending_length": [sort_length, True],

        'length_a': [sort_length, False], 'length a': [sort_length, False], 'a length': [sort_length, False], 
	'length ascending': [sort_length, False], 'ascending length': [sort_length, False], 
        'length_ascending': [sort_length, False], "ascending_length": [sort_length, False], 
	 "length": [sort_length, False],

        'middle': [sort_middle_first, False], 'outside': [sort_middle_first, True],

        'gate_d': [sort_gate, True], 'gates_d': [sort_gate, True], 'gates d': [sort_gate, True], 
	'gate d': [sort_gate, True], 'd_gate': [sort_gate, True], 'd gate': [sort_gate, True], 
	'gate_descending': [sort_gate, True], 'descending_gate': [sort_gate, True], 
	'gate descending': [sort_gate, True], 'descending gate': [sort_gate, True],

        'gate_a': [sort_gate, False], 'gates_a': [sort_gate, False], 'gates a': [sort_gate, False], 
	'gate': [sort_gate, False], 'gate a': [sort_gate, False], 'a_gate': [sort_gate, False], 
	'a gate': [sort_gate, False], 'gate_ascending': [sort_gate, False], 'ascending_gate': [sort_gate, False],
        'ascending gate': [sort_gate, False], 'gate ascending': [sort_gate, False], 'gates': [sort_gate, False],

        'intersections_d': [sort_exp_intersections, True], 'intersections d': [sort_exp_intersections, True], 																	
	'd intersections': [sort_exp_intersections, True], 'd_intersections': [sort_exp_intersections, True], 												
	'intersection_d': [sort_exp_intersections, True], 'intersections_descending': [sort_exp_intersections, True], 
	'descending_intersections': [sort_exp_intersections, True],  'intersection d': [sort_exp_intersections, True],

        'intersections_a': [sort_exp_intersections, False], 'intersections a': [sort_exp_intersections, False], 
	'a intersections': [sort_exp_intersections, False], 'a_intersections': [sort_exp_intersections, False], 
	'intersections_ascending': [sort_exp_intersections, False], 'ascending_intersections': [sort_exp_intersections, False],
        'intersections': [sort_exp_intersections, False], 'intersection': [sort_exp_intersections, False], 
	'intersection a': [sort_exp_intersections, False], 'intersection_a': [sort_exp_intersections, False]
    }

    possible_entries = {
        "b": "baseline", "base": "baseline", "basefunction": "baseline", "baseline": "baseline",

        "a": "a_star", "star": "a_star", "a star": "a_star", "a*": "a_star", "a-star": "a_star", "a_star": "a_star",

        "h": "hillclimber", "hill": "hillclimber", "hillc": "hillclimber", "hillclimb": "hillclimber", "climber": "hillclimber", "climb": "hillclimber", "hc": "hillclimber",
        "hillclimber": "hillclimber",

        "sa": "simulated_annealing", "s": "simulated_annealing", "sim": "simulated_annealing", "sim_a": "simulated_annealing", "sim a": "simulated_annealing",
        "sima": "simulated_annealing", "simulated_annealing": "simulated_annealing",
    }

    parser = argparse.ArgumentParser(description='Find the most efficient solution for a network of points to be connected without collisions')
    parser.add_argument("netlist", type=int, help="Netlist to be solved")

    parser.add_argument("-c", type=str, default=None, dest="algorithm", nargs="+", help="Algorithm to be used. Pick either baseline or a_star.")
    parser.add_argument("-i", type=str, default=None, dest="improving_algorithm", nargs="+", help="Algorithm to be used to improve existing solutions. Pick either hillclimber or simulated annealing.")
    parser.add_argument("-sort_c", type=str, default="length_a", dest="sorting_c", nargs="+", help="In which order must the netlists be ordered for the basis algorithm? Options: random, length_a, length_d, middle, outside, gate_a, gate_d, intersections_a, intersections_d. When no order is given (ascending or descending), ascending is chosen.")
    parser.add_argument("-sort_i", type=str, default="length_a", dest="sorting_i", nargs="+", help="In which order must the netlists be ordered for the iterative algorithm? Options: random, length_a, length_d, middle, outside, gate_a, gate_d, intersections_a, intersections_d. When no order is given (ascending or descending), ascending is chosen.")

    parser.add_argument("-vis", "--visualize", action='store_true', help="Renders a 3D plot of the grid with all its paths.")
    parser.add_argument("-leg", "--legend", action='store_true', help="Renders a legend for 3D plot.")
    parser.add_argument("-plotly", action='store_true', help="Renders a 3D plot of the grid with all its paths in your browser with plotly.")

    parser.add_argument("-iter", type=int, default=1000, dest="iterations", help="Number of iterations used by an improving algorithm.")
    parser.add_argument("-n", type=int, default=1, dest="N", help="number of solutions generated")
    parser.add_argument("-m", type=int, default=1, dest="N_improvements", help="number of improved solutions made for every prefound solution")
    parser.add_argument("-file", type=str, default="1", dest="specific_file", help="Specific file to be improved or plotted. If file is paths_netlist_4_C_19655, use -file C_19655. If file is paths_netlist_1_3, use -file 3.")

    parser.add_argument("-pop", type=int, default=0, dest="pop", help="Index at which item will be popped in A* algorithm when multiple states have the same priority.")
    parser.add_argument("-gs", type=int, default=2, dest="gate_space", help="Minimal height above a gate which will remain free of passing nets, so the gate is not unnecessarily blocked by other nets.")
    parser.add_argument("-random", "--randomized", action='store_true', help="Load random netlists instead of the originals.")

    # Parse the command line arguments
    args = parser.parse_args()

    # Error messages
    if len(sys.argv) < 3:
        print("Error message: You are missing some required arguments. Did you specify which algorithm you wanted to use?")

    if args.netlist < 1 or args.netlist > 9:
        print("Error message: See data directory! Enter a netlist between 1 and 9.")

    if args.algorithm:

        # Make string and case insensitive
        if isinstance(args.algorithm, list):
            args.algorithm = ' '.join(map(str, args.algorithm))
        if isinstance(args.sorting_c, list):
            args.sorting_c = ' '.join(map(str, args.sorting_c))
        args.algorithm.lower()
        args.sorting_c.lower()

        log_simulation(args.N, args.netlist, possible_entries[args.algorithm], function_map[args.sorting_c], args.randomized, args.pop, args.gate_space)

    if args.improving_algorithm:

        # Make string and case insensitive
        if isinstance(args.improving_algorithm, list):
            args.improving_algorithm = ' '.join(map(str, args.improving_algorithm))
        if isinstance(args.sorting_i, list):
            args.sorting_i = ' '.join(map(str, args.sorting_i))
        args.improving_algorithm.lower()
        args.sorting_i.lower()

        # Makes a new csv file for each improvement made in costs by hillclimber or simulated annealing
        # Final form will always be saved
        update_csv_paths = True

        # Makes CSV files after a hillclimber is done, storing the new costs per iteration
        make_csv_improvements = True

        # Plots the progress of Hillclimber or Simulated annealing as costs vs iteration
        make_iterative_plot = True
        improve(args.netlist, args.specific_file, possible_entries[args.improving_algorithm], update_csv_paths, make_csv_improvements, make_iterative_plot, args.iterations, args.N, args.N_improvements, function_map[args.sorting_i], args.randomized)

    if args.visualize or args.plotly:
        visualize_three_dimensional(args.netlist, args.specific_file, args.legend, args.randomized, args.visualize, args.plotly)
