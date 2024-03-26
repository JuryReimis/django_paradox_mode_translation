from django.contrib import admin
from django.contrib.admin import ModelAdmin

from moderators.models import Query

admin.site.register(Query)

