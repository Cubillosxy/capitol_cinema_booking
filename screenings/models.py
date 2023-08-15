from django.db import models


class Screening(models.Model):
    movie = models.ForeignKey("movies.Movie", on_delete=models.PROTECT)
    cinema = models.ForeignKey("cinemas.Cinema", on_delete=models.PROTECT)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_dubbed = models.BooleanField(default=False)
    is_subtitled = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.movie} {self.cinema} {self.date}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        super().save(*args, **kwargs)

    @property
    def is_full(self):
        return self.available_seats == 0

    @property
    def reserved_seats(self):
        return self.seats.filter(is_reserved=True).count()

    @property
    def available_seats(self):
        return self.seats.filter(is_reserved=False).count()


class Seat(models.Model):
    screening = models.ForeignKey(
        "screenings.Screening",
        on_delete=models.PROTECT,
        related_name="seats",
    )
    booking = models.ForeignKey(
        "bookings.Booking",
        on_delete=models.SET_NULL,
        related_name="seats",
        null=True,
        blank=True,
    )
    number = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["screening", "number"]

    def __str__(self) -> str:
        return f"{self.screening}{self.number}"
