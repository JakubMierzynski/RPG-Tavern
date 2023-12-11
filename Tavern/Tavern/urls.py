"""Tavern URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tavern_app.views import MainPage, \
    SignUpUserView,\
    LoginView,\
    logout_view,\
    FindUserView,\
    UserDetailsView,\
    CreateMasterSessionView,\
    CreateGamerSessionView,\
    CreateSessionBaseView,\
    AllSessionsView,\
    MasterSessionDetailsView,\
    GamerSessionDetailsView,\
    FindSessionView,\
    event_add_attendanceMS,\
    event_add_attendanceGS,\
    MyProfileView,\
    EditMasterSessionView,\
    EditGamerSessionView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", MainPage.as_view(), name="main"),
    path("sign-up/", SignUpUserView.as_view(), name="sign"),
    path("log-in/", LoginView.as_view(), name="login"),
    path("log-out/", logout_view, name="logout"),
    path("find-user/", FindUserView.as_view(), name="find-user"),
    path("user/<int:user_id>/", UserDetailsView.as_view(), name="user-details"),
    path("create-session/", CreateSessionBaseView.as_view(), name="create-session-base"),
    path("create-master-session/", CreateMasterSessionView.as_view(), name="create-master-session"),
    path("create-gamer-session/", CreateGamerSessionView.as_view(), name="create-gamer-session"),
    path("sessions/", AllSessionsView.as_view(), name="sessions"),
    path("master-session-details/<int:session_id>/", MasterSessionDetailsView.as_view(), name="master-session-details"),
    path("gamer-session-details/<int:session_id>/", GamerSessionDetailsView.as_view(), name="gamer-session-details"),
    path("find-session/", FindSessionView.as_view(), name="find-session"),
    path("add-attendance-ms/<int:session_id>/", event_add_attendanceMS, name="master-add-attendance"),
    path("add-attendance-gs/<int:session_id>/", event_add_attendanceGS, name="gamer-add-attendance"),
    path("my-profile/<int:user_id>/", MyProfileView.as_view(), name="my-profile"),
    path("edit-master-session/<int:session_id>/", EditMasterSessionView.as_view(), name="edit-master-session"),
    path("edit-gamer-session/<int:session_id>/", EditGamerSessionView.as_view(), name="edit-gamer-session")
]
