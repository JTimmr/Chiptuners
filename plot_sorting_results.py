import glob
import csv
import matplotlib.pyplot as plt
import re
import numpy as np 

path = "plotting/*.csv"

for fname in glob.glob(path):
    pattern = "plot_data_(.*?).csv"
    substring = re.search(pattern, fname).group(1)

    with open (f"{fname}") as file:

        iterations = []
        costs = []
        stds = [] 

        reader = csv.DictReader(file)
        for row in reader:
            iterations.append(int(float(row['iteration'])))
            costs.append(int(float(row['cost'])))
            stds.append(int(float(row['std'])))
        plt.errorbar(iterations, costs, stds, capthick=1, elinewidth=0.5, alpha = 0.5, label = substring)
        
        data = np.array(costs)
        average = np.average(data)
        sd = np.std(data)
        print(f" {substring}: m: {average}, sd: {sd}")
        
plt.xlabel              
plt.legend()
plt.savefig("results_sorting_plot.png")

