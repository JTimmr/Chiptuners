import code.classes.grid as rep
import csv

def run_once():

    grid = rep.Grid("0","1")
    grid.compute_costs()
    grid.to_csv()

def log_simulation(times):
    
    simulations = {}

    for i in range(times):
        grid = rep.Grid("0","1")
        grid.compute_costs()
        simulations[i] = grid.cost
        
    with open(f"output/{times}_tries.csv", "w", newline="") as csvfile:

        # Set up fieldnames 
        fieldnames = ["simulation", "cost"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for simulation in simulations:
            writer.writerow({
                    "simulation": simulation, "cost": simulations[simulation]
                    })
    
    print(grid)

    # with open(f"output/{times}_tries.csv", "w", newline="") as csvfile:

    #     # Set up fieldnames 
    #     fieldnames = ["simulation", "cost"]

    #     # Set up wiriter and write the header
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()

    #     # Run n simulations and log each run in a new row
    #     for i in range(times):
    #         grid = rep.Grid("0","1")
    #         grid.compute_costs()
    #         writer.writerow({
    #                 "simulation": i, "cost": grid.cost
    #                 })

if __name__ == "__main__": 

    log_simulation(4)
    