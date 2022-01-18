from code.algorithms.basic import base_movement

class Netlist:
    def __init__(self, start, end, grid) -> None:
        self.start = start
        self.end = end
        self.grid = grid
        self.path = []
    
    def find_path(self, position, destination):
        """Find the shortest path between two coordinates on a grid"""

        x, y, z = base_movement(position, destination, self.grid, self.path, self)

        return x, y, z
