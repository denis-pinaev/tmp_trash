from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^video/*$', views.video, {}, 'api_videoarchive_video'),                           
)