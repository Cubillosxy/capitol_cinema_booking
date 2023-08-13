from screenings.services.screening_service import ScreeningService


def get_cinema_screenings(cinema_id: int):
    filters = {"cinema_id": cinema_id, "is_disabled": False}
    return ScreeningService.get_all_screenings(filters=filters)
