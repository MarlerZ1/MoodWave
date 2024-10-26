from django.contrib import admin

from charts.models import Chat, UserInChat, ChatInfo

# Register your models here.

admin.site.register(Chat)
admin.site.register(ChatInfo)
admin.site.register(UserInChat)