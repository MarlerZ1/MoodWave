from django.urls import path, include

app_name = 'authorization'

urlpatterns = [
    path('api/', include('authorization.api.urls', namespace="api")),
    path('', include('authorization.web.urls', namespace="web")),
]
