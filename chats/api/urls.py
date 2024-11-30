from django.urls import path

from chats.api.views import ChatListApiView, MessagesApiView
from chats.web.views import ChatsView, MessagesView

app_name = "chats_api"

urlpatterns = [
    path('chat_list/', ChatListApiView.as_view(), name="chat_list"),
    path('chat/<chat_id>', MessagesApiView.as_view(), name="chat"),
]
