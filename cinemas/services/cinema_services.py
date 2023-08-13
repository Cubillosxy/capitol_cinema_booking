from cinemas.dataclasses import CinemaData
from cinemas.models import Cinema
from utils import get_data_instance, update_model_instance


class CinemaService:
    @classmethod
    def _get_all_cinemas(cls, is_disabled=False):
        return Cinema.objects.filter(is_disabled=is_disabled)

    @classmethod
    def _get_cinema_by_id(cls, cinema_id):
        return Cinema.objects.get(id=cinema_id)

    @classmethod
    def get_all_cinemas(cls, is_disabled=False):
        cinemas = cls._get_all_cinemas(is_disabled=is_disabled)
        return [get_data_instance(CinemaData, cinema) for cinema in cinemas]

    @classmethod
    def get_cinema_by_id(cls, cinema_id) -> CinemaData | None:
        try:
            cinema = cls._get_cinema_by_id(cinema_id)
        except Cinema.DoesNotExist:
            return None
        return get_data_instance(CinemaData, cinema)

    @classmethod
    def create_cinema(cls, data):
        return Cinema.objects.create(**data)

    @classmethod
    def update_cinema(cls, cinema, data):
        cinema = cls._get_cinema_by_id(cinema.id)
        update_model_instance(cinema, data)
        cinema.refresh_from_db()
        return get_data_instance(CinemaData, cinema)

    @classmethod
    def disable_cinema(cls, cinema):
        cinema = cls._get_cinema_by_id(cinema.id)
        cinema.is_disabled = True
        cinema.save()
