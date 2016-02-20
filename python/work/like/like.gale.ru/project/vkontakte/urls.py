from django.conf.urls.defaults import *
from vkontakte.views import *

urlpatterns = patterns('',
    url(r'^visit/$', visit, name="vkontakte_visit"),
#    url(r'^$', upload, name="vkontakte_main"),
)



