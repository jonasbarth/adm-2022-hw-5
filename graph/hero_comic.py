"""A python module with functions for constructing a comic-hero graph."""

import pandas as pd
import networkx as nx
from .preprocess import strip_trailing_characters

_ACCEPTED_TYPES = {str, pd.DataFrame}


def create_from(nodes=None, edges=None):
    """Creates an undirected, unweighted comic-hero graph from the provided hero-comic nodes and hero-comic edges.

    Both inputs must be specified and must be of the same type, either strings or pandas DataFrames. When providing
    strings, they will be interpreted as paths from where the nodes and edges will be read. When providing pandas
    DataFrames, the graph will be created from them.

    :arg
    nodes (str | pd.DataFrame) - the path to a file with nodes or a pandas dataframe with the nodes.
    edges (str | pd.DataFrame) - the path to a file with edges or a pandas dataframe with the edges.
    """

    if not (nodes and edges):
        raise ValueError(f'The graph must be created from both nodes and edges. Nodes: {nodes}; Edges: {edges}.')

    if not (type(nodes) in _ACCEPTED_TYPES and type(edges) in _ACCEPTED_TYPES):
        raise ValueError(f'Nodes and Edges must be of the allowed types {_ACCEPTED_TYPES}. type(nodes) = {type(nodes)}; type(edges) = {type(edges)}')

    if type(nodes) != type(edges):
        raise ValueError(f'Nodes and edges are expected to be of the same type. type(nodes) = {type(nodes)}; type('
                         f'edges) = {type(edges)}')

    if isinstance(nodes, str) and isinstance(edges, str):
        # both will be loaded from a path
        nodes = pd.read_csv(nodes)
        strip_trailing_characters(nodes)
        nodes = [(node, node_type) for node, node_type in zip(nodes.node, nodes.type)]

        edges = pd.read_csv(edges)
        strip_trailing_characters(edges)
        edges = zip(edges.hero, edges.comic)

        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)

        return graph

    elif isinstance(nodes, pd.DataFrame) and isinstance(edges, pd.DataFrame):
        # create graph from dataframes
        nodes = [(node, node_type) for node, node_type in zip(nodes.node, nodes.type)]
        edges = zip(edges.hero, edges.comic)

        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)

        return graph
