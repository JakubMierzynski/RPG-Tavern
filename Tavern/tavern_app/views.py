from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView
from tavern_app.models import NewUser
# from tavern_app.forms import UserSignUpForm


# Create your views here.


class MainPage(View):
    def get(self, request):
        return render(request, "tavern_app/mainpage.html")



class CreateUserView(CreateView):
    model = NewUser
    fields = ["username", "password", "email", "first_name", "age", "description"]
    template_name = "tavern_app/newuser_form.html"
    success_url = reverse_lazy("main")