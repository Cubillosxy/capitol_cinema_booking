import pytest
from django.urls import reverse
from rest_framework import status

from movies.models import Movie

pytestmark = pytest.mark.django_db


class TestMovieListView:
    @pytest.fixture
    def url(self):
        return reverse("movies:movie-list")

    def test_get_not_admin(self, api_client, movies, url):
        movie1, movie2, *_ = movies
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_admin(self, api_client, movies, url, user_admin_auth):
        movie1, movie2, *_ = movies
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert movie1.title in str(response.data)
        assert movie2.title in str(response.data)

    def test_get_movie_disabled(self, api_client, movie, url, user_admin_auth):
        movie.is_disabled = True
        movie.save()
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert movie.title not in str(response.data)

    def test_post_not_admin(self, api_client, url):
        data = {"title": "New Movie", "genre": "New Genre"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_invalid_data(self, api_client, url, user_admin_auth):
        data = {"title": "New Movie", "genre": "New Genre"}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This field is required." in str(response.data)
        assert "duration" in str(response.data)

    def test_post_valid_data(self, api_client, url, user_admin_auth):
        data = {"title": "New Movie", "genre": "New Genre", "duration": 100}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == data["title"]
        assert response.data["genre"] == data["genre"]
        assert response.data["duration"] == data["duration"]


class TestMovieDetailView:
    def url(self, movie):
        return reverse("movies:movie-detail", args=[movie.id])

    def test_get_invalid_id(self, api_client, movie, user_admin_auth):
        url = reverse("movies:movie-detail", args=[movie.id + 1])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_not_admin(self, api_client, movie):
        url = self.url(movie)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_admin(self, api_client, movie, user_admin_auth):
        url = self.url(movie)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert response.data["title"] == movie.title
        assert response.data["genre"] == movie.genre
        assert response.data["duration"] == movie.duration

    def test_put_not_admin(self, api_client, movie):
        url = self.url(movie)
        data = {"title": "New Movie", "genre": "New Genre", "duration": 100}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_put_invalid_data(self, api_client, movie, user_admin_auth):
        url = self.url(movie)
        data = {"title": "New Movie", "genre": "New Genre"}
        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This field is required." in str(response.data)
        assert "duration" in str(response.data)

    def test_put_valid_data(self, api_client, movie, user_admin_auth):
        url = self.url(movie)

        data = {"title": "New Movie", "genre": "New Genre", "duration": 100}
        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == data["title"]
        assert response.data["genre"] == data["genre"]
        assert response.data["duration"] == data["duration"]

    def test_delete_not_admin(self, api_client, movie):
        url = self.url(movie)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_valid_data(self, api_client, movie, user_admin_auth):
        url = self.url(movie)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
