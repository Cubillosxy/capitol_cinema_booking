import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestLoginView:
    def url(self):
        return reverse("users:user-login")

    def test_post_valid_data(self, api_client, user):
        url = self.url()
        data = {
            "username": user.email,
            "password": "password",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "successfully" in str(response.data)

    def test_post_invalid_username(self, api_client, user):
        url = self.url()
        data = {
            "username": user.username,
            "password": "password",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "blank" in str(response.data)

    def test_post_invalid_password(self, api_client, user):
        url = self.url()
        data = {
            "username": user.email,
            "password": "wrong_password",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid Credentials" in response.data["error"]


class TestRegisterView:
    def url(self):
        return reverse("users:user-register")

    def test_post_valid_data(self, api_client):
        url = self.url()
        data = {
            "username": "test_email@gmail.com",
            "password": "password",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_invalid_email(self, api_client):
        url = self.url()
        data = {
            "username": "test_email",
            "password": "password",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "invalid" in str(response.data)


class TestDetailView:
    def url(self, user_id):
        return reverse("users:detail-detail", args=[user_id])

    def test_get_user_detail(self, api_client, user):
        url = self.url(user.id)
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user_detail_unauthorized(self, api_client, user):
        url = self.url(user.id)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user_detail_admin(self, api_client, user_admin_auth, user):
        url = self.url(user.id)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email


class TestPermissionView:
    def url(self, user_id):
        return reverse("users:detail-set-owner-permissions", args=[user_id])

    def test_set_permissions_unauthorized(self, api_client):
        url = self.url(3)
        response = api_client.post(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_set_permission(
        self, api_client, user_admin_auth, user, group_book_permission
    ):
        url = self.url(user.id)
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
