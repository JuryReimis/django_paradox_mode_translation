from django.contrib import admin
from django.contrib.admin import ModelAdmin

from teams.models import Teams, TeamMembers, TeamInvites

admin.site.register(TeamMembers)
admin.site.register(TeamInvites)


@admin.register(Teams)
class TeamsAdmin(ModelAdmin):

    prepopulated_fields = {'slug': ['team_title']}




