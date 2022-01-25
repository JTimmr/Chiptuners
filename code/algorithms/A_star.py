from queue import PriorityQueue
import code.algorithms.sorting as sorting
import math
from copy import deepcopy

class A_Star:
    def __init__(self, grid):
        self.grid = grid

    def run(self):
        total = len(self.grid.netlists)
        completed = 0
        print(f"{completed}/{total} done")

        for netlist in sorting.sort_length(self.grid.netlists, descending=False):
            
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
            print(f"{completed}/{total} done")


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
    def __init__(self, grid, netlist, visitedQueue, value, parent, goal, start = 0):
        super(State_Path, self).__init__(value, parent, start, goal)
        self.dist = self.GetDistance()
        self.goal = goal
        self.grid = grid
        self.netlist = netlist
        self.intersections = 0
        self.visitedQueue = visitedQueue
 
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
                        child = State_Path(self.grid, self.netlist, self.visitedQueue, tuple(val), self, self.goal)
                        if child.value not in self.visitedQueue:    
                            self.children.append(child)
 

class A_Star_Solver:
    def __init__(self, grid, netlist, start, goal):
        self.path = []
        self.visitedQueue = set()
        self.priorityQueue = PriorityQueue(maxsize=0)
        self.start = start
        self.goal = goal
        self.grid = grid
        self.netlist = netlist
 
    def Solve(self):
        startState = State_Path(self.grid, self.netlist, self.visitedQueue, self.start, 0, self.goal, self.start)
        count = 0

        self.priorityQueue.put((0,count, startState, self.goal))

        while(not self.path and self.priorityQueue.qsize()):
            closesetChild = self.priorityQueue.get()[2]
            closesetChild.CreateChildren()
            self.visitedQueue.add(closesetChild.value)

            for child in closesetChild.children:
  
                # Chance of success is higher when gates aren't blocked unnessicarily
                illegal = False
                for gate in self.grid.gate_coordinates:
                    if child.value[:2] == gate[:2] and gate != self.goal and gate != self.start and child.value[2] <= 1:
                        illegal = True

                if illegal:
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
                        return self.path

                    self.priorityQueue.put(((child.dist), count, child))