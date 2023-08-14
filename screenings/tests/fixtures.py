import pytest

from screenings.tests.factories import ScreeningFactory, SeatFactory


@pytest.fixture
def screening():
    return ScreeningFactory()


@pytest.fixture
def screenings():
    return ScreeningFactory.create_batch(10)


@pytest.fixture
def screenings_by_cinema(cinema):
    return ScreeningFactory.create_batch(10, cinema=cinema)


@pytest.fixture
def seats_and_screening(screening):
    list_seats = [
        SeatFactory(screening=screening, number=i + 1)
        for i in range(screening.cinema.capacity)
    ]
    return list_seats, screening
