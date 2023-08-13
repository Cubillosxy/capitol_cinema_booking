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
    available_seats = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.movie} {self.cinema} {self.date}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.available_seats = self.cinema.capacity
        super().save(*args, **kwargs)
