import pytest

pytestmark = pytest.mark.django_db


class TestScreeningModel:
    def test_str(self, screening):
        assert (
            str(screening) == f"{screening.movie} {screening.cinema} {screening.date}"
        )

    def test_is_disabled(self, screening):
        assert not screening.is_disabled

    def test_created_at(self, screening):
        assert screening.created_at
