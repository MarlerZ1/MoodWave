from django.contrib import admin
from django.urls import path

from authorization.views import UserRegistrationView, UserLoginView, UserLogoutView

app_name = 'authorizetion'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
