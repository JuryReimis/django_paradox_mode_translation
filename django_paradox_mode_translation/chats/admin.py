from django.contrib import admin

from chats.models import PrivateChat, PrivateMessage, TeamChat, TeamMessage

admin.site.register(PrivateChat)
admin.site.register(PrivateMessage)
admin.site.register(TeamChat)
admin.site.register(TeamMessage)
