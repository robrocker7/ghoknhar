from django.contrib import admin

from website.actions.models import ActionLog, ActionDatastore

admin.site.register(ActionLog)
admin.site.register(ActionDatastore)