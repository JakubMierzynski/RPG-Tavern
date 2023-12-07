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
from tavern_app.views import MainPage, SignUpUserView, LoginView, logout_view, FindUserView, UserDetailsView, CreateMasterSessionView, CreateGamerSessionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", MainPage.as_view(), name="main"),
    path("sign-up/", SignUpUserView.as_view(), name="sign"),
    path("log-in/", LoginView.as_view(), name="login"),
    path("log-out/", logout_view, name="logout"),
    path("find-user/", FindUserView.as_view(), name="find-user"),
    path("user/<int:user_id>/", UserDetailsView.as_view(), name="user-details"),
    path("create-master-session/", CreateMasterSessionView.as_view(), name="create-master-session"),
    path("create-gamer-session/", CreateGamerSessionView.as_view(), name="create-gamer-session")

]
