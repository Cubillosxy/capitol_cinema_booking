import pytest

pytestmark = pytest.mark.django_db


class TestCinemaModel:
    def test_str(self, cinema):
        assert str(cinema) == f"{cinema.name} {cinema.city} {cinema.address}"

    def test_is_disabled(self, cinema):
        assert not cinema.is_disabled

    def test_created_at(self, cinema):
        assert cinema.created_at

    def test_capacity(self, cinema):
        assert cinema.capacity
