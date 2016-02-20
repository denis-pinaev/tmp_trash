# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *
from videoclient.settings import *
from videoclient.po2 import *

urlpatterns = patterns('',
    (r'^$', 'po3.views.wanted'),                   
    (r'^wanted/', 'po3.views.wanted'),
    (r'^wantedphotos/', 'po3.views.wantedphotos'),
    (r'^pageemployee/', 'po3.views.pageemployee'),
    (r'^help/', 'po3.views.help'),
    (r'^anketawanted/', 'po3.views.anketawanted'),
    (r'^anketawantedclear/', 'po3.views.anketawantedclear'),
    (r'^guards/', 'po3.views.guards'),
    (r'^anketaguard/(?P<id>\d+)/', 'po3.views.anketaguard'),
    (r'^anketaguard/', 'po3.views.anketaguard'),
    (r'^guardphotos/', 'po3.views.guardphotos'),
)