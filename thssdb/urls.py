from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from multimediadb import views
from django.conf import settings
from django.conf.urls.static import static


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.typeindex, name='home'),
    
    url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
	url(r'^accounts/new/$',  views.create_login, name='newuser'),
	url(r'^accounts/newpass/(?P<user_id>\d+)/(?P<source>\w+)/',  views.change_password, name='changepassword'),
	url(r'^accounts/all/$',  views.userindex, name='allusers'),
	url(r'^accounts/edit/(?P<user_id>\d+)/',  views.edit_user, name='edituser'),
	    
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

    url(r'^graphics/qa/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/', views.qaview, name='qaview'),
    url(r'^graphics/qaresult/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/(?P<graphic_version>\d+)/(?P<stage>\w+)/(?P<qa_id>\d+)/(?P<result>\w+)/', views.qaresult, name='qaresult'),
        
    url(r'^work/add/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/', views.workadd, name='workadd'),
    url(r'^work/edit/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/(?P<work_id>\d+)/', views.workedit, name='workedit'),
    
    url(r'^comment/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/(?P<graphic_version>\d+)/(?P<source>\w+)/(?P<commenttype>\w+)/', views.commentadd, name='commentadd'),
    
    url(r'^upload/(?P<type_id>\d+)/(?P<system_id>\d+)/(?P<graphic_id>\d+)/(?P<source>\w+)/', views.upload, name='uploadadd'),
    url(r'^download/(?P<pk>\d+)/', views.download_handler, name='download'),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
