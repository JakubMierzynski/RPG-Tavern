from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView
from tavern_app.models import Profile, MasterSession, GamerSession
from tavern_app.forms import UserForm, ProfileForm, User, LoginForm, FindUserForm, MasterSessionForm, GamerSessionForm
import django.contrib.messages


# Create your views here.


class MainPage(View):
    def get(self, request):
        return render(request, "tavern_app/mainpage.html")


class SignUpUserView(View):
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

            new_user = User.objects.create_user(username=username,
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

            return redirect("main")

        else:
            return render(request, 'tavern_app/sign_up.html', {'user_form': user_form,
                                                               'profile_form': profile_form})


class LoginView(FormView):
    form_class = LoginForm
    template_name = "tavern_app/login.html"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('main')


class FindUserView(View):
    def get(self, request):
        form = FindUserForm()
        request_method = request.method
        ctx = {"form": form,
               "request_method": request_method}

        return render(request, "tavern_app/find_user.html", ctx)

    def post(self, request):
        form = FindUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]

            users = User.objects.filter(username__icontains=username)

            request_method = request.method

            ctx = {"users": users,
                   "request_method": request_method,
                   "username": username,
                   "form": form}

            return render(request, "tavern_app/find_user.html", ctx)
        else:
            return render(request, "tavern_app/find_user.html", context={"form": form})


class UserDetailsView(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        # Później dodane zostaną tu sesje do których się będziemy odwoływać

        return render(request, "tavern_app/user_details.html", context={"user": user})


class CreateMasterSessionView(View):
    def get(self, request):
        form = MasterSessionForm
        return render(request, 'tavern_app/create_master_session.html', {'form': form})

    def post(self, request):
        form = MasterSessionForm(request.POST)

        if form.is_valid():
            # new user
            owner = request.user

            title = form.cleaned_data["title"]
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            number_of_players = form.cleaned_data["number_of_players"]
            description = form.cleaned_data["description"]
            difficulty = form.cleaned_data["difficulty"]
            adult_only = form.cleaned_data["adult_only"]
            other_requirements = form.cleaned_data["other_requirements"]

            new_session = MasterSession.objects.create(owner=owner,
                                                       title=title,
                                                       date=date,
                                                       time=time,
                                                       number_of_players=number_of_players,
                                                       description=description,
                                                       difficulty=difficulty,
                                                       adult_only=adult_only,
                                                       other_requirements=other_requirements)

            new_session.save()

            return redirect("main")

        else:
            return render(request, 'tavern_app/create_master_session.html', {"form": form})


class CreateGamerSessionView(View):
    def get(self, request):
        form = GamerSessionForm
        return render(request, 'tavern_app/create_gamer_session.html', {'form': form})

    def post(self, request):
        form = GamerSessionForm(request.POST)

        if form.is_valid():
            # new user
            owner = request.user

            title = form.cleaned_data["title"]
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            description = form.cleaned_data["description"]
            difficulty = form.cleaned_data["difficulty"]
            adult_only = form.cleaned_data["adult_only"]
            master_requirements = form.cleaned_data["master_requirements"]
            other_requirements = form.cleaned_data["other_requirements"]

            new_session = GamerSession.objects.create(owner=owner,
                                                      title=title,
                                                      date=date,
                                                      time=time,
                                                      description=description,
                                                      difficulty=difficulty,
                                                      adult_only=adult_only,
                                                      master_requirements=master_requirements,
                                                      other_requirements=other_requirements)

            new_session.save()

            return redirect("main")

        else:
            return render(request, 'tavern_app/create_gamer_session.html', {"form": form})
