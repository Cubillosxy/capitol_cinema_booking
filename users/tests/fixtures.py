import pytest
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from users.tests.factories import Permission, UserFactory


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


@pytest.fixture
def user_owner_auth(api_client, django_user_model) -> Model:
    user = django_user_model.objects.create(
        email="owner@cinema.com", password="password"
    )
    permission = Permission(
        codename="can_view_bookings",
        content_type=ContentType.objects.get_for_model(django_user_model),
    )
    user.user_permissions.add(permission)
    api_client.force_login(user)
    return user
