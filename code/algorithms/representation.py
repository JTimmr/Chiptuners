import pylab
from copy import deepcopy
"""
Defines/ contains the algorithm for random (uniformly distributed) movements as used in our base case.
"""

class Representation:
    def __init__(self, grid):
        self.grid = grid

    def make_connections(self):
        """Connects two points on the grid, and plots the result"""

        # Sorts the netlist by minimal path length
        for netlist in self.grid.netlists:

            # Retrieve starting and ending point
            start = deepcopy(self.grid.netlists[netlist].start)
            end = self.grid.netlists[netlist].end

            # Find the shortest path
            x, y, z, attempts = self.base_movement(start, end, netlist)

            self.grid.tot_attempts += attempts

            # Add path to plot
            pylab.plot(x, y, alpha = 0.5)
            pylab.locator_params(axis="both", integer=True)
            pylab.annotate(text = str(x[0])+ "," +str(y[0]), fontsize= 7, xy= (x[0], y[0]), xytext = (x[0] + 0.1, y[0] + 0.2))
            pylab.annotate(text = str(x[-1])+ "," +str(y[-1]), fontsize= 7, xy= (x[-1], y[-1]), xytext = (x[-1] + 0.1, y[-1] + 0.2))
            pylab.grid(alpha=0.2)
            pylab.xlabel('x-coordinates')
            pylab.ylabel('y-coordinates')
            pylab.legend(self.grid.netlists, prop={'size': 7}, loc = "upper left", title = "netlist", ncol = 6, bbox_to_anchor=(0.0, -0.22))
            
        # Save plot
        pylab.savefig("output/visual.png", dpi=100, bbox_inches="tight")

    def base_movement(self, origin, destination, netlist):
        """Description bla bla bla"""

        # Store path so plot can be made
        x = []
        y = []
        z = []
        path = []

        # Until destination is reached
        while True:
            x.append(origin[0])
            y.append(origin[1])
            z.append(origin[2])

            path.append(origin)

            # Find smartest move from current origin to destination
            new_origin = self.find_smartest_step(origin, destination)

            # If destination is not reached, make step
            if new_origin:

                # If the coordinate is not in the gate add wire segment and check for intersections
                if new_origin not in self.grid.gate_coordinates:

                    # Check if current segment makes an interection
                    if [segment for segment in self.grid.wire_segments if new_origin in segment]:
                        print(f"Intersection at: {new_origin}")
                        self.grid.intersections += 1

                self.grid.wire_segments[(origin, new_origin)] = netlist
                    
                origin = new_origin

            # Return path if destination is reached
            else:
                return x, y, z, 1


    def find_smartest_step(self, position, destination):
            """Calculate step to follow shortest path from current position to any location. If position equals destination, return None"""

            # No new position is required when destination is already reached
            if position == destination:
                return

            # Calculate total movement before destination is reached
            direction = (destination[0] - position[0], destination[1] - position[1], destination[2] - position[2])

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
