# Generated by Django 5.1.7 on 2025-03-22 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='event',
            table='Events',
        ),
        migrations.AlterModelTable(
            name='ticket',
            table='Tickets',
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='Users',
        ),
    ]
