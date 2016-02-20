from django.conf.urls.defaults import patterns, include, url
from videoclient.configuration.kpp import views

urlpatterns = patterns('',
    url(r'^new/*$', views.new, name='new_kpp'),
    url(r'^new/(?P<id>\d+)*', views.new, name='update_kpp'),
    url(r'^save/(?P<id>\d+)*', views.update, name='save_kpp'),
    url(r'^change_camera_cpp/', views.change_camera_cpp, name='change_camera_kpp'),
    url(r'^.*$', views.view_kpp, name='kpp_list'),
)
