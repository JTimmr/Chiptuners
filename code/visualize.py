import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def visualize(chip):
    """Text."""
    max_x = 0
    max_y = 0

    fig = plt.figure()
    ax = plt.axes(projection = "3d")
    
    ax.set_title("3D Visual Chips&Curcuits")
    
    for gate in chip.gates.values():
        ax.scatter3D(gate.coordinates[0], gate.coordinates[1], gate.coordinates[2], c = "black")

    for netlist in chip.netlists.values():
        path = netlist.path
        x = path[0]
        y = path[1]
        z = path[2]

        max_x = max(x)
        max_y = max(y)
        
        ax.plot(x, y, z, label = netlist)
    
    ax.set_xlim(0, max_x) 
    ax.set_ylim(0, max_x)
    ax.set_zlim(0, 7)
    ax.legend(chip.netlists.keys(), title = "Netlist", prop={'size': 7}, bbox_to_anchor=(1.15, 1),loc='upper left')
    plt.show()
    


        


