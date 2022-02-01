import matplotlib.pyplot as plt
import re

#plotly
import plotly.express as px
import plotly.io as pio

import pandas as pd


def visualize(chip, legend):
    """Makes a 3D visualization of the chip object instance."""

    x_eye = -1.25
    y_eye = 2
    z_eye = 0.5

    df1 = pd.DataFrame(index = ['x', 'y', 'z'], )

    for keys, values in chip.gates.items():

        df1[keys] = values.coordinates[0], values.coordinates[1], values.coordinates[2]

    df1[6] = 0, 0, 7

    df1 = df1.transpose()

    fig = px.scatter_3d(
        data_frame = df1,
        x = 'x',
        y = 'y',
        z = 'z',
        # template ='ggplot2'
    )
    fig.show()

    # # Get maximum x,y values for x,y axis size
    # max_x = chip.size[0]
    # max_y = chip.size[1]

    # plt.figure()
    # ax = plt.axes(projection="3d")

    # ax.set_title("3D Visual Chips&Circuits")

    # # Get all gate coordinates and make them visible in plot
    # for gate in chip.gates.values():
    #     ax.scatter3D(gate.coordinates[0],
    #                  gate.coordinates[1],
    #                  gate.coordinates[2],
    #                  c="black")

    # # Plot all net routes solutions of the chip object instance
    # for net in chip.nets.values():
    #     path = net.path
    #     x = path[0]
    #     y = path[1]
    #     z = path[2]

    #     ax.plot(x, y, z, label=net)

    # ax.set_xlim(0, max_x)
    # ax.set_ylim(0, max_y)
    # ax.set_zlim(0, 7)

    # # If user wants a legend, show it correctly
    # if legend is True:
    #     ax.legend(chip.nets.keys(),
    #               title='Nets',
    #               prop={'size': 7},
    #               bbox_to_anchor=(1.1, 1),
    #               ncol=3,
    #               loc='upper left')

    # # Filter inputfilename
    # pattern = "_(.*?).csv"
    # substring = re.search(pattern, chip.infile)

    # # If regex could filter the filename correctly use, else use inputfilename
    # if substring:
    #     substring = substring.group(1)
    #     plt.savefig(f"output/figs/fig_{substring}.png", bbox_inches="tight")
    # else:
    #     plt.savefig(f"output/figs/fig_{chip.infile}.png")

    # plt.show()
