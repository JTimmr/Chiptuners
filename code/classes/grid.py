import csv
from code.classes import gate, netlist


class Grid:
    def __init__(self, chip, netlist):

        self.chip = chip
        self.netlist = netlist
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

        self.cost = 0

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
    def to_csv(self):
        """Writes a csv file that contains an overview of the grid"""

        with open("output/output.csv", "w", newline="") as csvfile:

            # Set up fieldnames 
            fieldnames = ["net", "wires"]

            # Set up wiriter and write the header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Write the net and wire values
            for item in self.netlists:
                writer.writerow({
                    "net": item, "wires": self.netlists[item].path
                    })

            # Write total cost for the grid
            writer.writerow({"net": f"chip_{self.chip}_net_{self.netlist}", "wires": f"C = {self.cost}"})

    def compute_costs(self):
        """Calculate total cost of the current configuration"""
        
        wire_amount = len(self.wire_segments)

        # Update cost
        self.cost = wire_amount + 300 * self.intersections

    def __str__(self) -> str:
        return (f"grid for chip {self.chip} with netlist {self.netlist} \n"
                f"\033[1mCost: \033[0m\t\t{self.cost} \n"
                f"\033[1mIntersections: \033[0m\t{self.intersections} \n"
                f"\033[1mGates: \033[0m\t\t{self.gate_coordinates}\n"
                f"\033[1mWire: \033[0m\t\t{self.wire_segments}\n")
