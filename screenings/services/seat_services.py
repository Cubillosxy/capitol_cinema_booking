from django.db import transaction

from bookings.services.booking_services import BookingDatabaseService
from screenings.dataclasses import SeatData
from screenings.models import Seat
from utils.cache import acquire_lock, release_lock
from utils.instance_utils import get_data_instance


class SeatDatabaseService:
    @classmethod
    def _get_all_seats(cls, filters={}):
        return Seat.objects.filter(**filters)

    @classmethod
    def _create_seats_by_screening(cls, screening) -> list[Seat]:
        list_of_seats = [
            Seat.objects.create(screening=screening, number=i + 1)
            for i in range(screening.cinema.capacity)
        ]
        return list_of_seats

    @classmethod
    def _get_available_seats(cls, screening):
        return cls._get_all_seats(
            filters={"screening_id": screening.id, "is_reserved": False}
        )

    @classmethod
    def _get_reserved_seats(cls, screening):
        return cls._get_all_seats(
            filters={"screening_id": screening.id, "is_reserved": True}
        )

    @classmethod
    def _get_seat_by_id(cls, seat_id):
        return Seat.objects.get(id=seat_id)

    @classmethod
    def _get_seat_by_screening_id(cls, screening_id, seat_id):
        return Seat.objects.get(screening_id=screening_id, id=seat_id)

    @classmethod
    @transaction.atomic
    def _book_seats(cls, seats_data, screening_id, user_id):
        data = {"screening_id": screening_id, "user_id": user_id}
        booking = BookingDatabaseService._create_booking(data)
        for seat_data in seats_data:
            seat_id = seat_data["id"]
            lock_id = f"lock_seat_{seat_id}"
            if not acquire_lock(lock_id):
                transaction.set_rollback(True)
                raise ValueError(f"Seat ID {seat_id} already reserved")

            seat = cls._get_seat_by_screening_id(screening_id, seat_id)

            if seat.is_reserved:
                transaction.set_rollback(True)
                release_lock(lock_id)
                raise ValueError(f"Seat ID {seat_id} is not available")

            seat.is_reserved = True
            seat.booking = booking
            seat.save()
            release_lock(lock_id)

        booking.refresh_from_db()
        return booking


class SeatService:
    @classmethod
    def get_all_seats(cls, filters={}):
        seats = SeatDatabaseService._get_all_seats(filters=filters)
        return [get_data_instance(SeatData, seat) for seat in seats]

    @classmethod
    def get_seat_by_id(cls, seat_id):
        seat = SeatDatabaseService._get_seat_by_id(seat_id)
        return get_data_instance(SeatData, seat)

    @classmethod
    def get_available_seats(cls, screening):
        seats = SeatDatabaseService._get_available_seats(screening)
        return [get_data_instance(SeatData, seat) for seat in seats]

    @classmethod
    def get_reserved_seats(cls, screening):
        seats = SeatDatabaseService._get_reserved_seats(screening)
        return [get_data_instance(SeatData, seat) for seat in seats]

    @classmethod
    def create_seats_by_screening(cls, screening) -> list[SeatData]:
        seats = SeatDatabaseService._create_seats_by_screening(screening)
        return [get_data_instance(SeatData, seat) for seat in seats]

    @classmethod
    def book_seats(
        cls, seats_data: list[SeatData], screening_id: int, user_id: int
    ) -> list[SeatData] | None:
        try:
            booking = SeatDatabaseService._book_seats(seats_data, screening_id, user_id)
            return [get_data_instance(SeatData, seat) for seat in booking.seats.all()]
        except ValueError:
            return None

    @classmethod
    def validate_seats_availability(cls, seats_data: list[SeatData], screening_id: int):
        errors = []
        for seat_data in seats_data:
            seat_id = seat_data["id"]
            try:
                seat = SeatDatabaseService._get_seat_by_screening_id(
                    screening_id=screening_id, seat_id=seat_id
                )
            except Seat.DoesNotExist:
                errors.append(f"Seat ID {seat_id} does not exist")
                continue

            if seat.is_reserved:
                errors.append(f"Seat ID {seat_id} is not available")

        return errors
