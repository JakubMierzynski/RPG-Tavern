# Generated by Django 4.0.2 on 2023-12-08 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tavern_app', '0013_mastersessionregistration_gamersessionregistration'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastersession',
            name='counter_of_players',
            field=models.IntegerField(default=0),
        ),
    ]