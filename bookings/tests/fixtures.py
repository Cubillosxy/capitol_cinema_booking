import pytest

from bookings.tests.factories import BookingFactory


@pytest.fixture
def booking():
    return BookingFactory()
