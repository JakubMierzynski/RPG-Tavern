# Generated by Django 4.0.2 on 2023-12-04 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tavern_app', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='age',
            field=models.IntegerField(verbose_name='Wiek'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='description',
            field=models.TextField(blank=True, max_length=500, verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Adres email'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Imię'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='username',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nazwa użytkownika'),
        ),
    ]