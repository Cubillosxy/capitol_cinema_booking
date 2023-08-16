from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from bookings.api.serializers import (
    BookingCreateSerializer,
    BookingSerializer,
    SeatBookSerializer,
)
from bookings.providers import (
    book_seats,
    get_screening_by_id,
    validate_seats_availability,
)
from bookings.services.booking_services import BookingService


class BookingCreateView(APIView):
    """
    Create a booking for a screening.

    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BookingCreateSerializer,
        responses={201: SeatBookSerializer(many=True)},
    )
    def post(self, request, screening_id):
        screening = get_screening_by_id(screening_id)
        if screening is None:
            return Response(
                {"detail": "Screening not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            seats_data = serializer.validated_data["seats"]
            validation_errors = validate_seats_availability(seats_data, screening_id)
            if validation_errors:
                return Response(
                    {"errors": validation_errors}, status=status.HTTP_400_BAD_REQUEST
                )
            seats = book_seats(seats_data, screening_id, request.user.id)
            serialized_booking = SeatBookSerializer(seats, many=True).data
            return Response(serialized_booking, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDetailView(APIView):
    """
    Retrieve or delete a booking.

    get: retrieve a booking.
    delete: cinema owner or admin can cancel a booking.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: BookingSerializer})
    def get(self, request, booking_id):
        booking = BookingService.get_booking_by_id(booking_id)
        if not BookingService.has_booking_permission(
            user_id=request.user.id, booking=booking
        ):
            return Response(
                {"detail": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if booking is None:
            return Response(
                {"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serialized_booking = BookingSerializer(booking).data
        return Response(serialized_booking)

    def delete(self, request, booking_id):
        booking = BookingService.get_booking_by_id(booking_id)
        if not BookingService.has_booking_permission(
            user_id=request.user.id, booking=booking
        ):
            return Response(
                {"detail": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if booking is None:
            return Response(
                {"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )
        BookingService.cancel_booking(booking)
        return Response(status=status.HTTP_204_NO_CONTENT)
