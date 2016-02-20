from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     # Example:
     (r'^anketa/*(?P<pid>[0-9]*)/*$', 'videoarchive.person.views.anketa'),     
     (r'^addphotoperson/(?P<select_page>.+)/(?P<id>[0-9]+)/', 'videoarchive.person.views.addphotoperson'),
     (r'^choose_camera/(?P<select_page>[^/]+)/(?P<id>.+)/', 'videoarchive.person.views.choose_camera'),
     (r'^learn_camera/(?P<select_page>.+)/(?P<communicator>\d+)/(?P<numcamera>\d+)/(?P<person>.*)/', 'videoarchive.person.views.learn_camera'),
     (r'^upload/(?P<session_key>.+)/(?P<name_person>.+)/$', 'videoarchive.person.views.upload'),
     (r'^photosperson/(?P<id>\d+)/*', 'videoarchive.person.views.photosperson'),
     (r'^image/', 'videoarchive.person.views.image'),
     (r'^export/*', 'videoarchive.person.views.export'),
     (r'^exportfile/', 'videoarchive.person.views.exportfile'),
     (r'^delete_person/$', 'videoarchive.person.views.delete_person'),
     (r'^changepersonname/$', 'videoarchive.person.views.changepersonname'),  
     (r'^url_name_person/', 'videoarchive.person.views.url_name_person'),
     (r'^execute_method/$', 'videoarchive.person.views.execute_method'),
     (r'^execute_method_balancer/$', 'videoarchive.person.views.execute_method_balancer'),   
     (r'^.*$', 'videoarchive.person.views.anketa'),
)
