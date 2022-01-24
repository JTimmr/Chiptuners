import csv
import matplotlib.pyplot as plt
import numpy as np

all_costs = []
iterations = np.arange(50)
ticks = []
std = []

for i in range(1, 11):
    iterations = []
    costs = []

    with open (f"output/results_hillclimber/hill_netlist_3_1_{i}_length(d).csv") as file:
        reader = csv.DictReader(file)
        for row in reader:

            # Extract coordinates
            iteration, cost = int(row['iteration']), int(row['cost'])
            iterations.append(iteration)
            costs.append(cost)
        costs = np.array(costs)
        all_costs.append(costs)

for i in iterations:
    tmp = []
    for j in range(10):
        tmp.append(all_costs[j][i - 1])
    ticks.append(np.average(tmp))
    std.append(np.std(tmp))

# plt.plot(iterations, ticks)    
plt.errorbar(iterations, ticks, std, capthick=1, elinewidth=0.5)
plt.savefig("test.png")