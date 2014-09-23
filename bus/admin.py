from django.contrib import admin
from models import Bus, Stop, Route, Coordinate,SpecialCoordinate
# Register your models here.

admin.site.register(Bus)
admin.site.register(Stop)
admin.site.register(Route)
admin.site.register(Coordinate)
admin.site.register(SpecialCoordinate)