from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from translators_hub.models import ModTranslation, UserProfile, Titles, ProfileComments, Game, Roles, Invites

admin.site.register(ModTranslation)
admin.site.register(Roles)
admin.site.register(Invites)
admin.site.register(UserProfile)
admin.site.register(Titles)
admin.site.register(ProfileComments)
admin.site.register(Game)

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass
