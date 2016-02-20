from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    #url(r'^add/*$', views.add, {}, 'api_add_cameras'),
    url(r'^list/*$', views.list, {}, 'api_list_persons'),
    url(r'^manage/*$', views.manage, {}, 'api_manage_persons'),
    url(r'^delete/*$', views.delete, {}, 'api_delete_persons'),
    url(r'^delete_all/*$', views.delete_all, {}, 'api_delete_all_persons'),
    (r'^photos/', include('api.persons.photos.urls')),                           
)