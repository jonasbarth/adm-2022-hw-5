"""A hero service that provides information about marvel heroes."""
from collections import Counter

import pandas as pd


class HeroService:
    """A service class that provides hero information."""

    def __init__(self, edges):
        self.edges = edges

    @staticmethod
    def create_from(edges):
        """Creates the hero service from the provided edges.

        Edges can either be a path to a csv file, or a pandas dataframe.

        :arg
        edges (str, pd.DataFrame) - the edges to consider.
        """
        if not (isinstance(edges, str) or isinstance(edges, pd.DataFrame)):
            raise ValueError(f'The edges must either be of type string or a pandas DataFrame. Received type: {type(edges)}')
        if isinstance(edges, str):
            edges = pd.read_csv(edges)

        return HeroService(edges)

    def top_n(self, n):
        """Returns the top n heroes.

        The top N heroes are those who have appeared in the most number of comics.

        :arg
        n (int) - the number of heroes.

        :return
        a set of the top n heroes.
        """
        return Counter(self.edges.hero.values).most_common(n)
