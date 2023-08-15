from django.urls import path

from cinemas.api import views

urlpatterns = [
    path("", views.CinemaListCreateView.as_view(), name="cinema-list"),
    path("<int:cinema_id>/", views.CinemaDetailView.as_view(), name="cinema-detail"),
    path(
        "<int:cinema_id>/screenings/",
        views.CinemaScreeningsView.as_view(),
        name="cinema-screenings",
    ),
]

app_name = "cinemas"
