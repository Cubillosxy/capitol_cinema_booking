import factory
from django.apps import apps
from factory.django import DjangoModelFactory
from faker import Factory as FackerFactory

faker = FackerFactory.create()


class CinemaFactory(DjangoModelFactory):
    name = factory.LazyAttribute(lambda _: faker.name())
    city = factory.LazyAttribute(lambda _: faker.city())
    address = factory.LazyAttribute(lambda _: faker.address())
    capacity = factory.LazyAttribute(lambda _: faker.random_int(min=1, max=100))
    is_disabled = False

    class Meta:
        model = apps.get_model("cinemas", "Cinema")
        django_get_or_create = ("name", "city", "address", "capacity", "is_disabled")
