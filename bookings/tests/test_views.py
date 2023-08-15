import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestCreateView:
    def url(self, screening_id):
        return reverse("bookings:book", args=[screening_id])

    def test_post_not_authenticated(self, api_client, screening):
        url = self.url(screening.id)
        data = {"screening_id": 1}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_invalid_data(self, api_client, user, screening):
        api_client.force_login(user)
        url = self.url(screening.id)
        data = {"screening_id": 1}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_invalid_screening_id(self, api_client, user, screening):
        api_client.force_login(user)
        url = self.url(screening.id + 1)
        data = {"screening_id": screening.id + 1}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_invalid_seat_id(self, api_client, user, screening):
        api_client.force_login(user)
        url = self.url(screening.id)
        data = {
            "seats": [
                {
                    "id": 10232,
                }
            ]
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "does not exist" in str(response.data["errors"])

    def test_post_seat_is_reserved(self, api_client, user, seats_and_screening):
        seats, screening = seats_and_screening
        seat, *_ = seats
        seat.is_reserved = True
        seat.save()

        api_client.force_login(user)
        url = self.url(screening.id)
        data = {
            "seats": [
                {
                    "id": seat.id,
                }
            ]
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "is not available" in str(response.data["errors"])

    def test_post_seat_partial_reserved(self, api_client, user, seats_and_screening):
        seats, screening = seats_and_screening
        seat, seat2, *_ = seats
        seat.is_reserved = True
        seat.save()

        seats_list = [{"id": seat.id}, {"id": seat2.id}]

        api_client.force_login(user)
        url = self.url(screening.id)
        data = {"seats": seats_list}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "is not available" in str(response.data["errors"])

    def test_post_seat_reserved_ok(self, api_client, user, seats_and_screening):
        seats, screening = seats_and_screening
        seat, seat2, *_ = seats

        seats_list = [{"id": seat.id}, {"id": seat2.id}]

        api_client.force_login(user)
        url = self.url(screening.id)
        data = {"seats": seats_list}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data[1]["booking_id"] == response.data[0]["booking_id"]
        assert response.data[0]["is_reserved"] is True


class TestDetailView:
    def url(self, booking_id):
        return reverse("bookings:detail", args=[booking_id])

    def test_get_not_authenticated(self, api_client, booking):
        url = self.url(booking.id)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_not_owner(self, api_client, booking, user):
        api_client.force_login(user)
        url = self.url(booking.id)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_owner(self, api_client, booking):
        api_client.force_login(booking.user)
        url = self.url(booking.id)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == booking.id
        assert response.data["user"]["id"] == booking.user.id

    def test_get_owner_admin(self, api_client, booking, user_owner_auth):
        url = self.url(booking.id)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == booking.id
        assert response.data["user"]["id"] == booking.user.id

    def test_get_owner_admin_not_found(self, api_client, booking, user_owner_auth):
        url = self.url(booking.id + 2)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cancel_not_owner(self, api_client, booking, user):
        api_client.force_login(user)
        url = self.url(booking.id)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_cancel_owner(self, api_client, booking):
        api_client.force_login(booking.user)
        url = self.url(booking.id)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
