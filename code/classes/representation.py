import pylab
import csv
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

        # Create gate objects
        self.load_gates()

        # Create netlist objects
        self.load_netlists()

        # Find shortest connection paths
        self.make_connections()

        self.cost = 0


    def load_gates(self):
        """Reads requested file containing the location of the gates, and extracts their id's and coordinates. Creates gate object for each row"""

        with open (f"Data/chip_{self.chip}/print_{self.chip}.csv") as file:
            reader = csv.reader(file)
            for row in reader:

                # Only take rows with the actual data into account
                try:
                    id, x, y = int(row[0]), int(row[1]), int(row[2])

                    self.gate_coordinates.add((x,y))

                    # Make object and add to dictionary
                    gate = Gate(id, x, y)
                    self.gates[id] = gate

                except ValueError:
                    pass

    def load_netlists(self):
        """Reads requested file containing the requested netlists, and extracts their starting and ending coordinates. Creates gate object for each row"""

        with open (f"Data/chip_{self.chip}/netlist_{self.netlist}.csv") as file:
            reader = csv.reader(file)
            for row in reader:

                # Only take rows with the actual data into account
                try:

                    # Extract coordinates
                    start_gate_id, end_gate_id = int(row[0]), int(row[1])

                    # Retrieve gate objects corresponding with coordinates
                    start_gate = self.gates[start_gate_id]
                    end_gate = self.gates[end_gate_id]

                    # Make netlist object
                    netlist = Netlist(start_gate.coordinates, end_gate.coordinates, self)

                    # Create unique key per netlist
                    key = (start_gate_id, end_gate_id)

                    # Store netlist in dictionary with unique key
                    self.netlists[key] = netlist
                    
                except:
                    pass

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

            # set up fieldnames 
            fieldnames = ["net", "wires"]

            # set up wiriter and write the header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # write the net and wire values
            for item in self.netlists:
                writer.writerow({
                    "net": item, "wires": self.netlists[item].path
                    })

            # write total cost for the grid
            writer.writerow({"net": f"chip_{self.chip}_net_{self.netlist}", "wires": f"C = {self.cost}"})

    def compute_costs(self):
        
        wire_amount = len(self.wire_segments)

        # Update cost
        self.cost = wire_amount + 300 * self.intersections

        return self.cost



class Gate:
    def __init__(self, id, x, y) -> None:
        self.id = id
        self.coordinates = (x,y)


class Netlist:
    def __init__(self, start, end, grid) -> None:
        self.start = start
        self.end = end
        self.grid = grid
        self.path = []
    
    def find_path(self, position, destination):
        """Find the shortest path between two coordinates on a grid"""

        # Store path so plot can be made
        x = []
        y = []

        # Until destination is reached
        while True:
            x.append(position[0])
            y.append(position[1])

            self.path.append(position)

            # Find smartest move from current position to destination
            new_position = self.find_smartest_step(position, destination)

            # If destination is not reached, make step
            if new_position:

                # If the coordinate is not in the gate add wire segment and check for intersections
                if new_position not in self.grid.gate_coordinates:

                    # Check if current segment makes an interection
                    if [segment for segment in self.grid.wire_segments if new_position in segment]:
                        print(f"Intersection at: {new_position}")
                        self.grid.intersections += 1

                self.grid.wire_segments.add((position,new_position))
                    
                position = new_position

            # Return path if destination is reached
            else:
                return x, y


    def find_smartest_step(self, position, destination):
        """Calculate step to follow shortest path from current position to any location. If position equals destination, return None"""

        # No new position is required when destination is already reached
        if position == destination:
            return

        # Calculate total movement before destination is reached
        direction = (destination[0] - position[0], destination[1] - position[1])

        # First move in the y direction
        if direction[1] != 0:
            step_in_direction = 1
        else:
            step_in_direction = 0

        new_position = list(position)

        # Make single step in right direction
        new_position[step_in_direction] += direction[step_in_direction] // abs(direction[step_in_direction])
    
        new_position = tuple(new_position)

        return new_position
