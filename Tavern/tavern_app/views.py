from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView
from tavern_app.models import Profile
from tavern_app.forms import UserForm, ProfileForm, User

# Create your views here.


class MainPage(View):
    def get(self, request):
        return render(request, "tavern_app/mainpage.html")


class SignUpUser(View):
    def get(self, request):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, 'tavern_app/sign_up.html', {'user_form': user_form,
                                                           'profile_form': profile_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # new user
            username = user_form.cleaned_data["username"]
            first_name = user_form.cleaned_data["first_name"]
            last_name = user_form.cleaned_data["last_name"]
            email = user_form.cleaned_data["email"]
            password = user_form.cleaned_data["password"]

            new_user = User.objects.create(username=username,
                                           first_name=first_name,
                                           last_name=last_name,
                                           email=email,
                                           password=password)
            new_user.save()

            # new profile

            user = User.objects.get(username=username)
            description = profile_form.cleaned_data["description"]
            birth_date = profile_form.cleaned_data["birth_date"]

            new_profile = Profile.objects.get(user=user)
            new_profile.description = description
            new_profile.birth_date = birth_date

            new_profile.save()

            return HttpResponse("OK")

        else:
            print(user_form.errors)
            print("****")
            print(profile_form.errors)
            return HttpResponse("FAIL")

