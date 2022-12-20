"""Enum for the graph types."""
from enum import Enum
from attr import dataclass


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


@dataclass(frozen=True)
class GraphFeatures:
    """A dataclass for describing graph features."""
    n_nodes: int
    hero_collabs: any
    n_heroes_per_comic: any
    density: float
    degree_dist: any
    avg_degree: float
    hubs: set()
    mode: GraphMode
