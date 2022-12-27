"""This module is the central entry point to all backend functionalities."""

import networkx as nx

from backend.graph import get_n_heroes_per_comic, get_subgraph_with, get_hero_collabs
from backend.service import TopHeroService
from .describe import GraphMode, GraphType, GraphFeatures, get_degree_dist, get_hubs


def features(graph: nx.Graph, graph_type: GraphType, top_n: int):
    """Extracts the features of the graph.

    :arg
    graph (nx.Graph) - a networkx graph.
    graph_type (GraphType) - the type of the graph. Either the collaborative or hero-comic graph.
    top_n (int) - the top N heroes of which data will be considered.

    :return
    a GraphFeatures object.
    """
    hero_collabs = {}
    n_heroes_per_comic = []
    n_nodes = len(graph.nodes())
    hs = TopHeroService.create_from('data/edges.csv')

    top_heroes = hs.top_n(top_n)

    if graph_type == GraphType.COLLABORATIVE:
        subgraph = graph.subgraph(top_heroes)
        hero_collabs = get_hero_collabs(subgraph)

    elif graph_type == GraphType.HERO_COMIC:
        subgraph = get_subgraph_with(graph, top_heroes)
        n_heroes_per_comic = get_n_heroes_per_comic(subgraph)

    density = nx.density(graph)
    degree_dist = get_degree_dist(graph)

    avg_degree = sum(map(lambda node: graph.degree(node), graph.nodes)) / n_nodes

    hubs = get_hubs(graph, 95)

    return GraphFeatures(graph_type, n_nodes, hero_collabs, n_heroes_per_comic, density, degree_dist, avg_degree, hubs, GraphMode.DENSE)
