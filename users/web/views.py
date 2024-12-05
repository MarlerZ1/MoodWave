from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from chats import models as chats_models
from chats.models import UserInChat, Chat
from users import models as find_request_models
from users.models import FriendRequest


# Create your views here.
class FriendListView(LoginRequiredMixin, TemplateView):
    template_name = "users/friend_list.html"

    def get_context_data(self):
        context = super(FriendListView, self).get_context_data()

        context["pending_to"] = []
        context["accepted"] = []

        friend_request_from = FriendRequest.objects.filter(sender_id=self.request.user.id)

        for relation in friend_request_from:
            if relation.status == find_request_models.ACCEPTED:
                context["accepted"] += [relation.receiver]

        friend_request_to = FriendRequest.objects.filter(receiver_id=self.request.user.id)

        for relation in friend_request_to:
            if relation.status == find_request_models.PENDING:
                context["pending_to"] += [relation.sender]

            if relation.status == find_request_models.ACCEPTED:
                context["accepted"] += [relation.sender]

        return context


class RejectUser(LoginRequiredMixin, View):
    def post(self, request, friend_id):
        relationship = FriendRequest.objects.get(
            Q(sender=self.request.user, receiver_id=friend_id) |
            Q(receiver=self.request.user, sender_id=friend_id)
        )

        if relationship:
            relationship.status = find_request_models.REJECTED

            relationship.save()

            return JsonResponse({
                "status": "success"
            })
        return JsonResponse({
            "status": "error"
        })


class AcceptUser(LoginRequiredMixin, View):
    def post(self, request, friend_id):
        relationship = FriendRequest.objects.get(
            Q(sender=self.request.user, receiver_id=friend_id) |
            Q(receiver=self.request.user, sender_id=friend_id)
        )

        if relationship:
            relationship.status = find_request_models.ACCEPTED

            relationship.save()

            return JsonResponse({
                "status": "success"
            })
        return JsonResponse({
            "status": "error"
        })


class RedirectToChat(LoginRequiredMixin, View):
    def get(self, request, friend_id):
        logined_user_chats_rs = UserInChat.objects.filter(user=self.request.user)

        user_chat_ids = {
            user_in_chat.chat.id
            for user_in_chat in logined_user_chats_rs
            if user_in_chat.chat.format == chats_models.DIALOGUE
        }

        another_user_chat_rs = UserInChat.objects.filter(user_id=friend_id)

        for another_in_chat in another_user_chat_rs:
            if another_in_chat.chat.id in user_chat_ids: #log(n)
                return HttpResponseRedirect(reverse("chats:web:chat", args=[another_in_chat.chat.id]))

        with transaction.atomic():
            new_chat = Chat()
            new_chat.save()

            UserInChat(user=self.request.user, chat=new_chat).save()
            UserInChat(user_id=friend_id, chat=new_chat).save()

        return HttpResponseRedirect(reverse("chats:web:chat", args=[new_chat.id]))
