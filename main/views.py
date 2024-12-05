from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View


# Create your views here.
class MainView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("chats:web:chat_list"))
        return HttpResponseRedirect(reverse("authorization:web:login"))