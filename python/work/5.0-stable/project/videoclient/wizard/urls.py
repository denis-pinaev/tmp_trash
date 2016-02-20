from django.conf.urls.defaults import patterns, include, url
import settings
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^globalparams/*$', 'wizard.views.settings_globalparams'),
    (r'^balancer/*$', 'wizard.views.settings_balancer'),
    #(r'^videoarchive/*$', 'wizard.views.settings_videoarchive'),
    (r'^fin/*$', 'wizard.views.settings_fin'),
    (r'^restart-cs/*$', 'wizard.views.restart_cs', {}, 'restart-cs'),
    (r'^communicator/(?P<step>\d+)/*$', 'wizard.views.settings_communicator'),
    (r'^communicator/*$', 'wizard.views.settings_communicator'),
    (r'^user/*$', 'wizard.views.settings_user'),    
    (r'^.*$', 'wizard.views.settings_user'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)