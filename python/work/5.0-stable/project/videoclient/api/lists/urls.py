from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^list/*$', views.list, {}, 'api_list_lists'),
    url(r'^add/*$', views.add_list, {}, 'api_add_list'),
    url(r'^delete/*$', views.delete_list, {}, 'api_delete_list'),
)