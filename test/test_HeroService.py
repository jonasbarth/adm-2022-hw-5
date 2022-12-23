"""Unit tests for HeroSerivce class."""
import pytest

from backend.service import TopHeroService


@pytest.fixture
def hero_service():
    return TopHeroService.create_from('resources/test_edges.csv')


def test_that_top_n_are_correct(hero_service):
    expected_names = ['Captain America', 'Iron Man']

    names = hero_service.top_n(2)

    assert names == expected_names
