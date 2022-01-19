class Netlist:
    def __init__(self, start, end, grid) -> None:
        self.start = start
        self.end = end
        self.minimal_length = abs(start[0] - end[0]) + abs(start[1] - end[1])
        self.grid = grid
        self.path = []