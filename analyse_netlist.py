import csv
import argparse
from copy import deepcopy
import numpy as np
import make_netlists as make
import code.algorithms.A_star as a_star
import code.algorithms.sorting as sort
import code.classes.grid as grid


def load_nets(netlist, n, chip, randomized):
    """
    Reads requested file containing the requested nets,
    and extracts their starting and ending coordinates.
    Creates gate object for each row.
    """
    
    if randomized:
        add = "random/"
        second_add = f"_{n}"
    else:
        add = ""
        second_add = ""

    nets = set()
    with open(f"data/chip_{chip}/{add}netlist_{netlist}{second_add}.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            nets.add((row['chip_a'], row['chip_b']))

    return nets


def load_gates(chip):
    """
    Reads requested file containing the location of the gates,
    and extracts their id's and coordinates.
    Creates gate object for each row.
    """

    gates = {}
    coordinates = {}

    with open(f"data/chip_{chip}/print_{chip}.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            gate = (row['chip'])
            gates[gate] = 0
            coordinates[gate] = (int(row['x']), int(row['y']))
    return gates, coordinates


def check_gate_occupation(nets, gates):
    for net in nets:
        gates[net[0]] += 1
        gates[net[1]] += 1
        if gates[net[0]] > 5:
            print(f"Gate {net[0]} has to make {gates[net[0]]} connections, which is not possible. This netlist cannot be solved.")
            return "impossible"
        if gates[net[1]] > 5:
            print(f"Gate {net[1]} has to make {gates[net[1]]} connections, which is not possible. This netlist cannot be solved.")
            return "impossible"


def check_intersections(net_coordinates):

    exp_intersections = 0

    # For every net object copy the start- and end coordinates
    for net in net_coordinates:

        # Go over all other nets and compute the dot product with itself and the others one by one
        other_nets = deepcopy(net_coordinates)
        del other_nets[net]
        net = net_coordinates[net]
        for other_net in other_nets.values():
            # p0 = (y3 - y2)(x3 - x0) - (x3 - x2)(y3 - y0)
            p0 = (other_net[1][1] - other_net[0][1]) * (other_net[1][0] - net[0][0]) - (other_net[1][0] - other_net[0][0]) * (other_net[1][1] - net[0][1])

            # p1 = (y3 - y2)(x3 - x1) - (x3 - x2)(y3 - y1)
            p1 = (other_net[1][1] - other_net[0][1]) * (other_net[1][0] - net[1][0]) - (other_net[1][0] - other_net[0][0]) * (other_net[1][1] - net[1][1])

            # p2 = (y1 - y0)(x1 - x2) - (x1 - x0)(y1 - y2)
            p2 = (net[1][1] - net[0][1]) * (net[1][0] - other_net[0][0]) - (net[1][0] - net[0][0]) * (net[1][1] - other_net[0][1])

            # p3 = (y1 - y0)(x1 - x3) - (x1 - x0)(y1 - y3)
            p3 = (net[1][1] - net[0][1]) * (net[1][0] - other_net[1][0]) - (net[1][0] - net[0][0]) * (net[1][1] - other_net[1][1])

            # Check for expected intersections
            if (p0 * p1 < 0) and (p2 * p3 < 0):
                exp_intersections += 1

    print(f"There are {exp_intersections} intersections expected, {round(exp_intersections / len(net_coordinates), 2)} per net on average.")
    return exp_intersections


def check_density(net_coordinates):
    size = [0, 0]

    minimal_lengths = []
    for net in net_coordinates.values():
        x1 = net[0][0]
        x2 = net[1][0]
        y1 = net[0][1]
        y2 = net[1][1]
        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)

        if x1 > size[0]:
            size[0] = x1 + 1
        elif x2 > size[0]:
            size[0] = x2 + 1

        if y1 > size[1]:
            size[1] = y1 + 1
        elif y2 > size[1]:
            size[1] = y2 + 1

        minimal_lengths.append(delta_x + delta_y)
    minimal_lengths = np.array(minimal_lengths)
    total_segments = np.sum(minimal_lengths)
    density = total_segments / (size[0]*(size[1] - 1) + size[1]*(size[0] - 1))

    print(f"The average distance between the two gates a net connects is {round(np.average(minimal_lengths), 2)} +/- {round(np.std(minimal_lengths), 2)}")
    print(f"In total, at least {total_segments} are required. This results in {round(100 * density, 2)} % of the grid to be filled assuming only 1 layer.")

    return(density)


def main(netlist, randomized, n):
    chip = int((netlist - 1) / 3)
    overflow = False
    solved = False
    cost = 0

    nets = load_nets(netlist, n, chip, randomized)
    gates, coordinates = load_gates(chip)

    net_coordinates = {}
    for net in nets:
        start = coordinates[net[0]]
        end = coordinates[net[1]]
        net_coordinates[net] = (start, end)

    intersections = check_intersections(net_coordinates)

    density = check_density(net_coordinates)

    if check_gate_occupation(nets, gates) == "impossible":
        overflow = True
        return (density, intersections, overflow, solved, cost)
    else:
        print("No reason to conclude this netlilst is impossible (yet ...)")

    solvegrid = grid.Grid(chip, netlist, randomized=randomized)
    solve = a_star.A_Star(solvegrid, [sort.sort_length, False], 0, 0)

    if solve.run():
        print("cookie")
        solved = True
        solvegrid.compute_costs()
        cost = solvegrid.cost

    return (density, intersections, overflow, solved, cost)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyse a netlist')
    parser.add_argument("netlist", type=int, help="Netlist to be inspected")
    parser.add_argument("-random", "--randomized", action='store_true', help="Choose randomly generated netlists instead of the originals.")
    parser.add_argument("-n", type=int, default=1, dest="N", help="number of solutions analyzed")

    # Parse the command line arguments
    args = parser.parse_args()

    with open(f"output/netlist_test.csv", "w", newline="") as csvfile:
        
        fieldnames = ["simulation", "cost", "density", "intersections", "occupation overflow", "solved"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for n in range(1, args.N + 1):
            make.main(args.netlist, 1)
            answers = main(args.netlist, args.randomized, 1)
            writer.writerow({
                "simulation": n, 
                "cost": answers[4],
                "density": answers[0], 
                "intersections": answers[1], 
                "occupation overflow": answers[2], 
                "solved": answers[3],
                })
