"""Unit tests for HeroSerivce class."""
import pytest

from service.hero import HeroService


@pytest.fixture
def hero_service():
    return HeroService.create_from('resources/test_edges.csv')


def test_that_top_n_are_correct(hero_service):
    expected_names = ['Captain America', 'Iron Man']

    names = list(zip(*hero_service.top_n(2)))[0]
    names = list(names)

    assert names == expected_names
