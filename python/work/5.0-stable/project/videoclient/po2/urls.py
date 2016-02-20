# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import *
from videoclient.settings import *
from videoclient.po2 import *

urlpatterns = patterns('',
    (r'^$', 'po2.views.user'),                   
    (r'^user/', 'po2.views.user'),
    (r'^userphotos/', 'po2.views.userphotos'),
    (r'^pageemployee/', 'po2.views.pageemployee'),
    (r'^help/', 'po2.views.help'),
    (r'^anketa/', 'po2.views.anketa'),
    (r'^anketaclear/', 'po2.views.anketaclear'),                       
)