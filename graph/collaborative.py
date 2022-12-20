"""Python module for creating the collaborative hero graph."""
import networkx as nx
import pandas as pd

from .preprocess import remove_self_loops


def create_from(path=None, data=None):
    """Creates a collaborative hero graph.

    Only specify ONE of the parameters.

    :arg
    path (str) - the path to a file to create the graph from.
    data (pd.DataFrame) - a pandas dataframe to create the graph from.

    :return
    A networkx graph.
    """
    if path and data:
        raise ValueError('You should only specify either path or data, not both.')

    if path:
        hero_network = pd.read_csv(path)
        return _create_graph_from_data(hero_network)

    _create_graph_from_data(data)


def _create_graph_from_data(data):
    remove_self_loops(data)

    graph = nx.MultiGraph()
    nodes = set(data.hero1.values).union(set(data.hero2.values))
    edges = zip(data.hero1.values, data.hero2.values)
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    return graph


def calculate_weight(hero1, hero2):
    """Calculates the weight of the edges between two heroes in the hero graph.

    The more collaborations the two heros have, the lower the weight.

    :arg
    hero1 (str) - the name of the first hero.
    hero2 (str) - the name of the second hero.

    :return
    weight (float) - the weight between these two heroes.
    """

    # make weight inverse proportional to the number of collaborations?
    pass