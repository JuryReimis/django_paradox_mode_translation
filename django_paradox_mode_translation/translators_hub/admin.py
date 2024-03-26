from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from translators_hub.models import Translation, UserProfile, Titles, ProfileComments, Game, Roles, Invites, \
    ProjectComments, ProjectCommentsReaction, ProfileCommentsReaction, Language

admin.site.register(Translation)
admin.site.register(Roles)
admin.site.register(Invites)
admin.site.register(UserProfile)
admin.site.register(Titles)
admin.site.register(ProfileComments)
admin.site.register(ProfileCommentsReaction)
admin.site.register(ProjectComments)
admin.site.register(ProjectCommentsReaction)
admin.site.register(Game)
admin.site.register(Language)

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass
