from django.urls import path

from screenings.api.views import ScreeningCreateView, ScreeningDetailView

urlpatterns = [
    path("", ScreeningCreateView.as_view(), name="screening-create"),
    path("<int:screening_id>/", ScreeningDetailView.as_view(), name="screening-detail"),
]

app_name = "screenings"
