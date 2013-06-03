from django.conf.urls import patterns, include, url
from multimediadb import views

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
    
    url(r'^graphics/add/(?P<type_id>\d+)/(?P<system_id>\d+)/', views.graphicadd, name='graphicadd'),
    url(r'^graphics/edit/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/', views.graphicedit, name='graphicedit'),
)
