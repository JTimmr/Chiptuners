import random
import operator


def sort_length(netlists, descending=False):
    """
    Sorts netlist object instances on their distance
    between start- and end coordinates.
    """
    return (sorted(netlists.values(),
            key=operator.attrgetter('minimal_length'),
            reverse=descending))


def random_sort(netlists, descending="None"):
    """Sorts netlist object instances in a random order."""
    value_list = list(netlists.values())
    random.shuffle(value_list)
    return (value_list)


def sort_middle_first(netlists, descending=False):
    """
    Sorts netlist object instances on their position in the grid;
    in the middle or on the outside.
    """
    x_champion = 0
    y_champion = 0
    x_loser = 1000
    y_loser = 1000

    # Search for the gates with the highest x or y value
    for value in netlists.values():
        x_contestent = value.start[0]
        y_contestent = value.start[1]

        if x_contestent > x_champion:
            x_champion = x_contestent

        if y_contestent > y_champion:
            y_champion = y_contestent

        if x_contestent < x_loser:
            x_loser = x_contestent

        if y_contestent < y_loser:
            y_loser = y_contestent

    # TODO: Misschien even je wiskunde uitleggen?
    middle_x = round((x_champion + x_loser)/2)
    middle_y = round((x_champion + x_loser)/2)

    # Give every netlist object instance ranking position attribute to sort on
    for key in netlists:
        ranking = abs(
            middle_x - value.start[0]) + abs(middle_y - value.start[1])
        netlists[key].ranking = ranking

    return (sorted(netlists.values(),
            key=operator.attrgetter('ranking'),
            reverse=descending))


def sort_gate(grid, descending=True):
    """
    Sorts netlist object instances on how many connections a gate has
    with other gates.
    """
    gate_occupation = {}
    netlist_neighbors = {}

    # Set gate occupation to zero for all gate coordinates
    for gate in grid.gates.values():
        gate_occupation[gate.coordinates] = 0

    # Count occurrences of gate coordinates
    for netlist in grid.netlists.values():
        netlist_neighbors[netlist] = 0
        gate_occupation[netlist.start] += 1
        gate_occupation[netlist.end] += 1

    # TODO: add comment.
    for netlist in grid.netlists.values():
        netlist_neighbors[netlist] \
            += gate_occupation[netlist.start] \
            + gate_occupation[netlist.end] - 2

    return sorted(netlist_neighbors,
                  key=netlist_neighbors.get,
                  reverse=descending)


def sort_exp_intersections(netlists, descending=False):
    """
    Sorts netlist object instances based on
    how many intersections are expected.
    """

    # For every netlist object copy the start- and end coordinates
    for netlist in netlists.values():

        segment1 = [netlist.start[:2], netlist.end[:2]]

        # TODO: add comment here
        for other_netlist in netlists.values():

            segment2 = [other_netlist.start[:2], other_netlist.end[:2]]

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
                netlist.exp_intersections += 1

    return (sorted(netlists.values(),
            key=operator.attrgetter('exp_intersections'),
            reverse=descending))
