import pytest

from screenings.tests.factories import ScreeningFactory


@pytest.fixture
def screening():
    return ScreeningFactory()


@pytest.fixture
def screenings():
    return ScreeningFactory.create_batch(10)


@pytest.fixture
def screenings_by_cinema(cinema):
    return ScreeningFactory.create_batch(10, cinema=cinema)
