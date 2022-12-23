"""Enum for the graph types."""
from enum import Enum
from attr import dataclass
import networkx as nx
import pandas as pd
import numpy as np


class GraphType(Enum):
    """The type of a marvel graph.

    COLLABORATIVE - an undirected, weighted graph where heroes are nodes and edges between nodes indicate how often they
    appeared in the same comic.

    HERO_COMIC - an undirected, unweighted graph where nodes are heroes or comics, and edges mean that a hero appeared
    in a specific comic.
    """
    COLLABORATIVE = 1
    HERO_COMIC = 2


class GraphMode(Enum):
    """An enum that describes whether a graph is sparse or dense."""
    SPARSE = 0
    DENSE = 1


@dataclass(frozen=True, repr=True)
class GraphFeatures:
    """A dataclass for describing graph features."""
    graph_type: GraphType
    n_nodes: int
    hero_collabs: any
    n_heroes_per_comic: any
    density: float
    degree_dist: any
    avg_degree: float
    hubs: set()
    mode: GraphMode


def get_degree_dist(graph: nx.Graph):
    """Gets the distribution of degrees within a networkx graph.

    :arg
    graph (nx.Graph) - a networkx graph.

    :return
    a pandas dataframe with node and degree columns.
    """
    dist = [(hero, graph.degree(hero)) for hero in graph.nodes()]
    return pd.DataFrame(data=dist, columns=['node', 'degree'])


def get_hubs(graph: nx.Graph, percentile: int):
    """Returns the hubs of the graph.

    :arg
    graph (nx.Graph) - the graph to get the hubs from.
    percentile (int) - the percentile to calculate the hub on. E.g. 95 is the 95th percentile.
    """
    dist = get_degree_dist(graph)

    threshold = get_hub_threshold(dist, percentile)

    return dist[dist.degree >= threshold].node.values


def get_hub_threshold(dist: pd.DataFrame, percentile: int):
    """Gets the degree threshold for what classifies as a hub in a graph.

    :arg
    dist (pd.DataFrame) - the degree distribution of a network. Expects columns ['node', 'degree'].
    percentile (int) - the percentile to calculate the hub on. E.g. 95 is the 95th percentile.

    :return
    the hub threshold as an int value.
    """
    return np.percentile(dist.degree, percentile)
