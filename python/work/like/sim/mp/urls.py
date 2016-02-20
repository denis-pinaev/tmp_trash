from django.conf.urls.defaults import *
from sim.mp.views import *


urlpatterns = patterns('',
    url(r'iframe/$', 'sim.mp.views.iframe'),
    url(r'^upload/$', upload, name = "mp_upload"),
    url(r'^upload_url/$', upload_url, name = 'mp_upload_url'),
    url(r'^process/$', process, name = 'mp_process'),

)

