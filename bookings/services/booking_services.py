from django.db.models.query import QuerySet

from bookings.dataclasses import BookingData
from bookings.models import Booking
from users.services.user_services import UserDatabaseService
from utils.instance_utils import get_data_instance


class BookingDatabaseService:
    @classmethod
    def _get_all_bookings(
        cls, is_cancelled: bool = False, filters: dict = {}
    ) -> QuerySet:
        return Booking.objects.filter(is_cancelled=is_cancelled, **filters)

    @classmethod
    def _get_booking_by_id(cls, booking_id: int) -> Booking:
        return Booking.objects.get(id=booking_id)

    @classmethod
    def _create_booking(cls, data: dict):
        return Booking.objects.create(**data)

    @classmethod
    def _booking_update(cls, filters, update_data):
        return Booking.objects.filter(**filters).update(**update_data)


class BookingService:
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
    def get_booking_by_id(cls, booking_id: int) -> BookingData | None:
        try:
            booking = BookingDatabaseService._get_booking_by_id(booking_id)
        except Booking.DoesNotExist:
            return None
        return get_data_instance(BookingData, booking)

    @classmethod
    def cancel_booking(cls, booking: BookingData):
        booking = BookingDatabaseService._get_booking_by_id(booking.id)
        booking.is_cancelled = True
        booking.save()

    @classmethod
    def disabled_bookings_by_screening_id(cls, screening_id: int):
        filters = {"screening_id": screening_id, "is_active": True}
        update_data = {"is_active": False}
        return BookingDatabaseService._booking_update(filters, update_data)

    @classmethod
    def has_booking_permission(cls, user_id: int, booking: BookingData):
        owner_admin_permission = UserDatabaseService._user_has_booking_view_permission(
            user_id
        )
        if not owner_admin_permission:
            return booking and booking.user_id == user_id
        return True
