import pylab
import csv

class Grid:
    def __init__(self):

        # All coorinates where a linesegment is located
        self.points = set()

        # Dictionary of coordinates gates
        self.gates = {}

        self.netlists = {}

        self.load_gates()

        self.load_netlists()

        self.make_connections()

    def merge(self):
        pass


    def load_gates(self):
        chip = "chip_0"
        netlist = "print_0"
        with open (f"Data/{chip}/{netlist}.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    id, x, y = int(row[0]), int(row[1]), int(row[2])

                    gate = Gate(id, x, y)
                    self.gates[id] = gate
                except ValueError:
                    pass

    def load_netlists(self):
        chip = "chip_0"
        netlist = "netlist_1"
        with open (f"Data/{chip}/{netlist}.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    start_coordinates, end_coordinates = int(row[0]), int(row[1])
                    start_gate = self.gates[start_coordinates]
                    end_gate = self.gates[end_coordinates]

                    key = (start_coordinates, end_coordinates)

                    netlist = Netlist(start_gate.chips, end_gate.chips, self)
                    self.netlists[key] = netlist
                    
                except ValueError:
                    pass

    def make_connections(self):
        for netlist in self.netlists:
            start = self.netlists[netlist].start.copy()
            end = self.netlists[netlist].end
            x, y = self.netlists[netlist].find_path(start, end)
            pylab.plot(x, y)
        pylab.savefig("test.png")


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
        x = []
        y = []

        while True:
            x.append(position[0])
            y.append(position[1])
            new_position = self.find_smartest_step(position, end)
            if new_position:
                position = new_position
            else:
                return x, y

    def find_smartest_step(self, position, destination):
        """Calculate step to follow shortest path from current position to any location. If position equals destination, return None"""

        # No new position is required when destination is already reached
        if position == destination:
            return

        # Calculate total movement before destination is reached
        direction = (destination[0] - position[0], destination[1] - position[1])

        if direction[1] != 0:
            step_in_direction = 1
        else:
            step_in_direction = 0

        # Make single step in right direction
        position[step_in_direction] += direction[step_in_direction] // abs(direction[step_in_direction])

        return position
    

Grid()