from django.conf.urls.defaults import patterns, include, url
import settings

urlpatterns = patterns('',
    (r'^camera/$', 'distortion.views.camera', {}, 'distortion-camera'),
    (r'^camera/(?P<uuid>[\d\w-]+)/(?P<local_person_id>[\d\w-]+)/$', 'distortion.views.camera', {}, 'distortion-camera2'),
    (r'^set-distortion-by-points/$', 'distortion.views.set_distortion_by_points', {}, 'set_distortion_by_points'),
    (r'^get-image-with-distortion/$', 'distortion.views.get_image_with_distortion', {}, 'get_image_with_distortion'),
    (r'^upload-image-for-distortion/$', 'distortion.views.upload_image_for_distortion', {}, 'upload_image_for_distortion'),
    (r'^set/*$', 'distortion.views.set_distortion'),
    (r'^.*$', 'distortion.views.set_distortion'),
)