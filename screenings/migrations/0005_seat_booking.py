# Generated by Django 4.2.4 on 2023-08-14 00:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_remove_booking_seats'),
        ('screenings', '0004_remove_screening_available_seats_seat'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seats', to='bookings.booking'),
        ),
    ]