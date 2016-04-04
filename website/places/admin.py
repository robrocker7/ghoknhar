from django.contrib import admin

from .models import Place, PlaceMonitor, MonitorResults, MonitorRoute, MonitorFrequency

admin.site.register(Place)
admin.site.register(PlaceMonitor)
admin.site.register(MonitorResults)
admin.site.register(MonitorRoute)
admin.site.register(MonitorFrequency)