"""Python module for creating the collaborative hero graph."""
from collections import Counter

import networkx as nx
import pandas as pd

from .preprocess import remove_self_loops, strip_trailing_characters, replace_hero
from .weight import inverse_prob

_ACCEPTED_TYPES = {str, pd.DataFrame}


def create_from(data=None, weight=inverse_prob):
    """Creates a collaborative hero graph.

    Only specify either the path OR the data parameter, NOT both.

    :arg
    path (str) - the path to a file to create the graph from.
    data (pd.DataFrame) - a pandas dataframe to create the graph from.
    weight (function) - a function that is used to weight the edges between heroes.

    :return
    A networkx graph.
    """
    if not type(data) in _ACCEPTED_TYPES:
        raise ValueError(f'The data must be of the allowed types {_ACCEPTED_TYPES}. type(data) = {type(data)}')

    if isinstance(data, str):
        data = pd.read_csv(data)
        remove_self_loops(data)
        strip_trailing_characters(data)
        replace_hero(data, 'SPIDER-MAN/PETER PAR', 'SPIDER-MAN/PETER PARKER')

        return _create_graph_from_data(data)

    if isinstance(data, pd.DataFrame):
        return _create_graph_from_data(data)


def _create_graph_from_data(data, weight=inverse_prob):
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
    graph = nx.MultiGraph()
    nodes = set(data.hero1.values).union(set(data.hero2.values))
    edges = zip(data.hero1.values, data.hero2.values)
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    return graph


def _create_weighted_graph_from_multi_graph(multi_graph, weight=inverse_prob):
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
