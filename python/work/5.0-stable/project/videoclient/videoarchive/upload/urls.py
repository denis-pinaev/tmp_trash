from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#from videoclient.videoarchive import upload
import views

urlpatterns = patterns('',
     # Example:
     (r'^ping/$', views.ping),
     (r'^file/$', views.file),
     (r'^new_id/$', views.new_id),
     (r'^check/(?P<id>\d+)/$', views.check),
)
