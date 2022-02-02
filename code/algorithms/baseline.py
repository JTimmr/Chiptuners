from copy import deepcopy
import random


class Baseline:
    """
    Defines/contains the algorithm for random (uniformly distributed) movements
    as used in our base case.
    """

    def __init__(self, grid, sorting_method):
        self.grid = grid
        self.sorting = sorting_method

    def run(self):
        """Runs the algorithm until a solution is found"""

        print("Searching for semi random configuration...")

        # Until a solution is found, reset everything and try again
        while not self.make_connections():
            self.grid.wire_segments = {}
            self.grid.intersections = 0

    def make_connections(self):
        """Connects two points on the grid, and plots the result"""

        for net in self.sorting[0](self.grid.nets, descending=self.sorting[1]):
            current_attempt = 0

            # Retrieve starting and ending point
            start = net.start
            end = net.end

            # Search for path until a valid path is found
            while isinstance((path_data := self.find_path(start, end, net, current_attempt)), int):
                current_attempt += path_data

                # Give up if it takes too long
                if current_attempt > 50000:
                    return False

            # If a path is found, retrieve coordinates
            x, y, z = path_data[:3]
            net.path = [x, y, z]

        return True

    def find_path(self, origin, destination, net, current_attempt):
        """
        Takes a starting and ending point, and tries to make a connection between them.
        Returns the path if succeeded, otherwise nothing.
        """

        # Store path so plot can be made
        x = []
        y = []
        z = []
        max_pathlength = net.minimal_length * 2 + 6

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
            while not (new_origin := self.find_smartest_step(origin_tmp, destination,  path_tmp)):
                new_attempts += 1

                # Give up after 10 failed attempts to make a single step
                if new_attempts > 10:
                    return new_attempts

            # If destination is not reached, make step
            if new_origin != "reached":

                segment = self.grid.make_segment(new_origin, origin_tmp)

                # Check if segment already in use, try again otherwise
                if segment in self.grid.wire_segments or segment in wire_segments_tmp:
                    return new_attempts

                # Add segment to dictionary if it was new
                wire_segments_tmp[segment] = net

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
                for segment in wire_segments_tmp:
                    self.grid.coordinates.add(segment[0])
                    self.grid.coordinates.add(segment[1])
                self.grid.intersections += intersections_tmp
                path = path_tmp

                return x, y, z, path

        # Return number of failed attempts if destination was not reached
        return new_attempts + 1

    def find_smartest_step(self, position, destination, path_tmp):
        """
        Calculates step to follow semi random path from current position
        to any location. If origin equals destination, return None.
        """

        # No new position is required when destination is already reached
        if position == destination:
            return "reached"

        direction = (destination[0] - position[0],
                     destination[1] - position[1],
                     destination[2] - position[2])

        # Selects a dimension to move in by a weighted random choice
        step_in_dimension = random.choices([0, 1, 2], weights=[(abs(i) + 1) for i in direction])[0]

        # Cannot go down from lowest layer
        if step_in_dimension == 2 and position[2] == 0:
            step_in_direction = 1
        else:
            weights = [1, 1]
            prefered = 0

            if direction[step_in_dimension] < 0:
                prefered = 1

            # Select direction to make move in by weighted random choice
            weights[prefered] = abs(direction[step_in_dimension]) + 1
            step_in_direction = random.choices([1, -1], weights=weights)[0]

        new_position = list(position)

        # Make single step in random direction
        new_position[step_in_dimension] += step_in_direction

        new_position = tuple(new_position)

        # Check if step is legal
        if new_position in path_tmp or (
            new_position in self.grid.gate_coordinates and
                new_position != destination):
            return

        return new_position
