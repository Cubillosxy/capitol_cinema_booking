from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    genre = serializers.CharField(max_length=200)
    duration = serializers.IntegerField()
    is_disabled = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
