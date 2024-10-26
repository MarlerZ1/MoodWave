from django.contrib import admin
from django.urls import path, include

from chats.views import ChartsView

app_name = "chats"

urlpatterns = [
    path('chat_list/', ChartsView.as_view(), name="chat_list"),
]
