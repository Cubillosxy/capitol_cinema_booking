import pytest

from movies.tests.factories import MovieFactory


@pytest.fixture
def movie():
    return MovieFactory()


@pytest.fixture
def movies():
    return MovieFactory.create_batch(10)
