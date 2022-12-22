"""Unit tests for the collaboration module"""
from domain.hero import Collaboration
from graph.collaborative import get_hero_collabs, create_from
import networkx as nx
import pytest

@pytest.fixture
def graph():
    return create_from('resources/test_hero-network.csv')


def test_that_hero_collabs_correct(graph):
    expected_collabs = {Collaboration('Captain America', 'Iron Man', 2), Collaboration('Black Widow', 'Iron Man', 1)}
    collabs = get_hero_collabs(graph)

    assert expected_collabs == collabs