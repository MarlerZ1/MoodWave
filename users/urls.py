
from django.urls import include, path

app_name = "users"

urlpatterns = [
    path('', include("users.web.urls", namespace="web")),
    path('api/', include("users.api.urls", namespace="api")),
]
