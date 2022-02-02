import csv
import random
import argparse


def load_gates(chip):
    """
    Reads requested file containing the location of the gates,
    and extracts their id's and coordinates.
    Creates gate object for each row.
    """

    num_gates = 0

    with open(f"data/chip_{chip}/print_{chip}.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:

            num_gates += 1
    return num_gates


def load_nets(netlist, chip):
    """
    Reads requested file containing the requested nets,
    and extracts their starting and ending coordinates.
    Creates gate object for each row.
    """

    num_nets = 0
    with open(f"data/chip_{chip}/netlist_{netlist}.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            num_nets += 1

    return num_nets


def main(netlist):
    """
    Creates a random netlist equivalent of the netlist given as argument.
    Netlist will be stored in a CSV file, in the correct chip subfolder in the data directory.
    To prevent overwriting the original netlists, the random netlists will be stored in a folder named random.
    For the random netlists, there are a few criteria:
    - The number of nets are identical to the original netlist (hence 'eqiuivalent')
    - A gate cannot make a connection with itself
    - Each net in a netlist is unique. If path a to b already exists, neither a to b nor b to a can be added to the netlist.
    """

    # Calculate chip number from netlist number
    chip = int((netlist - 1) / 3)

    # Extract number of gates and nets
    num_gates = load_gates(chip)
    num_nets = load_nets(netlist, chip)

    # Creates random netlist conform to the criteria
    nets = set()
    while len(nets) < num_nets:
        gates = [i + 1 for i in range(num_gates)]
        start = random.choice(gates)

        # Ensure gate does not connect with itself
        gates.remove(start)
        end = random.choice(gates)

        # Ensure each net is unique
        if (start, end) not in nets and (end, start) not in nets:
            nets.add((start, end))

    # Save netlist to CSV
    with open(f"data/chip_{chip}/random/netlist_{netlist}.csv", "w", newline="") as csvfile:

        # Set up fieldnames
        fieldnames = ["chip_a", "chip_b"]

        # Set up wiriter and write the header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for net in nets:
            writer.writerow({
                "chip_a": net[0], "chip_b": net[1]
            })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make a new netlist')
    parser.add_argument("netlist", type=int, help="Netlist to be remade")

    # Parse the command line arguments
    args = parser.parse_args()

    main(args.netlist)
