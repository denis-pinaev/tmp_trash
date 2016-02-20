from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^archive/(?P<id>\d*)', views.archive, name="archive_settings_archive"),
    url(r'^add_archive/', views.add_archive, name="add_archive"),
    url(r'^delete_archive/', views.delete_archive, name="delete_archive"),
    url(r'^tasks/*', views.tasks, name="archive_settings_tasks"),
#    url(r'^communicators/*', views.communicators, name="archive_settings_communicators"),
#    url(r'^add_communicator/', views.add_communicator, name='add_communicator'),
#    url(r'^delete_communicator/', views.delete_communicator, name='delete_communicator'),
)