"""This module is the central entry point to all backend functionalities."""
import networkx as nx

from service.hero import TopHeroService
from .describe import GraphMode, GraphType, GraphFeatures


def features(graph: nx.Graph, graph_type: GraphType, top_n: int):
    """Extracts the features of the graph.

    :arg
    graph (nx.Graph) - a networkx graph.
    graph_type (GraphType) - the type of the graph. Either the collaborative or hero-comic graph.
    top_n (int) - the top N heroes of which data will be considered.

    :return
    a GraphFeatures object.
    """
    n_nodes = len(graph.nodes())
    hs = TopHeroService.create_from(graph.nodes())

    subgraph = graph.subgraph(hs.top_n(top_n))

    if graph_type == GraphType.COLLABORATIVE:
        hero_collabs = None

    elif graph_type == GraphType.HERO_COMIC:
        n_heroes_per_comic = None

    density = nx.density(graph)
    degree_dist = None

    avg_degree = sum(map(lambda node: graph.degree(node), graph.nodes)) / n_nodes
    hubs = {}

    return GraphFeatures(n_nodes, hero_collabs, n_heroes_per_comic, density, degree_dist, avg_degree, hubs, GraphMode.DENSE)