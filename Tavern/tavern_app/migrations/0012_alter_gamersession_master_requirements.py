# Generated by Django 4.0.2 on 2023-12-07 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tavern_app', '0011_gamersession_master_requirements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamersession',
            name='master_requirements',
            field=models.TextField(verbose_name='Wymagania dotyczące mistrza gry'),
        ),
    ]
