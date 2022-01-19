from copy import deepcopy
import random
import pylab
import math
import operator

"""
Defines/ contains the algorithm for random (uniformly distributed) movements as used in our base case.
"""

class Baseline:
    def __init__(self, grid):
        self.grid = grid
        self.attempts = 0
        pylab.clf()

    def run(self):
        """Runs the algorithm until a solution is found"""

        # Until a solution is found, reset everything and try again
        while not self.make_connections():
            pylab.clf()
            self.grid.wire_segments = {}
            self.grid.intersections = 0
        
        
    def make_connections(self):
        """Connects two points on the grid, and plots the result"""

        # Run over netlists
        # for netlist in self.grid.netlists.values():
        for netlist in (sorted(self.grid.netlists.values(), key=operator.attrgetter('minimal_length'))):

            current_attempt = 0

            # Retrieve starting and ending point
            start = netlist.start
            end = netlist.end

            # Search for path until a valid path is found
            while isinstance((path_data := self.find_path(start, end, netlist, current_attempt)), int):
                current_attempt += path_data

                # Give up if it takes too long
                if current_attempt > 10000:
                    self.grid.tot_attempts += current_attempt
                    print(f"break, total attempts {self.grid.tot_attempts}")
                    return False

            # If a path is found, update number of attempts and retrieve coordinates
            self.attempts += current_attempt
            x, y, z = path_data[:3]

            # Add path to plot
            pylab.plot(x, y, alpha = 0.5)
            pylab.locator_params(axis="both", integer=True)
            pylab.annotate(text = str(x[0])+ "," +str(y[0]), fontsize= 7, xy= (x[0], y[0]), xytext = (x[0] + 0.1, y[0] + 0.1))
            pylab.annotate(text = str(x[-1])+ "," +str(y[-1]), fontsize= 7, xy= (x[-1], y[-1]), xytext = (x[-1] + 0.1, y[-1] + 0.1))
            pylab.grid(alpha=0.2)
            pylab.xlabel('x-coordinates')
            pylab.ylabel('y-coordinates')
            pylab.legend(self.grid.netlists, prop={'size': 7}, loc = "upper left", title = "netlist", ncol = 6, bbox_to_anchor=(0.0, -0.22))
            
        # Save plot
        pylab.savefig("output/visual.png", dpi=100, bbox_inches="tight")

        self.grid.tot_attempts = self.attempts
        return True

    def find_path(self, origin, destination, netlist, current_attempt):

        # Store path so plot can be made
        x = []
        y = []
        z = []
        max_pathlength = netlist.minimal_length * 2

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
                    return new_attempts

            # If destination is not reached, make step
            if new_origin != "reached":

                # Save step as segment, and ensure two identical segments are never stored in reverse order (a, b VS b, a)
                if ((math.sqrt(sum(i**2 for i in origin_tmp))) >= (math.sqrt(sum(i**2 for i in new_origin)))):
                    segment = (new_origin, origin_tmp)
                else:
                    segment = (origin_tmp, new_origin)

                # Check if segment already in use, try again otherwise
                if segment in self.grid.wire_segments or segment in wire_segments_tmp:
                    return new_attempts

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
                print(f"Path found between {netlist.start} and {netlist.end} of length {current_length}: {x, y, z}, attempt {current_attempt}")

                # Make everything up to date
                self.grid.wire_segments.update(wire_segments_tmp)
                self.grid.intersections += intersections_tmp
                path = path_tmp

                return x, y, z, path

        # Return number of failed attempts if destination was not reached
        return new_attempts + 1

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
