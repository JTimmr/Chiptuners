import csv
from code.classes import gate, net
import pandas as pd
import math


class Grid:
    def __init__(self, chip, netlist, infile=None, randomized=False):

        self.chip = chip
        self.netlist = netlist
        self.infile = infile
        self.size = [0, 0, 7]
        self.randomized = randomized

        self.intersections = 0

        self.wire_segments = {}

        self.coordinates = set()

        # Dictionary containing all gates {gate_number: Gate}
        self.gates = {}

        self.gate_coordinates = set()

        # Dictionary containing all connections: {(startID, endID): Net}
        self.nets = {}

        # Create gate objects
        self.load_gates()

        # Create net objects
        self.load_nets()

        # Load previously generated configuration of one is given
        if infile:
            self.load_configuration()

        self.cost = 0

        self.theoretical_minimum = 0

    def load_configuration(self):
        """Loads a previously generated set of nets."""

        # Extract data from csv
        data = pd.read_csv(self.infile)
        x = pd.Series.tolist((data['x'].str.split(';')))
        y = pd.Series.tolist(data['y'].str.split(';'))
        z = pd.Series.tolist(data['z'].str.split(';'))

        # Run over all imported nets and change to list of ints
        for i in range(len(x)):

            for j in range(len(x[i])):
                x[i][j] = int(x[i][j])
            for j in range(len(y[i])):
                y[i][j] = int(y[i][j])
            for j in range(len(z[i])):
                z[i][j] = int(z[i][j])

            # Extract coordinates of the gates the net connects
            gate_origin = (x[i][0], y[i][0], 0)
            gate_destination = (x[i][-1], y[i][-1], 0)

            # Extract corresponding net from dictionary
            for net_object in self.nets.values():
                if (net_object.start == gate_origin and
                        net_object.end == gate_destination):

                    # Save path to correct net
                    net_object.path = [x[i], y[i], z[i]]

        # Update grid
        self.update()

    def update(self):
        """
        Ensure dictionary of segments and number of intersections are up
        to date when a change in the configuration of the grid has been made.
        """

        # Reset dictionary wire segments and number of intersections
        self.wire_segments = {}
        self.intersections = 0

        # Run over nets to extract their paths
        for net_object in self.nets.values():
            net_object.current_length = 0

            x, y, z = (net_object.path[0],
                       net_object.path[1],
                       net_object.path[2])

            for coordinate in range(len(x) - 1):

                # Keep count of actual length
                net_object.current_length += 1

                # Temporarily save coordinates of each segment
                start = (x[coordinate], y[coordinate], z[coordinate])
                end = (x[coordinate + 1], y[coordinate + 1], z[coordinate + 1])

                # Check for intersections
                if [segment for segment in self.wire_segments if end in segment
                        and end not in self.gate_coordinates]:
                    self.intersections += 1

                segment = self.make_segment(start, end)

                # Add segment to dictionary
                self.wire_segments[segment] = net_object
                self.coordinates.add(segment[0])
                self.coordinates.add(segment[1])

    def make_segment(self, start, end):
        """
        Saves two coordinates as a tuple, and ensure two identical segments are
        never stored in reverse order (a, b VS b, a).
        """

        if ((math.sqrt(sum(i**2 for i in end))) >= (math.sqrt(sum(i**2 for i in start)))):
            return (start, end)
        else:
            return (end, start)

    def load_gates(self):
        """
        Reads requested file containing the location of the gates,
        and extracts their id's and coordinates.
        Creates gate object for each row.
        """

        with open(f"data/chip_{self.chip}/print_{self.chip}.csv", 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:

                # Extract information
                uid, x, y = int(row['chip']), int(row['x']), int(row['y'])

                self.gate_coordinates.add((x, y, 0))

                # Find the size of the grid
                if x > self.size[0]:
                    self.size[0] = x + 1

                if y > self.size[1]:
                    self.size[1] = y + 1

                # Make object and add to dictionary
                gate_object = gate.Gate(uid, x, y, 0)
                self.gates[uid] = gate_object

    def load_nets(self):
        """
        Reads requested file containing the requested nets,
        and extracts their starting and ending coordinates.
        Creates gate object for each row.
        """

        if self.randomized:
            add = "random/"
        else:
            add = ""

        with open(f"data/chip_{self.chip}/{add}netlist_{self.netlist}_1.csv") as file:
        # with open(f"data/chip_{self.chip}/random/netlist_{self.netlist}_1.csv") as file:
            reader = csv.DictReader(file)

            for row in reader:

                # Extract coordinates
                start_gate_id, end_gate_id = (int(row['chip_a']),
                                              int(row['chip_b']))

                # Retrieve gate objects corresponding with coordinates
                start_gate = self.gates[start_gate_id]
                end_gate = self.gates[end_gate_id]

                # Make net object
                net_object = net.Net(start_gate.coordinates, end_gate.coordinates,  self)

                # Create unique key per net
                key = (start_gate_id, end_gate_id)
                net_object.key = key

                # Store net in dictionary with unique key
                self.nets[key] = net_object

    def to_csv(self, number=None, name=""):
        """Writes a csv file that contains all paths in the grid."""

        nets = {}
        x = {}
        y = {}
        z = {}

        # Run over nets
        for item in self.nets:

            # Extract list for coordinate in each dimension
            x_path = [str(element) for element in self.nets[item].path[0]]
            y_path = [str(element) for element in self.nets[item].path[1]]
            z_path = [str(element) for element in self.nets[item].path[2]]

            # Make individual coordinates ;-seperated
            x[item] = ";".join(x_path)
            y[item] = ";".join(y_path)
            z[item] = ";".join(z_path)
            nets[item] = item

        # Ensure correct file is created/modified
        if number:
            string = f"_C_{number}"
        else:
            string = ""

        if name:
            name = f"_{name}"
        else:
            name = ""

        if self.randomized:
            add = "random_"
        else:
            add = ""

        # Save dataframe to csv
        df = pd.DataFrame({'net': nets, 'x': x, 'y': y, 'z': z})
        df.to_csv(f"output/{add}paths_netlist_{self.netlist}{name}{string}.csv", index=False)

    def compute_costs(self):
        """Calculates total cost of the current configuration."""

        self.update()
        wire_amount = len(self.wire_segments)

        # Update cost
        self.cost = wire_amount + 300 * self.intersections

    def compute_minimum(self):
        for net_object in self.nets.values():
            self.theoretical_minimum += net_object.minimal_length

    def __str__(self) -> str:
        return (f"grid for chip {self.chip} with netlist {self.netlist} \n"
                f"\033[1mCost: \033[0m\t\t{self.cost} \n"
                f"\033[1mIntersections: \033[0m\t{self.intersections} \n"
                f"\033[1mGates: \033[0m\t\t{self.gate_coordinates}\n"
                f"\033[1mWire: \033[0m\t\t{self.wire_segments}\n")
