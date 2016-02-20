# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('configuration.web_api_users.views',
    url(r'^users/*$', 'getPageUsers', name='web_api_users'),
    
    url(r'^ip/*$', 'getPageIp', name='user_ip'),
    url(r'^table_ip/*$', 'getTableIp', name='user_table_ip'),    
    url(r'^ip_add/*$', 'getPageIpAdd', name='user_ip_add'),
    url(r'^post_ip_del/*$', 'postIpDel', name='post_ip_del'),
    url(r'^post_ip_add/*$', 'postIpAdd', name='post_ip_add'),
    
    url(r'^security/*$', 'getPageSecurity', name='user_security'),
    url(r'^post_change_key/*$', 'postChangeKeyAccess', name='change_key'),
    
    url(r'^restrictions/*$', 'getPageRestrictions', name='user_restrictions'),
    url(r'^post_restr/*$', 'postTableRestrictions', name='post_restr'),

    
    url(r'^statistics/*$', 'getPageStatistics', name='user_statistics'),
    url(r'^post_table_stat/*$', 'postTableStatistics', name='table_statistics'),
    url(r'^post_data_stat/*$', 'postDataStatistics', name='data_statistics'),
)   