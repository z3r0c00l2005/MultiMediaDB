from django.contrib import admin
from multimediadb.models import Aircrafttype, Aircraftsystem, Systemgraphic

class TypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status')
    
class GraphicAdmin(admin.ModelAdmin):
    list_display = ('media_label', 'title', 'description', 'status')

admin.site.register(Aircrafttype, TypesAdmin)
admin.site.register(Aircraftsystem, SystemAdmin)
admin.site.register(Systemgraphic, GraphicAdmin)
