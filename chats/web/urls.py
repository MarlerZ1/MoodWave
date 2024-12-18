from django.urls import path

from chats.web.views import ChatsView, MessagesView

app_name = "chats_web"

urlpatterns = [
    path('chat_list/', ChatsView.as_view(), name="chat_list"),
    path('chat/<chat_id>', MessagesView.as_view(), name="chat"),
]
