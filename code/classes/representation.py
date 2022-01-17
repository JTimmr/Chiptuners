import pylab
import csv
from code.algorithms.basic import base_movement
from copy import deepcopy

class Grid:
    def __init__(self, chip, netlist):

        self.chip = chip
        self.netlist = netlist

        # All intersections
        self.intersections = 0

        # All segments
        self.wire_segments = set()

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

        # Find shortest connection paths
        self.make_connections()

        self.cost = 0


    def load_gates(self):
        """Reads requested file containing the location of the gates, and extracts their id's and coordinates. Creates gate object for each row"""

        with open (f"Data/chip_{self.chip}/print_{self.chip}.csv", 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:

                # Extract information
                uid, x, y = int(row['chip']), int(row['x']), int(row['y'])

                self.gate_coordinates.add((x, y))

                # Make object and add to dictionary
                gate = Gate(uid, x, y)
                self.gates[uid] = gate


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
                netlist = Netlist(start_gate.coordinates, end_gate.coordinates, self)

                # Create unique key per netlist
                key = (start_gate_id, end_gate_id)

                # Store netlist in dictionary with unique key
                self.netlists[key] = netlist


    def make_connections(self):
        """Connects two points on the grid, and plots the result"""

        for netlist in self.netlists:
            # Retrieve starting and ending point
            start = deepcopy(self.netlists[netlist].start)
            end = self.netlists[netlist].end

            # Find the shortest path
            x, y = self.netlists[netlist].find_path(start, end)

            # Add path to plot
            pylab.plot(x, y, alpha = 0.5)
            pylab.locator_params(axis="both", integer=True)
            pylab.annotate(text = str(x[0])+ "," +str(y[0]), fontsize= 7, xy= (x[0], y[0]), xytext = (x[0] + 0.1, y[0] + 0.2))
            pylab.annotate(text = str(x[-1])+ "," +str(y[-1]), fontsize= 7, xy= (x[-1], y[-1]), xytext = (x[-1] + 0.1, y[-1] + 0.2))
            pylab.grid(alpha=0.2)
            pylab.xlabel('x-coordinates')
            pylab.ylabel('y-coordinates')
            pylab.legend(self.netlists, prop={'size': 7}, loc = "upper left", title = "netlist", ncol = 6, bbox_to_anchor=(0.0, -0.22))
            
        # Save plot
        pylab.savefig("output/visual.png", dpi=100, bbox_inches="tight")

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



class Gate:
    def __init__(self, uid, x, y) -> None:
        self.id = uid
        self.coordinates = (x,y)


class Netlist:
    def __init__(self, start, end, grid) -> None:
        self.start = start
        self.end = end
        self.grid = grid
        self.path = []
    
    def find_path(self, position, destination):
        """Find the shortest path between two coordinates on a grid"""

        x,y = base_movement(position, destination, self.grid, self.path)

        return x,y
