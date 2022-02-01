import matplotlib.pyplot as plt
import re
import plotly.graph_objects as go
import pandas as pd


def visualize(chip, legend):
    """Makes a 3D visualization of the chip object instance."""

    # Make df out of gates to plot
    df_gates = pd.DataFrame(index = ['x', 'y', 'z'])

    for keys, values in chip.gates.items():
        df_gates[keys] = values.coordinates[0], values.coordinates[1], values.coordinates[2]
    
    df_gates = df_gates.transpose()

    # Create a df for every path in the netlist and store it in a dict
    path_df_dict = {}

    for keys in chip.nets.keys():
        path_df_dict[keys] = pd.DataFrame(columns = ['x', 'y', 'z'])

    for keys, values in chip.nets.items():
        df = path_df_dict[keys]
        for i in range(len(values.path[0])):
            df.loc[i] = [values.path[0][i], values.path[1][i], values.path[2][i]]

    # Plot gates and paths and show it in users browser
    fig = go.Figure()

    fig = go.Figure(data=[go.Scatter3d(
        x=df_gates['x'],
        y=df_gates['y'],
        z=df_gates['z'],
        mode = 'markers',
        showlegend=False
        )])

    for i in path_df_dict:
        label = str(i)
        fig = fig.add_trace(go.Scatter3d(x = path_df_dict[i]["x"],
                                   y = path_df_dict[i]["y"], 
                                   z = path_df_dict[i]['z'],
                                   name = label,
                                   mode = 'lines'),)
        fig.update_traces(
            line=dict(
                width=5
    fig.update_layout(scene = dict(zaxis = dict(nticks=7, range=[-1,7])))
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
