import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class ChatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"group_{self.scope["user"].id}")
        await self.channel_layer.group_add(f"group_{self.scope["user"].id}", self.channel_name)
        await self.accept()


    @staticmethod
    def redefine_chats(users):
        channel_layer = get_channel_layer()

        for user in users:
            async_to_sync(channel_layer.group_send)(
                f"group_{user.id}",
                {
                    "type": "chat_message",
                    "text": "SendMessageWeb"
                },
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"websocket_message": event["text"]}))