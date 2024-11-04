import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.core.exceptions import ObjectDoesNotExist

from chats.business_logic import ChatsListPageBL, MessagesPageBL
from chats.models import UserInChat, Message, CHAT
from common.exceptions.exceptions import IncorrectDialoguePeopleNumber


class ChatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"group_{self.scope["user"].id}")
        await self.channel_layer.group_add(f"group_chatlist_{self.scope["user"].id}", self.channel_name)
        await self.accept()


    @staticmethod
    def redefine_chats(user_ids):
        channel_layer = get_channel_layer()

        user_in_chats = UserInChat.objects.all()
        for id in user_ids:
            chats_info = ChatsListPageBL.get_chats(user_in_chats, id)

            async_to_sync(channel_layer.group_send)(
                f"group_chatlist_{id}",
                {
                    "type": "chat_message",
                    "text": chats_info
                },
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"websocket_message": event["text"]}))
        print(json.dumps({"websocket_message": event["text"]}))



class MessagesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(f"group_messages_{self.scope["user"].id}", self.channel_name)
        await self.accept()


    @staticmethod
    def redefine_messages(new_message,  user_ids):
        channel_layer = get_channel_layer()

        for user_id in user_ids:
            message = MessagesPageBL.get_formated_message(new_message, user_id)

            async_to_sync(channel_layer.group_send)(
                f"group_messages_{user_id}",
                {
                    "type": "chat_message",
                    "text": message
                },
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"websocket_message": event["text"]}))
        print(json.dumps({"websocket_message": event["text"]}))