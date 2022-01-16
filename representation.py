import pylab
import csv

class Grid:
    def __init__(self, chip, netlist):

        self.chip = chip
        self.netlist = netlist

        # All coorinates where a linesegment is located
        self.points = set()

        # Dictionary of coordinates gates
        self.gates = {}

        # Dictionary containing all connections
        self.netlists = {}

        # Create gate objects
        self.load_gates()

        # Create netlist objects
        self.load_netlists()

        # Find shortest connection paths
        self.make_connections()


    def load_gates(self):
        """Reads requested file containing the location of the gates, and extracts their id's and coordinates. Creates gate object for each row"""

        with open (f"Data/chip_{self.chip}/print_{self.chip}.csv") as file:
            reader = csv.reader(file)
            for row in reader:

                # Only take rows with the actual data into account
                try:
                    id, x, y = int(row[0]), int(row[1]), int(row[2])

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
                    start_coordinates, end_coordinates = int(row[0]), int(row[1])

                    # Retrieve gate objects corresponding with coordinates
                    start_gate = self.gates[start_coordinates]
                    end_gate = self.gates[end_coordinates]

                    # Make netlist object
                    netlist = Netlist(start_gate.chips, end_gate.chips, self)

                    # Create unique key per netlist
                    key = (start_coordinates, end_coordinates)

                    # Store netlist in dictionary with unique key
                    self.netlists[key] = netlist
                    
                except:
                    pass

    def make_connections(self):
        """Connects two points on the grid, and plots the result"""

        for netlist in self.netlists:

            # Retrieve starting and ending point
            start = self.netlists[netlist].start.copy()
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
        pylab.savefig("test.png", dpi=100, bbox_inches="tight")


class Gate:
    def __init__(self, id, x, y) -> None:
        self.x = x
        self.y = y
        self.id = id
        self.chips = [x,y]


class Netlist:
    def __init__(self, start, end, grid) -> None:
        self.start = start
        self.end = end
        self.grid = grid
    
    def find_path(self, position, end):
        """Find the shortest path between two coordinates on a grid"""

        # Store path so plot can be made
        x = []
        y = []

        # Until destination is reached
        while True:
            x.append(position[0])
            y.append(position[1])

            # Find smartest move from current position to destination
            new_position = self.find_smartest_step(position, end)

            # If destination is not reached, make step
            if new_position:
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

        # Make single step in right direction
        position[step_in_direction] += direction[step_in_direction] // abs(direction[step_in_direction])

        return position


chip = "2"
netlist = "7"
Grid(chip, netlist)