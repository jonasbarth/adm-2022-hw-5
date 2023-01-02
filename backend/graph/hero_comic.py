"""A python module with functions for constructing a comic-hero graph."""
import itertools

import pandas as pd
import networkx as nx

from backend.describe import GraphType
from .preprocess import strip_trailing_characters, replace_hero
from backend.domain import Comic

_ACCEPTED_TYPES = {str, pd.DataFrame}


def create_from(nodes=None, edges=None):
    """Creates an undirected, unweighted comic-hero graph from the provided hero-comic nodes and hero-comic edges.

    Both inputs must be specified and must be of the same type, either strings or pandas DataFrames. When providing
    strings, they will be interpreted as paths from where the nodes and edges will be read. When providing pandas
    DataFrames, the graph will be created from them.

    :arg
    nodes (str | pd.DataFrame) - the path to a file with nodes or a pandas dataframe with the nodes.
    edges (str | pd.DataFrame) - the path to a file with edges or a pandas dataframe with the edges.

    :return
    an undirected, unweighted networkx graph with comics and heroes as nodes, and its graph type.
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
        replace_hero(nodes, 'SPIDER-MAN/PETER PARKERKER', 'SPIDER-MAN/PETER PARKER')
        nodes = [(node, {'type': node_type}) for node, node_type in zip(nodes.node, nodes.type)]

        edges = pd.read_csv(edges)
        strip_trailing_characters(edges)
        edges = zip(edges.hero, edges.comic)

        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)

        return graph, GraphType.HERO_COMIC

    elif isinstance(nodes, pd.DataFrame) and isinstance(edges, pd.DataFrame):
        # create graph from dataframes
        nodes = [(node, node_type) for node, node_type in zip(nodes.node, nodes.type)]
        edges = zip(edges.hero, edges.comic)

        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)

        return graph, GraphType.HERO_COMIC


def get_subgraph_with(graph: nx.Graph, heroes: iter, neighbours=True):
    """Gets a subgraph of the given graph with the heroes and their neighbours.

    :arg
    graph (nx.Graph) - a networkx graph consisting of heroes that are connected to comics.
    heroes (iter) - an iterable of heroes that should be included in the subgraph.

    :return
    a networkx graph that is a subgraph of the given graph with all the provided heroes and the comics they appear in.
    """
    if neighbours:
        comics = list(itertools.chain(*set(graph.neighbors(hero) for hero in heroes)))
        return graph.subgraph(heroes + comics)

    return graph.subgraph(heroes)


def get_comic_nodes(graph: nx.Graph):
    """Returns all nodes in the graph with the type attribute set to 'comic'.

    :arg
    graph (nx.Graph) - a networkx graph.

    :return
    a list of node names that are comics.
    """
    return [node for node, attributes in graph.nodes(data=True) if attributes['type'] == 'comic']


def get_n_heroes_per_comic(graph: nx.Graph):
    """Gets the number of heroes per comic.

    :arg
    graph (nx.Graph) - the graph where of comics and heroes. Comics nodes should have 'comic' as data and be connected
    to the heroes that appear in them.

    :return
    a list of Comic instances.
    """
    comics = []
    for comic in get_comic_nodes(graph):
        comics.append(Comic(comic, graph.degree(comic)))

    return comics
