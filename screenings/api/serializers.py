from rest_framework import serializers

from cinemas.api.serializers import CinemaSerializer
from movies.api.serializers import MovieSerializer

# from bookings.api.serializers import BookingSerializer


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
    id = serializers.IntegerField(read_only=True)
    screening_id = serializers.IntegerField()
    screening = ScreeningSerializer(read_only=True)
    booking_id = serializers.IntegerField(read_only=True)
    # booking = BookingSerializer(read_only=True)
    number = serializers.IntegerField()
    is_reserved = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
