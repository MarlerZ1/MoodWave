from django.urls import path

from authorization.views import UserRegistrationView, UserLoginView, logout_user

app_name = 'authorization'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
