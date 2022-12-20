"""Python module for creating the collaborative hero graph."""
import pandas as pd
import networkx as nx
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
        # create from path
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