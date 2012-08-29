from django.contrib import admin
from apps.common.models import Setting

class SettingAdmin(admin.ModelAdmin):
    pass
admin.site.register(Setting, SettingAdmin)