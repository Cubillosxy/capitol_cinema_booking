from bookings.services.booking_services import BookingService


def disabled_bookings(screening_id: int):
    return BookingService.disabled_bookings_by_screening_id(screening_id)
