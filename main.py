import code.classes.representation as rep

if __name__ == "__main__": 
    grid = rep.Grid("0","1")
    grid.compute_costs()
    grid.to_csv()


    # Main values for checking
    print()
    print(f"The gate coordinates are: {grid.gate_coordinates}")
    print(f"The wire segment paths are: {grid.wire_segments}")
    print(f"The number of intersections: {grid.intersections}")
    print()
    print(f"The total amount of costs = {grid.cost}")
    print()