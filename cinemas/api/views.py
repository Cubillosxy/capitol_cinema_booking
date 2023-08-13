from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from cinemas.api.serializers import CinemaSerializer
from cinemas.services.cinema_services import CinemaService
from screenings.api.serializers import ScreeningSerializer


class CinemaListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        cinemas = CinemaService.get_all_cinemas()
        serialized_cinemas = CinemaSerializer(cinemas, many=True).data
        return Response(serialized_cinemas)

    def post(self, request):
        serializer = CinemaSerializer(data=request.data)
        if serializer.is_valid():
            cinema = CinemaService.create_cinema(serializer.validated_data)
            serialized_cinema = CinemaSerializer(cinema).data
            return Response(serialized_cinema, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CinemaDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, cinema_id):
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        if cinema is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_cinema = CinemaSerializer(cinema).data
        return Response(serialized_cinema)

    def put(self, request, cinema_id):
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        if cinema is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CinemaSerializer(cinema, data=request.data)
        if serializer.is_valid():
            updated_cinema = CinemaService.update_cinema(
                cinema, serializer.validated_data
            )
            serialized_cinema = CinemaSerializer(updated_cinema).data
            return Response(serialized_cinema)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cinema_id):
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        if cinema is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        CinemaService.disable_cinema(cinema)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CinemaScreeningsView(APIView):
    permission_classes = []

    def get(self, request, cinema_id):
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        if cinema is None or cinema.is_disabled:
            return Response(status=status.HTTP_404_NOT_FOUND)

        screenings = CinemaService.get_cinema_screenings(cinema)
        serialized_screenings = ScreeningSerializer(screenings, many=True).data
        return Response(serialized_screenings)
