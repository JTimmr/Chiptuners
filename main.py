import csv
import code.classes.grid as grid
from code import algorithms
from code.algorithms import representation as rep
from code.algorithms import baseline as base
from code.algorithms import hillclimber as climber
from code.algorithms import A_star as star
from code.visualize import visualize as vis
from code.algorithms import simulated_annealing as sim
import argparse

def to_csv(costs):

    with open(f"output/heavy_out.csv", "w", newline="") as csvfile:


        fieldnames = ["simulation", "cost"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 

        for i in range(len(costs)):

            writer.writerow({
                    "simulation": i + 1, "cost": costs[i]
                    })



def log_simulation(runs, netlist, constructive_algorithm):
    """Run the given algorithm a number of times, creating a set of solutions. Set N to 1 if a single solution suffices."""
    
    # Calculate chip number from netlist number
    chip_nr = int((netlist - 1) / 3)

    # Open file where results will be stored
    with open(f"output/netlist_{netlist}_{runs}x.csv", "w", newline="") as csvfile:

        # Set up fieldnames 
        fieldnames = ["simulation", "cost", "attempts"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()        
        costs = []

        # Run n simulations and log each run in a new row
        for i in range(1, runs + 1):
            chip = grid.Grid(chip_nr, netlist)
            if constructive_algorithm == "baseline":
                baseline = base.Baseline(chip)
                baseline.run()
            elif constructive_algorithm == "a_star":
                a = star.A_Star(chip)
                a.run()

            chip.compute_costs()

            # Save path data to csv
            chip.to_csv(name=i)

            costs.append(chip.cost)
            writer.writerow({
                    "simulation": i, "cost": chip.cost, "attempts": chip.tot_attempts
                    })
            add = ""
            if chip.tot_attempts > 0: 
                add = f", found on attempt {chip.tot_attempts}"
                
            print(f"Completed simulation {i}: C = {chip.cost}{add}")

        avgCosts = sum(costs)/runs
        writer.writerow({
            "simulation": "Avg costs", "cost": avgCosts
        })

def improve(netlist, specific_file, algorithm, update_csv_paths, make_csv_improvements, make_sim_annealing_plot, iterations, N, N_improvements):
    """Takes a csv containing previously generated paths, and tries to improve the costs of the solution using an iterative algorithm."""

    costs = []

    for i in range(1, N+1):

        for j in range(1, N_improvements + 1):

            # Open specific set of paths if desired
            add_string = ""
            try :
                int(specific_file)
                add_string = f"_{specific_file}"
            except ValueError:
                if N > 1:
                    add_string = f"_{i}"
                else:
                    add_string = f"_{specific_file}"


            # Open file
            inputfile = f"output/paths_netlist_{netlist}{add_string}.csv"
            chip_nr = int((netlist - 1) / 3)

            # Load paths into grid
            chip = grid.Grid(chip_nr, netlist, inputfile)

            # Run hillclimber algorithm with a number of iterations
            if algorithm == "hillclimber":
                hillclimber = climber.Hillclimber(chip, iterations, update_csv_paths, make_csv_improvements, i, j)
                cost = hillclimber.run()

                costs.append(cost)

            elif algorithm == "simulated_annealing":
                simanneal = sim.SimulatedAnnealing(chip, iterations, update_csv_paths, make_csv_improvements, make_sim_annealing_plot, i, j, temperature = 3000)
                costs = simanneal.run()

    return costs

def visualize_three_dimensional(netlist, specific_file):
    """Takes a csv file containing previously generates paths, and create a 3-dimensional plot to visualize them."""

    # Open specific set of paths if desired
    add_string = "_1"
    if specific_file:
        add_string = f"_{specific_file}"

    # Open file
    inputfile = f"output/paths_netlist_{netlist}{add_string}.csv"
    chip_nr = int((netlist - 1) / 3)

    # Load paths into grid
    chip = grid.Grid(chip_nr, netlist, inputfile)

    # Make visualization
    vis(chip)


if __name__ == "__main__": 

    parser = argparse.ArgumentParser(description='Find the most efficient solution for a network of points to be connected without collisions')
    parser.add_argument("netlist", type=int, help="Netlist to be solved")

    parser.add_argument("-c", type=str, default=None, dest="algorithm", help="Algorithm to be used. Pick either baseline or a_star.")
    parser.add_argument("-i", type=str, default=None, dest="improving_algorithm", help="Algorithm to be used to improve existing solutions. Pick either hillclimber or simulated annealing.")
    parser.add_argument("-vis", "--visualize", action='store_true', help="Renders a 3D plot of the grid with all its paths.")   

    parser.add_argument("-n", type=int, default=1, dest="N", help="number of solutions generated")
    parser.add_argument("-m", type=int, default=1, dest="N_improvements", help="number of improved solutions made for every prefound solution")
    parser.add_argument("-file", type=str, default=1, dest="specific_file", help="Specific file to be improved or plotted. If file is paths_netlist_4_C_19655, use -file C_19655. If file is paths_netlist_1_3, use -file 3.")

    # Parse the command line arguments
    args = parser.parse_args()


    if args.algorithm:
        log_simulation(args.N, args.netlist, args.algorithm)

    if args.improving_algorithm:

        # Each iteration attempts to improve all netlists until improvement is found or none it found after long tim
        iterations = 50

        # Makes a new csv file for each improvement made in costs by hillclimber or simulated annealing
        # Final form will always be saved
        update_csv_paths = False

        # Makes CSV files after a hillclimber is done, storing the new costs per iteration
        make_csv_improvements = False
        make_sim_annealing_plot = False
        improve(args.netlist, args.specific_file, args.improving_algorithm, update_csv_paths, make_csv_improvements, make_sim_annealing_plot, iterations, args.N, args.N_improvements)

    if args.visualize:
        visualize_three_dimensional(args.netlist, args.specific_file)
