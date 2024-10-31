from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from chats.forms import TextInputForm
from chats.models import UserInChat, CHAT, Message, Chat, AttachmentImage
from common.exceptions.exceptions import IncorrectDialoguePeopleNumber


# Create your views here.

class ChatsView(ListView):
    model = UserInChat
    template_name = 'chats/chat_list_page/chat_list.html'

    def get_queryset(self):
        queryset = super(ChatsView, self).get_queryset().filter(user_id=self.request.user.id)

        chats = []
        for relationship in queryset:
            chats += [relationship.chat]


        chats_info = []

        for chat in chats:
            message = Message.objects.filter(chat_id=chat.id).last()

            message_text = message.text[:32] + "..." if message else None


            if chat.format == CHAT:
                try:
                    chats_info += [{'name': chat.chatinfo.name, 'logo': chat.chatinfo.logo, 'message_text': message_text, 'format': 'chat', 'chat_id': chat.id}]
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

                chats_info += [{'name': another_user.first_name + " " + another_user.last_name, 'logo': another_user.logo ,'message_text': message_text, 'format': 'dialogue', 'chat_id': chat.id}]

        return chats_info

class MessagesView(ListView):
    model = Message
    template_name = 'chats/chat/chat.html'

    def get_queryset(self):
        queryset = super(MessagesView, self).get_queryset()

        users_in_chat = UserInChat.objects.filter(chat_id=self.kwargs['chat_id'])

        queryset = queryset.filter(user_id__in=[user.user_id for user in users_in_chat], chat_id=self.kwargs['chat_id'])

        messages = [{
            'from_me': message.user_id == self.request.user.id,
            'name': message.user.first_name + " " + message.user.last_name,
            'text': message.text,
            'logo': message.user.logo,
            'image': images[0].image if (images:=AttachmentImage.objects.filter(message_id=message.id)) else None
        } for message in queryset]

        return messages

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MessagesView, self).get_context_data()
        context['message_form'] = TextInputForm()
        context['chat_id'] = self.kwargs['chat_id']
        return context

    def post(self, request, chat_id):
        form = TextInputForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=self.request.user, chat_id=chat_id)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])