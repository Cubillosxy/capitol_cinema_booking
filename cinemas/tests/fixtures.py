import pytest
from rest_framework.test import APIClient

from cinemas.tests.factories import CinemaFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def cinema():
    return CinemaFactory()


@pytest.fixture
def cinemas():
    return [CinemaFactory() for _ in range(5)]
