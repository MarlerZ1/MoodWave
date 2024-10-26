from django.contrib import admin

from chats.models import Chat, UserInChat, ChatInfo

# Register your models here.

admin.site.register(Chat)
admin.site.register(ChatInfo)
admin.site.register(UserInChat)