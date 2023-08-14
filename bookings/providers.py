from screenings.services.screening_service import ScreeningService, SeatService


def get_screening_by_id(screening_id):
    return ScreeningService.get_active_screening_by_id(screening_id)


def validate_seats_availability(data: dict, screening_id: int):
    return SeatService.validate_seats_availability(
        seats_data=data, screening_id=screening_id
    )
