import random
from copy import deepcopy
import csv
import matplotlib.pyplot as plt


class Hillclimber:
    def __init__(self, grid, iterations, update_csv_paths, make_csv_improvements, make_iterative_plot, n, m, sorting_method):
        self.grid = grid
        self.iterations = iterations
        self.iteration = 0
        self.attempts_without_improvement = 0
        self.update_csv_paths = update_csv_paths
        self.make_iterative_plot = make_iterative_plot
        self.make_csv_improvements = make_csv_improvements
        self.costs = []
        self.m = f"_{m}"
        self.n = f"_{n}"
        self.lowest_costs = None
        self.sorting = sorting_method

    def run(self):
        """Keeps the Hillclimber algorithm running."""

        print("Searching for improvements...")
        self.grid.compute_costs
        self.lowest_costs = self.grid.cost

        # Run a number of iterations
        while self.iteration < self.iterations:
            print(f"Iteration {self.iteration}")

            # Sort net in desired order
            nets = self.sorting[0](self.grid.nets, descending=self.sorting[1])

            for net in nets:

                # Try to make an improvement
                self.improve_connection(net)

                # Quit when no improvement is made after a large amount of attempts
                if self.attempts_without_improvement > 500:
                    continue

            self.iteration += 1

            while len(self.costs) < self.iteration:
                self.costs.append(self.lowest_costs)

        self.grid.compute_costs()
        print(f"Reached max number of iterations. Costs are {self.grid.cost}")
        self.grid.to_csv(self.grid.cost)

        if self.make_csv_improvements:
            self.to_csv()

        if self.make_iterative_plot:
            self.plot()

    def improve_connection(self, net):
        """Takes a net as an input, and tries to find a shorter path between its two gates."""

        origin = net.start
        destination = net.end

        # Make copies so original values aren't lost
        self.grid.compute_costs()
        best_costs = deepcopy(self.grid.cost)

        # Try a number of times before succes becomes unlikely
        for attempt in range(100):

            new_path = self.find_path(origin, destination, net)

            # If path is found, calculate new costs
            if new_path:
                old_path = deepcopy(net.path)
                net.path = new_path
                self.grid.compute_costs()

                # Allow change of path with no benefit once every 5 attempts
                if self.attempts_without_improvement % 5 == 0:

                    # Make change if costs are equal or lower
                    if self.grid.cost <= best_costs:
                        best_costs = self.grid.cost
                        self.attempts_without_improvement = 0

                        # Keep csv updated if update_csv is set to True in main function
                        if self.update_csv_paths:
                            self.grid.to_csv(self.grid.cost)

                    # Reset if new path is worse
                    else:
                        net.path = old_path
                        self.attempts_without_improvement += 1

                # Only allow changes to decrease the cost 4/5 attempts
                else:

                    # Make change if costs are lower
                    if self.grid.cost < best_costs:
                        self.lowest_costs = self.grid.cost
                        print(f"Improvement found: Reduced costs from {best_costs} to {self.grid.cost}")
                        best_costs = self.grid.cost
                        self.attempts_without_improvement = 0

                        # Keep csv updated if update_csv is set to True in main function
                        if self.update_csv_paths:
                            self.grid.to_csv(self.grid.cost)
                        return

                    # Reset if new path is denied
                    else:
                        net.path = old_path
                        self.attempts_without_improvement += 1

            # If no path was found at all, register as failed attempt
            else:
                self.attempts_without_improvement += 1

    def find_path(self, origin, destination, net):
        """
        Takes a starting and ending point, and tries to make a connection between them.
        Returns the path if succeeded, otherwise nothing.
        """

        # Store path so plot can be made
        x = []
        y = []
        z = []

        #  Set limit for pathlength
        max_pathlength = net.minimal_length * 2 + 10

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
                wire_segments_tmp[segment] = net

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
        """
        Calculates step to follow semi random path from current position
        to any location. If origin equals destination, return None.
        """

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
        path = "output/results_hillclimber/hill_netlist_"
        with open(f"{path}{self.grid.netlist}{self.n}{self.m}_intersections_ascending.csv", "w", newline="") as csvfile:
            fieldnames = ["iteration", "cost"]

            # Set up wiriter and write the header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(self.iterations):
                writer.writerow({
                    "iteration": i + 1, "cost": self.costs[i]
                })

    def plot(self):
        """Plots hillclimber with iterations on x-axis and costs on y-axis."""

        plt.figure()
        plt.plot([i + 1 for i in range(self.iterations)], self.costs)
        plt.xlabel("Iterations")
        plt.ylabel("Costs")
        plt.savefig(f"output/figs/hillclimber_{self.grid.netlist}_I_{self.iterations}_C_{self.lowest_costs}.png")
