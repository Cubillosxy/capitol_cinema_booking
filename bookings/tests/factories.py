from django.apps import apps

import factory
from factory.django import DjangoModelFactory
from faker import Factory as FackerFactory

from screenings.tests.factories import ScreeningFactory
from users.tests.factories import UserFactory

faker = FackerFactory.create()


class BookingFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    screening = factory.SubFactory(ScreeningFactory)
    is_cancelled = False
    is_active = True

    class Meta:
        model = apps.get_model("bookings", "Booking")
        django_get_or_create = ("user", "screening", "is_cancelled")
