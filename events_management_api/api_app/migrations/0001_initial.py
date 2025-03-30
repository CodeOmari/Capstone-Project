# Generated by Django 5.1.7 on 2025-03-30 10:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(max_length=100)),
                ('event_category', models.CharField(choices=[('Tech', 'Tech'), ('Business', 'Business'), ('Social', 'Social'), ('Art', 'Art'), ('Trade Expos', 'Trade Expos'), ('Education', 'Education')], max_length=100)),
                ('event_description', models.TextField()),
                ('event_date', models.DateField()),
                ('event_time', models.TimeField()),
                ('event_location', models.CharField(max_length=100)),
                ('virtual_location', models.URLField(blank=True, default='N/A', null=True)),
                ('event_price', models.DecimalField(decimal_places=2, default='0.00', max_digits=6)),
                ('event_slots', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('attendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.event')),
            ],
            options={
                'db_table': 'Tickets',
                'unique_together': {('event', 'attendee')},
            },
        ),
    ]
