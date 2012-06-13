from django.contrib import admin
from apps.faith.models import Vote, Bar

class VoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vote, VoteAdmin)

class BarAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bar, BarAdmin)
