import random
from urllib import request

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView
from tavern_app.models import Profile, MasterSession, GamerSession, MasterSessionRegistration, GamerSessionRegistration
from tavern_app.forms import UserForm, ProfileForm, User, LoginForm, FindUserForm, MasterSessionForm, GamerSessionForm, FindSessionForm, EditMasterSessionForm, EditGamerSessionForm
from datetime import datetime
from django.contrib import messages
from random import shuffle






# Create your views here.

class MainPage(View):
    def get(self, request):
        all_sessions = []
        all_master_sessions = MasterSession.objects.all()
        all_gamer_sessions = GamerSession.objects.all()

        for session in all_master_sessions:
            all_sessions.append(session)

        for session in all_gamer_sessions:
            all_sessions.append(session)

        random.shuffle(all_sessions)

        session1 = all_sessions[0]
        session2 = all_sessions[1]
        session3 = all_sessions[2]

        return render(request, "tavern_app/mainpage.html", context={
            'session1': session1,
            'session2': session2,
            'session3': session3})


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

        redirect_to = self.request.GET.get('next', None)
        if redirect_to:
            return HttpResponseRedirect(redirect_to)
        else:
            return HttpResponseRedirect(reverse_lazy("main"))

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

            if len(users) == 0:
                ctx = {"not_found": True,
                       "form": form,
                       "username": username}
                return render(request, "tavern_app/find_user.html", ctx)

            else:
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

        #Jeśli i mistrz i gracz:
        if MasterSessionRegistration.objects.filter(user_id=user_id).exists() and GamerSessionRegistration.objects.filter(user_id=user_id).exists():
            master_sessions_registered = MasterSessionRegistration.objects.filter(user_id=user_id)
            gamer_sessions_registered = GamerSessionRegistration.objects.filter(user_id=user_id)
            owning_master_sessions = MasterSession.objects.filter(owner=user)
            owning_gamer_sessions = GamerSession.objects.filter(owner=user)

            master_sessions_active_only = []
            gamer_sessions_active_only = []

            for session in master_sessions_registered:
                date = session.session.date
                time = session.session.time

                combined = datetime.combine(date, time)

                if combined > datetime.now():
                    master_sessions_active_only.append(session.session)

            for session in gamer_sessions_registered:
                date = session.session.date
                time = session.session.time

                combined = datetime.combine(date, time)

                if combined > datetime.now():
                   gamer_sessions_active_only.append(session.session)

            for session in owning_master_sessions:
                date = session.date
                time = session.time

                combined = datetime.combine(date, time)

                if combined > datetime.now():
                    master_sessions_active_only.append(session)

            for session in owning_gamer_sessions:
                date = session.date
                time = session.time

                combined = datetime.combine(date, time)

                if combined > datetime.now():
                    gamer_sessions_active_only.append(session)

            return render(request, "tavern_app/user_details.html", context={"user": user,
                                                                            "master_sessions": set(master_sessions_active_only),
                                                                            "gamer_sessions": set(gamer_sessions_active_only)})

        #Jeśli tylko mistrz
        if not MasterSessionRegistration.objects.filter(user_id=user_id).exists() and GamerSessionRegistration.objects.filter(user_id=user_id).exists():
            gamer_sessions_registered = GamerSessionRegistration.objects.filter(user_id=user_id)
            owning_gamer_sessions = GamerSession.objects.filter(owner=user)
            gamer_sessions_active_only = []

            for session in gamer_sessions_registered:
                date = session.session.date
                time = session.session.time

                combined = datetime.combine(date, time)

                if combined > datetime.now():
                    gamer_sessions_active_only.append(session.session)

            for session in owning_gamer_sessions:
                date = session.date
                time = session.time

                combined = datetime.combine(date, time)

                if combined > datetime.now():
                    gamer_sessions_active_only.append(session)

            return render(request, "tavern_app/user_details.html", context={"user": user,
                                                                            "gamer_sessions": set(gamer_sessions_active_only)})

        # Jeśli tylko gracz
        if not GamerSessionRegistration.objects.filter(user_id=user_id).exists() and MasterSessionRegistration.objects.filter(user_id=user_id).exists():
            master_sessions_registered = MasterSessionRegistration.objects.filter(user_id=user_id)
            owning_master_sessions = MasterSession.objects.filter(owner=user)
            master_sessions_active_only = []

            for session in master_sessions_registered:
                date = session.session.date
                time = session.session.time

                combined = datetime.combine(date, time)

                if combined > datetime.now():
                    master_sessions_active_only.append(session.session)

            for session in owning_master_sessions:
                date = session.date
                time = session.time

                combined = datetime.combine(date, time)

                if combined > datetime.now():
                    master_sessions_active_only.append(session)

            return render(request, "tavern_app/user_details.html", context={"user": user,
                                                                            "master_sessions": set(master_sessions_active_only)})

        else:
            return render(request, "tavern_app/user_details.html", context={"user": user})


