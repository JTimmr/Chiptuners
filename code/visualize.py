import matplotlib.pyplot as plt

def visualize(chip):
    """Makes a 3D visualization of the chip object."""

    max_x = chip.size[0]
    max_y = chip.size[1]

    ax = plt.axes(projection = "3d")
    
    ax.set_title("3D Visual Chips&Circuits")
    
    for gate in chip.gates.values():
        ax.scatter3D(gate.coordinates[0], gate.coordinates[1], gate.coordinates[2], c = "black")

    for netlist in chip.netlists.values():
        path = netlist.path
        x = path[0]
        y = path[1]
        z = path[2]

        ax.plot(x, y, z, label = netlist)
    
    ax.set_xlim(0, max_x) 
    ax.set_ylim(0, max_y)
    ax.set_zlim(0, 7)
    ax.legend(chip.netlists.keys(), title = "Netlist", prop={'size': 7}, bbox_to_anchor=(1.15, 1),loc='upper left')
    plt.savefig("62.png")
    # plt.show()
