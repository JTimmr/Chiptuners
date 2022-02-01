class A_Star:
    def __init__(self, grid, sorting_method, pop, gate_space):
        self.grid = grid
        self.sorting = sorting_method
        self.pop = pop
        self.gate_space = gate_space

    def run(self):
        """
        Runs the A* algorithm to find solutions for the given netlist.
        Stores all paths in the netlist objects, and makes sure the grid object is up to date.
        """

        total = len(self.grid.nets)
        completed = 0

        # Sort the nets in the given order
        for net in self.sorting[0](self.grid.nets, descending=self.sorting[1]):

            # Retrieve starting and ending point
            start = net.start
            end = net.end

            # Make solver object and run algorithm
            solver = A_Star_Solver(self.grid, net, start, end, self.pop, self.gate_space)
            if not solver.Solve():
                return False

            # Extract path from solver
            x, y, z = [], [], []
            for coordinate in solver.path:
                x.append(coordinate[0])
                y.append(coordinate[1])
                z.append(coordinate[2])

            # Store path in net object
            path = [x, y, z]
            net.path = path
            completed += 1
            print(f"Finished {net.start} to {net.end}, {completed}/{total}")

        # Update grid
        self.grid.update()
        return True

class PriorityQueue:
    def __init__(self):
        self.queue = {}
        self.in_queue = set()

    def size(self):
        """Returns the size of the queue."""

        return len(self.queue)

    def put(self, priority, costs, item):
        """Puts an element in the queue."""

        self.in_queue.add(item.value)

        # Add element to correct list or create list
        try:
            self.queue[priority + costs].append(item)
        except KeyError:
            self.queue[priority + costs] = [item]

    def get(self, pop):
        """
        Returns item from queue with lowest sum of estimated remaining distance and current costs.
        Deletes item from list afterwards.
        """

        # Ensure there is always a lower cost to be found
        lowest_costs = 999999

        # Find list with lowest priority value in dictionary
        for items in self.queue:
            if items < lowest_costs:
                lowest_costs = items

        # Retrieve and delete item from list
        best_choice = self.queue[lowest_costs].pop(pop)

        # Delete dictionary item if list is empty
        if len(self.queue[lowest_costs]) == 0:
            del self.queue[lowest_costs]

        # Delete item from set and return item
        self.in_queue.remove(best_choice.value)
        return best_choice


class State(object):
    def __init__(self, value, parent, start=0, goal=0):
        self.children = []
        self.parent = parent
        self.value = value
        self.heuristic = 0
        if parent:
            self.start = parent.start
            self.goal = parent.goal
            self.path = parent.path[:]
            self.path.append(value)

        else:
            self.path = [value]
            self.start = start
            self.goal = goal


class State_Path(State):
    def __init__(self, grid, net, visitedQueue, costs, value, parent, goal, start=0):
        super(State_Path, self).__init__(value, parent, start, goal)
        self.heuristic = self.get_distance()
        self.goal = goal
        self.grid = grid
        self.net = net
        self.visitedQueue = visitedQueue
        self.costs = costs

    def get_distance(self):
        """Returns the estimated distance from current poit to goal."""

        if self.value == self.goal:
            return 0
        return abs(self.goal[0] - self.value[0]) + abs(self.goal[1] - self.value[1]) + abs(self.goal[2] - self.value[2])

    def create_children(self):
        """Find all possible steps from a starting point, and store them in list."""

        # If state has no children
        if not self.children:

            # Find all neighboring point which are still on the grid
            for i in range(3):
                if self.value[i] == 0:
                    directions = [1]
                elif self.value[i] == self.grid.size[i]:
                    directions = [-1]
                else:
                    directions = [-1, 1]

                # Make new tuple with coordinate
                for j in directions:
                    val = list(self.value)
                    val[i] += j
                    val = tuple(val)

                    # Check if coordinate is already visited
                    if val not in self.visitedQueue:

                        # Calculate new costs
                        costs_tmp = self.costs + 1

                        # Check if coordinate makes intersection
                        if val in self.grid.coordinates and val not in self.grid.gate_coordinates:
                            costs_tmp += 300

                        # Create child object
                        child = State_Path(self.grid, self.net, self.visitedQueue, costs_tmp, val, self, self.goal)
                        self.children.append(child)


class A_Star_Solver:
    def __init__(self, grid, net, start, goal, pop, gate_space):
        self.path = []
        self.visitedQueue = set()
        self.queue = PriorityQueue()
        self.start = start
        self.goal = goal
        self.grid = grid
        self.net = net
        self.pop = pop
        self.gate_space = gate_space

    def Solve(self):
        """Finds and returns solution for current path."""

        # Make state object
        startState = State_Path(self.grid, self.net, self.visitedQueue, 0, self.start, 0, self.goal, self.start)
        count = 0

        # Put object in queue
        self.queue.put(0, 0, startState)

        # Untill queue is empty or path is found
        while(not self.path and self.queue.size()):

            # Get item from queue
            current_state = self.queue.get(self.pop)

            # Make children
            current_state.create_children()
            self.visitedQueue.add(current_state.value)
            for child in current_state.children:

                # Chance of success is higher when gates aren't blocked unnessicarily
                illegal = False
                for gate in self.grid.gate_coordinates:
                    if child.value[:2] == gate[:2] and gate != self.goal and gate != self.start\
                            and child.value[2] <= self.gate_space:
                        illegal = True
                        continue

                # If child blockes another gate or if child is already in queue, go to next child
                if illegal or child.value in self.queue.in_queue:
                    continue

                segment = self.grid.make_segment(child.value, child.path[-2])

                # If segment is not already in use
                if segment not in self.grid.wire_segments:
                    count += 1

                    # If path reached destination
                    if child.heuristic == 0:
                        self.path = child.path

                        # Ensure dictionary with wiresegments and set with all used coordinates are up to date
                        for coordinate in range(len(self.path) - 1):

                            segment = self.grid.make_segment(self.path[coordinate + 1], self.path[coordinate])

                            self.grid.wire_segments[segment] = self.net
                            self.grid.coordinates.add(segment[0])
                            self.grid.coordinates.add(segment[1])

                        # Calculate costs path, assuming no path has a length of >300.
                        self.net.intersections = child.costs // 300
                        return self.path

                    # Put child in queue
                    priority = child.heuristic
                    self.queue.put(priority, child.costs, child)

        return False
