from django.urls import path

from authorization.web.views import UserRegistrationView, UserLoginView, logout_user

app_name = 'authorization_web'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
