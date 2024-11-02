from django.core.exceptions import ObjectDoesNotExist

from chats.models import Message, CHAT, UserInChat
from common.exceptions.exceptions import IncorrectDialoguePeopleNumber



class ChatsListPageBL:
    @staticmethod
    def get_chats(user_in_chat, auth_user_id):
        user_in_chat = user_in_chat.filter(user_id=auth_user_id)
        chats = []
        for relationship in user_in_chat:
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