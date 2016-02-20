from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^universal/', views.universal, {}, 'integration_universal'),
    url(r'^smtp/', views.smtp, {}, 'integration_smtp'),
    url(r'^snmp/', views.snmp, {}, 'integration_snmp'),
    url(r'^$', views.universal, {}, 'integration'),
)