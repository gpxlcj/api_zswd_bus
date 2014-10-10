from django.contrib import admin
from models import Bus, Stop, Route, Coordinate,SpecialCoordinate
# Register your models here.

class BusAdmin(admin.ModelAdmin):
    list_display = ('number', 'stop', 'route')
    list_filter = ('route',)

class StopAdmin(admin.ModelAdmin):
    list_display = ('name', 'route', 'longitude', 'latitude', 'arrive_time')
    list_filter = ('route',)

class RouteAdmin(admin.ModelAdmin):
    list_display = ('departure_stop', 'final_stop')



admin.site.register(Bus, BusAdmin)
admin.site.register(Stop, StopAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Coordinate)
admin.site.register(SpecialCoordinate)
