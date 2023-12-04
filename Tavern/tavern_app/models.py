from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, password, first_name, age, description, **other_fields):

        if not email:
            raise ValueError("Pole email nie może być puste.")
        if not username:
            raise ValueError("Pole username nie może być puste.")


        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name,
                          age=age, description=description)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, username, password, first_name, age, description, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, first_name, age, description)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Adres email")
    username = models.CharField(max_length=100, unique=True, verbose_name="Nazwa użytkownika")
    first_name = models.CharField(max_length=100, verbose_name="Imię")
    age = models.IntegerField(verbose_name="Wiek")
    description = models.TextField(max_length=500, blank=True, verbose_name="Opis")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "age", "description"]

    def __str__(self):
        return self.username

# You have to register your customer user model in admin.py so it uses you create_user method.
#
# Then, to register this custom user model with Django’s admin, the mentioned code would be required in the app’s admin.py file: