"""Module for preprocessing graph input."""
import pandas as pd


def remove_self_loops(data: pd.DataFrame):
    """Remove self loops from the data in place.

    A self loop is defined as having the same hero in both columns of the dataframe.

    :arg
    data (pd.DataFrame) - a pandas dataframe with heros.
    """
    data.drop(data.index[data.hero1 == data.hero2], inplace=True)