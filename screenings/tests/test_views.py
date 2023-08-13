import pytest
from django.urls import reverse
from rest_framework import status

from screenings.models import Screening

pytestmark = pytest.mark.django_db


class TestScreeningCreateView:
    @pytest.fixture
    def url(self):
        return reverse("screenings:screening-create")

    def test_post_not_admin(self, api_client, url):
        data = {"movie": 1, "cinema": 1, "date": "2023-08-15 08:00:00", "price": 8.0}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_invalid_data(self, api_client, url, user_admin_auth):
        data = {"movie": 2, "cinema": 3, "price": 8}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This field is required." in str(response.data)
        assert "date" in str(response.data)

    def test_post_valid_data(self, api_client, url, movie, cinema, user_admin_auth):
        data = {
            "movie_id": movie.id,
            "cinema_id": cinema.id,
            "date": "2023-08-15 08:00:00",
            "price": 8,
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        # assert response.data["movie"]["id"] == data["movie"]
        # assert response.data["cinema"]["id"] == data["cinema"]
        assert response.data["available_seats"] == cinema.capacity
        assert float(response.data["price"]) == float(data["price"])


class TestScreeningDetailView:
    def url(self, screening):
        return reverse("screenings:screening-detail", args=[screening.id])

    def test_get_invalid_id(self, api_client, screening, user_admin_auth):
        url = reverse("screenings:screening-detail", args=[screening.id + 1])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_not_admin(self, api_client, screening):
        url = self.url(screening)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_admin(self, api_client, screening, user_admin_auth):
        url = self.url(screening)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert response.data["movie_id"] == screening.movie.id
        assert response.data["cinema_id"] == screening.cinema.id
        assert response.data["available_seats"] == screening.cinema.capacity
        assert float(response.data["price"]) == float(screening.price)

    def test_edit_invalid_id(self, api_client, screening, user_admin_auth):
        url = reverse("screenings:screening-detail", args=[screening.id + 1])
        response = api_client.put(url, {})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_edit_not_admin(self, api_client, screening):
        url = self.url(screening)
        response = api_client.put(url, {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_edit_invalid_data(self, api_client, screening, user_admin_auth):
        url = self.url(screening)
        data = {"movie": 2, "cinema": 3, "price": 8}
        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This field is required." in str(response.data)
        assert "date" in str(response.data)

    def test_put_valid_data(self, api_client, screening, user_admin_auth):
        url = self.url(screening)
        data = {
            "movie_id": screening.movie.id,
            "cinema_id": screening.cinema.id,
            "date": "2023-08-15 08:00:00",
            "price": 8,
        }
        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["movie"]["id"] == data["movie_id"]
        assert response.data["cinema_id"] == data["cinema_id"]
        assert response.data["available_seats"] == screening.cinema.capacity
        assert float(response.data["price"]) == float(data["price"])

    def test_delete_not_admin(self, api_client, screening):
        url = self.url(screening)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_invalid_id(self, api_client, screening, user_admin_auth):
        url = reverse("screenings:screening-detail", args=[screening.id + 1])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_valid_data(self, api_client, screening, user_admin_auth):
        url = self.url(screening)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Screening.objects.filter(is_disabled=False).count() == 0
