from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
from videoclient.settings import *
from videoclient.po1.views import *

urlpatterns = patterns('',
    (r'^persons/add/photo', 'po1.views.personsaddphoto'),                       
    (r'^persons/add', 'po1.views.personsadd'),
    (r'^persons/', 'po1.views.persons'),
    (r'^person/(?P<person>.+)/(?P<id>\d+)/', 'po1.views.person'),
    (r'^photos/(?P<person>.+)/(?P<id>\d+)/', 'po1.views.photos'),
    (r'^profile/', 'po1.views.profile'),
    (r'^journal/', 'po1.views.journal'),
    (r'^signal/(?P<param>\d+)/', 'po1.views.signal'),
    (r'^signal/', 'po1.views.signal'),
    (r'^wanted/(?P<param>.+)', 'po1.views.wanted'),
    (r'^wanted/', 'po1.views.wanted'),
    (r'^record/', 'po1.views.record'),
    (r'^kpp/(?P<param>.+)', 'po1.views.kpp'),
    (r'^kpp/', 'po1.views.kpp'),
    (r'^help/', 'po1.views.help'),
    (r'^pageemployee/', 'po1.views.pageemployee'),
    (r'^$', 'po1.views.journal'),
#    (r'^admin/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ADMIN, 'show_indexes': True}),
#    (r'^admin/', include(admin.site.urls)),
#    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True}),
)
