import pytest

from screenings.tests.factories import ScreeningFactory


@pytest.fixture
def screening():
    return ScreeningFactory()


@pytest.fixture
def screenings():
    return ScreeningFactory.create_batch(10)
