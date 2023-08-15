from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)

    # override for allow null fields
    username = models.CharField(max_length=20, default="", null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def clean(self):
        if validate_email(self.email):
            raise ValidationError("Invalid email")

    def __str__(self) -> str:
        return f"{self.email}"
