import random
from copy import deepcopy
import math
import code.algorithms.sorting as sort

class Hillclimber:
    def __init__(self, grid, limit):
        self.grid = grid
        self.limit = limit
        self.iterations = 0

    def run(self):
        while self.iterations < self.limit:
            netlists = sort.sort_length(self.grid.netlists, descending=True)
            for netlist in netlists:
                self.improve_connection(netlist)
            self.iterations += 1
            
        # self.grid.to_csv()

    def improve_connection(self, netlist):
        origin = netlist.start
        destination = netlist.end
        best_path = deepcopy(netlist.path)
        self.grid.compute_costs()
        best_costs = deepcopy(self.grid.cost)

        for attempt in range(100):
            new_path = self.find_path(origin, destination, netlist)
            if new_path:
                netlist.path = new_path
                self.grid.compute_costs()
                print(self.grid.cost, best_costs)
                if self.grid.cost < best_costs:
                    print(f"Improvement found: from {best_costs} to {self.grid.cost}")
                    best_path = deepcopy(new_path)
                    best_costs = deepcopy(self.grid.cost)



    def find_path(self, origin, destination, netlist):

        # Store path so plot can be made
        x = []
        y = []
        z = []
        max_pathlength = netlist.minimal_length * 2

        current_attempt = 0

        # Temporary values until path is confirmed
        origin_tmp = deepcopy(origin)
        wire_segments_tmp = {}
        intersections_tmp = 0
        path_tmp = []
        new_attempts = 0

        current_length = 0

        # Until destination is reached
        while current_length < max_pathlength:
            x.append(origin_tmp[0])
            y.append(origin_tmp[1])
            z.append(origin_tmp[2])

            path_tmp.append(origin_tmp)

            # Try random moves until a legal one is found
            while not (new_origin := self.find_smartest_step(origin_tmp, destination, path_tmp)):
                new_attempts += 1

                # Give up after 10 failed attempts to make a single step
                if new_attempts > 10:
                    return

            # If destination is not reached, make step
            if new_origin != "reached":

                # Save step as segment, and ensure two identical segments are never stored in reverse order (a, b VS b, a)
                if ((math.sqrt(sum(i**2 for i in origin_tmp))) >= (math.sqrt(sum(i**2 for i in new_origin)))):
                    segment = (new_origin, origin_tmp)
                else:
                    segment = (origin_tmp, new_origin)

                # Check if segment already in use, try again otherwise
                if segment in self.grid.wire_segments or segment in wire_segments_tmp:
                    return

                # Add segment to dictionary if it was new
                wire_segments_tmp[segment] = netlist

                # If the coordinate does not host a gate
                if new_origin not in self.grid.gate_coordinates:

                    # Check if current segment makes an interection
                    if [segment for segment in self.grid.wire_segments if new_origin in segment]:
                        intersections_tmp += 1
                    
                # Set new temporary origin
                origin_tmp = new_origin

                current_length += 1

            # Return path if destination is reached
            else:
                current_attempt += new_attempts

                # Make everything up to date
                self.grid.wire_segments.update(wire_segments_tmp)
                self.grid.intersections += intersections_tmp
                path = path_tmp

                return [x, y, z]

        # Return number of failed attempts if destination was not reached
        return 

    def find_smartest_step(self, position, destination, path_tmp):
            """Calculate step to follow random path from current position to any location. If origin equals destination, return None"""

            # No new position is required when destination is already reached
            if position == destination:
                return "reached"
            
            # Cannot go down from the lowest layer
            if position[2] == 0:
                step_in_direction = random.choices([0, 1, 2], weights=[2, 2, 1])[0]
                if step_in_direction == 2:
                    direction = 1
                else:
                    direction = random.choice([-1, 1])

            # If in middle of grid, all directions are equally likely
            else:
                step_in_direction = random.choice([0, 1, 2])
                direction = random.choice([-1, 1])

            new_position = list(position)

            # Make single step in random direction
            new_position[step_in_direction] += direction
        
            new_position = tuple(new_position)

            # Check if step is legal
            if new_position in path_tmp or (new_position in self.grid.gate_coordinates and new_position != destination):
                return

            return new_position

