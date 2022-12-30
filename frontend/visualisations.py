"""Module for visualising backend functionalities."""

import networkx as nx
import matplotlib.pyplot as plt


def disconnected_graph(num_links: int, original_graph: nx.Graph, graph_a: nx.Graph, graph_b: nx.Graph, hero_a: str,
                       hero_b: str):
    """Visualises disconnected graphs.

    :arg
    num_links (int) - the number of edges that were removed from the original graph.
    original_graph (nx.Graph) - the original graph.
    graph_a (nx.Graph) - the subgraph containing hero_a.
    graph_b (nx.Graph) - the subgraph containing hero_b.
    hero_a (str) - the first hero.
    hero_b (str) - the second hero.

    :return
    (str, plt.figure, plt.figure) - a message about the number of edges that were removed, a plot of the original grpah,
    a plot of the original graph after the links were removed with the two hero nodes highlighted.
    """
    message = f'The number of edges that were removed from the original graph is: {num_links}'

    colour_map = ['red' if node in {hero_a, hero_b} else 'blue' for node in original_graph.nodes]
    nx.draw(original_graph, node_color=colour_map, with_labels=True)
