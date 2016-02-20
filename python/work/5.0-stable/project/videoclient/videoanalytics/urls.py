# coding=utf-8
from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.journal_videoanalytics, {}, 'journal-videoanalytics'),
    #Вынесен в основной urls.py для того чтобы сменить префикс урла с settings на journal 
    #url(r'^journal/', views.journal_videoanalytics, {}, 'journal-videoanalytics'),
    url(r'^settings/$', views.settings_videoanalytics, {}, 'settings_videoanalytics'),
    url(r'^settings/(?P<uuid>[\d\w-]+)/$', views.settings_videoanalytics, {}, 'settings_videoanalytics2'),
    url(r'^set_settings_videoanalytics/$', views.set_settings_videoanalytics, {}, 'set_settings_videoanalytics'),
    url(r'^bg-generation/$', views.bg_generation, {}, 'bg_generation'),
    url(r'^get-preview-image/(?P<id>[\d\w-]+)/$', views.get_preview_image, {}, 'get_preview_image'),
    url(r'^get-original-image/(?P<id>[\d\w-]+)/$', views.get_original_image, {}, 'get_original_image'),
    url(r'^clear-journal/$', views.clearjournal, {}, 'clear_journal_va'),
    url(r'^check-detector-warnings/$', views.check_detector_warnings, {}, 'check_detector_warnings'),
) 
