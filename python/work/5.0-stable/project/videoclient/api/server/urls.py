from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^get-server-time/*$', views.get_server_time, {}, 'api_get_server_time'),   
)
