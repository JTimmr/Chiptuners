"""
sorting algortihms
"""

import random
import operator


def sort_length(netlist, descending=False):
    return (sorted(netlist.values(),key=operator.attrgetter('minimal_length'),reverse=descending))

def random_sort(netlist):
    value_list = list(netlist.values())
    return (random.shuffle(value_list))

def middle_first(netlist):
    # for netlist in self.netlists.values():
    pass
        

