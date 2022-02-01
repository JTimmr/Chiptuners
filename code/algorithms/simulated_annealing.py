import random
import math
from copy import deepcopy

import numpy
import csv 
import matplotlib.pyplot as plt
import code.algorithms.A_star as A_star
import code.algorithms.sorting as sorting

def linear_cooling(temprature, cooling_speed = 20, t_lower = 1):
    """
    Linear decreasing temprature
    """
    temprature -= cooling_speed

    if temprature <= t_lower:
        temprature = t_lower

    return temprature


def log_cooling(temprature, iteration):
    """
    Logarithmic decrease as described by Aarts and Korst in 1989
    """
    log_factor = 1 + numpy.log(1 + iteration)
    temprature = temprature / log_factor

    return temprature
   

def geomtric_cooling(temprature, iteration, beta = 0.9):
    """
    Geomtric cooling schedule
    """
    new_temprature = pow(beta, iteration) * temprature

    return new_temprature


def LundyMees_cooling(temprature, beta = 0.9):
    """
    As proposed by Lundy And Mees
    """
    temprature = temprature / (1 + beta * temprature)

    return temprature


def VCF_cooling(temprature, iteration, starting_temprature, t_lower = 1):
    """
    Cooling schedule following a VCF model
    """
    beta = (starting_temprature - t_lower)/(iteration * starting_temprature * t_lower)
    temprature = temprature / (1 + beta * temprature)

    return temprature


def exponential_cooling(temprature, alpha = 0.98):
    """
    Cooling schedule based on exponential decrease
    """
    if alpha > 1 or alpha < 0:
        raise Exception("Please enter values for alpha between 0-1")

    temprature = temprature * alpha

    return temprature
 


class SimulatedAnnealing:
    def __init__(self, grid, limit, update_csv_paths, make_csv_improvements, make_iterative_plot, name, n, temperature, sorting_method):
        self.grid = grid
        self.limit = limit
        self.iterations = 0
        self.update_csv_paths = update_csv_paths
        self.make_csv_improvements = make_csv_improvements

        self.make_iterative_plot = make_iterative_plot

        self.iterationlist = []
        self.costs = []
        self.name = name
        self.n = n
        self.lowest_costs = deepcopy(self.grid.cost)
        self.sorting = sorting_method
        
        # Starting temperature and current temperature
        self.Starting_T = temperature
        self.Current_T = temperature

    def run_per_paths(self, netlist):
        # Retrieve starting and ending point
        start = netlist.start
        end = netlist.end
        a = A_star.A_Star_Solver(self.grid, netlist, start, end)
        a.Solve()

        x, y, z = [], [], []
        for coordinate in range(len(a.path)):
            x.append(a.path[coordinate][0])
            y.append(a.path[coordinate][1])
            z.append(a.path[coordinate][2])
        path = [x, y, z]

        return path

    def update_temperature(self):
        """Updates the current temperature."""
        
        # Check that ensures the temperature only updates when the iteration number has increased
        if self.iterationlist and self.Current_T > 0:
            if self.iterationlist[-1] != self.iterations:
                self.Current_T = geomtric_cooling(self.Current_T, self.iterations ,beta = 0.8)
                return self.Current_T

    def run(self):
        """Keeps the simulated annealing algorithm running until all iteration limit reached."""

        print("Searching for improvements...")

        # While iteration limit not reached search for improvements with specific sort function
        while self.iterations < self.limit:

            # print(f"iteration: {self.iterations} and Temprature: {self.Current_T}")


            netlists = self.sorting[0](self.grid.netlists, descending=self.sorting[1])

            for netlist in netlists:
                self.improve_connection(netlist)

                self.iterationlist.append(self.iterations)
                self.iterations += 1

                while len(self.costs) < len(self.iterationlist):
                    self.costs.append(self.lowest_costs)

        self.grid.compute_costs()
        print(f"Reached max number of iterations. Costs are {self.grid.cost}")

        # Write to csv
        self.grid.to_csv(self.grid.cost)

        if self.make_csv_improvements:
            self.to_csv()
        
        # If user wants to see algorithm plotted, plot
        if self.make_iterative_plot:
            self.plot()

        return self.grid.cost

    def improve_connection(self, netlist):
        """Takes a netlist as an input, and tries to find a shorter path between its two gates.
            While sometimes accepting worse solutions, to eventually find a better one."""

        origin = netlist.start
        destination = netlist.end

        # Make copies so original values aren't lost
        best_path = deepcopy(netlist.path)
        self.grid.compute_costs()
        best_costs = deepcopy(self.grid.cost)

        for attempt in range(50):
            # If path is found, calculate new costs
            new_path = self.find_path(origin, destination, netlist)

            # new_path = self.run_per_paths(netlist)
            if new_path:
                old_grid = deepcopy(self.grid)
                old_path = deepcopy(netlist.path)

                netlist.path = new_path
                self.grid.compute_costs()

