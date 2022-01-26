import csv
import code.classes.grid as grid
from code import algorithms
from code.algorithms import representation as rep, simulated_annealing
from code.algorithms import baseline as base
from code.algorithms import hillclimber as climber
from code.algorithms import A_star as star
from code.visualize import visualize as vis
from code.algorithms import simulated_annealing as sim

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



def log_simulation(runs, netlist):
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
            baseline = base.Baseline(chip)
            baseline.run()
            chip.compute_costs()

            # Save path data to csv
            chip.to_csv(name=i)


            costs.append(chip.cost)
            writer.writerow({
                    "simulation": i, "cost": chip.cost, "attempts": chip.tot_attempts
                    })
            print(f"Completed simulation {i}: C = {chip.cost}, found on attempt {chip.tot_attempts}")

        avgCosts = sum(costs)/runs
        writer.writerow({
            "simulation": "Avg costs", "cost": avgCosts
        })

def improve(netlist, specific_file, algorithm, update_csv_paths, make_csv_improvements, iterations, N, N_improvements):
    """Takes a csv containing previously generated paths, and tries to improve the costs of the solution using an iterative algorithm."""

    costs = []

    for i in range(1, N+1):

        for j in range(1, N_improvements + 1):

            # Open specific set of paths if desired
            add_string = ""
            if specific_file:
                add_string = f"_C_{specific_file}"

            run = f"_{i}"

            # Open file
            inputfile = f"output/paths_netlist_{netlist}{run}{add_string}.csv"
            chip_nr = int((netlist - 1) / 3)

            # Load paths into grid
            chip = grid.Grid(chip_nr, netlist, inputfile)

            # Run hillclimber algorithm with a number of iterations
            if algorithm == "hillclimber":
                hillclimber = climber.Hillclimber(chip, iterations, update_csv_paths, make_csv_improvements, i, j)
                cost = hillclimber.run()

                costs.append(cost)

            elif algorithm == "simulated_annealing":
                simanneal = sim.SimulatedAnnealing(chip, iterations, update_csv_paths, make_csv_improvements, i, j, temperature = 10000)
                costs = simanneal.run()

    return costs

def visualize_three_dimensional(netlist, specific_file):
    """Takes a csv file containing previously generates paths, and create a 3-dimensional plot to visualize them."""

    # Open specific set of paths if desired
    add_string = ""
    if specific_file:
        add_string = f"_C_{specific_file}"
    else:
        add_string = f"_1"

    # Open file
    inputfile = f"output/paths_netlist_{netlist}{add_string}.csv"
    chip_nr = int((netlist - 1) / 3)

    # Load paths into grid
    chip = grid.Grid(chip_nr, netlist, inputfile)

    # Make visualization
    vis(chip)


if __name__ == "__main__": 

    # Number of solutions the function log_simulation will try to find
    N = 1

    # Number of improved solution an optimizing algorithm will produce per inputsolution
    N_improvements = 1

    # Each iteration attempts to improve all netlists until improvement is found or none it found after long time

    iterations = 1000000

    # Netlist to be solved
    netlist = 1

    algorithm = "simulated_annealing"

    # Indicator from which specific file the paths will be extracted
    specific_file = None

    # Makes a new csv file for each improvement made in costs by hillclimber or simulated annealing
    # Final form will always be saved
    update_csv_paths = False

    # Makes CSV files after a hillclimber is done, storing the new costs per iteration
    make_csv_improvements = False

    log_simulation(N, netlist)
    
    # visualize_three_dimensional(netlist, specific_file)

    improve(netlist, specific_file, algorithm, update_csv_paths, make_csv_improvements, iterations, N, N_improvements)


    # chip_nr = int((netlist - 1) / 3)
    # chip = grid.Grid(chip_nr, netlist)
    # a = star.A_Star(chip)
    # a.run()
    # chip.to_csv()
    # visualize_three_dimensional(netlist, specific_file)

