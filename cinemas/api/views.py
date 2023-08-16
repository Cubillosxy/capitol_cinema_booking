from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from cinemas.api.serializers import CinemaSerializer
from cinemas.providers import get_cinema_screenings
from cinemas.services.cinema_services import CinemaService
from screenings.api.serializers import ScreeningSerializer


class CinemaListCreateView(APIView):
    """
    Create new cinema and list cinemas

    """

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(responses={200: CinemaSerializer(many=True)})
    def get(self, request):
        filters = request.query_params
        cinemas = CinemaService.get_all_cinemas(filters=filters)
        serialized_cinemas = CinemaSerializer(cinemas, many=True).data
        return Response(serialized_cinemas)

    @swagger_auto_schema(request_body=CinemaSerializer)
    def post(self, request):
        serializer = CinemaSerializer(data=request.data)
        if serializer.is_valid():
            cinema = CinemaService.create_cinema(serializer.validated_data)
            serialized_cinema = CinemaSerializer(cinema).data
            return Response(serialized_cinema, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(cache_page(60 * 60), name="dispatch")
class CinemaDetailView(APIView):
    """
    Get, update or delete cinema by id


    """

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(responses={200: CinemaSerializer})
    def get(self, request, cinema_id):
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        if cinema is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_cinema = CinemaSerializer(cinema).data
        return Response(serialized_cinema)

    @swagger_auto_schema(request_body=CinemaSerializer)
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
    """
    Get screenings for cinema by id
    list screenings availables in a cinema
    """

    permission_classes = []

    @swagger_auto_schema(responses={200: ScreeningSerializer(many=True)})
    def get(self, request, cinema_id):
        cinema = CinemaService.get_cinema_by_id(cinema_id)
        if cinema is None or cinema.is_disabled:
            return Response(status=status.HTTP_404_NOT_FOUND)

        screenings = get_cinema_screenings(cinema.id)
        serialized_screenings = ScreeningSerializer(screenings, many=True).data
        return Response(serialized_screenings)
