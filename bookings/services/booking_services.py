from django.db.models.query import QuerySet

from bookings.dataclasses import BookingData
from bookings.models import Booking
from utils.instance_utils import get_data_instance, update_model_instance


class BookingService:
    @classmethod
    def _get_all_bookings(
        cls, is_cancelled: bool = False, filters: dict = {}
    ) -> QuerySet:
        return Booking.objects.filter(is_cancelled=is_cancelled, **filters)

    @classmethod
    def _get_booking_by_id(cls, booking_id: int) -> Booking:
        return Booking.objects.get(id=booking_id)

    @classmethod
    def _validate_filters(cls, filters: dict) -> dict:
        validation_dict = {
            "user_id": "user_id",
            "screening_id": "screening_id",
        }
        for key, value in filters.items():
            if key in validation_dict:
                filters[validation_dict[key]] = value
                del filters[key]
        return filters

    @classmethod
    def get_all_bookings(
        cls, is_cancelled: bool = False, filters: dict = {}
    ) -> list[BookingData]:
        validated_filters = cls._validate_filters(filters)
        bookings = cls._get_all_bookings(
            is_cancelled=is_cancelled, filters=validated_filters
        )
        return [get_data_instance(BookingData, booking) for booking in bookings]

    @classmethod
    def get_booking_by_id(cls, booking_id: int) -> BookingData | None:
        try:
            booking = cls._get_booking_by_id(booking_id)
        except Booking.DoesNotExist:
            return None
        return get_data_instance(BookingData, booking)

    @classmethod
    def create_booking(cls, data: dict):
        return Booking.objects.create(**data)

    @classmethod
    def update_booking(cls, booking: BookingData, data: dict):
        booking = cls._get_booking_by_id(booking.id)
        update_model_instance(booking, data)
        booking.refresh_from_db()
        return get_data_instance(BookingData, booking)

    @classmethod
    def cancel_booking(cls, booking: BookingData):
        booking = cls._get_booking_by_id(booking.id)
        booking.is_cancelled = True
        booking.save()

    @classmethod
    def disabled_bookings_by_screening_id(cls, screening_id: int):
        return Booking.objects.filter(screening_id=screening_id, is_active=True).update(
            is_active=False
        )
