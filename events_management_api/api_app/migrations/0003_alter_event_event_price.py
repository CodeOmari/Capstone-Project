# Generated by Django 5.1.7 on 2025-03-28 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0002_alter_event_organizer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_price',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=6),
        ),
    ]
