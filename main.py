import code.classes.grid as grid
from code.algorithms import representation as rep
from code.algorithms import baseline as base

if __name__ == "__main__": 

    chip = grid.Grid("1","4")
    # representation = rep.Representation(chip)
    # representation.make_connections()

    baseline = base.Baseline(chip)
    baseline.run()

    chip.compute_costs()
    chip.to_csv()


    # Main values for checking
    print()
    print(f"The gate coordinates are: {chip.gate_coordinates}")
    #print(f"The wire segment paths are: {grid.wire_segments}")
    print(f"The number of intersections: {chip.intersections}")
    print()
    print(f"The total amount of costs = {chip.cost}")
    print(f"The total amount of attempts taken = {chip.tot_attempts}")
    print()


