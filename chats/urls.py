from django.urls import path, include

app_name = "chats"

urlpatterns = [
    path('', include("chats.web.urls", namespace="web")),
    path('api/', include("chats.api.urls", namespace="api")),
]