# # --------------------------------------- update all other paths via A* --------------------------------------- #
#                 deepcopy_netlists = deepcopy(self.grid.netlists)
#                 deepcopy_netlists.pop(netlist.key)
#                 other_netlists = deepcopy_netlists

#                 for netlist in sorting.sort_exp_intersections(other_netlists, descending=False):

#                     # Retrieve starting and ending point
#                     start = netlist.start
#                     end = netlist.end
#                     a = A_star.A_Star_Solver(self.grid, netlist, start, end)
#                     a.Solve()
#                     x, y, z = [], [], []
#                     for coordinate in range(len(a.path)):
#                         x.append(a.path[coordinate][0])
#                         y.append(a.path[coordinate][1])
#                         z.append(a.path[coordinate][2])
#                     path = [x, y, z]
#                     netlist.path = path
#                 self.grid.update()
# # --------------------------------------- update all other paths via A* --------------------------------------- #

                delta = self.grid.cost - best_costs
                
                if self.grid.cost >= best_costs:
                    if self.Current_T == 0:
                        probability = 0
                    else:
                        probability = math.exp(-delta/self.Current_T)
                        # print(f"probability = {probability}")
                else:
                    # print("not worse")
                    probability = 1
                rand = random.random() 

                if probability > rand:
                    self.lowest_costs = self.grid.cost
                    print(f"Alternate path found: new costs are {self.grid.cost}")
                    best_path = deepcopy(new_path)
                    best_costs = deepcopy(self.grid.cost)
                    self.update_temperature()

                    if self.update_csv_paths:
                        self.grid.to_csv(self.grid.cost)
                    return
                else:
                    netlist.path = old_path

                return

    def find_path(self, origin, destination, netlist):
        """Attempts to find a path between two coordinates in the grid."""

        # Store path so plot can be made
        x = []
        y = []
        z = []

        #  Set limit for pathlength
        # max_pathlength = netlist.minimal_length * 2 + 10
        max_pathlength = netlist.current_length + 10

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

                segment = self.grid.make_segment(new_origin, origin_tmp)

                # Check if segment already in use, try again otherwise
                if segment in self.grid.wire_segments or segment in wire_segments_tmp:
                    return

                # Add segment to dictionary if it was new
                wire_segments_tmp[segment] = netlist

                # If the coordinate does not host a gate
                if new_origin not in self.grid.gate_coordinates:

                    # Check if current segment makes an interection
                    if new_origin in self.grid.coordinates:
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
        with open(f"output/results_annealing/annealing_netlist_{self.grid.netlist}{self.name}{self.n}_length(a).csv", "w", newline="") as csvfile:
            fieldnames = ["iteration", "cost"]

            # Set up wiriter and write the header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(len(self.iterationlist)):
                    writer.writerow({
                    "iteration": i + 1, "cost": self.costs[i]
                })
    
    def plot(self):
        """Plots simulated annealing with iterations on x-axis and costs on y-axis."""
        
        plt.figure()
        plt.plot(self.iterationlist, self.costs, label = f"start temp: {self.Starting_T} \xb0C")
        plt.legend()
        plt.xlabel("Iterations")
        plt.ylabel("Costs")
        plt.savefig(f"output/figs/annealing_N{self.grid.netlist}_T{self.Starting_T}_I{self.limit}_C{self.lowest_costs}.png")