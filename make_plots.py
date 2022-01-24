import csv
import matplotlib.pyplot as plt
import numpy as np

average_per_configuration = []
iterations = np.arange(50)
ticks = []
std = []
netlist = 3

for i in range(1, 11):
    many_costs = []
    tmp2 = []
    for j in range(1, 11):
        costs = []

        with open (f"output/results_hillclimber/hill_netlist_{netlist}_{i}_{j}_length(d).csv") as file:
            reader = csv.DictReader(file)
            for row in reader:

                # Extract coordinates
                cost = int(row['cost'])
                costs.append(cost)
            costs = np.array(costs)
            many_costs.append(costs)
    
    
    for iteration in range(len(iterations)):
        tmp = []
        for j in range(10):
            tmp.append(many_costs[j][iteration])
        tmp2.append(np.average(tmp))
    average_per_configuration.append(tmp2)

for i in range(len(iterations)):
    tmp = []
    for j in range(10):
        tmp.append(average_per_configuration[j][i])
    ticks.append(np.average(tmp))
    std.append(np.std(tmp))

plt.errorbar(iterations, ticks, std, capthick=1, elinewidth=0.5)
plt.savefig("test.png")


with open(f"output/results_hillclimber/hill_netlist_{netlist}_plot_data_length(d).csv", "w", newline="") as csvfile:
    fieldnames = ["iteration", "cost", "std"]

    # Set up wiriter and write the header
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(len(iterations)):
            writer.writerow({
            "iteration": i + 1, "cost": ticks[i], "std": std[i]
            })