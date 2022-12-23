"""A hero service that provides information about marvel heroes."""
from collections import Counter

import pandas as pd

from backend.graph import strip_trailing_characters, replace_hero


class TopHeroService:
    """A service class that provides hero information about top heroes.

    A top hero is a hero that has appeared in many comics.
    """

    def __init__(self, heroes):
        self.heroes = heroes
        self.hero_counts = None

    @staticmethod
    def create_from(data, preprocess=True):
        """Creates the hero service from the provided data.

        The data can either be a path to a csv file, or a pandas dataframe.

        :arg
        data (str, pd.DataFrame) - the data to consider,
        preprocess (bool) - indicator of whether data should be preprocessed.

        :return
        an instance of the HeroService.
        """
        if not (isinstance(data, str) or isinstance(data, pd.DataFrame)):
            raise ValueError(f'The data must either be of type string or a pandas DataFrame. Received type: {type(data)}')
        if isinstance(data, str):
            data = pd.read_csv(data)

        if preprocess:
            strip_trailing_characters(data)
            replace_hero(data, 'SPIDER-MAN/PETER PAR', 'SPIDER-MAN/PETER PARKER')

        data = data.hero.values

        return TopHeroService(data)

    def top_n(self, n):
        """Returns the top n heroes.

        The top N heroes are those who have appeared in the most number of comics.

        :arg
        n (int) - the number of heroes.

        :return
        a list of the top n heroes.
        """
        if not self.hero_counts:
            self.hero_counts = Counter(self.heroes)

        top_n = list(zip(*self.hero_counts.most_common(n)))[0]
        return list(top_n)
