import csv
import code.classes.grid as grid
from code.algorithms import representation as rep
from code.algorithms import baseline as base
from code.algorithms import hillclimber as climber
from code.algorithms import A_star as star
from code.visualize import visualize as vis


def log_simulation(times, print_connections, netlist):
    """Run the given algorithm a number of times, creating a set of solutions. Set N to 1 if a single solution suffices."""
    
    simulations = {}
    chip_nr = int((netlist - 1) / 3)

    with open(f"output/netlist_{netlist}_{times}x.csv", "w", newline="") as csvfile:

        # Set up fieldnames 
        fieldnames = ["simulation", "cost", "attempts"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        costs = []

        # Run n simulations and log each run in a new row
        for i in range(1, times + 1):
            chip = grid.Grid(chip_nr, netlist)
            baseline = base.Baseline(chip, print_connections)
            baseline.run()
            chip.compute_costs()

            chip.to_csv(name=i)

            costs.append(chip.cost)
            simulations[i] = chip
            writer.writerow({
                    "simulation": i, "cost": chip.cost, "attempts": chip.tot_attempts
                    })
            print(f"Completed simulation {i}: C = {chip.cost}, found on attempt {chip.tot_attempts}")
            chip.to_csv()

        avgCosts = sum(costs)/times
        writer.writerow({
            "simulation": "Avg costs", "cost": avgCosts
        })


def improve(netlist, specific_file, update_csv, iterations, i, j):
    """Takes a csv containing previously generated paths, and tries to improve the costs of the solution using an iterative algorithm."""
    
    # Open specific set of paths if desired
    add_string = ""
    if specific_file:
        add_string = f"_C_{specific_file}"

    if i:
        i = f"_{i}"
    else:
        i = ""
    
    if j:
        j = f"_{j}"
    else:
        j = ""

    # Open file
    inputfile = f"output/paths_netlist_{netlist}{i}{add_string}.csv"
    chip_nr = int((netlist - 1) / 3)

    # Load paths into grid
    chip = grid.Grid(chip_nr, netlist, inputfile)

    # Run hillclimber algorithm with a number of iterations
    hillclimber = climber.Hillclimber(chip, iterations, update_csv, i, j)
    costs = hillclimber.run()

    # visualize_three_dimensional(netlist, costs)


def visualize_three_dimensional(netlist, specific_file):
    """Takes a csv file containing previously generates paths, and create a 3-dimensional plot to visualize them."""

    # Open specific set of paths if desired
    add_string = ""
    if specific_file:
        add_string = f"_C_{specific_file}"

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

    # Each iteration attempts to improve all netlists until improvement is found or none it found after long time
    iterations = 50

    # Prints all paths immediately when found
    print_connections = False

    # Netlist to be solved
    netlist = 9

    # Indicator from which specific file the paths will be extracted
    specific_file = None

    # Makes a new csv file for each improvement made in costs
    # Final form will always be saved
    update_csv = False

    # log_simulation(N, print_connections, netlist)
    # for i in range(1,2):
    #     for j in range(1, N+1):
    #         improve(netlist, specific_file, update_csv, iterations, i, j)

    # improve(netlist, specific_file, update_csv, iterations, 3)

    # visualize_three_dimensional(netlist, specific_file)
    # improve(netlist, specific_file, update_csv, iterations)

    chip_nr = int((netlist - 1) / 3)
    chip = grid.Grid(chip_nr, netlist)
    a = star.A_Star(chip)
    a.run()
    chip.to_csv()
    visualize_three_dimensional(netlist, specific_file)
