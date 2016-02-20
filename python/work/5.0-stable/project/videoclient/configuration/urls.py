from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    (r'^integration/', include('configuration.integration.urls')),
    (r'^web_api/', include('configuration.web_api_users.urls')),
    (r'^turnstiles/', include('configuration.turnstiles.urls')),
    (r'^setup/', include('configuration.setup.urls')),
    (r'^kpp/', include('configuration.kpp.urls')),
)
