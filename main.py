import csv
import code.classes.grid as grid
from code.algorithms import representation as rep
from code.algorithms import baseline as base


def log_simulation(times):
    
    simulations = {}

    with open(f"output/{times}_tries.csv", "w", newline="") as csvfile:

        # Set up fieldnames 
        fieldnames = ["simulation", "cost"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Run n simulations and log each run in a new row
        for i in range(times):
            chip = grid.Grid("0","1")
            baseline = base.Baseline(chip)
            baseline.run()
            chip.compute_costs()
            simulations[i] = chip
            writer.writerow({
                    "simulation": i, "cost": chip.cost
                    })

if __name__ == "__main__": 

    log_simulation(10)

    # # Main values for checking
    # print()
    # # print(f"The gate coordinates are: {chip.gate_coordinates}")
    # #print(f"The wire segment paths are: {grid.wire_segments}")
    # print(f"The number of intersections: {chip.intersections}")
    # print()
    # print(f"The total amount of costs = {chip.cost}")
    # print(f"The total amount of attempts taken = {chip.tot_attempts}")
    # print()
