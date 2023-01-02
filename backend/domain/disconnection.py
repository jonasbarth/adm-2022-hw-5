"""Module for disconnecting graph domain objects."""
import networkx as nx
from attr import dataclass


@dataclass(frozen=True)
class Disconnection:
    links: iter
    weight: float
    original_graph: nx.Graph
    hero_a: str
    hero_b: str
    graph_a: nx.Graph
    graph_b: nx.Graph

    def num_links(self):
        return len(self.links)
