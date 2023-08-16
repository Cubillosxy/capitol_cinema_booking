from unittest.mock import patch

import pytest

from screenings.services.seat_services import SeatDatabaseService

pytestmark = pytest.mark.django_db


class TestBookSeatsMethod:
    @patch("screenings.services.seat_services.acquire_lock")
    @patch("screenings.services.seat_services.release_lock")
    def test_book_seats(
        self, mock_acquire_lock, mock_release_lock, seats_and_screening, user
    ):
        mock_acquire_lock.return_value = True

        seats, screening = seats_and_screening
        seat, seat2, *_ = seats
        seats_data = [{"id": seat.id}, {"id": seat2.id}]

        booking = SeatDatabaseService._book_seats(seats_data, screening.id, user.id)

        assert mock_acquire_lock.call_count == 2
        assert mock_release_lock.call_count == 2

        seat.refresh_from_db()
        seat2.refresh_from_db()
        assert seat.is_reserved
        assert seat2.is_reserved

        assert seat.booking == booking
        assert seat2.booking == booking
