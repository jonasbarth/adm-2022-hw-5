"""Module for community objects."""
from attr import dataclass
import networkx as nx


@dataclass(frozen=True)
class Communities:
    links: iter
    original_graph: nx.Graph
    hero_1: str
    hero_2: str
    community_1: nx.Graph
    community_2: nx.Graph
    same_community: bool

    def num_links(self):
        return len(self.links)