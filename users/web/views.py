from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from chats import models as chats_models
from chats.models import UserInChat, Chat
from common.mixins.title_mixin import TitleMixin
from users import models as find_request_models
from users.filters import UserFilter
from users.models import FriendRequest, User
from users.serializers import UserSearchSerializer
from users.web.forms import UserSearchForm


# Create your views here.
class FriendListView(TitleMixin, LoginRequiredMixin, TemplateView):
    template_name = "users/friend_list_page/friend_list.html"
    title = "Friend List — MoodWave"
    def get_context_data(self):
        context = super(FriendListView, self).get_context_data()

        context["pending_to"] = []
        context["pending_from"] = []
        context["accepted"] = []
        context["rejected"] = []


        friend_request_from = FriendRequest.objects.filter(sender_id=self.request.user.id)

        for relation in friend_request_from:
            match relation.status:
                case find_request_models.ACCEPTED:
                    context["accepted"] += [relation.receiver]
                case find_request_models.PENDING:
                    context["pending_to"] += [relation.receiver]
                case find_request_models.REJECTED:
                    context["rejected"] += [relation.receiver]

        friend_request_to = FriendRequest.objects.filter(receiver_id=self.request.user.id)

        for relation in friend_request_to:
            match relation.status:
                case find_request_models.PENDING:
                    context["pending_from"] += [relation.sender]
                case find_request_models.ACCEPTED:
                    context["accepted"] += [relation.sender]
                case find_request_models.REJECTED:
                    context["rejected"] += [relation.sender]

        context["user_search_form"] = UserSearchForm()

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


class DeleteRequest(LoginRequiredMixin, View):
    def post(self, request, friend_id):
        relationship = FriendRequest.objects.get(
            Q(sender=self.request.user, receiver_id=friend_id) |
            Q(receiver=self.request.user, sender_id=friend_id)
        )

        if relationship:
            relationship.delete()

            return JsonResponse({
                "status": "success"
            })
        return JsonResponse({
            "status": "error"
        })

class SearchUser(LoginRequiredMixin, View):
    def get(self, request):
        user_filter = UserFilter(request.GET, queryset=User.objects.all())

        finded_users =  user_filter.qs
        couples = []
        if finded_users:
            for user in finded_users:
                if user.id == request.user.id:
                    continue

                user_js = UserSearchSerializer(user).data

                try:
                    from_me_request = FriendRequest.objects.get(sender=request.user.id, receiver_id=user.id)

                    match from_me_request.status:
                        case find_request_models.ACCEPTED:
                            couples += [(user_js, "accept")]
                        case find_request_models.PENDING:
                            couples += [(user_js, "pending")]
                except FriendRequest.DoesNotExist:
                    try:
                        to_me_request = FriendRequest.objects.get(receiver=request.user.id,sender=user.id)

                        match to_me_request.status:
                            case find_request_models.ACCEPTED:
                                couples += [(user_js, "accept")]
                            case find_request_models.PENDING:
                                couples += [(user_js, "waiting")]
                            case find_request_models.REJECTED:
                                couples += [(user_js, "rejected")]
                    except FriendRequest.DoesNotExist:
                        couples += [(user_js, "invite")]
            print(couples)
        return JsonResponse({
            'status': 'success',
            'filter': couples
        })



class InviteUser(LoginRequiredMixin, View):
    def post(self, request, friend_id):
        try:
            new_request = FriendRequest(sender=request.user, receiver_id=friend_id)

            new_request.save()
            return JsonResponse({
                'status': 'success',
            })
        except BaseException as e:
            print(e)
            return JsonResponse({
                "status": "error"
            })