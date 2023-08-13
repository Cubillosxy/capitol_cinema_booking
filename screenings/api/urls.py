from django.urls import path

from screenings.api import views

urlpatterns = [
    path("", views.ScreeningCreateView.as_view(), name="screening-create"),
    path(
        "<int:screening_id>/", views.ScreeningAPIView.as_view(), name="screening-detail"
    ),
    path(
        "<int:screening_id>/seats/",
        views.ScreeningSeatsView.as_view(),
        name="screening-seats",
    ),
]

app_name = "screenings"
