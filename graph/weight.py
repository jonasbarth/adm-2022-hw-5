"""A module for functions that calculate weights between nodes in a graph."""


def inverse_prop(hero1, hero2, n_edges):
    """Calculates the weight of the edges between two heroes in the hero graph as an inverse proportion: 1 / n_edges.

    The more collaborations the two heros have, the lower the weight.

    :arg
    hero1 (str) - the name of the first hero.
    hero2 (str) - the name of the second hero.
    n_edges (int) - the number of edges between the two heroes.

    :return
    weight (float) - the weight between these two heroes.
    """

    return 1 / n_edges
