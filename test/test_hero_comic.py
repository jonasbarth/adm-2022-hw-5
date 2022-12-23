"""Unit tests for the hero_comic module"""

from backend.graph import hero_comic
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


def test_that_get_comic_nodes_correct(graph):
    expected_comics = ['Civil War']

    comics = hero_comic.get_comic_nodes(graph)

    assert comics == expected_comics
