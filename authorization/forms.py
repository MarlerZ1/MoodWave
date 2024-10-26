from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4" id="inputEmailAddress',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4" id="inputEmailAddress',
        'placeholder': 'Введите фамилию'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4" id="inputEmailAddress',
        'placeholder': 'Введите имя пользователя'
    }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4" id="inputEmailAddress',
        'placeholder': 'Введите адрес эл.почты'
    }))

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4" id="inputEmailAddress',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4" id="inputEmailAddress',
        'placeholder': 'Повторите пароль'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')