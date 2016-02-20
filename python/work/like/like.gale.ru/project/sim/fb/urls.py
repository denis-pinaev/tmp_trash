from django.conf.urls.defaults import *
from sim.fb.views import *


urlpatterns = patterns('',
    url(r'iframe/$', 'sim.fb.views.iframe'),
    url(r'^upload/$', upload, name = "fb_upload"),
    url(r'^upload_url/$', upload_url, name = 'fb_upload_url'),
    url(r'^process/$', process, name = 'fb_process'),

    url(r'^test/$', test, name = 'fb_test'),

)

