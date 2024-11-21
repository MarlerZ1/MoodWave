import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from chats.business_logic import ChatsListPageBL, MessagesPageBL
from chats.forms import TextInputForm
from chats.models import UserInChat, Message


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


    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if text_data_json["message_type"] == "delete_message":
            try:
                message_object = await sync_to_async(Message.objects.get)(id=int(text_data_json["message_id"]), user_id=self.scope["user"].id)
                await sync_to_async(message_object.delete)()

                await self.send(text_data=json.dumps({"websocket_message": {
                    "message_type": "delete_message",
                    "message_id": text_data_json["message_id"]
                }}))
            except Message.DoesNotExist as e:
                print(e)
        elif text_data_json["message_type"] == "send_message":
            chat_id = text_data_json["chat_id"]

            form_data = text_data_json.get('form_data')

            form = TextInputForm(form_data)
            form["image"].initial = text_data_json["images_data"]


            if form.is_valid():
                await sync_to_async(form.save)(user_id=self.scope["user"].id, chat_id=chat_id)


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"websocket_message": event["text"]}))
        print(json.dumps({"websocket_message": event["text"]}))