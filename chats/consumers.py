import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.core.exceptions import ObjectDoesNotExist

from chats.models import UserInChat, Message, CHAT
from common.exceptions.exceptions import IncorrectDialoguePeopleNumber


class ChatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"group_{self.scope["user"].id}")
        await self.channel_layer.group_add(f"group_{self.scope["user"].id}", self.channel_name)
        await self.accept()


    @staticmethod
    def redefine_chats(user_ids):
        channel_layer = get_channel_layer()

        for id in user_ids:
            user_in_chats = UserInChat.objects.filter(user_id=id)
            chats = []
            for relationship in user_in_chats:
                chats += [relationship.chat]

            couples = []

            for chat in chats:
                couples += [(chat, Message.objects.filter(chat_id=chat.id).last())]

            couples = sorted(couples, key=lambda x: x[1].sending_time, reverse=True)

            chats_info = []

            for couple in couples:
                chat = couple[0]
                message = couple[1]

                message_text = message.text[:32] + "..." if message else None

                if chat.format == CHAT:
                    try:
                        chats_info += [{
                            'name': chat.chatinfo.name,
                            'logo': chat.chatinfo.logo.url if chat.chatinfo.logo else None,
                            'message_text': message_text,
                            'format': 'chat', 'chat_id': chat.id}]
                    except ObjectDoesNotExist as e:
                        raise e
                else:
                    users_in_chat = UserInChat.objects.filter(chat_id=chat.id)

                    if len(users_in_chat) != 2:
                        raise IncorrectDialoguePeopleNumber()

                    if id == users_in_chat[0].user.id:
                        another_user = users_in_chat[1].user
                    else:
                        another_user = users_in_chat[0].user

                    chats_info += [{
                        'name': another_user.first_name + " " + another_user.last_name,
                        'logo': another_user.logo.url if another_user.logo else None,
                        'message_text': message_text,
                        'format': 'dialogue',
                        'chat_id': chat.id}
                    ]




            async_to_sync(channel_layer.group_send)(
                f"group_{id}",
                {
                    "type": "chat_message",
                    "text": chats_info
                },
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"websocket_message": event["text"]}))
        print(json.dumps({"websocket_message": event["text"]}))