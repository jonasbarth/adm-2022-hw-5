"""Module for visualising backend functionalities."""
import logging
import os
from tkinter import *

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from IPython.display import display
from pyvis.network import Network

from backend.describe import GraphFeatures, GraphType
from backend.domain import Disconnection, Communities

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def visualise_features(features: GraphFeatures):
    """Visualises a features object.

    :arg
    features (GraphFeatures) - the GraphFeatures object.


    """
    # Basic features:
    print('')
    print('SOME BASIC FEATURE:')
    print('')
    print(f'-->  This network has {features.n_nodes} nodes.')
    print(f'-->  The density of the network is {features.density}')
    # Since the density varies between 0 and 1, we set 0.5 as a treshold to decide wheter the network is dense or sparse

    print(f'-->  Since the density is {features.density}, we say that the network is {features.mode.name}.')

    print(f'-->  The average degree in the network is {features.avg_degree} nodes.')
    print('')
    print('*' * 50)
    print('')

    print('SOME INFO ABOUT THE HUBS:')
    print('')
    print('-->  The Hubs of the network are the following:')
    display(features.hubs)
    print('')
    print('*' * 70)
    print('')

    # Number of collabs for each hero:
    if features.graph_type == GraphType.COLLABORATIVE:
        print('SOME INFO ABOUT THE COLLABORATION OF EACH HERO:')
        print('')
        display(features.hero_collabs)
        print('')
        print('*' * 70)

        # Number of heroes for each comic:
    if features.graph_type == GraphType.HERO_COMIC:
        print('SOME INFO ABOUT THE COMICS:')
        print('')
        display(features.n_heroes_per_comic)
        print('')
        print('*' * 70)

        # Degree Distribution
    print('')
    print('THE DEGREE DISTRIBUTION:')

    fig = plt.figure(figsize=(8, 8))
    axgrid = fig.add_gridspec(5, 4)

    ax1 = fig.add_subplot(axgrid[3:, :2])
    ax1.plot(features.degree_dist.degree, marker=".", markersize=4, color='tomato')
    ax1.set_title("Degree Distribution")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")


def get_screen_size():
    """Gets the width and height of the screen size in pixels.

    :return
    (int, int) - the (width, height) of the current screen.
    """
    # Create an instance of tkinter frame
    win = Tk()

    # Set the geometry of frame
    win.geometry("650x250")

    # Get the current screen width and height
    return win.winfo_screenwidth(), win.winfo_screenheight()


def visualise_disconnected_graph(disc: Disconnection):
    """Visualises disconnected graphs.

    :arg
    disc (Disconnection) - the disconnection to be visualised.

    :return
    (str, str, str) - a message about the disconnected graphs and the two paths for the generated html for the
    original and disconnected graphs.
    """

    target_directory = "doc/visualisations/disconnected"
    original_graph_file = f'{target_directory}/original_graph.html'
    disconnected_graphs_file = f'{target_directory}/disconnected_graphs.html'

    os.makedirs(target_directory, exist_ok=True)

    message = f'The number of edges that were removed from the original graph is: {disc.num_links()}'

    attrs = {}
    # use different colours for the two main heroes to distinguish them from the rest.
    for node in disc.original_graph.nodes():
        if node in {disc.hero_a, disc.hero_b}:
            attrs[node] = {'color': 'red'}
        else:
            attrs[node] = {'color': 'blue'}

    nx.set_node_attributes(disc.original_graph, attrs)
    # Get the current screen width and height
    screen_width, screen_height = get_screen_size()

    def node_size(x):
        return 50

    nt = Network(height=f'{screen_height}px', width='100%')

    nt.barnes_hut()
    # nt.toggle_physics(False)
    nt.from_nx(disc.original_graph, node_size_transf=node_size)
    nt.show_buttons(filter_=['nodes'])

    nt.write_html(original_graph_file)
    logger.info(f"Successfully wrote original graph to: {original_graph_file}.")

    nt = Network(height=f'{screen_height}px', width='100%')

    removed_graphs = nx.Graph()
    removed_graphs.add_nodes_from(list(disc.graph_a.nodes(data=True)) + list(disc.graph_b.nodes(data=True)))
    removed_graphs.add_edges_from(list(disc.graph_a.edges(data=True)) + list(disc.graph_b.edges(data=True)))

    nt.from_nx(removed_graphs)

    pos = nx.spring_layout(removed_graphs, k=2, scale=1000)

    for node in nt.get_nodes():
        nt.get_node(node)['x'] = pos[node][0]
        nt.get_node(node)['y'] = -pos[node][1]  # the minus is needed here to respect ntworkx y-axis convention 
        nt.get_node(node)['physics'] = False
        nt.get_node(node)['label'] = str(node)  # set the node label as a string so that it can be displayed
        nt.get_node(node)['size'] = 25

    nt.toggle_physics(False)
    nt.show_buttons(filter_=['nodes'])

    nt.write_html(disconnected_graphs_file)

    logger.info(f"Successfully wrote disconnected graphs to: {disconnected_graphs_file}.")

    return message, original_graph_file, disconnected_graphs_file


