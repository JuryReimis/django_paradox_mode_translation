from django.contrib import admin

from chats.models import PrivateChat, PrivateMessage

admin.site.register(PrivateChat)
admin.site.register(PrivateMessage)
