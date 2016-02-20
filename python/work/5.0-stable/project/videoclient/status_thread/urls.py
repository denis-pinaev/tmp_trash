from django.conf.urls.defaults import patterns, include, url
import views

import status_thread

urlpatterns = patterns('',
    url(r'^list/*$', views.list, {}, 'api_status_thread_list'),
)
