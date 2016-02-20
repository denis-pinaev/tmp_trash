from django.conf.urls.defaults import *
from sim.vk.views import * 


urlpatterns = patterns('',
    url(r'^upload/$', upload, name = "vk_upload"),
    url(r'^upload_url/$', upload_url, name = 'vk_upload_url'),
    url(r'^process/$', process, name = 'vk_process'),
)

