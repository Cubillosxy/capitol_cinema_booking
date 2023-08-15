# Generated by Django 4.2.4 on 2023-08-13 23:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screenings', '0003_screening_available_seats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screening',
            name='available_seats',
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('is_reserved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('screening', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seats', to='screenings.screening')),
            ],
            options={
                'unique_together': {('screening', 'number')},
            },
        ),
    ]