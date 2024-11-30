"""
ASGI config for MoodWave project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from Middleware.CombinedAuthMiddleware import CombinedAuthMiddleware
from MoodWave.routings import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MoodWave.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(CombinedAuthMiddleware(URLRouter(ws_urlpatterns)))
    }
)