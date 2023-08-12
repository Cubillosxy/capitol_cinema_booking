import pytest
from django.urls import reverse
from rest_framework import status

from cinemas.models import Cinema

pytestmark = pytest.mark.django_db


class TestCinemaListView:
    @pytest.fixture
    def url(self):
        return reverse("cinemas:cinema-list")

    def test_get_not_admin(self, api_client, cinemas, url):
        cinema1, cinema2, *_ = cinemas
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_admin(self, api_client, cinemas, url, user_admin_auth):
        cinema1, cinema2, *_ = cinemas
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert cinema1.name in str(response.data)
        assert cinema2.name in str(response.data)

    def test_get_cinema_disabled(self, api_client, cinema, url, user_admin_auth):
        cinema.is_disabled = True
        cinema.save()
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert cinema.name not in str(response.data)

    def test_post_not_admin(self, api_client, url):
        data = {"name": "New Cinema", "city": "New City"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_invalid_data(self, api_client, url, user_admin_auth):
        data = {"name": "New Cinema", "city": "New City"}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This field is required." in str(response.data)
        assert "capacity" in str(response.data)

    def test_post_valid_data(self, api_client, url, user_admin_auth):
        data = {"name": "New Cinema", "city": "New City", "capacity": 100}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]
        assert response.data["city"] == data["city"]
        assert response.data["capacity"] == data["capacity"]


class TestCinemaDetailView:
    def url(self, cinema):
        return reverse("cinemas:cinema-detail", args=[cinema.id])

    def test_get_invalid_id(self, api_client, user_admin_auth):
        url = reverse("cinemas:cinema-detail", args=[1000])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_not_admin(self, api_client, cinema):
        url = self.url(cinema)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_admin(self, api_client, cinema, user_admin_auth):
        url = self.url(cinema)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == cinema.name

    def test_edit_not_admin(self, api_client, cinema):
        url = self.url(cinema)
        data = {"name": "New Cinema", "city": "New City", "capacity": 100}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_edit_invalid_id(self, api_client, user_admin_auth):
        url = reverse("cinemas:cinema-detail", args=[1000])
        data = {"name": "New Cinema", "city": "New City", "capacity": 100}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_edit_admin(self, api_client, cinema, user_admin_auth):
        url = self.url(cinema)
        data = {"name": "New Cinema", "city": "New City", "capacity": 100}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]
        assert response.data["city"] == data["city"]
        assert response.data["capacity"] == data["capacity"]

    def test_delete_not_admin(self, api_client, cinema):
        url = self.url(cinema)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_invalid_id(self, api_client, user_admin_auth):
        url = reverse("cinemas:cinema-detail", args=[1000])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_admin(self, api_client, cinema, user_admin_auth):
        url = self.url(cinema)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Cinema.objects.filter(pk=cinema.id, is_disabled=False).exists()


"""
@pytest.mark.django_db
def test_cinema_detail_view(api_client):
    cinema = CinemaService.create_cinema({"name": "Test Cinema", "location": "Test Location"})
    url = reverse("cinema-detail", args=[cinema.id])

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == cinema.name

@pytest.mark.django_db
def test_create_cinema(api_client):
    data = {"name": "New Cinema", "location": "New Location"}
    url = reverse("cinema-list")

    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    cinema = Cinema.objects.get(pk=response.data["id"])
    assert cinema.name == data["name"]

# Similarmente, puedes escribir pruebas para la vista de edición y eliminación

# Por ejemplo, para la vista de edición
@pytest.mark.django_db
def test_update_cinema(api_client):
    cinema = CinemaService.create_cinema({"name": "Test Cinema", "location": "Test Location"})
    url = reverse("cinema-detail", args=[cinema.id])
    updated_data = {"name": "Updated Cinema", "location": "Updated Location"}

    response = api_client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK

    cinema.refresh_from_db()
    assert cinema.name == updated_data["name"]

# Y para la vista de eliminación
@pytest.mark.django_db
def test_delete_cinema(api_client):
    cinema = CinemaService.create_cinema({"name": "Test Cinema", "location": "Test Location"})
    url = reverse("cinema-detail", args=[cinema.id])

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    cinema.refresh_from_db()
    assert not cinema.is_active
"""
