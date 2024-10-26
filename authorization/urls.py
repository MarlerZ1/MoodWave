from django.contrib import admin
from django.urls import path

from authorization.views import index

app_name = 'authorizetion'

urlpatterns = [
    path('registration/', index),
]
