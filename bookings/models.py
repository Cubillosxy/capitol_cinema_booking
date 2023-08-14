from django.db import models


class Booking(models.Model):
    screening = models.ForeignKey(
        "screenings.Screening",
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    is_cancelled = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True, help_text="Is the booking active?, False if screening played"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.screening} {self.user}"
