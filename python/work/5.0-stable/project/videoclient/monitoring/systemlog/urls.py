from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^journal$', views.syslog_journal, {}, "syslog_journal"),
)