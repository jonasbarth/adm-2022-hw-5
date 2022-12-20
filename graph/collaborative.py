"""Python module for creating the collaborative hero graph."""
from collections import Counter

import networkx as nx
import pandas as pd

from .preprocess import remove_self_loops
from .weight import inverse_prop


def create_from(path=None, data=None, weight=inverse_prop):
    """Creates a collaborative hero graph.

    Only specify either the path OR the data parameter, NOT both.

    :arg
    path (str) - the path to a file to create the graph from.
    data (pd.DataFrame) - a pandas dataframe to create the graph from.
    weight (function) - a function that is used to weight the edges between heroes.

    :return
    A networkx graph.
    """
    if path and data:
        raise ValueError('You should only specify either path or data, not both.')

    if path:
        data = pd.read_csv(path)

    return _create_graph_from_data(data)


def _create_graph_from_data(data, weight=inverse_prop):
    multi_graph = _create_multi_graph_from_data(data)
    return _create_weighted_graph_from_multi_graph(multi_graph)


def _create_multi_graph_from_data(data):
    """Creates an undirected, unweighted multigraph from the data.

    Self loops are removed from the data.

    :arg
    data (pd.DataFrame) - a pandas dataframe with two columns: hero1, hero2. Each row in the dataframe represents an
    edge between hero1 and hero2.

    :return
    an networkx multigraph.
    """
    remove_self_loops(data)

    graph = nx.MultiGraph()
    nodes = set(data.hero1.values).union(set(data.hero2.values))
    edges = zip(data.hero1.values, data.hero2.values)
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    return graph


def _create_weighted_graph_from_multi_graph(multi_graph, weight=inverse_prop):
    """Creates an undirected, weighted graph from an existing multigraph.

    :arg
    multigraph (networkx.Multigraph) - a networkx multigraph.

    :return
    an networkx graph with weighted edges.
    """
    weighted_edges = []
    for node in multi_graph.nodes():
        node_n_edges = Counter(multi_graph.edges(node))

        for edge, n in node_n_edges.items():
            weighted_edges.append((*edge, {'weight': weight(*edge, n)}))

    weighted_graph = nx.Graph()
    weighted_graph.add_nodes_from(multi_graph.nodes())
    weighted_graph.add_edges_from(weighted_edges)

    return weighted_graph
