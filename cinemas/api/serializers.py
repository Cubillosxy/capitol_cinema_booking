from rest_framework import serializers


class CinemaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=200)
    is_disabled = serializers.BooleanField(default=False)
    capacity = serializers.IntegerField()
    # created_at = serializers.DateTimeField(read_only=True)


class CinemaCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=200)
