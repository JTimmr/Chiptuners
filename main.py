import csv
import code.classes.grid as grid
from code.algorithms import representation as rep
from code.algorithms import baseline as base


def log_simulation(times, render):
    
    simulations = {}

    with open(f"output/{times}_tries.csv", "w", newline="") as csvfile:

        # Set up fieldnames 
        fieldnames = ["simulation", "cost"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Run n simulations and log each run in a new row
        for i in range(times):
            chip = grid.Grid("1","4")
            baseline = base.Baseline_optimized(chip, render)
            baseline.run()
            chip.compute_costs()
            simulations[i] = chip
            writer.writerow({
                    "simulation": i, "cost": chip.cost
                    })

if __name__ == "__main__": 

    N = 5
    render = False
    log_simulation(N, render)

