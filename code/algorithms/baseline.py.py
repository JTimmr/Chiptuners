"""
Defines/ contains the algorithm for random (uniformly distributed) movements as used in our base case.
"""

def base_movement(origin, destination, grid, path, netlist):
    """Description bla bla bla"""

    # Store path so plot can be made
    x = []
    y = []
    z = []

    # Until destination is reached
    while True:
        x.append(origin[0])
        y.append(origin[1])
        z.append(origin[2])

        path.append(origin)

        # Find smartest move from current origin to destination
        new_origin = find_smartest_step(origin, destination)

        # If destination is not reached, make step
        if new_origin:

            # If the coordinate is not in the gate add wire segment and check for intersections
            if new_origin not in grid.gate_coordinates:

                # Check if current segment makes an interection
                if [segment for segment in grid.wire_segments if new_origin in segment]:
                    print(f"Intersection at: {new_origin}")
                    grid.intersections += 1

            grid.wire_segments[(origin, new_origin)] = netlist
                
            origin = new_origin

        # Return path if destination is reached
        else:
            return x, y, z


def find_smartest_step(position, destination):
        """Calculate step to follow shortest path from current position to any location. If position equals destination, return None"""

        # No new position is required when destination is already reached
        if position == destination:
            return

        # Calculate total movement before destination is reached
        direction = (destination[0] - position[0], destination[1] - position[1], destination[2] - position[2])

        # First move in the y direction
        if direction[1] != 0:
            step_in_direction = 1
        else:
            step_in_direction = 0

        new_position = list(position)

        # Make single step in right direction
        new_position[step_in_direction] += direction[step_in_direction] // abs(direction[step_in_direction])
    
        new_position = tuple(new_position)

        return new_position
