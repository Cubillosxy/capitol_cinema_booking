from rest_framework import serializers

from cinemas.api.serializers import CinemaSerializer
from movies.api.serializers import MovieSerializer


class ScreeningSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    cinema_id = serializers.IntegerField()
    cinema = CinemaSerializer(read_only=True)
    movie_id = serializers.IntegerField()
    movie = MovieSerializer(read_only=True)
    date = serializers.DateTimeField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    is_disabled = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)


class SeatSerializer(serializers.Serializer):
    available_seats = serializers.IntegerField(read_only=True)
    reserved_seats = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    cinema = CinemaSerializer(read_only=True)
