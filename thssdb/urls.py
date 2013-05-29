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
    url(r'^types/(?P<type_id>\d+)/', views.typeview, name='typeview'),
)
