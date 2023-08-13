import factory
from django.apps import apps
from factory.django import DjangoModelFactory
from faker import Factory as FackerFactory

faker = FackerFactory.create()


class MovieFactory(DjangoModelFactory):
    title = factory.LazyAttribute(lambda _: faker.name())
    genre = factory.LazyAttribute(lambda _: faker.city())
    duration = factory.LazyAttribute(lambda _: faker.random_int(min=70, max=160))
    is_disabled = False

    class Meta:
        model = apps.get_model("movies", "Movie")
        django_get_or_create = ("title", "genre", "duration", "is_disabled")
