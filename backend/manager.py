"""This module is the central entry point to all backend functionalities."""

import networkx as nx
import numpy as np
import pandas as pd

from backend.graph import get_n_heroes_per_comic, get_subgraph_with, get_hero_collabs
from backend.service import TopHeroService
from .describe import GraphType, GraphFeatures, get_degree_dist, get_hubs, get_graph_mode
from .domain import Disconnection, Communities

hero_service = None

def create_hero_service(data, preprocess=True):
    global hero_service
    hero_service = TopHeroService.create_from(data, preprocess)

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

    global hero_service
    if not hero_service:
        raise ValueError(f'The hero service must be created before calling any function.')

    top_heroes = hero_service.top_n(top_n)

    if graph_type == GraphType.COLLABORATIVE:
        subgraph = graph.subgraph(top_heroes)
        hero_collabs = get_hero_collabs(subgraph)

    elif graph_type == GraphType.HERO_COMIC:
        subgraph = get_subgraph_with(graph, top_heroes)
        n_heroes_per_comic = get_n_heroes_per_comic(subgraph)

    n_nodes = len(subgraph.nodes())
    density = nx.density(subgraph)
    degree_dist = get_degree_dist(subgraph)

    avg_degree = sum(map(lambda node: subgraph.degree(node), subgraph.nodes)) / n_nodes

    hubs = get_hubs(subgraph, 95)

    graph_mode = get_graph_mode(subgraph)

    return GraphFeatures(graph_type, n_nodes, hero_collabs, n_heroes_per_comic, density, degree_dist, avg_degree, hubs,
                         graph_mode)


def shortest_order_route(graph: nx.Graph, N: int, **kwargs):

    initial_hero = kwargs.get('initial_hero')
    final_hero = kwargs.get('final_hero')
    superheroes = kwargs.get('superheroes')
    hero_comic = kwargs.get('hero_comic')  # path of the .csv file

    hero_comic = pd.read_csv(hero_comic)

    top_heroes = pd.DataFrame(hero_comic.groupby(['hero'])['hero'].count()).rename(columns={'hero':'Total_Appearances'}).sort_values('Total_Appearances', ascending = False)

    def top_N(data, N):
        return data[0:N-1]


    if initial_hero == final_hero:
          return('You are already there!')

    # First of all, we initialize the list which will contain the shortes path
    path = []

    # Second, we have to focus on the top N nodes in the graph.
    # To do it, we first remove the nodes (and the edges, of course) that are not in the top-N nodes
    subg = get_subgraph_with(graph, list(top_N(top_heroes, N).index))

    #if len(superheroes) == 0:
          #return(nx.bidirectional_shortest_path(subg, initial_hero, final_hero))

    # Now we want to create a list containing all the superheroes we have to visit, inlcluding the starting one and the ending one
    superheroes.insert(0, initial_hero)
    superheroes.append(final_hero)

    # Now, we compute the shortest path between the first and the second, then between the second and the third, and so on,
    # until we visit (in order) all the nodes contained in the original list given as input
    for h in range(len(superheroes) - 1):
        try:
            if superheroes[h] not in subg.nodes():
                return('WARNING: this here is not in the graph! Try to change N or check if the spelling is correct')

            a = nx.bidirectional_shortest_path(subg, superheroes[h], superheroes[h+1])
            if len(a) == 0:
                return("WARNING: There is no such path!")
            path.append(a)
            
        except:
            print('Sorry, there is no such path...') 
            return   

    return(path)  

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
    (int, float), (str, float) - a tuple with the mean metric value for the top n heroes, anda tuple the metric value
    for the specific node.
    """

    node, metric = kwargs.get('node'), kwargs.get('metric')

    global hero_service
    if not hero_service:
        raise ValueError(f'The hero service must be created before calling any function.')

    top_heroes = hero_service.top_n(top_n)

    if not node:
        raise ValueError(f'The node must not be None.')

    if node not in top_heroes:
        raise ValueError(f'The node: {node} is not part of the top {top_n} heroes.')

    subgraph = nx.subgraph(graph, top_heroes)

    if metric == 'betweenness_centrality':
        metric_values = nx.betweenness_centrality(subgraph)
    elif metric == 'pagerank':
        metric_values = nx.pagerank_numpy(subgraph)
    elif metric == 'closeness_centrality':
        metric_values = nx.closeness_centrality(subgraph)
    elif metric == 'degree_centrality':
        metric_values = nx.degree_centrality(subgraph)
    else:
        raise ValueError(f'Invalid metric: {metric}.')

    # Get the metric value for the given node
    node_metric_value = metric_values[node]

    # Get the average metric value
    mean_metric = np.array(list(metric_values.values())).mean()

    return (top_n, mean_metric), (node, node_metric_value)


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

    global hero_service
    if not hero_service:
        raise ValueError(f'The hero service must be created before calling any function.')

    top_heroes = hero_service.top_n(top_n)

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
