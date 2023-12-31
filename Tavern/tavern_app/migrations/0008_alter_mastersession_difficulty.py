# Generated by Django 4.0.2 on 2023-12-07 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tavern_app', '0007_mastersession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastersession',
            name='difficulty',
            field=models.CharField(choices=[('Pokojowa', 'Pokojowa'), ('Zrównoważona', 'Zrównoważona'), ('Niebezpieczna', 'Niebezpieczna'), ('Śmiertelnie groźna', 'Śmiertelnie groźna')], max_length=50, verbose_name='Poziom trudności przygody'),
        ),
    ]
