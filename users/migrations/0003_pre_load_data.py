# Generated by Django 4.2.4 on 2023-08-16 14:27

from django.db import migrations
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from users.models import User




def create_data(apps, schema_editor):
    from utils.security import add_salt_to_password
    # Create a superuser

    admin_pass = add_salt_to_password("admin")
    User.objects.create(
        username='admin',
        email="admin@admin.com",
        password=make_password(admin_pass), #nosec
        is_superuser=True, is_staff=True
    )

    # Create a cinema_owner user and assign permissions
    group = Group.objects.get(name='Cinema Owner')
    cinema_pass = add_salt_to_password("owner")
    cinema_owner = User.objects.create(
        username='cinema_owner',
        email="owner@owner.com",
        password=make_password(cinema_pass) #nosec
    )

    cinema_owner.groups.add(group)

    # Create movies (assuming you have a Movie model in your app)
    Movie = apps.get_model('movies', 'Movie')
    Movie.objects.create(title='Spiderman', genre="action", duration=40)
    Movie.objects.create(title='Rat man', genre="action", duration=40)
    Movie.objects.create(title='bug man', genre="fiction", duration=100)


    # Create cinemas (assuming you have a Cinema model in your app)
    Cinema = apps.get_model('cinemas', 'Cinema')
    Cinema.objects.create(name='Capitol cinema', capacity=10, address="Calle 1", city="Madrid")
    Cinema.objects.create(name='cinecolombia', capacity=20, address="Calle 2", city="Bogota")
    Cinema.objects.create(name='old cinema', capacity=15, address="Calle 2", city="New York")


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_owner_permission'),
    ]

    operations = [
        migrations.RunPython(create_data)
    ]