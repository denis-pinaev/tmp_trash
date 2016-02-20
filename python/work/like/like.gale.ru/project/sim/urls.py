from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include( admin.site.urls)),
    (r'^vk/', include( 'sim.vk.urls')),
    (r'^fb/', include( 'sim.fb.urls')),
)

