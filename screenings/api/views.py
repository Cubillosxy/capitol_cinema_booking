from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from screenings.api.serializers import ScreeningSerializer, SeatSerializer
from screenings.providers import disabled_bookings
from screenings.services.screening_service import ScreeningService
from utils.permissions import IsAdminOrReadOnly


class ScreeningCreateView(CreateAPIView):
    """
    Create a new screening


    """

    serializer_class = ScreeningSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(responses={201: "Created", 400: "Bad request"})
    def post(self, request):
        serializer = ScreeningSerializer(data=request.data)
        if serializer.is_valid():
            screening = ScreeningService.create_screening(serializer.validated_data)
            serialized_screening = ScreeningSerializer(screening).data
            return Response(serialized_screening, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScreeningSeatsView(APIView):
    """
    List Seats for a screening

    results: seats list
    """

    permission_classes = []

    @swagger_auto_schema(responses={200: "OK", 404: "Not found"})
    def get(self, request, screening_id):
        seats = ScreeningService.get_seats_by_screening_id(screening_id)
        if seats is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_seats = SeatSerializer(seats, many=True).data
        return Response(serialized_seats)


class ScreeningAPIView(APIView):
    """
    Retrieve, update or delete a screening instance.

    regular_user: read only
    admin: read, write, delete
    """

    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(responses={200: "OK", 404: "Not found"})
    def get(self, request, screening_id):
        screening = ScreeningService.get_active_screening_by_id(screening_id)
        if screening is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_screening = ScreeningSerializer(screening).data
        return Response(serialized_screening)

    @swagger_auto_schema(
        request_body=ScreeningSerializer,
        responses={200: "OK", 404: "Not found", 400: "Bad request"},
    )
    def put(self, request, screening_id):
        screening = ScreeningService.get_active_screening_by_id(screening_id)
        if screening is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ScreeningSerializer(screening, data=request.data)
        if serializer.is_valid():
            updated_screening = ScreeningService.update_screening(
                screening, serializer.validated_data
            )
            serialized_screening = ScreeningSerializer(updated_screening).data
            return Response(serialized_screening)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No content", 404: "Not found"})
    def delete(self, request, screening_id):
        screening = ScreeningService.get_active_screening_by_id(screening_id)
        if screening is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ScreeningService.disable_screening(screening)
        disabled_bookings(screening.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
