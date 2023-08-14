from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.api.serializers import BookingCreateSerializer, BookingSerializer
from bookings.providers import get_screening_by_id, validate_seats_availability
from bookings.services.booking_services import BookingService


class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, screening_id):
        screening_id = get_screening_by_id(screening_id)
        if screening_id is None:
            return Response(
                {"detail": "Screening not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            seats_data = serializer.validated_data["seats"]
            validation_errors = validate_seats_availability(seats_data)
            if validation_errors:
                return Response(
                    {"errors": validation_errors}, status=status.HTTP_400_BAD_REQUEST
                )

            booking = BookingService.create_booking(serializer.validated_data)
            serialized_booking = BookingSerializer(booking).data
            return Response(serialized_booking, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
