"""Module for visualising backend functionalities."""
import logging
import os
from tkinter import *

import networkx as nx
from pyvis.network import Network

from backend.domain import Disconnection


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


def disconnected_graph(disc: Disconnection):
    """Visualises disconnected graphs.

    :arg
    disc (Disconnection) - the disconnection to be visualised.

    :return
    (str, plt.figure, plt.figure) - a message about the number of edges that were removed, a plot of the original grpah,
    a plot of the original graph after the links were removed with the two hero nodes highlighted.
    """

    target_directory = "doc/visualisations/disconnected"


    os.makedirs(target_directory, exist_ok=True)

    logger.info("Starting visualisation of disconnected graph.")
    message = f'The number of edges that were removed from the original graph is: {disc.num_links()}'

    #colour_map = ['red' if node in {disc.hero_a, disc.hero_b} else 'blue' for node in disc.original_graph.nodes]
    #nx.draw(disc.original_graph, node_color=colour_map, with_labels=True)
    attrs = {}
    for node in disc.original_graph.nodes():
        if node in {disc.hero_a, disc.hero_b}:
            attrs[node] = {'color': 'red'}
        else:
            attrs[node] = {'color': 'blue'}

    nx.set_node_attributes(disc.original_graph, attrs)
    # Get the current screen width and height
    screen_width, screen_height = get_screen_size()


    def node_size(x): return 50
    # populates the nodes and edges data structures
    # Network.set_options()
    nt = Network(height=f'{screen_height}px', width='100%')

    nt.barnes_hut()
    # nt.toggle_physics(False)
    nt.from_nx(disc.original_graph, node_size_transf=node_size)
    nt.show_buttons(filter_=['nodes'])

    nt.write_html(f'{target_directory}/original_graph.html')


    nt = Network(height=f'{screen_height}px', width='100%')

    #nt.barnes_hut()
    #nt.toggle_physics(False)
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

    nt.write_html(f'{target_directory}/disconnected_graphs.html')

    logger.info("Successfully wrote html.")

