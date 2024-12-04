from django.urls import path

from chats.consumers import ChatsConsumer, MessagesConsumer


ws_urlpatterns = [
    path('chats/chats_updating/', ChatsConsumer.as_asgi()),
    path('chats/messages/add_new_message', MessagesConsumer.as_asgi())
]