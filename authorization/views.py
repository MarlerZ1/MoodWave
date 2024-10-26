from lib2to3.fixes.fix_input import context

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from authorization.forms import UserRegistrationForm, UserLoginForm


class UserRegistrationView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    template_name = 'authorization/registration.html'
    success_url = reverse_lazy("authorization:login")


class UserLoginView(LoginView):
    template_name = 'authorization/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy("authorization:registraion")


class UserLogoutView(LogoutView):
    success_url = reverse_lazy("authorization:login")