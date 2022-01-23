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

def sort_intersections():
    pass
