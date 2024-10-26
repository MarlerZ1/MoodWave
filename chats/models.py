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