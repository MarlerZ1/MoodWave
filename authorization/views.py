from lib2to3.fixes.fix_input import context

from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
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


    def get_success_url(self):
        return reverse_lazy("chats:chat_list")

def logout_user(request):
    logout(request)
    return redirect(reverse('authorization:login'))