class CreateSessionBaseView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):

        return render(request, "tavern_app/create_session_base.html")



class CreateMasterSessionView(LoginRequiredMixin, View):
    login_url = 'login'

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

            return redirect("sessions")

        else:
            return render(request, 'tavern_app/create_master_session.html', {"form": form})


class CreateGamerSessionView(LoginRequiredMixin, View):
    login_url = 'login'
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

            return redirect("sessions")

        else:
            return render(request, 'tavern_app/create_gamer_session.html', {"form": form})


class AllSessionsView(View):
    def get(self, request):
        all_master_sessions = MasterSession.objects.all().order_by("date", "time")
        all_gamer_sessions = GamerSession.objects.filter(is_master_chosen=False).order_by("date", "time")

        gamer_sessions_active_only = []
        master_sessions_active_only = []

        for session in all_gamer_sessions:
            date = session.date
            time = session.time

            combined = datetime.combine(date, time)

            if combined > datetime.now():
                gamer_sessions_active_only.append(session)

        for session in all_master_sessions:
            date = session.date
            time = session.time

            combined = datetime.combine(date, time)

            if combined > datetime.now():
                master_sessions_active_only.append(session)

        return render(request, "tavern_app/all_sessions.html", context={"master_sessions": master_sessions_active_only,
                                                                        "gamer_sessions": gamer_sessions_active_only})


class MasterSessionDetailsView(View):
    def get(self, request, session_id):
        session = MasterSession.objects.get(pk=session_id)

        if MasterSessionRegistration.objects.filter(session=session_id).exists():
            players = MasterSessionRegistration.objects.filter(session=session_id)

            return render(request, "tavern_app/master_session_details.html", context={"master_session": session,
                                                                                      "players": players})
        else:
            return render(request, "tavern_app/master_session_details.html", context={"master_session": session})


class GamerSessionDetailsView(View):
    def get(self, request, session_id):
        session = GamerSession.objects.get(pk=session_id)

        if GamerSessionRegistration.objects.filter(session=session_id).exists():
            found_session = GamerSessionRegistration.objects.get(session=session_id)
            master = User.objects.get(id=found_session.user_id)

            return render(request, "tavern_app/gamer_session_details.html", context={"gamer_session": session,
                                                                                     "master": master})
        else:
            return render(request, "tavern_app/gamer_session_details.html", context={"gamer_session": session})


