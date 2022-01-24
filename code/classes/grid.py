import csv
from code.classes import gate, netlist
import pandas as pd


class Grid:
    def __init__(self, chip, netlist, infile=None):

        self.chip = chip
        self.netlist = netlist
        self.infile = infile
        self.size = [0, 0, 7]

        # All intersections
        self.intersections = 0

        self.tot_attempts = 0

        # All segments
        self.wire_segments = {}

        # Dictionary of coordinates gates
        self.gates = {}

        # Set op gate points
        self.gate_coordinates = set()

        # Dictionary containing all connections
        self.netlists = {}

        # Set boundaries such that the paths do not leave the grid
        self.layers= ()

        # Create gate objects
        self.load_gates()

        # Create netlist objects
        self.load_netlists()
        if infile:
            self.load_configuration()

        self.cost = 0

    def load_configuration(self):
        """Load a previously generated set of netlists."""

        # Extract data from csv
        data = pd.read_csv(self.infile)
        x = pd.Series.tolist((data['x'].str.split(';')))
        y = pd.Series.tolist(data['y'].str.split(';'))
        z = pd.Series.tolist(data['z'].str.split(';'))
        
        # Run over all imported netlists
        for i in range(len(x)):

            # Change to list of integers
            for j in range(len(x[i])):
                x[i][j] = int(x[i][j])
            for j in range(len(y[i])):
                y[i][j] = int(y[i][j])
            for j in range(len(z[i])):
                z[i][j] = int(z[i][j])

            # Extract coordinates of the gates the netlist connects
            gate_origin = (x[i][0], y[i][0], 0)
            gate_destination = (x[i][-1], y[i][-1], 0)

            # Extract corresponding netlist from dictionry
            for netlist in self.netlists.values():
                if netlist.start == gate_origin and netlist.end == gate_destination:

                    # Save path to correct netlist
                    netlist.path = [x[i], y[i], z[i]]

        # Update grid
        self.update()

    def update(self):
        """Ensure dictionary of segments and number of intersections are up to date when a change in the configuration of the grid has been made."""
        
        # Reset dictionary wire segments and number of intersections
        self.wire_segments = {}
        self.intersections = 0

        # Run over netlists
        for netlist in self.netlists.values():
            netlist.current_length = 0

            # Extract path
            x, y, z = netlist.path[0], netlist.path[1], netlist.path[2]
            for coordinate in range(len(x) - 1):

                # Keep count of actual length
                netlist.current_length += 1

                # Temporarily save coordinates of each segment
                start = (x[coordinate], y[coordinate], z[coordinate])
                end = (x[coordinate + 1], y[coordinate + 1], z[coordinate + 1])

                # Check for intersections
                if [segment for segment in self.wire_segments if end in segment and end not in self.gate_coordinates]:
                    self.intersections += 1

                # Add segment to dictionary
                segment = (start, end)
                self.wire_segments[segment] = netlist

    def load_gates(self):
        """Reads requested file containing the location of the gates, and extracts their id's and coordinates. Creates gate object for each row"""

        with open (f"Data/chip_{self.chip}/print_{self.chip}.csv", 'r') as file:
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

    def load_netlists(self):
        """Reads requested file containing the requested netlists, and extracts their starting and ending coordinates. Creates gate object for each row"""

        with open (f"Data/chip_{self.chip}/netlist_{self.netlist}.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:

                # Extract coordinates
                start_gate_id, end_gate_id = int(row['chip_a']), int(row['chip_b'])

                # Retrieve gate objects corresponding with coordinates
                start_gate = self.gates[start_gate_id]
                end_gate = self.gates[end_gate_id]

                # Make netlist object
                netlist_object = netlist.Netlist(start_gate.coordinates, end_gate.coordinates, self)

                # Create unique key per netlist
                key = (start_gate_id, end_gate_id)

                # Store netlist in dictionary with unique key
                self.netlists[key] = netlist_object

    def to_csv(self, number=None, name=""):
        """Writes a csv file that contains an overview of the grid"""

        netlists = {}
        x = {}
        y = {}
        z = {}

        # Run over netlists
        for item in self.netlists:

            # Extract list for coordinate in each dimension
            x_path = [str(element) for element in self.netlists[item].path[0]]
            y_path = [str(element) for element in self.netlists[item].path[1]]
            z_path = [str(element) for element in self.netlists[item].path[2]]

            # Make individual coordinates ;-seperated
            x[item] = ";".join(x_path)
            y[item] = ";".join(y_path)
            z[item] = ";".join(z_path)
            netlists[item] = item

        # Ensure correct file is created/modified
        if number:
            string = f"_C_{number}"
        else:
            string = ""

        if name:
            name = f"{name}_"
        else:
            name = ""
        
        # Save dataframe to csv
        df = pd.DataFrame({'netlist': netlists, 'x': x, 'y': y, 'z': z})
        df.to_csv(f"output/paths_netlist_{name}{self.netlist}{string}.csv", index=False)

    def compute_costs(self):
        """Calculate total cost of the current configuration"""

        self.update()
        wire_amount = len(self.wire_segments)

        # Update cost
        self.cost = wire_amount + 300 * self.intersections

    def __str__(self) -> str:
        return (f"grid for chip {self.chip} with netlist {self.netlist} \n"
                f"\033[1mCost: \033[0m\t\t{self.cost} \n"
                f"\033[1mIntersections: \033[0m\t{self.intersections} \n"
                f"\033[1mGates: \033[0m\t\t{self.gate_coordinates}\n"
                f"\033[1mWire: \033[0m\t\t{self.wire_segments}\n")
