from django.contrib import admin
from django.contrib.admin import ModelAdmin

from moderators.models import Query, Topic

admin.site.register(Query)
admin.site.register(Topic)
