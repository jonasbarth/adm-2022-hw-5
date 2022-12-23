"""Module for preprocessing graph input."""
import pandas as pd


def remove_self_loops(data: pd.DataFrame):
    """Remove self loops from the data in place.

    A self loop is defined as having the same hero in both columns of the dataframe.

    :arg
    data (pd.DataFrame) - a pandas dataframe with heros.
    """
    data.drop(data.index[data.hero1 == data.hero2], inplace=True)


def replace_hero(data: pd.DataFrame, old_hero: str, new_hero: str, cols: iter = None):
    """Replaces a hero in the dataframe, in place.

    :arg
    data (pd.DataFrame) - a pandas dataframe with hero names.
    old_hero (str) - the hero name to be replaced.
    new_hero (str) - the hero name to replace.
    cols (iterable) - the columns where to replace the hero. If not specified, all columns will be considered.
    """
    if not cols:
        cols = data.columns

    for col in cols:
        data[col].loc[data[col] == old_hero] = new_hero


def strip_trailing_characters(data: pd.DataFrame, cols: iter = None):
    """Strips trailing whitespace and trailing forward slash, in place.

    :arg
    data (pd.DataFrame) - a pandas dataframe with hero data.
    cols (iterable) - the columns to strip the whitespace and forward slashes from. If not specified, all columns
    will be considered.
    """
    if not cols:
        cols = data.columns

    for col in cols:
        data[col] = data[col].apply(_strip_trailing)


def _strip_trailing(hero: str):
    hero = hero.rstrip()
    hero = hero.rstrip("/")
    return hero
