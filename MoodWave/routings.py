from channels.routing import URLRouter
from django.urls import path

from chats.routings import ws_urlpatterns

ws_urlpatterns = [
    path('', URLRouter(ws_urlpatterns))
]