from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from chats.business_logic import ChatsListPageBL, MessagesPageBL
from chats.forms import TextInputForm
from chats.models import UserInChat, CHAT, Message, Chat, AttachmentImage
from common.exceptions.exceptions import IncorrectDialoguePeopleNumber


# Create your views here.

class ChatsView(LoginRequiredMixin, ListView):
    model = UserInChat
    template_name = 'chats/chat_list_page/chat_list.html'
    login_url = reverse_lazy('authorization:login')

    def get_queryset(self):

        return  ChatsListPageBL.get_chats(super(ChatsView, self).get_queryset(), self.request.user.id)

class MessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chats/chat/chat.html'
    login_url = reverse_lazy('authorization:login')

    def get_queryset(self):

        return MessagesPageBL.get_formated_messages(super(MessagesView, self).get_queryset(), self.kwargs['chat_id'], self.request.user.id)

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