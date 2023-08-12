from django.db import models


class Cinema(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    capacity = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} {self.city} {self.address}"
