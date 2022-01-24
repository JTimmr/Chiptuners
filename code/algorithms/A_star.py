from queue import PriorityQueue
import code.algorithms.sorting as sorting
import math

class A_Star:
    def __init__(self, grid):
        self.grid = grid
    
    def run(self):
        for netlist in sorting.sort_length(self.grid.netlists, descending=True):

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
            netlist.path = [x, y, z]


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
    def __init__(self, grid, netlist, value, parent, goal, start = 0):
        super(State_Path, self).__init__(value, parent, start, goal)
        self.dist = self.GetDistance()
        self.goal = goal
        self.grid = grid
        self.netlist = netlist
 
    def GetDistance(self):
            if self.value == self.goal:
                return 0
            return abs(self.goal[0] - self.value[0]) + abs(self.goal[1] - self.value[1]) + abs(self.goal[2] - self.value[2])
 
    def CreateChildren(self):
            if not self.children:
                for i in range(3):
                    for j in [-1, 1]:
                        val = list(self.value)
                        val[i] += j
                        child = State_Path(self.grid, self.netlist, tuple(val), self, self.goal)
                        self.children.append(child)
 

class A_Star_Solver:
    def __init__(self, grid, netlist, start, goal):
        self.path = []
        self.vistedQueue =[]
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
        self.grid = grid
        self.netlist = netlist
        self.tmp_segments = {}
 
    def Solve(self):
        startState = State_Path(self.grid, self.netlist, self.start, 0, self.goal, self.start)
        count = 0
        self.priorityQueue.put((0,count, startState, self.goal))

        while(not self.path and self.priorityQueue.qsize()):
            closesetChild = self.priorityQueue.get()[2]
            closesetChild.CreateChildren()
            self.vistedQueue.append(closesetChild.value)

            for child in closesetChild.children:
                
                # Save step as segment, and ensure two identical segments are never stored in reverse order (a, b VS b, a)
                if ((math.sqrt(sum(i**2 for i in child.path[-2]))) >= (math.sqrt(sum(i**2 for i in child.value)))):
                    segment = (child.value, child.path[-2])
                else:
                    segment = (child.path[-2], child.value)

                if segment not in self.grid.wire_segments:
                    self.tmp_segments[self.netlist] = segment
                    count += 1
                    if child.dist == 0:
                        self.path = child.path
                        self.grid.wire_segments.update(self.tmp_segments)
                        return self.path

                    self.priorityQueue.put((child.dist, count, child))