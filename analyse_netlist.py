import csv
import argparse
from copy import deepcopy


def load_nets(netlist, chip, randomized):
    """
    Reads requested file containing the requested nets,
    and extracts their starting and ending coordinates.
    Creates gate object for each row.
    """
    
    if randomized:
        add = "random/"
    else:
        add = ""

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

    print(f"There are {exp_intersections} intersections expected, {exp_intersections / len(net_coordinates)} per net on average.")


def check_density(net_coordinates):
    for net in net_coordinates.values():
        delta_x = abs(net[0][0] - net[1][0])
        delta_y = abs(net[0][0] - net[1][0])

def main(netlist, randomized):
    chip = int((netlist - 1) / 3)

    nets = load_nets(netlist, chip, randomized)
    gates, coordinates = load_gates(chip)

    if check_gate_occupation(nets, gates) == "impossible":
        return
    else:
        print("No reason to conclude this netlilst is impossible (yet ...)")

        net_coordinates = {}
        for net in nets:
            start = coordinates[net[0]]
            end = coordinates[net[1]]
            net_coordinates[net] = (start, end)

    check_intersections(net_coordinates)

    check_density(net_coordinates)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyse a netlist')
    parser.add_argument("netlist", type=int, help="Netlist to be inspected")
    parser.add_argument("-random", "--randomized", action='store_true', help="Choose randomly generated netlists instead of the originals.")

    # Parse the command line arguments
    args = parser.parse_args()

    main(args.netlist, args.randomized)
