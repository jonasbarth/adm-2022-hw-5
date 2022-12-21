"""Module for unit testing the preprocess module."""

import pytest
import pandas as pd
import numpy as np

from graph.preprocess import strip_trailing_characters, replace_hero

@pytest.fixture
def data():
    return pd.DataFrame(data=[['a ', 'b'], ['c/', 'd '], ['e', 'f']], columns=['A', 'B'])


@pytest.fixture
def heroes():
    return pd.DataFrame(data=[['Peter Parker ', 'Iron Mann'], ['Iron Mann', 'Captain America ']], columns=['Hero1', 'Hero2'])


def test_that_whitespace_removed(data):
    expected_values_col_A = ['a', 'c', 'e']
    expected_values_col_B = ['b', 'd', 'f']

    strip_trailing_characters(data, ['A', 'B'])

    assert expected_values_col_A == list(data.A.values)
    assert expected_values_col_B == list(data.B.values)


def test_that_hero_replaced(heroes):
    old_hero = 'Iron Mann'
    new_hero = 'Iron Man'
    n_old_heroes = np.sum((heroes == old_hero).values)

    replace_hero(heroes, old_hero, new_hero)
    n_new_heroes = np.sum((heroes == new_hero).values)

    assert not (heroes == old_hero).values.all()
    assert n_old_heroes == n_new_heroes
