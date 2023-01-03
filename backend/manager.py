"""This module is the central entry point to all backend functionalities."""

import networkx as nx

from backend.graph import get_n_heroes_per_comic, get_subgraph_with, get_hero_collabs
from backend.service import TopHeroService
from .describe import GraphType, GraphFeatures, get_degree_dist, get_hubs, get_graph_mode
from .domain import Disconnection, Communities


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

    if not graph_type:
        raise ValueError(f'You must specify the graph_type kwargs parameter. It is: {graph_type}.')
    if not isinstance(graph_type, GraphType):
        raise ValueError(
            f'The provided graph_type kwargs parameter must be of type GraphType. type(graph_type): {type(graph_type)}.')

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

    graph_mode = get_graph_mode(subgraph)

    return GraphFeatures(graph_type, n_nodes, hero_collabs, n_heroes_per_comic, density, degree_dist, avg_degree, hubs,
                         graph_mode)


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
    (float, int, nx.Graph, nx.Graph) - The cumulative weight of the removed edges, the number of removed edges, the two
    disconnected subgraphs.
    """

    def edge_is_bridge(edge, graph_a, graph_b):
        start, end = edge
        return (start in graph_a and end in graph_b) or (start in graph_b and end in graph_a)

    hero_a = kwargs.get('hero_a')
    hero_b = kwargs.get('hero_b')

    hs = TopHeroService.create_from('data/edges.csv')
    top_heroes = hs.top_n(top_n)
    subgraph = nx.subgraph(graph, top_heroes)

    if hero_a not in top_heroes:
        raise ValueError(f'The provided hero_a: {hero_a} is not part of the top_n: {top_n} heroes.')

    if hero_b not in top_heroes:
        raise ValueError(f'The provided hero_b: {hero_b} is not part of the top_n: {top_n} heroes.')

    # First, find the min cut max flow using the networkx API. This will return the max flow (min possible weight) and
    # the nodes of the two subgraphs
    weight, nodes = nx.minimum_cut(subgraph, hero_a, hero_b, capacity='weight')
    nodes_a, nodes_b = nodes

    graph_a, graph_b = nx.subgraph(subgraph, nodes_a), nx.subgraph(subgraph, nodes_b)

    bridges = list(filter(lambda edge: edge_is_bridge(edge, graph_a, graph_b), subgraph.edges))

    return Disconnection(bridges, weight, subgraph, hero_a, hero_b, graph_a, graph_b)


def metrics(graph: nx.Graph, top_n: int, **kwargs):
    """Calculates the metric values for the entire graph and for a given node.

    :arg
    graph (nx.Graph) - a networkx graph.
    top_n (int) - the top N heroes to consider.
    **node (str) - the node to consider.
    **metric (str) - the metric to be applied. Possible metrics are: betweenness_centrality, pagerank,
    closeness_centrality, degree_centrality.

    :return
    (dict, float) - a dictionary with the metric values for the top n heroes, and the metric value for the specific node.
    """

    node, metric = kwargs.get('node'), kwargs.get('metric')

    hs = TopHeroService.create_from('data/edges.csv')
    top_heroes = hs.top_n(top_n)

    if not node:
        raise ValueError(f'The node must not be None.')

    if node not in top_heroes:
        raise ValueError(f'The node: {node} is not part of the top {top_n} heroes.')

    subgraph = nx.subgraph(graph, top_heroes)

    if metric == 'betweenness_centrality':
        metric_values = nx.betweenness_centrality(subgraph)
    elif metric == 'pagerank':
        metric_values = nx.pagerank(subgraph)
    elif metric == 'closeness_centrality':
        metric_values = nx.closeness_centrality(subgraph)
    elif metric == 'degree_centrality':
        metric_values = nx.degree_centrality(subgraph)
    else:
        raise ValueError(f'Invalid metric: {metric}.')

    # Get the metric value for the given node
    node_metric_value = metric_values[node]

    # Get the top N nodes with the most edges
    top_n_edges = sorted(subgraph.degree, key=lambda x: x[1], reverse=True)[:top_n]
    top_n_nodes = [t[0] for t in top_n_edges]

    # Filter the metric values for the top N nodes
    top_n_metric_values = {k: v for k, v in metric_values.items() if k in top_n_nodes}

    return top_n_metric_values, {node: node_metric_value}


def _edge_to_remove(graph):
    G_dict = nx.edge_betweenness_centrality(graph)
    edge = ()

    # extract the edge with highest edge betweenness centrality score
    for key, value in sorted(G_dict.items(), key=lambda item: item[1], reverse=True):
        edge = key
        break

    return edge


def _girvan_newman(graph):
    # find number of connected components
    sg = nx.connected_components(graph)
    sg_count = nx.number_connected_components(graph)

    while (sg_count == 1):
        graph.remove_edge(_edge_to_remove(graph)[0], _edge_to_remove(graph)[1])
        sg = nx.connected_components(graph)
        sg_count = nx.number_connected_components(graph)

    return sg


def extract_communities(graph: nx.Graph, top_n: int, **kwargs):
    """Cuts the given graph into separate communities.

    :arg
    graph (nx.Graph) - a networkx graph where heroes are connected to heroes.
    top_n (int) - the top n heroes to consider.
    **hero_1 (str) - the hero to be checked if it is in the same community as hero_2.
    **hero_2 (str) - the hero to be checked if it is in the same community as hero_1.

    :return
    (int, list, bool) - the lenght of the minimum cut that separates communities, the found communities, whether the
    two heroes are in the same community.
    """

    hero_1, hero_2 = kwargs.get('hero_1'), kwargs.get('hero_2')

    if not hero_1:
        raise ValueError(f'The hero_1 kwargs needs to be set.')
    if not hero_2:
        raise ValueError(f'The hero_2 kwargs needs to be set.')

    hs = TopHeroService.create_from('data/edges.csv')
    top_heroes = hs.top_n(top_n)
    
    if hero_1 not in top_heroes:
        raise ValueError(f'The provided hero_1: {hero_1} is not part of the top_n: {top_n} heroes.')

    if hero_2 not in top_heroes:
        raise ValueError(f'The provided hero_2: {hero_2} is not part of the top_n: {top_n} heroes.')

    subgraph = get_subgraph_with(graph, top_heroes, neighbours=False)

    min_cut = nx.minimum_edge_cut(subgraph)

    # Find the communities using girvan_newman function
    unf = nx.Graph(subgraph)
    communities = list(_girvan_newman(unf))

    # Check if the hero_1 and hero_2 belong to the same community
    same_community = False
    for community in communities:
        if hero_1 in community and hero_2 in community:
            same_community = True
            break

    community_1, community_2 = communities
    return Communities(min_cut, subgraph, hero_1, hero_2, community_1, community_2, same_community)
