from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^add/*$', views.add, {}, 'api_add_cameras'),
    url(r'^list/*$', views.list, {}, 'api_list_cameras'),
    url(r'^saved/list/*$', views.saved_cameras, {}, 'api_saved_list_cameras'),
    url(r'^delete/*$', views.delete, {}, 'api_delete_cameras'),
    url(r'^detect/*$', views.detect, {}, 'api_detect_cameras'),    
    url(r'^turn/*$', views.turn, {}, 'api_turn_cameras'),
)