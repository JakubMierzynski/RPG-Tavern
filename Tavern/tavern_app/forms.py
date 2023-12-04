from django.contrib.auth import authenticate
from django import forms


class UserSignUpForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło")
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=100, label="Imię")
    age = forms.IntegerField(label="Wiek")
    description = forms.Textarea()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     login = cleaned_data.get("username")
    #     password = cleaned_data.get("password")
    #
    #     self.user = authenticate(username=login, password=password)
    #     if self.user is None:
    #         raise forms.ValidationError("Niewłaściwy login lub hasło")