class FindSessionView(View):
    def get(self, request):
        form = FindSessionForm()
        request_method = request.method
        ctx = {"form": form,
               "request_method": request_method}

        return render(request, "tavern_app/find_session.html", ctx)

    def post(self, request):
        form = FindSessionForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            if_gamer = form.cleaned_data["if_gamer"]
            if_master = form.cleaned_data["if_master"]
            active_only = form.cleaned_data["if_active_only"]

            if if_master:
                if active_only:
                    gamer_sessions = GamerSession.objects.filter(title__icontains=title).order_by("date", "time")
                    gamer_sessions_active_only = []

                    for session in gamer_sessions:
                        date = session.date
                        time = session.time

                        combined = datetime.combine(date, time)

                        if combined > datetime.now():
                            gamer_sessions_active_only.append(session)

                    if len(gamer_sessions) == 0:
                        ctx = {"not_found": True,
                               "title": title,
                               "form": form}
                        return render(request, "tavern_app/find_session.html", ctx)

                    else:
                        request_method = request.method
                        ctx = {"gamer_sessions": gamer_sessions_active_only,
                               "request_method": request_method,
                               "title": title,
                               "form": form}

                        return render(request, "tavern_app/find_session.html", ctx)

                else:
                    gamer_sessions = GamerSession.objects.filter(title__icontains=title).order_by("date", "time")
                    request_method = request.method

                    if len(gamer_sessions) == 0:
                        ctx = {"not_found": True,
                               "title": title,
                               "form": form}
                        return render(request, "tavern_app/find_session.html", ctx)

                    ctx = {"gamer_sessions": gamer_sessions,
                           "request_method": request_method,
                           "title": title,
                           "form": form}

                    return render(request, "tavern_app/find_session.html", ctx)

            if if_gamer:
                if active_only:
                    master_sessions = MasterSession.objects.filter(title__icontains=title).order_by("date", "time")
                    master_sessions_active_only = []

                    for session in master_sessions:
                        date = session.date
                        time = session.time

                        combined = datetime.combine(date, time)

                        if combined > datetime.now():
                            master_sessions_active_only.append(session)

                    if len(master_sessions) == 0:
                        ctx = {"not_found": True,
                               "title": title,
                               "form": form}
                        return render(request, "tavern_app/find_session.html", ctx)

                    else:
                        request_method = request.method
                        ctx = {"master_sessions": master_sessions_active_only,
                               "request_method": request_method,
                               "title": title,
                               "form": form}

                        return render(request, "tavern_app/find_session.html", ctx)

                else:

                    master_sessions = MasterSession.objects.filter(title__icontains=title).order_by("date", "time")

                    if len(master_sessions) == 0:
                        ctx = {"not_found": True,
                               "title": title,
                               "form": form}
                        return render(request, "tavern_app/find_session.html", ctx)

                    else:
                        request_method = request.method

                        ctx = {"master_sessions": master_sessions,
                               "request_method": request_method,
                               "title": title,
                               "form": form}

                        return render(request, "tavern_app/find_session.html", ctx)
        else:
            return render(request, "tavern_app/find_session.html", context={"form": form})


@login_required(login_url="login")
def event_add_attendanceMS(request, session_id):
    this_event = MasterSession.objects.get(pk=session_id)

    if this_event.counter_of_players < this_event.number_of_players:
        if MasterSessionRegistration.objects.filter(session= session_id, user_id=request.user.id).exists():
            messages.info(request, 'Bierzesz już udział w tej sesji')
            return redirect('master-session-details', session_id=session_id)
        else:
            this_event.add_user_to_list_of_attendeesMS(user=request.user)
            this_event.counter_of_players += 1
            this_event.save()

            messages.info(request, 'Udało Ci się dołączyć do sesji')
            return redirect('master-session-details', session_id=session_id)

    else:
        messages.info(request, 'Lista graczy pełna. Nie możesz dołączyć do tej sesji')
        return redirect('master-session-details', session_id=session_id)


# def event_cancel_attendanceMS(request, session_id):
#     this_event = MasterSession.objects.get(pk=session_id)
#     this_event.remove_user_from_list_of_attendees(request.user)
#     return redirect('master-session-details', session_id=session_id)


