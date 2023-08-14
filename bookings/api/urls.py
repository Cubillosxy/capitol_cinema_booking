from django.urls import path

from bookings.api import views

urlpatterns = [
    path(
        "<int:screening_id>/book/", views.BookingListCreateView.as_view(), name="book"
    ),
    path("<int:booking_id>/", views.BookingDetailView.as_view(), name="detail"),
    # todo detail
]

app_name = "bookings"
