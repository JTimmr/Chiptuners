import random
import pylab

def find_smartest_step(position, destination):
    """Calculate step to follow shortest path from current position to any location. If position equals destination, return None"""

    # No new position is required when destination is already reached
    if position == destination:
        return

    # Calculate total movement before destination is reached
    direction = (destination[0] - position[0], destination[1] - position[1])

    # Choose random move, weighted with number of required steps
    step_in_direction = random.choices([0, 1], direction)[0]

    # Make single step in right direction
    position[step_in_direction] += direction[step_in_direction] // abs(direction[step_in_direction])

    return position


position = [0, 0]
destination = [10, 27]
x = []
y = []

while True:
    new_position = find_smartest_step(position, destination)
    if new_position:
        position = new_position
        x.append(position[0])
        y.append(position[1])
    else:
        break

pylab.title("Shortest path")
pylab.plot(x, y)
pylab.savefig("test.png")










