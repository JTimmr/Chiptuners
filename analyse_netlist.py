import csv
import argparse


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

    with open(f"data/chip_{chip}/print_{chip}.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            gate = (row['chip'])
            gates[gate] = 0
    return gates


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


def main(netlist, randomized):
    chip = int((netlist - 1) / 3)

    nets = load_nets(netlist, chip, randomized)
    gates = load_gates(chip)

    if check_gate_occupation(nets, gates) == "impossible":
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyse a netlist')
    parser.add_argument("netlist", type=int, help="Netlist to be inspected")
    parser.add_argument("-random", "--randomized", action='store_true', help="Choose randomly generated netlists instead of the originals.")

    # Parse the command line arguments
    args = parser.parse_args()

    main(args.netlist, args.randomized)
