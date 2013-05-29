from django.contrib import admin
from multimediadb.models import Aircrafttype, Aircraftsystem

class TypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Aircrafttype, TypesAdmin)
admin.site.register(Aircraftsystem, SystemAdmin)
