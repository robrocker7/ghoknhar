from django.contrib import admin
from apps.games.models import Mod, Game

class ModInline(admin.TabularInline):
    model = Mod

class GameAdmin(admin.ModelAdmin):
    inlines = [
        ModInline,
    ]
admin.site.register(Game, GameAdmin)