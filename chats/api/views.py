from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chats.business_logic import ChatsListPageBL
from chats.models import UserInChat


class ChatListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(ChatsListPageBL.get_chats(UserInChat.objects.all(), request.user.id), status=status.HTTP_200_OK)
