import random
import operator


def sort_length(nets, descending=False):
    """
    Sorts net object instances on their distance
    between start- and end coordinates.
    """
    return (sorted(nets.values(),
            key=operator.attrgetter('minimal_length'),
            reverse=descending))


def random_sort(nets, descending="None"):
    """Sorts net object instances in a random order."""

    # Load the net values and randomly shuffle its order
    value_list = list(nets.values())
    random.shuffle(value_list)

    return value_list


def sort_middle_first(nets, descending=False):
    """
    Sorts net object instances on their position in the grid;
    in the middle or on the outside.
    """

    # Find the size of the grid and compute its middle
    a_net = list(nets.values())[0]
    size = a_net.grid.size[:2]

    middle_x = round(size[0]/2)
    middle_y = round(size[1]/2)

    # Determine for every net its total summed distance to the middle of the grid
    # for key in nets:

    #     delta_middle_start = abs(middle_x - nets[key].start[0]) + abs(middle_y - nets[key].start[1])
    #     delta_middle_end = abs(middle_x - nets[key].end[0]) + abs(middle_y - nets[key].end[1])
    #     total_distance_middle = delta_middle_start + delta_middle_end

    #     nets[key].total_distance_middle = total_distance_middle

    # # Sort the nets
    # return (sorted(nets.values(),
    #         key=operator.attrgetter('total_distance_middle'),
    #         reverse=descending))

    for net in nets.values():

        delta_middle_start = abs(middle_x - net.start[0]) + abs(middle_y - net.start[1])
        delta_middle_end = abs(middle_x - net.end[0]) + abs(middle_y - net.end[1])
        total_distance_middle = delta_middle_start + delta_middle_end

        net.total_distance_middle = total_distance_middle

    # Sort the nets
    return (sorted(nets.values(),
            key=operator.attrgetter('total_distance_middle'),
            reverse=descending))


# ------------------------------------------------ OLD ------------------------------------------------ #

    # # Set easy to improve upper (champion) and lower (loser) bounds for x and y
    # x_champion = 0
    # y_champion = 0
    # x_loser = 9999
    # y_loser = 9999

    # # Search for the highest + lowest x and y values found in the gates
    # for value in nets.values():
    #     x_contestent = value.start[0]
    #     y_contestent = value.start[1]

    #     if x_contestent > x_champion:
    #         x_champion = x_contestent

    #     if y_contestent > y_champion:
    #         y_champion = y_contestent

    #     if x_contestent < x_loser:
    #         x_loser = x_contestent

    #     if y_contestent < y_loser:
    #         y_loser = y_contestent

    # # Determine the middle of the grid
    # middle_x = round((x_champion + x_loser)/2)
    # middle_y = round((x_champion + x_loser)/2)

    # # Determine for every net its total summed distance to the middle of the grid
    # for key in nets:

    #     delta_middle_start = abs(middle_x - value.start[0]) + abs(middle_y - value.start[1])
    #     delta_middle_end = abs(middle_x - value.end[0]) + abs(middle_y - value.end[1])
    #     total_distance_middle = delta_middle_start + delta_middle_end

    #     nets[key].total_distance_middle = total_distance_middle

    # # Sort the nets
    # return (sorted(nets.values(),
    #         key=operator.attrgetter('total_distance_middle'),
    #         reverse=descending))


def sort_gate(grid, descending=True):
    """
    Sorts net object instances on how many connections a gate has
    with other gates.
    """
    gate_occupation = {}
    net_neighbors = {}

    # Set gate occupation to zero for all gate coordinates
    for gate in grid.gates.values():
        gate_occupation[gate.coordinates] = 0

    # Count occurrences of gate coordinates
    for net in grid.nets.values():
        net_neighbors[net] = 0
        gate_occupation[net.start] += 1
        gate_occupation[net.end] += 1

    # TODO: add comment.
    for net in grid.nets.values():
        net_neighbors[net] \
            += gate_occupation[net.start] \
            + gate_occupation[net.end] - 2

    return sorted(net_neighbors,
                  key=net_neighbors.get,
                  reverse=descending)


def sort_exp_intersections(nets, descending=False):
    """
    Sorts net object instances based on
    how many intersections are expected.
    """

    # For every net object copy the start- and end coordinates
    for net in nets.values():

        segment1 = [net.start[:2], net.end[:2]]

        # TODO: add comment here
        for other_net in nets.values():

            segment2 = [other_net.start[:2], other_net.end[:2]]

            dx1 = segment1[1][0]-segment1[0][0]
            dy1 = segment1[1][1]-segment1[0][1]
            dx2 = segment2[1][0]-segment2[0][0]
            dy2 = segment2[1][1]-segment2[0][1]

            p1 = dy2*(segment2[1][0]-segment1[0][0]) \
                - dx2*(segment2[1][1]-segment1[0][1])
            p2 = dy2*(segment2[1][0]-segment1[1][0]) \
                - dx2*(segment2[1][1]-segment1[1][1])
            p3 = dy1*(segment1[1][0]-segment2[0][0]) \
                - dx1*(segment1[1][1]-segment2[0][1])
            p4 = dy1*(segment1[1][0]-segment2[1][0]) \
                - dx1*(segment1[1][1]-segment2[1][1])

            if (p1 * p2 <= 0) & (p3 * p4 <= 0):
                net.exp_intersections += 1

    return (sorted(nets.values(),
            key=operator.attrgetter('exp_intersections'),
            reverse=descending))
