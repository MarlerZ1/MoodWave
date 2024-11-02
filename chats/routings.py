from django.urls import path

from chats.consumers import ChatsConsumer

ws_urlpatterns = [
    path('chats/test/', ChatsConsumer.as_asgi())
]