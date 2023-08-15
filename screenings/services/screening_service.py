from django.core.cache import cache

from screenings.dataclasses import ScreeningData
from screenings.models import Screening
from screenings.services.seat_services import SeatService
from utils.instance_utils import get_data_instance, update_model_instance


class ScreeningService:
    timeout_1_hour = 60 * 60

    @classmethod
    def _get_all_screenings(cls, filters={}):
        return Screening.objects.filter(**filters)

    @classmethod
    def get_all_screenings(cls, filters={}):
        cache_key = "".join([f"{key}_{value}" for key, value in filters.items()])

        screening_data = cache.get(cache_key)
        if not screening_data:
            screenings = cls._get_all_screenings(filters=filters)
            screening_data = [
                get_data_instance(ScreeningData, screening) for screening in screenings
            ]
            cache.set(cache_key, screening_data, timeout=cls.timeout_1_hour)
        return screening_data

    @classmethod
    def _get_screening_by_id(cls, screening_id):
        return Screening.objects.get(id=screening_id)

    @classmethod
    def _get_active_screening_by_id(cls, screening_id) -> ScreeningData | None:
        try:
            screening = cls._get_screening_by_id(screening_id)
            if screening.is_disabled:
                return None
        except Screening.DoesNotExist:
            return None
        return screening

    @classmethod
    def get_active_screening_by_id(cls, screening_id) -> ScreeningData | None:
        screening = cls._get_active_screening_by_id(screening_id)
        return get_data_instance(ScreeningData, screening) if screening else None

    @classmethod
    def get_seats_by_screening_id(cls, screening_id) -> list[object] | None:
        screening = cls._get_active_screening_by_id(screening_id)
        if screening is None:
            return None
        return SeatService.get_available_seats(screening)

    @classmethod
    def _create_screening(cls, data):
        return Screening.objects.create(**data)

    @classmethod
    def create_screening(cls, data):
        screening = cls._create_screening(data)
        SeatService.create_seats_by_screening(screening)
        return get_data_instance(ScreeningData, screening)

    @classmethod
    def update_screening(cls, screening, data):
        screening = cls._get_screening_by_id(screening.id)
        update_model_instance(screening, data)
        screening.refresh_from_db()
        return get_data_instance(ScreeningData, screening)

    @classmethod
    def disable_screening(cls, screening):
        screening = cls._get_screening_by_id(screening.id)
        screening.is_disabled = True
        screening.save()
