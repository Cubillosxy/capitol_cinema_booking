from django.db.models.query import QuerySet

from cinemas.dataclasses import CinemaData
from cinemas.models import Cinema
from utils.instance_utils import get_data_instance, update_model_instance


class CinemaService:
    @classmethod
    def _get_all_cinemas(
        cls, is_disabled: bool = False, filters: dict = {}
    ) -> QuerySet:
        return Cinema.objects.filter(is_disabled=is_disabled, **filters)

    @classmethod
    def _get_cinema_by_id(cls, cinema_id: int):
        return Cinema.objects.get(id=cinema_id)

    @classmethod
    def _validate_filters(cls, filters: dict):
        validation_dict = {
            "name": "name__icontains",
            "city": "city__icontains",
        }
        for key, value in filters.items():
            if key in validation_dict:
                filters[validation_dict[key]] = value
                del filters[key]
        return filters

    @classmethod
    def get_all_cinemas(cls, is_disabled: bool = False, filters: dict = {}):
        validated_filters = cls._validate_filters(filters)
        cinemas = cls._get_all_cinemas(
            is_disabled=is_disabled, filters=validated_filters
        )
        return [get_data_instance(CinemaData, cinema) for cinema in cinemas]

    @classmethod
    def get_cinema_by_id(cls, cinema_id: int) -> CinemaData | None:
        try:
            cinema = cls._get_cinema_by_id(cinema_id)
        except Cinema.DoesNotExist:
            return None
        return get_data_instance(CinemaData, cinema)

    @classmethod
    def create_cinema(cls, data: dict):
        return Cinema.objects.create(**data)

    @classmethod
    def update_cinema(cls, cinema: CinemaData, data: dict):
        cinema = cls._get_cinema_by_id(cinema.id)
        update_model_instance(cinema, data)
        cinema.refresh_from_db()
        return get_data_instance(CinemaData, cinema)

    @classmethod
    def disable_cinema(cls, cinema: CinemaData):
        cinema = cls._get_cinema_by_id(cinema.id)
        cinema.is_disabled = True
        cinema.save()
