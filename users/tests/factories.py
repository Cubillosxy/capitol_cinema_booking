import factory
from django.apps import apps
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
