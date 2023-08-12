from django.urls import path

from cinemas.api.views import CinemaDetailView, CinemaListView

urlpatterns = [
    path("", CinemaListView.as_view(), name="cinema-list"),
    path("<int:cinema_id>/", CinemaDetailView.as_view(), name="cinema-detail"),
]

app_name = "cinemas"
