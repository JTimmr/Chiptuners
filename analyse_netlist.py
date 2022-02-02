"""
analyse_netlist.py

Calculates a number of factors which might influence the solvability of a netlist without actually solving it.
Netlist will only be solved if those factors cannot guarantee it is impossibe to solve. Factors to be calculated are:
- Number of connections the most occupied gate has to make
- Average pathlength of all nets if a greedy algorithm solves the netlist without preventing collisions or intersections
- Sum of all pathlengths if all paths are solved with a greedy algorithm without preventing collisions or intersecionts
- Density of the lowest layer if sum of all pathlengths are stored in the lowest layer
- Estimated number of intersections, calculated by drawing straight lines for all nets and keeping count of the intersections
- Average number of intersections per net

A gate can host no more than 5 connections, so a solution cannot be found and hence will not be searched for
if a gate has to make 6 connections or more. Otherwise, a solution will be searched for using an A* algorithm.
The arguments for the A* are pop=0, gate_space=2, sorting_algorithm=(sort_length, acending).
See the README on Github of or the description in A_star.py for an explanation of what those parameters represent.
It could very well be that this set of parameters can't find a solution while another set can, but
it takes way too long to test a large set of netlists with all different combinations.
"""


import csv
import argparse
from copy import deepcopy
import numpy as np
import make_netlists as make
import code.algorithms.A_star as a_star
import code.algorithms.sorting as sort
import code.classes.grid as grid


def load_nets(netlist, chip, randomized):
    """
    Reads requested file containing the requested nets,
    and extracts their starting and ending coordinates.
    Creates gate object for each row.
    """

    # Ensure correct netlist is loaded
    if randomized:
        add = "random/"
    else:
        add = ""

    # Extract information from CSV
    nets = set()
    with open(f"data/chip_{chip}/{add}netlist_{netlist}.csv") as file:
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

    # Dictionary where number of connections per gate will be stored
    gates = {}

    # Dictionary where gate_id with its coordinates will be stored
    coordinates = {}

    with open(f"data/chip_{chip}/print_{chip}.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            gate = (row['chip'])
            gates[gate] = 0
            coordinates[gate] = (int(row['x']), int(row['y']))
    return gates, coordinates


def check_gate_occupation(nets, gates, display):
    """"
    Each gate lies on the lowest layer, which implies a gate can make no more than 5 connections,
    since each point on the lowest layer has 5 neighboring points.
    Hence this function counts the number of connections each gate has to make, and returns "impossible"
    if a gate has to make 6 connections or more.
    """

    # Run over all nets
    for net in nets:

        # Add one to counter of both gates
        gates[net[0]] += 1
        gates[net[1]] += 1

        # Check if gate can host the required number of connections
        a = "which is not possible. This netlist cannot be solved."

        if gates[net[0]] > 5:
            if display:
                print(f"Gate {net[0]} has to make at least {gates[net[0]]} connections, {a}")
                print(f"\n{'---'*40}\n")
            return "impossible"
        if gates[net[1]] > 5:
            if display:
                print(f"Gate {net[1]} has to make at least {gates[net[1]]} connections, {a}")
                print(f"\n{'---'*40}\n")
            return "impossible"


def check_intersections(net_coordinates, display):
    """
    Estimate the number of intersections this netlist will produce.
    This algorithm draws straight lines between all gates which have to be connected, and
    counts the number of intersections. This is not a valid solution for the netlist,
    since these lines won't follow the gridlines, yet it might give an indication of
    the number of intersections when a greedy algorithm tries to solve the netlist in one dimension.
    """

    exp_intersections = 0

    # Run over all nets
    for net in net_coordinates:

        # Make new dictionary of nets excluding the examined one
        other_nets = deepcopy(net_coordinates)
        del other_nets[net]
        net = net_coordinates[net]

        # Run over all other nets
        for other_net in other_nets.values():

            # Calculate relevant factors accoring to formulas

            # p0 = (y3 - y2)(x3 - x0) - (x3 - x2)(y3 - y0)
            p0 = (other_net[1][1] - other_net[0][1]) * (other_net[1][0] - net[0][0]) - \
                 (other_net[1][0] - other_net[0][0]) * (other_net[1][1] - net[0][1])

            # p1 = (y3 - y2)(x3 - x1) - (x3 - x2)(y3 - y1)
            p1 = (other_net[1][1] - other_net[0][1]) * (other_net[1][0] - net[1][0]) - \
                 (other_net[1][0] - other_net[0][0]) * (other_net[1][1] - net[1][1])

            # p2 = (y1 - y0)(x1 - x2) - (x1 - x0)(y1 - y2)
            p2 = (net[1][1] - net[0][1]) * (net[1][0] - other_net[0][0]) - \
                 (net[1][0] - net[0][0]) * (net[1][1] - other_net[0][1])

            # p3 = (y1 - y0)(x1 - x3) - (x1 - x0)(y1 - y3)
            p3 = (net[1][1] - net[0][1]) * (net[1][0] - other_net[1][0]) - \
                 (net[1][0] - net[0][0]) * (net[1][1] - other_net[1][1])

            # Check for expected intersections
            if (p0 * p1 < 0) and (p2 * p3 < 0):
                exp_intersections += 1

    # Prints results if requested
    if display:
        a = round(exp_intersections / len(net_coordinates), 2)
        print(f"\n{'---'*40}\n")
        print(f"There are {exp_intersections} intersections expected, {a} per net on average.")

    return exp_intersections


def check_density(net_coordinates, display):
    """
    Calculate the total number of segments used if each neet follows the shortest path, as a greedy algorithm
    would produce them. Calculates the average length per net, and calculates the percentage of segments which
    will be filled of the required number of segments are all stored within the lowest layer. This can most of the time
    not produce a valid solution, so this is only an indication of the density of the grid."""

    # Stores dimension of the grid
    size = [0, 0]

    minimal_lengths = []
    for net in net_coordinates.values():

        # Calculate minimal pathlength
        x1 = net[0][0]
        x2 = net[1][0]
        y1 = net[0][1]
        y2 = net[1][1]
        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)

        # Keep size of grid up to date
        if x1 > size[0]:
            size[0] = x1 + 1
        elif x2 > size[0]:
            size[0] = x2 + 1

        if y1 > size[1]:
            size[1] = y1 + 1
        elif y2 > size[1]:
            size[1] = y2 + 1

        # Add pathlength to list
        minimal_lengths.append(delta_x + delta_y)

    # Convert list to numpy array, and calculate total number of segments and corresponding density
    minimal_lengths = np.array(minimal_lengths)
    total_segments = np.sum(minimal_lengths)
    density = total_segments / (size[0]*(size[1] - 1) + size[1]*(size[0] - 1))

    # Print results if requested
    if display:
        a = round(np.average(minimal_lengths), 2)
        b = round(np.std(minimal_lengths), 2)
        print(f"""The average distance between the two gates a net connects is {a} +/- {b}""")
        print(f"In total, at least {total_segments} segments are required. ")
        print(f"This results in {round(100 * density, 2)} % of the grid to be filled assuming only 1 layer.")

    return(density)


