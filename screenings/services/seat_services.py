from django.db import transaction

from screenings.dataclasses import SeatData
from screenings.models import Seat
from utils.instance_utils import get_data_instance


class SeatDataBaseService:
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
    def book_seats(cls, seats_data, screening_id, booking_id):
        for seat_data in seats_data:
            seat_id = seat_data["id"]
            # TODO cache id
            seat = cls._get_seat_by_screening_id(screening_id, seat_id)
            if seat.is_reserved == True:
                transaction.set_rollback(True)
                raise ValueError(f"Seat ID {seat_id} is not available")

            seat.is_reserved = True
            seat.booking_id = booking_id

            seat.save()


class SeatService:
    @classmethod
    def get_all_seats(cls, filters={}):
        seats = SeatDataBaseService._get_all_seats(filters=filters)
        return [get_data_instance(SeatData, seat) for seat in seats]

    @classmethod
    def get_seat_by_id(cls, seat_id):
        seat = SeatDataBaseService._get_seat_by_id(seat_id)
        return get_data_instance(SeatData, seat)

    @classmethod
    def get_available_seats(cls, screening):
        seats = SeatDataBaseService._get_available_seats(screening)
        return [get_data_instance(SeatData, seat) for seat in seats]

    @classmethod
    def get_reserved_seats(cls, screening):
        seats = SeatDataBaseService._get_reserved_seats(screening)
        return [get_data_instance(SeatData, seat) for seat in seats]

    @classmethod
    def create_seats_by_screening(cls, screening) -> list[SeatData]:
        seats = SeatDataBaseService._create_seats_by_screening(screening)
        return [get_data_instance(SeatData, seat) for seat in seats]
