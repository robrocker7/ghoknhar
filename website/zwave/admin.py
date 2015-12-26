from django.contrib import admin

from .models import Device, Instance, CommandClass

admin.site.register(Device)
admin.site.register(Instance)
admin.site.register(CommandClass)
