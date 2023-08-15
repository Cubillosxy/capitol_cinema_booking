from django.apps import apps
from django.utils import timezone

import factory
from factory.django import DjangoModelFactory
from faker import Factory as FackerFactory

from cinemas.tests.factories import CinemaFactory
from movies.tests.factories import MovieFactory

faker = FackerFactory.create()


class ScreeningFactory(DjangoModelFactory):
    movie = factory.SubFactory(MovieFactory)
    cinema = factory.SubFactory(CinemaFactory)
    date = factory.LazyFunction(
        lambda: timezone.make_aware(
            faker.date_time_between(start_date="+1d", end_date="+1y")
        )
    )

    price = factory.LazyAttribute(lambda _: faker.random_int(min=70, max=160))
    is_subtitled = factory.LazyAttribute(lambda _: faker.boolean())
    is_dubbed = factory.LazyAttribute(lambda _: faker.boolean())
    is_disabled = False

    class Meta:
        model = apps.get_model("screenings", "Screening")
        django_get_or_create = ("movie", "cinema", "date", "is_disabled")


class SeatFactory(DjangoModelFactory):
    screening = factory.SubFactory(ScreeningFactory)
    number = factory.LazyAttribute(lambda _: faker.random_int(min=1, max=100))
    is_reserved = False

    class Meta:
        model = apps.get_model("screenings", "Seat")
        django_get_or_create = ("screening", "number")
