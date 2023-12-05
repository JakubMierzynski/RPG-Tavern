from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput, SelectDateWidget

from tavern_app.models import Profile


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
