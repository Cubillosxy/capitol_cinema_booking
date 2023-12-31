from django.core.cache import cache

from movies.dataclasses import MovieData
from movies.models import Movie
from utils.instance_utils import get_data_instance, update_model_instance


class MovieService:
    timeout_12_hours = 60 * 60 * 12

    @classmethod
    def _get_all_movies(cls, is_disabled=False):
        return Movie.objects.filter(is_disabled=is_disabled)

    @classmethod
    def _get_movie_by_id(cls, movie_id):
        return Movie.objects.get(id=movie_id)

    @classmethod
    def get_all_movies(cls, is_disabled=False):
        cache_key = f"movies_{is_disabled}"
        movies_data = cache.get(cache_key)
        if not movies_data:
            movies = cls._get_all_movies(is_disabled=is_disabled)
            movies_data = [get_data_instance(MovieData, movie) for movie in movies]
            cache.set(cache_key, movies_data, timeout=cls.timeout_12_hours)

        return movies_data

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