def visualise_metrics(graph_metrics: tuple, node_metrics: tuple, metric: str):
    """Returns a table of the average metric values over the graph metrics and the single node metric.

    :arg
    graph_metrics (dict) - a dictionary with node names as keys and metric values as values.
    node_metrics (dict) a dictionary with with a single node name as key and its metric as value.
    metric (str) - the name of the metric that was used.
    table_format (str) - the format of the table to be returned.
    """
    top_n, top_n_avg_metric = graph_metrics
    node, metric_value = node_metrics

    data = [[top_n_avg_metric, metric_value]]
    headers = [f'Top {top_n} Heroes Average', f'{node}']

    df_metrics = pd.DataFrame(data=data, columns=headers)

    fig = plt.figure(figsize=(8, 2))
    ax = fig.add_subplot(211)

    table = ax.table(cellText=df_metrics.values,
                     colLabels=df_metrics.columns,
                     loc="center",
                     cellLoc='center',
                     colLoc='center')

    ax.set_title(metric)
    table.set_fontsize(12)
    table.scale(2, 2)
    ax.axis("off");


def visualise_communities(comms: Communities):
    """Visualises the communities."""
    target_directory = "doc/visualisations/communities"
    original_graph_file = f'{target_directory}/original_graph.html'
    communities_graphs_file = f'{target_directory}/communities_graph.html'
    final_graphs_file = f'{target_directory}/final_graph.html'

    os.makedirs(target_directory, exist_ok=True)

    # Print the number of links that should be removed to have the communities
    message = f'The number of links that should be removed to have two communities is: {comms.num_links()}.'

    # A table depicting the communities and the heroes that belong to each community

    community_1, community_2 = pd.Series(list(comms.community_1)), pd.Series(list(comms.community_2))
    df_communities = pd.DataFrame({'Community 1': community_1, 'Community2': community_2})
    for col in df_communities.columns:
        df_communities[col].fillna('-', inplace=True)
    fig = plt.figure(figsize=(8, df_communities.shape[0]))
    ax = fig.add_subplot(211)

    colors = np.array(list(zip(["w"] * df_communities.shape[0], ["w"] * df_communities.shape[0])))

    hero_1_index, hero_2_index = np.where(df_communities.values == comms.hero_1), np.where(df_communities.values == comms.hero_2)
    colors[hero_1_index] = 'blue'
    colors[hero_2_index] = 'red'

    table = ax.table(cellText=df_communities.values,
                     colLabels=df_communities.columns,
                     loc="center",
                     cellLoc='center',
                     colLoc='center',
                     cellColours=colors)

    ax.set_title("Two communities and their heroes.")
    table.set_fontsize(12)
    table.scale(2, 2)
    ax.axis("off")

    screen_width, screen_height = get_screen_size()

    def node_size(x):
        return 50

    # Create the original graph
    nt = Network(height=f'{screen_height}px', width='100%')

    nt.barnes_hut()
    nt.from_nx(comms.original_graph, node_size_transf=node_size)
    nt.show_buttons(filter_=['nodes'])

    nt.write_html(original_graph_file)
    logger.info(f"Successfully wrote original graph to: {original_graph_file}.")

    # Create the graph showing the communities in the network
    communities_graph = nx.Graph(comms.original_graph)
    attrs = {}

    # use different colours for the two heroes to distinguish them from the rest.
    for node in communities_graph.nodes():
        if node in comms.community_1:
            attrs[node] = {'color': 'red'}
        elif node in comms.community_2:
            attrs[node] = {'color': 'blue'}

    nx.set_node_attributes(communities_graph, attrs)

    nt = Network(height=f'{screen_height}px', width='100%')

    nt.barnes_hut()
    nt.from_nx(communities_graph, node_size_transf=node_size)
    nt.show_buttons(filter_=['nodes'])

    nt.write_html(communities_graphs_file)
    logger.info(f"Successfully wrote communities graph to: {original_graph_file}.")

    # Create the final graph and identify the community/communities of Hero_1 and Hero_2
    hero_1_community = comms.community_1 if comms.hero_1 in comms.community_1 else comms.community_2
    hero_2_community = comms.community_1 if comms.hero_2 in comms.community_1 else comms.community_2

    final_graph = nx.Graph(comms.original_graph)
    attrs = {}

    for node in final_graph.nodes():
        # Green means that both heroes are in the same community
        if node in hero_1_community and node in hero_2_community:
            attrs[node] = {'color': 'green'}
        # Blue means that a node is in hero 1 community
        elif node in hero_1_community:
            attrs[node] = {'color': 'blue'}
        # Red means that a node is in hero 2 community
        elif node in hero_2_community:
            attrs[node] = {'color': 'red'}
        # Yellow means that the node is in neither community
        else:
            attrs[node] = {'color': 'yellow'}

    nx.set_node_attributes(final_graph, attrs)

    nt = Network(height=f'{screen_height}px', width='100%')

    nt.barnes_hut()
    nt.from_nx(final_graph, node_size_transf=node_size)
    nt.show_buttons(filter_=['nodes'])

    nt.write_html(final_graphs_file)
    logger.info(f"Successfully wrote final graph to: {final_graphs_file}.")

    return message, fig, original_graph_file, communities_graphs_file, final_graphs_file


def visualize_shortest_path(shortest_path):

    nodes_path = []

    for p in shortest_path:
        nodes_path.append(p[1])

    print('The shortest path in terms of comics is:', nodes_path)
    print('')
    print('*'*75)
    print('')

    # create a directed graph
    G = nx.DiGraph()

    # add edges to the graph
    for path in shortest_path:
        for i in range(len(path)-1):
            G.add_edge(path[i], path[i+1])


    # Plot the graph
    plt.figure(figsize=(10, 10))
    nx.draw(G, with_labels=True, node_size = 500)


    # show the plot
    plt.figure(figsize = (5, 5))
    plt.show()