from movies.dataclasses import MovieData
from movies.models import Movie
from utils.instance_utils import get_data_instance, update_model_instance


class MovieService:
    @classmethod
    def _get_all_movies(cls, is_disabled=False):
        return Movie.objects.filter(is_disabled=is_disabled)

    @classmethod
    def _get_movie_by_id(cls, movie_id):
        return Movie.objects.get(id=movie_id)

    @classmethod
    def get_all_movies(cls, is_disabled=False):
        movies = cls._get_all_movies(is_disabled=is_disabled)
        return [get_data_instance(MovieData, movie) for movie in movies]

    @classmethod
    def get_movie_by_id(cls, movie_id) -> MovieData | None:
        try:
            movie = cls._get_movie_by_id(movie_id)
        except Movie.DoesNotExist:
            return None
        return get_data_instance(MovieData, movie)

    @classmethod
    def create_movie(cls, data):
        return Movie.objects.create(**data)

    @classmethod
    def update_movie(cls, movie, data):
        movie = cls._get_movie_by_id(movie.id)
        update_model_instance(movie, data)
        movie.refresh_from_db()
        return get_data_instance(MovieData, movie)

    @classmethod
    def disable_movie(cls, movie):
        movie = cls._get_movie_by_id(movie.id)
        movie.is_disabled = True
        movie.save()
