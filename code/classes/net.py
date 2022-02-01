
class Net:
    def __init__(self, start, end, grid) -> None:
        self.start = start
        self.end = end
        self.minimal_length = abs(start[0] - end[0]) + abs(start[1] - end[1])
        self.current_length = None
        self.grid = grid
        self.path = []
        self.total_distance_middle = 0
        self.exp_intersections = 0
        self.key = ()
        self.intersection = 0

    def __str__(self) -> str:
        return ("\n\t\t")