from django.apps import apps
from django.contrib.contenttypes.models import ContentType

import factory
from factory.django import DjangoModelFactory
from faker import Factory as FackerFactory

faker = FackerFactory.create()


class UserFactory(DjangoModelFactory):
    email = factory.LazyAttribute(lambda x: faker.email())
    is_staff = False
    is_active = True

    @factory.post_generation
    def set_password(self, create, value, **kwargs):
        self.set_password("password")

    class Meta:
        model = apps.get_model("users", "User")


class Permission(DjangoModelFactory):
    codename = factory.Sequence(lambda n: f"perm_codename_{n}")
    name = factory.Sequence(lambda n: f"Permission Name {n}")
    content_type = factory.Iterator(ContentType.objects.all())

    class Meta:
        model = apps.get_model("auth", "Permission")
        django_get_or_create = ("name", "codename")
