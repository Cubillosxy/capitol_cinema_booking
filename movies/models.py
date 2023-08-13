from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    duration = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} {self.genre} {self.duration}"
