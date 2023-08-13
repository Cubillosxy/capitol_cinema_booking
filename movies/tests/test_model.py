import pytest

pytestmark = pytest.mark.django_db


class TestMovieModel:
    def test_str(self, movie):
        assert str(movie) == f"{movie.title} {movie.genre} {movie.duration}"

    def test_is_disabled(self, movie):
        assert not movie.is_disabled

    def test_created_at(self, movie):
        assert movie.created_at