def main(netlist, randomized, display):
    """
    Calculates a number of factors which might influence the solvability of a netlist without actually solving it.
    Netlist will only be solved if those factors cannot guarantee it is impossibe to solve. Factors to be calculated are:
    - Number of connections the most occupied gate has to make
    - Average pathlength of all nets if a greedy algorithm solves the netlist without preventing collisions or intersections
    - Sum of all pathlengths if all paths are solved with a greedy algorithm without preventing collisions or intersecionts
    - Density of the lowest layer if sum of all pathlengths are stored in the lowest layer
    - Estimated number of intersections, calculated by drawing straight lines for all nets and keeping count of the intersections
    - Average number of intersections per net
    
    A gate can host no more than 5 connections, so a solution cannot be found and hence will not be searched for
    if a gate has to make 6 connections or more. Otherwise, a solution will be searched for using an A* algorithm.
    The arguments for the A* are pop=0, gate_space=2, sorting_algorithm=(sort_length, acending).
    See the README on Github of or the description in A_star.py for an explanation of what those parameters represent.
    It could very well be that this set of parameters can't find a solution while another set can, but
    it takes way too long to test a large set of netlists with all different combinations.
    """

    # Calculate chip number from netlist number
    chip = int((netlist - 1) / 3) 
    overflow = False
    solved = False
    cost = 0

    # Load nets
    nets = load_nets(netlist, chip, randomized)

    # Load gates
    gates, coordinates = load_gates(chip)

    # Make dictionary containing netlist_id and start- and end coordinates
    net_coordinates = {}
    for net in nets:
        start = coordinates[net[0]]
        end = coordinates[net[1]]
        net_coordinates[net] = (start, end)

    # Estimate number of intersections
    intersections = check_intersections(net_coordinates, display)

    # Calculate density
    density = check_density(net_coordinates, display)

    # Check if there is a gate-overflow
    if check_gate_occupation(nets, gates, display) == "impossible":
        overflow = True
        return (cost, density, intersections, overflow, solved)
    else:
        if display:
            print("No reason to conclude this netlist is impossible (yet ...)")
            print(f"\n{'---'*40}\n")

    # Solve netlist if it seems possible
    solvegrid = grid.Grid(chip, netlist, randomized=randomized)

    solve = a_star.A_Star(solvegrid, [sort.sort_length, False], 0, 2, display)

    # If netlist could be solved, calculate costs
    if solve.run():
        solved = True
        solvegrid.compute_costs()
        cost = solvegrid.cost
        print("Netlist solved!")
        print()

    return cost, density, intersections, overflow, solved


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyse a netlist')
    parser.add_argument("netlist", type=int, help="Netlist to be inspected")
    parser.add_argument("-random", "--randomized", action='store_true', help="Choose randomly generated netlists.")
    parser.add_argument("-n", type=int, default=1, dest="N", help="number of solutions analyzed")
    parser.add_argument("-print", "--display", action='store_true', help="Prints the calculated data.")

    # Parse the command line arguments
    args = parser.parse_args()

    with open(f"results/netlist_test{args.netlist}.csv", "w", newline="") as csvfile:

        fieldnames = ["simulation", "cost", "density", "intersections", "occupation overflow", "solved"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for n in range(1, args.N + 1):
            make.main(args.netlist)
            answers = main(args.netlist, args.randomized, args.display)
            writer.writerow({
                "simulation": n,
                "cost": answers[0],
                "density": answers[1],
                "intersections": answers[2],
                "occupation overflow": answers[3],
                "solved": answers[4],
                })
