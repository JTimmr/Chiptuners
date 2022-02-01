class Gate:
    def __init__(self, uid, x, y, z) -> None:
        self.id = uid
        self.coordinates = (x, y, z)

    def __str__(self) -> str:
        return (f"gate {self.id} with coordinates {self.coordinates}")
