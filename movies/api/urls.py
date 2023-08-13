from django.urls import path

from movies.api.views import MovieDetailView, MovieListView

urlpatterns = [
    path("", MovieListView.as_view(), name="movie-list"),
    path("<int:movie_id>/", MovieDetailView.as_view(), name="movie-detail"),
]

app_name = "movies"
