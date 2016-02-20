# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('security.views',
    url(r'^.*$', 'security', name='security'),
)   