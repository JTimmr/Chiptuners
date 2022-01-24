from copy import deepcopy
import code.algorithms.sorting as sorting
import random
import pylab
import math
import matplotlib.pyplot as plt

"""
caption
"""

class BridgeWalk:
    def __init__(self, grid, render, print_connections):
        self.grid = grid
        self.render = render
        self.print_connections = print_connections

        if render:
            self.ax = plt.axes(projection='3d')

    def run(self):
        """Runs the algorithm until a solution is found"""
        
        if self.render:
            self.ax.set_title("3D Visual Chips&Curcuits")
            
            # set labels
            self.ax.set_xlabel('X axis')
            self.ax.set_ylabel('Y axis')
            self.ax.set_zlabel('Layer')

        # Until a solution is found, reset everything and try again
        while not self.make_connections():
            pylab.clf()
            self.grid.wire_segments = {}
            self.grid.intersections = 0
        
        
    def make_connections(self):
        """Connects two points on the grid, and plots the result"""

        max_x = 0
        max_y = 0

        # Run over netlists
        for netlist in sorting.sort_middle_first(self.grid.netlists):
            current_attempt = 0

            # Retrieve starting and ending point
            start = netlist.start
            end = netlist.end

            for key, value in self.grid.gates.items():
                if netlist.start == value.coordinates:
                    start_gate = key
                if netlist.end == value.coordinates:
                    end_gate = key

            # Search for path until a valid path is found
            while isinstance((path_data := self.find_path(start, end, netlist, current_attempt)), int):
                current_attempt += path_data

                # Give up if it takes too long
                if current_attempt > 50000:
                    self.grid.tot_attempts += current_attempt
                    if self.print_connections:
                        print(f"break, total attempts {self.grid.tot_attempts}")
                    return False

            # If a path is found, update number of attempts and retrieve coordinates
            self.grid.tot_attempts += current_attempt
            x, y, z = path_data[:3]
            netlist.path = [x, y, z]

            if self.render:
                # Find maximum x and y values
                if max(x) > max_x:
                    max_x = max(x)
                if max(y) > max_y:
                    max_y = max(y)

                # 3D plot netlists and gates
                self.ax.plot(x, y, z, label = f"chip {start_gate} to {end_gate}")
                self.ax.scatter3D(start[0], start[1], start[2], c = "black")
                self.ax.scatter3D(end[0], end[1], end[2], c = "black")
                self.ax.legend(title = "Netlist", prop={'size': 7}, bbox_to_anchor=(1.15, 1),loc='upper left')

        if self.render:

            # set axis values
            self.ax.set_xlim(0, max_x)
            self.ax.set_ylim(0, max_y)
            self.ax.set_zlim(0, 7)

            plt.show()
        return True

    def find_path(self, origin, destination, netlist, current_attempt):

        # Store path so plot can be made
        x = []
        y = []
        z = []

        # Temporary values until path is confirmed
        origin_tmp = deepcopy(origin)
        wire_segments_tmp = {}
        intersections_tmp = 0
        path_tmp = []
        new_attempts = 0

        current_length = 0

        x.append(origin_tmp[0])
        y.append(origin_tmp[1])
        z.append(origin_tmp[2])

        path_tmp.append(origin_tmp)

        

        return x,y,z,path

    def find_smartest_step(self, origin, position, destination, path_tmp):
            """Calculate step to follow random path from current position to any location. If origin equals destination, return None"""

            # No new position is required when destination is already reached
            if position == destination:
                return "reached"

            direction = (destination[0] - position[0], destination[1] - position[1], destination[2] - position[2])

            step_in_dimension = random.choices([0, 1, 2], weights=[(abs(i) + 1) for i in direction])[0]
            if step_in_dimension == 2 and position[2] == 0:
                step_in_direction = 1
            else:
                weights = [1, 1]
                prefered = 0

                if direction[step_in_dimension] < 0:
                    prefered = 1

                weights[prefered] = abs(direction[step_in_dimension]) + 1
                step_in_direction = random.choices([1, -1], weights=weights)[0]

            new_position = list(position)

            # Make single step in random direction
            new_position[step_in_dimension] += step_in_direction
        
            new_position = tuple(new_position)

            # Check if step is legal
            if new_position in path_tmp or (new_position in self.grid.gate_coordinates and new_position != destination):
                return

            return new_position
