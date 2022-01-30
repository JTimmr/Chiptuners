"""
sorting algortihms
"""

import random
import operator



def sort_length(netlists, descending=False):
    return (sorted(netlists.values(),key=operator.attrgetter('minimal_length'),reverse=descending))


def random_sort(netlists):
    value_list = list(netlists.values())
    random.shuffle(value_list)
    return (value_list)


def sort_middle_first(netlists, descending=False):
    x_champion = 0
    y_champion = 0
    x_loser = 1000
    y_loser = 1000

    # search for the gates with the highest x or y value
    for value in netlists.values():
        # breakpoint()
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

    middle_x = round((x_champion + x_loser)/2)
    middle_y = round((x_champion + x_loser)/2)

    for key in netlists:
        ranking = abs(middle_x - value.start[0]) + abs(middle_y - value.start[1])
        netlists[key].ranking = ranking

    return (sorted(netlists.values(),key=operator.attrgetter('ranking'),reverse=descending))

def sort_gate(grid, descending=True):
    gate_occupation = {}
    netlist_neighbors = {}

    for gate in grid.gates.values():
        gate_occupation[gate.coordinates] = 0

    for netlist in grid.netlists.values():
        netlist_neighbors[netlist] = 0
        gate_occupation[netlist.start] += 1
        gate_occupation[netlist.end] += 1

    for netlist in grid.netlists.values():
        netlist_neighbors[netlist] += gate_occupation[netlist.start] + gate_occupation[netlist.end] - 2

    return sorted(netlist_neighbors, key=netlist_neighbors.get, reverse=descending)


def sort_exp_intersections(netlists, descending=False):

    # for netlist in netlists.values():

    #     # create the set of all numbers that span the distance of x and y for a netlist
    #     dx = set(range(netlist.start[0], netlist.end[0]+1))
    #     dy = set(range(netlist.start[1], netlist.end[1]+1))

    #     # check whether the spanned distance of the other netlists is a sub or superset of the current netlist
    #     for other_netlist in netlists.values():

    #         # create the set of all numbers that span the distance of x and y for all other netlists
    #         dx_other = set(range(other_netlist.start[0], other_netlist.end[0]+1))
    #         dy_other = set(range(other_netlist.start[1], other_netlist.end[1]+1))

    #         # if the spanned distance is for both x and y a sub/super set of another then they must cross
    #         if dx.issubset(dx_other) or dx.issuperset(dx_other) and dy.issubset(dy_other) or dy.issuperset(dy_other):
    #             netlist.exp_intersections += 1

    # return (sorted(netlists.values(),key=operator.attrgetter('exp_intersections'),reverse=descending))

    for netlist in netlists.values():
        for other_netlist in netlists.values():
            segment1 = [netlist.start[:2], netlist.end[:2]]
            segment2 = [other_netlist.start[:2], other_netlist.end[:2]]
            
            dx1 = segment1[1][0]-segment1[0][0]
            dy1 = segment1[1][1]-segment1[0][1]
            dx2 = segment2[1][0]-segment2[0][0]
            dy2 = segment2[1][1]-segment2[0][1]

            p1 = dy2*(segment2[1][0]-segment1[0][0]) - dx2*(segment2[1][1]-segment1[0][1])
            p2 = dy2*(segment2[1][0]-segment1[1][0]) - dx2*(segment2[1][1]-segment1[1][1])
            p3 = dy1*(segment1[1][0]-segment2[0][0]) - dx1*(segment1[1][1]-segment2[0][1])
            p4 = dy1*(segment1[1][0]-segment2[1][0]) - dx1*(segment1[1][1]-segment2[1][1])

            if (p1*p2<=0) & (p3*p4<=0):
                netlist.exp_intersections += 1

    
    return (sorted(netlists.values(),key=operator.attrgetter('exp_intersections'),reverse=descending))
