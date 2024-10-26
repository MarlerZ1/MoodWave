from lib2to3.fixes.fix_input import context

from django.shortcuts import render

from authorization.forms import UserRegistrationForm


# Create your views here.
def index(request):
    context = {
        'form': UserRegistrationForm(),
    }
    return render(request, 'authorization/registration.html', context)