# Generated by Django 4.0.2 on 2023-12-05 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tavern_app', '0004_alter_newuser_age_alter_newuser_description_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewUser',
        ),
    ]