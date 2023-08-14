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
