from django.contrib import admin
from multimediadb.models import Aircrafttype, Aircraftsystem, Systemgraphic, Graphicworkdone, Comments, Uploads, QA

class TypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status')
    
class GraphicAdmin(admin.ModelAdmin):
    list_display = ('media_label', 'title', 'description', 'status')
    
class GraphicWDAdmin(admin.ModelAdmin):
    list_display = ('systemgraphic','work_carried_out',)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('source','source_id','comment',)
    
class UploadsAdmin(admin.ModelAdmin):
    list_display = ('file','description',)

class QAAdmin(admin.ModelAdmin):
    list_display = ('systemgraphic','qa_stage','result',)


admin.site.register(Aircrafttype, TypesAdmin)
admin.site.register(Aircraftsystem, SystemAdmin)
admin.site.register(Systemgraphic, GraphicAdmin)
admin.site.register(Graphicworkdone, GraphicWDAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Uploads, UploadsAdmin)
admin.site.register(QA, QAAdmin)
