from copy import deepcopy
import code.algorithms.sorting as sorting
import random
import math


class level_walk:

    def __init__(self, grid) -> None:
        self.grid = grid

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
                path = self.find_path(self, start, end, netlist)

                # Check if a valid path has been found if so add to netlist
                if path:
                    netlist.path = path
                    return True

            return False

    def find_path(self, start, end, netlist) -> list[int, int, int]:

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
            new_position = self.find_smartest_step(self, position, end)

            # Check for intersections
            if new_position not in self.grid.gate_coordinates:
                    if [segment for segment in self.grid.wire_segments if new_position in segment]:
                        intersections_tmp += 1

            # Save the wire segment
            segment = (position, new_position)
            wire_segments_tmp[segment] = netlist

            # Update the position
            position = new_position

            # Make everything else up to date
            self.grid.wire_segments.update(wire_segments_tmp)
            self.grid.intersections += intersections_tmp

        return [x,y,z]

    def find_smartest_step(self, position, end) -> list[int, int, int]:

        # Calculate total movement before destination is reached
        direction = (destination[0] - position[0], destination[1] - position[1])

        
        return [x,y,z]
        
    