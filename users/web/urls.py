from django.urls import path

from users.web.views import FriendListView, RejectUser, AcceptUser

app_name = "users_web"

urlpatterns = [
    path('friend_list/', FriendListView.as_view(), name="friend_list"),
    path('friend_list/reject_friend/<friend_id>', RejectUser.as_view(), name="reject_friend"),
    path('friend_list/accept_friend/<friend_id>', AcceptUser.as_view(), name="accept_friend"),
]
