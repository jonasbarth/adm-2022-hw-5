"""Python module for creating the collaborative hero graph."""
import logging
from collections import Counter

import networkx as nx
import pandas as pd

from backend.describe import GraphType
from backend.domain.hero import Collaboration
from .preprocess import remove_self_loops, strip_trailing_characters, replace_hero
from .weight import reciprocal_prop, max_prop

_ACCEPTED_TYPES = {str, pd.DataFrame}


logging.basicConfig(format='%(asctime)s %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_from(data=None, weight=max_prop):
    """Creates a collaborative hero graph.

    Only specify either the path OR the data parameter, NOT both.

    :arg
    path (str) - the path to a file to create the graph from.
    data (pd.DataFrame) - a pandas dataframe to create the graph from.
    weight (function) - a function that is used to weight the edges between heroes.

    :return
    A weighted, undirected, collaborative networkx graph of the hero data, and its graph type.
    """
    if not type(data) in _ACCEPTED_TYPES:
        raise ValueError(f'The data must be of the allowed types {_ACCEPTED_TYPES}. type(data) = {type(data)}')

    if isinstance(data, str):
        data = pd.read_csv(data)
        remove_self_loops(data)
        strip_trailing_characters(data)
        replace_hero(data, 'SPIDER-MAN/PETER PAR', 'SPIDER-MAN/PETER PARKER')
        logger.info(f'Creating collaborative hero graph from a csv file.')
        return _create_graph_from_data(data, weight), GraphType.COLLABORATIVE

    if isinstance(data, pd.DataFrame):
        logger.info(f'Creating collaborative hero graph from a pandas DataFrame.')
        return _create_graph_from_data(data, weight), GraphType.COLLABORATIVE


def _create_graph_from_data(data, weight=reciprocal_prop):
    multi_graph = _create_multi_graph_from_data(data)
    return _create_weighted_graph_from_multi_graph(multi_graph, weight)


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


def _create_weighted_graph_from_multi_graph(multi_graph, weight=reciprocal_prop):
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
            weighted_edges.append((*edge, {'weight': weight(*edge, n, multi_graph), 'n_collabs': n}))

    weighted_graph = nx.Graph()
    weighted_graph.add_nodes_from(multi_graph.nodes())
    weighted_graph.add_edges_from(weighted_edges)

    return weighted_graph


def get_hero_collabs(graph: nx.Graph):
    """Gets the number of collaborations between all heroes.

    For every hero, it will find the number of collaborations it has with each other hero. There will only ever be one
    object per hero collaboration. E.g. if Iron Man and Captain America have 2 collaborations, there won't be
    { Collaboration('Iron Man', 'Captain America', 2), Collaboration('Captain America', 'Iron Man', 2) } but only one
    of them.

    :arg
    graph (nx.Graph) - a networkx graph.

    :return
    a set of unique hero collaborations.
    """
    collabs = set()
    for hero in graph.nodes():

        for neigh in graph.neighbors(hero):
            n_collabs = graph.get_edge_data(hero, neigh)['n_collabs']
            collab = Collaboration(hero, neigh, n_collabs)
            collabs.add(collab)

    return collabs


