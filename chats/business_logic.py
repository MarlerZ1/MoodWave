from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from chats.web.forms import TextInputForm
from chats.models import Message, CHAT, UserInChat, AttachmentImage
from common.exceptions.exceptions import IncorrectDialoguePeopleNumber, UserToChatAccessError


class MessagesPageBL:
    @staticmethod
    def get_formated_messages(messages, chat_id, user_id):
        users_in_chat = UserInChat.objects.filter(chat_id=chat_id)

        messages = messages.filter(user_id__in=[user.user_id for user in users_in_chat], chat_id=chat_id)

        messages = [MessagesPageBL.get_formated_message(message, user_id) for message in messages]

        return messages

    @staticmethod
    def get_formated_message(message,user_id):
        return {
            'message_type': 'new_message',
            'message_id': message.id,
            'from_me': message.user_id == user_id,
            'name': message.user.first_name + " " + message.user.last_name,
            'text': message.text,
            'logo_url': message.user.logo.url if message.user.logo else None,
            'image_url': images[0].image.url if (images := AttachmentImage.objects.filter(message_id=message.id)) else None
        }

class ChatsListPageBL:
    @staticmethod
    async def delete_message(text_data_json, user_id):
        try:
            message_object = await sync_to_async(Message.objects.get)(id=int(text_data_json["message_id"]), user_id=user_id)
            await sync_to_async(message_object.delete)()
        except Message.DoesNotExist as e:
            print(e)
            raise e

    @staticmethod
    def send_message(text_data_json, user_id):
        chat_id = text_data_json["chat_id"]

        try:
            user_in_chat = UserInChat.objects.filter(user_id=user_id)
            chat_ids = []
            for relationship in user_in_chat:
                chat_ids += [relationship.chat.id]

            if chat_id not in chat_ids:
                raise UserToChatAccessError()
        except UserToChatAccessError as e:
            print(e, user_id)

        form_data = text_data_json.get('form_data')

        form = TextInputForm(form_data)
        form["image"].initial = text_data_json["images_data"]

        if form.is_valid():
            form.save(user_id=user_id, chat_id=chat_id)

    @staticmethod
    def get_chats(user_in_chat, auth_user_id):
        user_in_chat = user_in_chat.filter(user_id=auth_user_id)
        chats = []
        for relationship in user_in_chat:
            chats += [relationship.chat]

        couples = []

        for chat in chats:
            last_msg = Message.objects.filter(chat_id=chat.id).last()
            if last_msg:
                couples += [(chat, last_msg)]

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
                        'format': 'chat',
                        'chat_id': chat.id}
                    ]
                except ObjectDoesNotExist as e:
                    raise e
            else:

                users_in_chat = UserInChat.objects.filter(chat_id=chat.id)

                if len(users_in_chat) != 2:
                    raise IncorrectDialoguePeopleNumber()

                if auth_user_id == users_in_chat[0].user.id:
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

        return chats_info