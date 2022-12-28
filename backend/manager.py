"""This module is the central entry point to all backend functionalities."""

import networkx as nx

from backend.graph import get_n_heroes_per_comic, get_subgraph_with, get_hero_collabs
from backend.service import TopHeroService
from .describe import GraphMode, GraphType, GraphFeatures, get_degree_dist, get_hubs


def features(graph: nx.Graph, top_n: int, **kwargs):
    """Extracts the features of the graph.

    :arg
    graph (nx.Graph) - a networkx graph.
    top_n (int) - the top N heroes of which data will be considered.
    **graph_type (GraphType) - the type of the graph. Either the collaborative or hero-comic graph.

    :return
    a GraphFeatures object.
    """
    graph_type = kwargs.get('graph_type')
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


def shortest_ordered_route(graph: nx.Graph, top_n: int, **kwargs):
    """The shortest walk of comics that you need to read to get from the starting node to the end node.

    :arg
    graph (nx.Graph) - a networkx graph that is of type GraphType.HERO_COMIC.
    hero_sequence (list) - a sequence of super heroes, excluding the start and end heroes.
    **start_hero (str) - the first node of the walk.
    **end_hero (str) - the last node of the walk.
    **top_n (int) - the top N heroes to consider.

    :return
    the shortest walk that goes from the start hero to the end hero and which visits the nodes in the hero sequence, in
    order.
    """
    hs = TopHeroService.create_from('data/edges.csv')

    top_heroes = hs.top_n(top_n)

    subgraph = get_subgraph_with(graph, top_heroes)

    hero_sequence, start_hero, end_hero = kwargs.get('hero_sequence'), kwargs.get('start_hero'), kwargs.get('end_hero')
    # I could get all of the shortest paths and then filter them
    shortest_paths = nx.all_shortest_paths(subgraph, start_hero, end_hero)

    walk = shortest_paths[0]


def disconnecting_graphs(graph: nx.Graph, top_n: int, **kwargs):
    """Finds the minimum number of links (by considering their weights) required to disconnect the original graph in two
    disconnected subgraphs: G_a and G_b.

    :arg
    graph (nx.Graph) - a networkx graph of type GraphType.COLLABORATIVE, where heroes are connected to heroes.
    top_n (int) - the top N heroes to consider.
    **hero_a (str) - a hero to which the first subgraph is related.
    **hero_b (str) - a hero to which the second subgraph is related.

    :return
    The minimum number of links required to disconnect the original graph in two disconnected subgraphs.
    """
    hs = TopHeroService.create_from('data/edges.csv')
    top_heroes = hs.top_n(top_n)
    subgraph = get_subgraph_with(graph, top_heroes)

    hero_a = kwargs.get('hero_a')
    hero_b = kwargs.get('hero_b')

    # I need to look at the edges, and find the set of edges that once I remove it, will give me two subgraphs with hero_a in the first and hero_b in the second.
    # the set of nodes should be the cheapest set possible, considering all of the weights.