from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from sim import settings

urlpatterns = patterns('',
    (r'^admin/', include( admin.site.urls)),
    (r'^fb/', include( 'sim.fb.urls')),
    (r'^wizers/', include( 'sim.wizers.urls')),
    (r'^wizer/', include( 'sim.wizers.urls')),
    (r'^mymail/', 'sim.fb.views.mymail'),    
    (r'^files/media/tmp/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+settings.TMP_IMG+"tmp/"}),
    (r'^files/media/preview/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+settings.TMP_IMG+"preview/"}),
    (r'^files/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+settings.STORE_IMG}),
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.WWW_ROOT+"/files/"}),    
)

