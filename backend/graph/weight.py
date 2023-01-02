"""A module for functions that calculate weights between nodes in a graph."""

import networkx as nx


def reciprocal_prop(hero1, hero2, n_edges: int, graph: nx.Graph):
    """Calculates the weight of the edges between two heroes in the hero graph as an inverse proportion: 1 / n_edges.

    The more collaborations the two heroes have, the lower the weight.

    :arg
    hero1 (str) - the name of the first hero.
    hero2 (str) - the name of the second hero.
    n_edges (int) - the number of edges between the two heroes.
    graph (nx.Graph) - the graph that the heroes are part of.

    :return
    weight (float) - the weight between these two heroes.
    """

    return 1 / n_edges


def max_prop(hero1, hero2, n_edges: int, graph: nx.Graph):
    """Calculates the weight of the edges between two heroes in the hero graph as a proportion of the maximum number of
    collaborations.

    The more collaborations the two heroes have, the lower the weight.

    :arg
    hero1 (str) - the name of the first hero.
    hero2 (str) - the name of the second hero.
    n_edges (int) - the number of edges between the two heroes.
    graph (nx.Graph) - the graph that the heroes are part of.

    :return
    weight (float) - the weight between these two heroes.
    """
    if not hasattr(max_prop, 'max_collabs'):
        max_prop.max_collabs = max(map(lambda node: nx.degree(graph, node), graph.nodes()))
    return 1 - (n_edges / (max_prop.max_collabs + 1))
