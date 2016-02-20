from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#admin.autodiscover()
#from videoarchive import settings
from videoclient import settings
from videoarchive import views

#import django_cron
#django_cron.autodiscover()

if settings.ARCHIVE_URL == "":
    MEDIA_ADMIN = settings.WWW_ROOT+'admin/media/'
    MEDIA_ROOT = settings.WWW_ROOT+'files/'
else:
    from videoclient import settings
    MEDIA_ADMIN = settings.MEDIA_ROOT+settings.ARCHIVE_URL+'/admin/media/'
    MEDIA_ROOT = settings.MEDIA_ROOT+settings.ARCHIVE_URL+'/files/'

    
MEDIA_ADMIN_TOOLS = MEDIA_ROOT+'admin_tools/'

import os

TEMPLATE_DIRS = (
    os.path.join( os.path.dirname(__file__), 'templates'),                 
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
) 

urlpatterns = patterns('',
#    url(r'^admin_tools/', include('admin_tools.urls')),
    #(r'^$', 'videoarchive.views.login'),
    #(r'^admin', include(admin.site.urls)),
    #(r'^logout/$', 'videoarchive.views.logout'),
    #url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^upload/', include('videoarchive.upload.urls')),
    
    #(r'^admin/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ADMIN, 'show_indexes': True}),
    #(r'^admin_tools/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ADMIN_TOOLS, 'show_indexes': True}),
    url(r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True}, name='archive_files'),
    (r'^start_processes/$', 'videoarchive.views.start_processes'),
    #(r'^person/', include('videoarchive.person.urls')),    
    (r'^settings/', include('videoarchive.archive_settings.urls')),
    #(r'^communicator/', include('videoarchive.communicator.urls')),
    (r'^command/(?P<path>.*)$', 'videoarchive.views.command', {}, "archive_command"),
    (r'^download/(?P<id>.*)$', 'videoarchive.views.DownloadVideo', {}, "archive_download_video"),
    (r'^gettmpfile/', 'videoarchive.views.gettmpfile'),
    (r'^(?P<path>.*)$', 'videoarchive.views.pages', {}, "archive_page"),
    url(r'^calendar/$', views.pages, {}, "archive"),
)
