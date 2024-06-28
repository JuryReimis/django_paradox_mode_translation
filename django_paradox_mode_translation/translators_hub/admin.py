from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from translators_hub.models import Translation, Titles, Game, Roles, Invites, \
    Language

admin.site.register(Translation)
admin.site.register(Roles)
admin.site.register(Invites)
admin.site.register(Titles)
admin.site.register(Game)
admin.site.register(Language)

User = get_user_model()

# @admin.register(User)
# class UserAdmin(UserAdmin):
#     pass
