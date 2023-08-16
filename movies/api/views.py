from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from movies.api.serializers import MovieSerializer
from movies.services.movie_services import MovieService
from utils.permissions import IsAdminOrReadOnly


class MovieListCreate(APIView):
    """
    List movies or create a new movie

    get: List all movies
    post: Create a new movie
    """

    permission_classes = [IsAdminUser]
    serializer_class = MovieSerializer

    def get(self, request):
        movies = MovieService.get_all_movies()
        # TODO: paginate
        serialized_movies = MovieSerializer(movies, many=True).data
        return Response(serialized_movies)

    @swagger_auto_schema(request_body=MovieSerializer)
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = MovieService.create_movie(serializer.validated_data)
            serialized_movie = MovieSerializer(movie).data
            return Response(serialized_movie, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    """
    Retrieve, update or delete a movie
    get: regular user
    put-delete: admin user
    """

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, movie_id):
        movie = MovieService.get_movie_by_id(movie_id)
        if movie is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_movie = MovieSerializer(movie).data
        return Response(serialized_movie)

    @swagger_auto_schema(request_body=MovieSerializer)
    def put(self, request, movie_id):
        movie = MovieService.get_movie_by_id(movie_id)
        if movie is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            updated_movie = MovieService.update_movie(movie, serializer.validated_data)
            serialized_movie = MovieSerializer(updated_movie).data
            return Response(serialized_movie)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id):
        movie = MovieService.get_movie_by_id(movie_id)
        if movie is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        MovieService.disable_movie(movie)
        return Response(status=status.HTTP_204_NO_CONTENT)
