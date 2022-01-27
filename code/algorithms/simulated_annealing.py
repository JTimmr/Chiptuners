import random
import math
from copy import deepcopy

import numpy
import code.algorithms.sorting as sort
import csv 


class SimulatedAnnealing:
    def __init__(self, grid, limit, update_csv_paths, make_csv_improvements, name, n, temperature):
        self.grid = grid
        self.limit = limit
        self.iterations = 0
        self.attempts_without_improvement = 0
        self.update_csv_paths = update_csv_paths
        self.make_csv_improvements = make_csv_improvements
        self.iterationlist = []
        self.costs = []
        self.name = name
        self.n = n
        self.lowest_costs = None
        
        # Starting temperature and current temperature
        self.Starting_T = temperature
        self.Current_T = temperature

    def update_temperature(self):

    # Check that ensures the temperature only updates when the iteration number has increased
       if self.iterationlist and self.Current_T > 1:
            if self.iterationlist[-1] != self.iterations:

                # Temperature decreases linearly with every iteration
                self.Current_T -= 20
                if self.Current_T <= 0:
                    self.Current_T = 1
                return self.Current_T

                # Logarithmic decrease as described by Aarts and Korst in 1989
                # log_factor = 1 + numpy.log(1 + self.iterations)
                # self.Current_T = self.Current_T / log_factor
                # return self.Current_T

                #Exponential
                # alpha = 0.999
                # self.Current_T = self.Current_T * alpha
                # return self.Current_T

    def run(self):
        print("Searching for improvements...")

        while self.iterations < self.limit:

            netlists = sort.sort_length(self.grid.netlists, descending=False)

            for netlist in netlists:

                self.improve_connection(netlist)

            self.iterationlist.append(self.iterations)
            self.iterations += 1

            self.update_temperature()

            while len(self.costs) < len(self.iterationlist):
                self.costs.append(self.lowest_costs)

        self.grid.compute_costs()
        print(f"Reached max number of iterations. Costs are {self.grid.cost}")

        self.grid.to_csv(self.grid.cost)

        if self.make_csv_improvements:
            self.to_csv()

        return self.grid.cost


    def improve_connection(self, netlist):

        origin = netlist.start
        destination = netlist.end

        best_path = deepcopy(netlist.path)
        self.grid.compute_costs()
        best_costs = deepcopy(self.grid.cost)

        new_path = self.find_path(origin, destination, netlist)
        if new_path:
            old_path = deepcopy(netlist.path)
            netlist.path = new_path
            self.grid.compute_costs()

            # delta = best_costs - self.grid.cost

            # if delta < 0:
            #     probability = math.exp(delta/self.Current_T)
            # else:
            #     probability = 1
            # rand = random.random() 

            delta = self.grid.cost - best_costs
            
            if self.grid.cost > best_costs:
                if self.Current_T == 0:
                    probability = 0
                else:
                    probability = math.exp(-delta/self.Current_T)
            else:
                probability = 1
            rand = random.random() 

            


            if rand < probability:
                self.lowest_costs = self.grid.cost
                print(f"Alternatice path found: new costs are {self.grid.cost}")
                best_path = deepcopy(new_path)
                best_costs = deepcopy(self.grid.cost)

                if self.update_csv_paths:
                    self.grid.to_csv(self.grid.cost)

            else:
                netlist.path = old_path


    def find_path(self, origin, destination, netlist):
        """Attempts to find a path between two coordinates in the grid."""

        # Store path so plot can be made
        x = []
        y = []
        z = []

        #  Set limit for pathlength
        max_pathlength = netlist.minimal_length * 2 + 10

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

    def to_csv(self):
        with open(f"output/results_annealing/hill_netlist_{self.grid.netlist}{self.name}{self.n}_length(a).csv", "w", newline="") as csvfile:
            fieldnames = ["iteration", "cost"]

            # Set up wiriter and write the header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(len(self.iterationlist)):
                    writer.writerow({
                    "iteration": i + 1, "cost": self.costs[i]
                })