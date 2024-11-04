from django.db import models

from authorization.models import User


CHAT = 0
DIALOGUE = 1


# Create your models here.


class Chat(models.Model):
    FORMATS = (
        (CHAT, "Беседа"),
        (DIALOGUE, "Личка")
    )
    format = models.PositiveSmallIntegerField(default=DIALOGUE, choices=FORMATS)

class ChatInfo(models.Model):
    name = models.CharField(max_length=127,null=False, blank=True)
    chat = models.OneToOneField(to=Chat, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(upload_to='chat_logo', null=True, blank=True)


class UserInChat(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)

class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False)
    sending_time = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, has_attach_image=None,user_ids=None):
        super().save(force_insert, force_update, using, update_fields)

        if not user_ids:
            user_ids = [user_in_chat.user.id for user_in_chat in UserInChat.objects.filter(chat=self.chat)]

        from chats.consumers import ChatsConsumer
        from chats.consumers import MessagesConsumer
        ChatsConsumer.redefine_chats(user_ids) # WHERE IS A PROBLEM WITH ATTACHMENT IMAGE VISABILITY IN CHAT LIST

        if not has_attach_image:
            MessagesConsumer.redefine_messages(self, user_ids)

class AttachmentImage(models.Model):
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='attachment_image')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None,user_ids=None):
        super().save(force_insert, force_update, using, update_fields)

        from chats.consumers import MessagesConsumer
        MessagesConsumer.redefine_messages(self.message, user_ids)