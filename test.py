import random
import pylab
import csv

class Grid:
    def __init__(self):

        # All coorinates where a linesegment is located
        self.points = set()

        # Dictionary of coordinates gates
        self.gates = {}

        # Set of all connections between gates
        self.netlists = set()

        self.load_gates()

        self.load_netlists()

        self.make_connections()


    def load_gates(self):
        chip = "chip_0"
        netlist = "print_0"
        with open (f"Data/{chip}/{netlist}.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    id, x, y = int(row[0]), int(row[1]), int(row[2])
                    
                    # print(f"Row id: {id}")
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
                    start, end = int(row[0]), int(row[1])
                    start = self.gates[start]
                    end = self.gates[end]

                    # print(f"Netlist from {start} to {end}")
                    netlist = Netlist(start, end, self)
                    self.netlists.add(netlist)
                except ValueError:
                    pass

    def make_connections(self):
        for netlist in self.netlists:
            start = netlist.start
            end = netlist.end
            start = start.chips
            end = end.chips
            netlist.find_path(start, end)

    def add_wire():
        pass


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
    
    def find_path(self, position, destination):
        print("test")
        while True:
            new_position = self.find_smartest_step(position, destination)
            if new_position:
                position = new_position
            else:
                break

    def find_smartest_step(self, position, destination):
        """Calculate step to follow shortest path from current position to any location. If position equals destination, return None"""

        # No new position is required when destination is already reached
        if position == destination:
            return
        
        # Calculate total movement before destination is reached
        direction = [destination[0] - position[0], destination[1] - position[1]]
        print(direction)

        weights = direction
        for i in range(len(direction)):
            weights[i] = abs(direction[i])

        # Choose random move, weighted with number of required steps
        step_in_direction = random.choices([0, 1], weights)[0]

        # Make single step in right direction
        position[step_in_direction] += direction[step_in_direction] // abs(direction[step_in_direction])

        return position
    

