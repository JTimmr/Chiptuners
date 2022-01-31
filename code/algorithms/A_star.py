import math
from copy import deepcopy

class A_Star:
    def __init__(self, grid, sorting_method):
        self.grid = grid
        self.sorting = sorting_method


    def run(self):
        total = len(self.grid.netlists)
        completed = 0
        for netlist in self.sorting[0](self.grid.netlists, descending=self.sorting[1]):
            
            # Retrieve starting and ending point
            start = netlist.start
            end = netlist.end
            a = A_Star_Solver(self.grid, netlist, start, end)
            a.Solve()
            x, y, z = [], [], []
            for coordinate in range(len(a.path)):
                x.append(a.path[coordinate][0])
                y.append(a.path[coordinate][1])
                z.append(a.path[coordinate][2])
            path = [x, y, z]
            netlist.path = path
            completed += 1
            # print(f"Finished {netlist.start} to {netlist.end}, {completed}/{total}")

        self.grid.update()

class PriorityQueue:
    def __init__(self):
        self.queue = {}
        self.in_queue = set()

    def size(self):
        return len(self.queue)

    def put(self, priority, costs, item):
        self.in_queue.add(item.value)
        try:
            self.queue[priority + costs].append(item)
        except KeyError:
            self.queue[priority + costs] = [item]

    def get(self):

        lowest_costs = 999999
        for items in self.queue:
            if items < lowest_costs:
                lowest_costs = items
        best_choice = self.queue[lowest_costs][0]

        del self.queue[lowest_costs][0]

        if len(self.queue[lowest_costs]) == 0:
            del self.queue[lowest_costs]
        self.in_queue.remove(best_choice.value)
        return best_choice

class State(object):
    def __init__(self, value, parent, start = 0, goal = 0):
        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0
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
    def __init__(self, grid, netlist, visitedQueue, costs, value, parent, goal, start = 0):
        super(State_Path, self).__init__(value, parent, start, goal)
        self.dist = self.GetDistance()
        self.goal = goal
        self.grid = grid
        self.netlist = netlist
        self.visitedQueue = visitedQueue
        self.costs = costs
 
    def GetDistance(self):
            if self.value == self.goal:
                return 0
            return abs(self.goal[0] - self.value[0]) + abs(self.goal[1] - self.value[1]) + abs(self.goal[2] - self.value[2])
 
    def CreateChildren(self):
            if not self.children:
                for i in range(3):
                    if self.value[i] == 0:
                        directions = [1]
                    elif self.value[i] == self.grid.size[i]:
                        directions = [-1]
                    else:
                        directions = [-1, 1]

                    for j in directions:
                        val = list(self.value)
                        val[i] += j
                        val = tuple(val)
                        if val not in self.visitedQueue: 

                            costs_tmp = self.costs + 1
                            if val in self.grid.coordinates and val not in self.grid.gate_coordinates:

                                costs_tmp += 300
                            child = State_Path(self.grid, self.netlist, self.visitedQueue, costs_tmp, val, self, self.goal)
                            self.children.append(child)


class A_Star_Solver:
    def __init__(self, grid, netlist, start, goal):
        self.path = []
        self.visitedQueue = set()
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
        self.grid = grid
        self.netlist = netlist

    def Solve(self):
        startState = State_Path(self.grid, self.netlist, self.visitedQueue, 0, self.start, 0, self.goal, self.start)
        count = 0
        self.priorityQueue.put(0, 0, startState)

        while(not self.path and self.priorityQueue.size()):
            closesetChild = self.priorityQueue.get()

            closesetChild.CreateChildren()
            self.visitedQueue.add(closesetChild.value)
            for child in closesetChild.children:

                # Chance of success is higher when gates aren't blocked unnessicarily
                illegal = False
                for gate in self.grid.gate_coordinates:
                    if child.value[:2] == gate[:2] and gate != self.goal and gate != self.start and child.value[2] <= 2:
                        illegal = True
                        continue

                if illegal or child.value in self.priorityQueue.in_queue:
                    continue

                # Save step as segment, and ensure two identical segments are never stored in reverse order (a, b VS b, a)
                if ((math.sqrt(sum(i**2 for i in child.path[-2]))) >= (math.sqrt(sum(i**2 for i in child.value)))):
                    segment = (child.value, child.path[-2])
                else:
                    segment = (child.path[-2], child.value)

                if segment not in self.grid.wire_segments:
                    count += 1

                    if child.dist == 0:
                        self.path = child.path
                        tmp_segments = {}
                        for coordinate in range(len(self.path) - 1):
                            if ((math.sqrt(sum(i**2 for i in self.path[coordinate]))) >= (math.sqrt(sum(i**2 for i in self.path[coordinate + 1])))):
                                segment = (self.path[coordinate + 1], self.path[coordinate])
                            else:
                                segment = (self.path[coordinate], self.path[coordinate + 1])
                            tmp_segments[segment] = self.netlist
                        self.grid.wire_segments.update(tmp_segments)
                        
                        for segment in tmp_segments:
                            self.grid.coordinates.add(segment[0])
                            self.grid.coordinates.add(segment[1])
                        self.netlist.intersections = child.costs // 300
                        print(self.netlist.intersections, self.netlist.start)
                        return self.path
                    
                    priority = child.dist
                    self.priorityQueue.put(priority, child.costs, child)
