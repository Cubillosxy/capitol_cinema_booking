import pytest
from django.db.models import Model

from users.tests.factories import UserFactory


@pytest.fixture
def user() -> Model:
    return UserFactory()


@pytest.fixture
def user_admin_auth(api_client, django_user_model) -> Model:
    user = django_user_model.objects.create(
        email="admin@cinema.com", is_staff=True, password="password"
    )
    api_client.force_login(user)
    return user
