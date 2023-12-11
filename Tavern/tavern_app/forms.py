from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput, SelectDateWidget
from datetime import datetime

from tavern_app.models import Profile, MasterSession, GamerSession


# class UserSignUpForm(forms.Form):
#     username = forms.CharField(label="Login")
#     password = forms.CharField(widget=forms.PasswordInput(), label="Hasło")
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(max_length=100, label="Imię")
#     age = forms.IntegerField(label="Wiek")
#     description = forms.Textarea()
#
#     # def clean(self):
#     #     cleaned_data = super().clean()
#     #     login = cleaned_data.get("username")
#     #     password = cleaned_data.get("password")
#     #
#     #     self.user = authenticate(username=login, password=password)
#     #     if self.user is None:
#     #         raise forms.ValidationError("Niewłaściwy login lub hasło")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

        widgets = {
            "password": PasswordInput(
                attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
        }




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'birth_date')

        labels = {
            "description": "Opis",
            "birth_date": "Data urodzenia"
        }

        widgets = {
            "birth_date": SelectDateWidget(years=range(1900, 2008)),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło")

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get("username")
        password = cleaned_data.get("password")

        self.user = authenticate(username=login, password=password)
        if self.user is None:
            raise forms.ValidationError("Niewłaściwy login lub hasło")


class FindUserForm(forms.Form):
    username = forms.CharField(label="Login szukanego użytkownika", max_length=100)



class MasterSessionForm(forms.ModelForm):
    class Meta:
        model = MasterSession
        fields = ('title', 'date', 'time', 'number_of_players', 'description', 'difficulty', 'adult_only', 'other_requirements')

        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'date': SelectDateWidget(years=range(2023, 2026))
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        today = date.today()

        print(type(date))
        print(type(today))

        if date < today:
            raise forms.ValidationError("Sesja nie może się odbyć w przeszłości")

        if time < datetime.now().time():
            raise forms.ValidationError("Godzina sesji jest z przeszłości")


class GamerSessionForm(forms.ModelForm):
    class Meta:
        model = GamerSession
        fields = ('title', 'date', 'time', 'description', 'difficulty', 'adult_only', 'master_requirements', 'other_requirements')

        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'date': SelectDateWidget(years=range(2023, 2026))
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        today = date.today()


        if date < today:
            raise forms.ValidationError("Sesja nie może się odbyć w przeszłości")

        if time < datetime.now().time():
            raise forms.ValidationError("Godzina sesji jest z przeszłości")


class FindSessionForm(forms.Form):
    title = forms.CharField(label="Słowo klucz / Tytuł przygody", max_length=100)
    if_gamer = forms.BooleanField(required=False, label='Poszukuję jako Gracz')
    if_master = forms.BooleanField(required=False, label='Poszukuję jako Mistrz Gry')
    if_active_only = forms.BooleanField(required=False, label='Wyszukaj tylko aktywne sesje')

    def clean(self):
        cleaned_data = super().clean()
        if_gamer = cleaned_data.get("if_gamer")
        if_master = cleaned_data.get("if_master")

        if if_gamer and if_master:
            raise forms.ValidationError("Nie można wyszukiwać jednocześnie jako Mistrz Gry i Gracz")

        if not if_gamer and not if_master:
            raise forms.ValidationError("Wybierz jedną z opcji wyszukiwania")


class EditMasterSessionForm(forms.ModelForm):
    class Meta:
        model = MasterSession
        fields = ('title', 'date', 'time', 'number_of_players', 'description', 'difficulty', 'adult_only', 'other_requirements')

        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'date': SelectDateWidget(years=range(2023, 2026))
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        today = date.today()

        print(type(date))
        print(type(today))

        if date < today:
            raise forms.ValidationError("Sesja nie może się odbyć w przeszłości")

        if time < datetime.now().time():
            raise forms.ValidationError("Godzina sesji jest z przeszłości")


class EditGamerSessionForm(forms.ModelForm):
    class Meta:
        model = GamerSession
        fields = ('title', 'date', 'time', 'description', 'difficulty', 'adult_only', 'master_requirements', 'other_requirements')

        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'date': SelectDateWidget(years=range(2023, 2026))
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        today = date.today()


        if date < today:
            raise forms.ValidationError("Sesja nie może się odbyć w przeszłości")

        if time < datetime.now().time():
            raise forms.ValidationError("Godzina sesji jest z przeszłości")
