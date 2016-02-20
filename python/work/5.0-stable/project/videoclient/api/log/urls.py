from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^data/videoanalytics/*$', views.data, {"type":"va"}, 'api_get_videoanalytics_log'),
    url(r'^data/faces/*$', views.data, {"type":"ident"}, 'api_get_faces_log'),
    url(r'^last_data/videoanalytics/*$', views.last_data, {"type":"va"}, 'api_get_videoanalytics_last_log'),
    url(r'^last_data/faces/*$', views.last_data, {"type":"ident"}, 'api_get_faces_last_log'),                           
)