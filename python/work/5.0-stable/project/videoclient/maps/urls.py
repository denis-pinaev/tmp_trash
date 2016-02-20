from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.map, {}, 'maps'),
    url(r'^add-map/', views.view_add_map, {}, 'add-map'),
    url(r'^save-terminal-position/', views.save_terminal_position, {}, 'save-terminal-position'),
    url(r'^clear-map-terminals/', views.clear_map_terminals, {}, 'clear-map-terminals'),
    url(r'^delete-map-terminal/', views.delete_map_terminal, {}, 'delete-map-terminal'),
    url(r'^delete-terminal-camera/', views.delete_terminal_camera, {}, 'delete-terminal-camera'),
    url(r'^add-terminal/', views.add_terminal, {}, 'add-terminal'),
    url(r'^edit-terminal/', views.edit_terminal, {}, 'edit-terminal'),
    url(r'^get-terminal-info/', views.get_terminal_info, {}, 'get-terminal-info'),
    url(r'^get-camera-info/', views.get_camera_info, {}, 'get-camera-info'),
    url(r'^get-camera-video/', views.get_camera_video, {}, 'get-camera-video'),
    url(r'^get-terminal-full-info/', views.get_terminal_full_info, {}, 'get-terminal-full-info'),
    url(r'^add-camera/', views.add_camera, {}, 'add-camera'),
    url(r'^edit-camera/', views.edit_camera, {}, 'edit-camera'),
    url(r'^get-image/(?P<id>[\d\w-]+)/$', views.get_image, {}, 'get-map-image'),
    url(r'^get-video-frame/', views.get_video_frame, {}, 'get-video-frame'),
    url(r'^update-objname-select/$', views.update_objname_select, {}, 'update-obj-name-select'),
    url(r'^(?P<map_id>[\d\w-]+)/$', views.map, {}, 'mapid')
)