"""Module for preprocessing graph input."""
import pandas as pd


def remove_self_loops(data: pd.DataFrame):
    """Remove self loops from the data in place.

    A self loop is defined as having the same hero in both columns of the dataframe.

    :arg
    data (pd.DataFrame) - a pandas dataframe with heros.
    """
    data.drop(data.index[data.hero1 == data.hero2], inplace=True)


def strip_trailing_characters(data: pd.DataFrame, cols: iter = None):
    """Strips trailing whitespace and trailing forward slash, in place.

    :arg
    data (pd.DataFrame) - a pandas dataframe with hero data.
    cols (iterable) - the columns to strip the whitespace and forward slashes from.
    """
    if not cols:
        cols = data.columns

    for col in cols:
        data[col] = data[col].apply(_strip_trailing)


def _strip_trailing(hero: str):
    hero = hero.rstrip()
    hero = hero.rstrip("/")
    return hero
