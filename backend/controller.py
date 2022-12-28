"""A controller module for the Marvel Hero graph."""

import networkx as nx

from .manager import features, shortest_ordered_route, disconnecting_graphs


class Controller:
    """The controller class is the main interface for the user to run methods on marvel graphs."""

    def __init__(self, graph: nx.Graph):
        """Initialises the Controller.

        :arg
        graph (nx.Graph) - the graph that this controller will operate on.
        """
        self.graph = graph
        self.funcs = {features.__name__: features,
                      shortest_ordered_route.__name__: shortest_ordered_route,
                      disconnecting_graphs.__name__: disconnecting_graphs}

    def run(self, identifier: str, top_n: int, **kwargs):
        """Runs the function that maps to the specific identifier on the graph of this controller.

        :arg
        identifier (str) - the name of the function to be run.
        **kwargs - keyword arguments that depend on the identifier that is provided. For example, <features> expects to
        find graph_type in the **kwargs.

        :return
        the result of the function that was run.
        """
        if identifier not in self.funcs:
            raise ValueError(f'The identifier {identifier} does not map to an existing function.')

        return self.funcs[identifier](self.graph, top_n, **kwargs)
