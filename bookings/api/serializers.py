from rest_framework import serializers

from screenings.api.serializers import ScreeningSerializer, SeatSerializer
from users.api.serializers import UserSerializer


class BookingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    screening_id = serializers.IntegerField()
    screening = ScreeningSerializer(read_only=True)
    user_id = serializers.IntegerField()
    user = UserSerializer(read_only=True)
    seats = SeatSerializer(many=True, read_only=True)
    is_cancelled = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class SeatBookSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class BookingCreateSerializer(serializers.Serializer):
    seats = SeatBookSerializer(many=True)
