from django.urls import path

from screenings.api.views import ScreeningAPIView, ScreeningCreateView

urlpatterns = [
    path("", ScreeningCreateView.as_view(), name="screening-create"),
    path("<int:screening_id>/", ScreeningAPIView.as_view(), name="screening-detail"),
]

app_name = "screenings"
