from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    (r'^cameras/', include('api.cameras.urls')),
    (r'^server/', include('api.server.urls')),
    (r'^communicators/', include('api.communicators.urls')),
    (r'^lists/', include('api.lists.urls')),
    (r'^log/', include('api.log.urls')),
    (r'^persons/', include('api.persons.urls')),
    (r'^videoarchive/', include('api.videoarchive.urls')),
    (r'^status_thread/', include('videoclient.status_thread.urls')),
)
