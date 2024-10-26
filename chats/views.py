from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from pyexpat.errors import messages

from chats.models import Chat, UserInChat, CHAT, Message
from common.exceptions.exceptions import IncorrectDialoguePeopleNumber


# Create your views here.

class ChartsView(ListView):
    model = UserInChat
    template_name = 'chats/chart_list.html'

    def get_queryset(self):
        queryset = super(ChartsView, self).get_queryset().filter(user_id=self.request.user.id)

        chats = []
        for relationship in queryset:
            chats += [relationship.chat]


        chats_info = []

        for chat in chats:
            message = Message.objects.filter(chat_id=chat.id).last()

            if chat.format == CHAT:
                try:
                    chats_info += [{'name': chat.chatinfo.name, 'logo': chat.chatinfo.logo, 'message': message, 'format': 'chat'}]
                except ObjectDoesNotExist as e:
                    raise e
            else:

                users_in_chat = UserInChat.objects.filter(chat_id=chat.id)

                if len(users_in_chat) != 2:
                    raise IncorrectDialoguePeopleNumber()

                if self.request.user.id == users_in_chat[0].user.id:
                    another_user = users_in_chat[1].user
                else:
                    another_user = users_in_chat[0].user

                chats_info += [{'name': another_user.first_name + " " + another_user.last_name, 'logo': another_user.logo ,'message': message, 'format': 'dialogue'}]

        return chats_info
