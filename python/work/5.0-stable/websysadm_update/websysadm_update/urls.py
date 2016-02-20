from django.conf.urls.defaults import patterns, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/*(?P<result>[0|1]*)$', 'views.main', name="main"),
    (r'^upload$', 'views.upload'),
    (r'^export/*$', 'views.export'),
    (r'^reboot/$', 'views.reboot'),
    (r'^rebootsystem/$', 'views.rebootsystem'),
    (r'^exportinfo$', 'views.exportinfo'),
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),    
    # Example:
    # (r'^websysadm_update/', include('websysadm_update.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

