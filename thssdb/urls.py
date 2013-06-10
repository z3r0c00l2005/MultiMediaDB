from django.conf.urls import patterns, include, url
from multimediadb import views
from django.conf import settings
from django.conf.urls.static import static


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'thssdb.views.home', name='home'),
    # url(r'^thssdb/', include('thssdb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	
    url(r'^types/$', views.typeindex, name='typeindex'),
    url(r'^types/add$', views.typeadd, name='typeadd'),
    url(r'^types/(?P<type_id>\d+)/', views.typeview, name='typeview'),
	
	url(r'^systems/add/(?P<type_id>\d+)/', views.systemadd, name='systemadd'),
	url(r'^systems/(?P<type_id>\d+)/(?P<system_id>\d+)/', views.systemview, name='systemview'),
    url(r'^systems/edit/(?P<type_id>\d+)/(?P<system_id>\d+)/', views.systemedit, name='systemedit'),
    url(r'^systems/comment/system/(?P<type_id>\d+)/(?P<system_id>\d+)/', views.commentadd, name='systemcommentadd'),
    
    url(r'^graphics/add/(?P<type_id>\d+)/(?P<system_id>\d+)/', views.graphicadd, name='graphicadd'),
    url(r'^graphics/edit/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/', views.graphicedit, name='graphicedit'),
    url(r'^graphics/view/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/', views.graphicview, name='graphicview'),
    url(r'^graphics/hold/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/', views.graphicholdtoggle, name='graphichold'),
    url(r'^graphics/done/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/', views.graphicdone, name='graphicdone'),
        
    url(r'^work/add/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/', views.workadd, name='workadd'),
    url(r'^work/edit/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/(?P<work_id>\d+)/', views.workedit, name='workedit'),
    
    url(r'^comment/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/(?P<source>\w+)/(?P<commenttype>\w+)/', views.commentadd, name='commentadd'),
    url(r'^upload/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/(?P<source>\w+)/', views.upload, name='uploadadd'),
    url(r'^download/(?P<pk>\d+)/', views.download_handler, name='download'),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
