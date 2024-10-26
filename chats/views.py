from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

from chats.models import Chat, UserInChat, CHAT


# Create your views here.

class ChartsView(ListView):
    model = Chat
    template_name = 'chats/chart_list.html'

    def get_queryset(self):
        queryset = super(ChartsView, self).get_queryset()

        chats = []

        for chat in queryset:
            if chat.format == CHAT:
                try:
                    chats += [{'name': chat.chatinfo.name, 'logo': chat.chatinfo.logo, 'format': 'chat'}]
                except ObjectDoesNotExist as e:
                    raise e
            else:
                users_in_chat = UserInChat.objects.filter(chat_id=chat.id)

                if self.request.user.id == users_in_chat[0].user.id:
                    another_user = users_in_chat[1].user
                else:
                    another_user = users_in_chat[0].user

                chats += [{'name': another_user.first_name + " " + another_user.last_name, 'logo': another_user.logo ,'format': 'dialogue'}]

        return chats
