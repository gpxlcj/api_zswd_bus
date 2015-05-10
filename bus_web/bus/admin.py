from django.contrib import admin
from models import Bus, Stop, Route, Coordinate, SpecialCoordinate, TestCoordinate
# Register your models here.


class BusAdmin(admin.ModelAdmin):
    list_display = ('number', 'stop', 'route', 'coordinate')
    list_filter = ('route',)


class StopAdmin(admin.ModelAdmin):
    list_display = ('name', 'route', 'longitude', 'latitude', 'arrive_time')
    list_filter = ('route',)


class RouteAdmin(admin.ModelAdmin):
    list_display = ('departure_stop', 'final_stop', 'id')


class SpecialCoAdmin(admin.ModelAdmin):
    list_display = ('route_name', )


admin.site.register(Bus, BusAdmin)
admin.site.register(Stop, StopAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Coordinate)
admin.site.register(SpecialCoordinate, SpecialCoAdmin)
admin.site.register(TestCoordinate)
