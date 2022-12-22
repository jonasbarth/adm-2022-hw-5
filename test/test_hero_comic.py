"""Unit tests for the hero_comic module"""

from graph import hero_comic
import pytest
import networkx as nx

@pytest.fixture
def graph():
    g = nx.Graph()
    g.add_nodes_from([('Civil War', {'type': 'comic'}), ('Captain America', {'type': 'hero'})])
    g.add_edge('Civil War', 'Captain America')

    return g


def test_that_n_heroes_per_comic_correct(graph):
    heroes_per_comic, *_ = hero_comic.get_n_heroes_per_comic(graph)

    assert heroes_per_comic.name == 'Civil War'
    assert heroes_per_comic.n_heroes == 1
