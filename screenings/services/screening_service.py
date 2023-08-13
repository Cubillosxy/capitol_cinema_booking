from cinemas.services.cinema_services import CinemaService
from movies.services.movie_services import MovieService
from screenings.dataclasses import ScreeningData
from screenings.models import Screening
from utils import get_data_instance, update_model_instance


class ScreeningService:
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