@login_required(login_url="login")
def event_add_attendanceGS(request, session_id):
    this_event = GamerSession.objects.get(pk=session_id)

    if this_event.is_master_chosen is False:
        this_event.add_user_to_list_of_attendeesGS(user=request.user)
        this_event.is_master_chosen = True
        this_event.save()

        messages.info(request, 'Zostałeś Mistrzem Gry tej sesji')
        return redirect('gamer-session-details', session_id=session_id)


# def event_cancel_attendanceGS(request, session_id):
#     this_event = GamerSession.objects.get(pk=session_id)
#     this_event.remove_user_from_list_of_attendees(request.user)
#     return redirect('gamer-session-details', session_id=session_id)


class MyProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)

        return render(request, "tavern_app/my_profile.html", context={"user": user})


class EditMasterSessionView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, session_id):
        form = EditMasterSessionForm(initial={"title": MasterSession.objects.get(id=session_id).title,
                                              "date": MasterSession.objects.get(id=session_id).date,
                                              "time": MasterSession.objects.get(id=session_id).time,
                                              "number_of_players": MasterSession.objects.get(id=session_id).number_of_players,
                                              "description": MasterSession.objects.get(id=session_id).description,
                                              "difficulty": MasterSession.objects.get(id=session_id).difficulty,
                                              "adult_only": MasterSession.objects.get(id=session_id).adult_only,
                                              "other_requirements": MasterSession.objects.get(id=session_id).other_requirements})

        return render(request, 'tavern_app/edit_master_session.html', {'form': form})

    def post(self, request, session_id):
        form = EditMasterSessionForm(request.POST)
        session = MasterSession.objects.get(id=session_id)

        if form.is_valid():
            title = form.cleaned_data["title"]
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            number_of_players = form.cleaned_data["number_of_players"]
            description = form.cleaned_data["description"]
            difficulty = form.cleaned_data["difficulty"]
            adult_only = form.cleaned_data["adult_only"]
            other_requirements = form.cleaned_data["other_requirements"]

            session.title = title
            session.date = date
            session.time = time
            session.number_of_players = number_of_players
            session.description = description
            session.difficulty = difficulty
            session.adult_only = adult_only
            session.other_requirements = other_requirements

            session.save()

            return redirect(f"/master-session-details/{session_id}/")

        else:
            return render(request, 'tavern_app/edit_master_session.html', {"form": form})


class EditGamerSessionView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, session_id):
        form = EditGamerSessionForm(initial={"title": GamerSession.objects.get(id=session_id).title,
                                             "date": GamerSession.objects.get(id=session_id).date,
                                             "time": GamerSession.objects.get(id=session_id).time,
                                             "description": GamerSession.objects.get(id=session_id).description,
                                             "difficulty": GamerSession.objects.get(id=session_id).difficulty,
                                             "adult_only": GamerSession.objects.get(id=session_id).adult_only,
                                             "master_requirements": GamerSession.objects.get(id=session_id).master_requirements,
                                             "other_requirements": GamerSession.objects.get(id=session_id).other_requirements})

        return render(request, 'tavern_app/edit_gamer_session.html', {'form': form})

    def post(self, request, session_id):
        form = EditGamerSessionForm(request.POST)
        session = GamerSession.objects.get(id=session_id)

        if form.is_valid():
            title = form.cleaned_data["title"]
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            description = form.cleaned_data["description"]
            difficulty = form.cleaned_data["difficulty"]
            adult_only = form.cleaned_data["adult_only"]
            master_requirements = form.cleaned_data["master_requirements"]
            other_requirements = form.cleaned_data["other_requirements"]

            session.title = title
            session.date = date
            session.time = time
            session.description = description
            session.difficulty = difficulty
            session.adult_only = adult_only
            session.master_requirements = master_requirements
            session.other_requirements = other_requirements

            session.save()

            return redirect(f"/gamer-session-details/{session_id}/")

        else:
            return render(request, 'tavern_app/edit_gamer_session.html', {"form": form})