from copy import deepcopy
import code.algorithms.sorting as sorting
import random
import math


class level_walk:

    def __init__(self, grid) -> None:
        self.grid = grid

    def run(self):
        """Runs the algorithm until a solution is found"""

        print("Searching for semi random configuration...")

        # Until a solution is found, reset everything and try again
        while not self.make_connections():
            self.grid.wire_segments = {}
            self.grid.intersections = 0

    def make_connections(self) -> bool:
        
        # Run over netlists
        for netlist in sorting.sort_length(self.grid.netlists, descending=True):

            # Retrieve starting and ending point
            start = netlist.start
            end = netlist.end

            current_attempt = 0

            # Find shortest path up to 1000 times
            while current_attempt <= 1000:
                current_attempt += 1
                path = self.find_path(start, end, netlist)

                # Check if a valid path has been found if so add to netlist
                if path:
                    netlist.path = path
                    return True

            return False

    def find_path(self, start, end, netlist):

        # Temporary values until path is confirmed
        position = deepcopy(start)
        wire_segments_tmp = {}
        intersections_tmp = 0
        path_tmp = []

        # Store path so plot can be made
        x = [position[0]]
        y = [position[1]]
        z = [position[2]]

        # If the algorithm is at its end destination then it returns the path
        while position != end:

            # Find where to move to
            new_position = self.find_smartest_step(position, end)

            # Check for intersections
            if new_position not in self.grid.gate_coordinates:
                    if [segment for segment in self.grid.wire_segments if new_position in segment]:
                        intersections_tmp += 1

            # Save the wire segment
            segment = (position, new_position)
            wire_segments_tmp[segment] = netlist

            # Update the position
            position = new_position

            x.append(new_position[0])
            y.append(new_position[1])
            z.append(new_position[2])

            # Make everything else up to date
            self.grid.wire_segments.update(wire_segments_tmp)
            self.grid.intersections += intersections_tmp

        return x,y,z

    def find_smartest_step(self, position, end) -> tuple():

        x = position[0]
        y = position[1]
        z = position[2]

        # Calculate total movement before destination is reached
        if end[0] > x:
            x += 1
        elif end[0] < x:
            x -= 1
        elif end[1] > y:
            y += 1
        elif end[1] < y:
            y -= 1

        return (x,y,z)
        
    