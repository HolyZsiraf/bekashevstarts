# Generated by Django 4.0.3 on 2022-04-27 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtfshandler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HevDepartures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departureTime', models.DateTimeField(verbose_name='Date of departure')),
                ('startsFromBekas', models.BooleanField(verbose_name='Whether the train starts from Bekasmegyer or not')),
            ],
        ),
    ]
