# Generated by Django 4.0.3 on 2022-04-28 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gtfshandler', '0003_rename_hevdepartures_hevdeparture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hevdeparture',
            old_name='departureTime',
            new_name='departure_time',
        ),
    ]