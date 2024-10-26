from django.contrib import admin

from chats.models import Chat, UserInChat, ChatInfo, Message

# Register your models here.

admin.site.register(Chat)
admin.site.register(ChatInfo)
admin.site.register(UserInChat)
admin.site.register(Message)