from lib2to3.fixes.fix_input import context

from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, TemplateView

from users import models
from users.models import User, FriendRequest


# Create your views here.
class FriendListView(TemplateView):
    template_name = "users/friend_list.html"


    def get_context_data(self):
        context = super(FriendListView, self).get_context_data()

        context["pending_to"] = []
        context["accepted"] = []


        friend_request_from = FriendRequest.objects.filter(sender_id=self.request.user.id)

        for relation in friend_request_from:
            if relation.status == models.ACCEPTED:
                    context["accepted"] += [relation.receiver]

        friend_request_to = FriendRequest.objects.filter(receiver_id=self.request.user.id)

        for relation in friend_request_to:
            if relation.status == models.PENDING:
                    context["pending_to"] += [relation.sender]

            if relation.status == models.ACCEPTED:
                    context["accepted"] += [relation.sender]

        return context


class RejectUser(View):
    def post(self, request, friend_id):
        relationship = FriendRequest.objects.get(
            Q(sender=self.request.user,receiver_id=friend_id) |
            Q(receiver=self.request.user,sender_id=friend_id)
        )

        if relationship:
            relationship.status = models.REJECTED

            relationship.save()

            return JsonResponse({
                "status": "success"
            })
        return JsonResponse({
            "status": "error"
        })


class AcceptUser(View):
    def post(self, request, friend_id):
        relationship = FriendRequest.objects.get(
            Q(sender=self.request.user, receiver_id=friend_id) |
            Q(receiver=self.request.user, sender_id=friend_id)
        )

        if relationship:
            relationship.status = models.ACCEPTED

            relationship.save()

            return JsonResponse({
                "status": "success"
            })
        return JsonResponse({
            "status": "error"
        })