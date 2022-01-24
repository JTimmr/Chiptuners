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
