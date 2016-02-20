from django.conf.urls.defaults import *
from wizer.vkontakte.adm.views import *

urlpatterns = patterns('',
    url(r'^dispatch/', dispatch, name="vkontakte_dispatch"),
)



