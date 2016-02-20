from django.conf.urls.defaults import patterns, include, url
import settings
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$',  login, {"template_name": "control_settings_login.html"}),
    (r'^accounts/logout/$', logout, {"next_page": "/control_settings/users/"}),
    (r'^users/$', 'control_settings.views.user_list'),
    url(r'^user/*(?P<uid>[^/]*)$', 'control_settings.views.user_list', name="user"),
    (r'^users/+(?P<num>[^/]+)$', 'control_settings.views.user_list'),
    (r'^add_user/*$', 'control_settings.views.add_user'),
    (r'^add_param/*$', 'control_settings.views.add_param'),
    (r'^export_settings/*$', 'control_settings.views.export_settings'),
    (r'^import_settings/*$', 'control_settings.views.import_settings'),
    (r'^delete_param/*$', 'control_settings.views.delete_param'),
    (r'^rename_param/*$', 'control_settings.views.rename_param'),
    (r'^copy_param/*$', 'control_settings.views.copy_param'),
    (r'^settings/*$', 'control_settings.views.all_params'),
    (r'^save_settings/*$', 'control_settings.views.save_params'),
    (r'^default/*$', 'control_settings.views.default_params'),
    (r'^smedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^rebootsystem/$', 'control_settings.views.rebootsystem', {}, "rebootsystem"),
    (r'^(?P<num>[0-9]+)*$', 'control_settings.views.user_list'),
    (r'^.*$', 'control_settings.views.user_list'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)