from django.contrib import admin

from users.models import UserInfo, Conversation, Message

admin.site.register(UserInfo)
admin.site.register(Message)
admin.site.register(Conversation)