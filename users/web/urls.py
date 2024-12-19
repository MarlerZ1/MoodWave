from django.urls import path

from users.web.views import FriendListView, RejectUser, AcceptUser, RedirectToChat, DeleteRequest, SearchUser, InviteUser

app_name = "users_web"

urlpatterns = [
    path('friend_list/', FriendListView.as_view(), name="friend_list"),
    path('friend_list/reject_friend/<friend_id>', RejectUser.as_view(), name="reject_friend"),
    path('friend_list/accept_friend/<friend_id>', AcceptUser.as_view(), name="accept_friend"),
    path('friend_list/delete_friend/<friend_id>', DeleteRequest.as_view(), name="delete_request"),
    path('friend_list/invite_friend/<friend_id>', InviteUser.as_view(), name="invite_request"),
    path('friend_list/search_user/', SearchUser.as_view(), name="search_request"),
    path('friend_list/redirect_to_chat/<friend_id>', RedirectToChat.as_view(), name="redirect_to_chat"),
]
