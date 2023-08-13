from screenings.dataclasses import ScreeningData
from screenings.models import Screening
from utils.instance_utils import get_data_instance, update_model_instance


class ScreeningService:
    @classmethod
    def _get_all_screenings(cls, filters={}):
        return Screening.objects.filter(**filters)

    @classmethod
    def get_all_screenings(cls, filters={}):
        screenings = cls._get_all_screenings(filters=filters)
        return [get_data_instance(ScreeningData, screening) for screening in screenings]

    @classmethod
    def _get_screening_by_id(cls, screening_id):
        return Screening.objects.get(id=screening_id)

    @classmethod
    def get_screening_by_id(cls, screening_id) -> ScreeningData | None:
        try:
            screening = cls._get_screening_by_id(screening_id)
        except Screening.DoesNotExist:
            return None
        return get_data_instance(ScreeningData, screening)

    @classmethod
    def create_screening(cls, data):
        return Screening.objects.create(**data)

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
