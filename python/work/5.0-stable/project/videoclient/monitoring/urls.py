from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    (r'^syslog/', include('videoclient.monitoring.systemlog.urls')),
    url(r'^$', views.events, name="monitoring"),
    url(r'^events/$', views.events, name='monitoring_events'),
    url(r'^system/$', views.system, name='monitoring_system'),
    url(r'^system/(?P<uuid>[\d\w-]+)/$', views.system, {}, 'monitoring_system2'),
    
    url(r'^videoanalytics/$', views.videoanalytics, name='monitoring_videoanalytics'),
    url(r'^videoanalytics/(?P<uuid>[\d\w-]+)/$', views.videoanalytics, {}, 'monitoring_videoanalytics2'),
    url(r'^get_camera_va_statistics_js/$', views.get_camera_va_statistics_js, name='monitoring_get_camera_va_statistics_js'),
    
    
    url(r'^versions/$', views.versions, name='monitoring_versions'),
    
    url(r'^communicator/$', views.communicator, name='monitoring_communicator'),
    url(r'^communicator/(?P<uuid>[\d\w-]+)/$', views.communicator, {}, 'monitoring_communicator2'),
    url(r'^get_camera_frames_statistics_js/$', views.get_camera_frames_statistics_js, name='monitoring_get_camera_frames_statistics_js'),
    
    
    url(r'^get_upload_file/(?P<path>.+)/', views.get_upload_file, {}, 'monitoring_get_upload_file'),
    url(r'^alert/', views.alert, name="monitoring_alert"),
    url(r'^checkmessage/$', views.checkmessage, name='monitoring_checkmessage'),
    url(r'^export_events_journal/$', views.export_events_journal, name='export_events_journal'),
    url(r'^download_zip_journal/$', views.download_events_journal_zip, name='download_zip_journal'),
    url(r'^testfr/start_test/', views.start_test, name='monitoring_testfr_start_test'),
    url(r'^testfr/', views.testfr, name='monitoring_testfr'),
    url(r'^upload_recognition/', views.upload_recognition, name='upload_recognition'),
)