from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.api.serializers import MovieSerializer
from movies.services.movie_services import MovieService


class MovieListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        movies = MovieService.get_all_movies()
        serialized_movies = MovieSerializer(movies, many=True).data
        return Response(serialized_movies)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = MovieService.create_movie(serializer.validated_data)
            serialized_movie = MovieSerializer(movie).data
            return Response(serialized_movie, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, movie_id):
        movie = MovieService.get_movie_by_id(movie_id)
        if movie is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized_movie = MovieSerializer(movie).data
        return Response(serialized_movie)

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
