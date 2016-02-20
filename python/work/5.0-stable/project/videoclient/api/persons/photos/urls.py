from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^list/*$', views.list, {}, 'api_list_photos'),
    url(r'^left/*$', views.left, {}, 'api_left_photos'),    
)