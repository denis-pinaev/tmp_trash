from django.conf.urls.defaults import patterns, include, url
import settings

urlpatterns = patterns('',
    (r'^camera/save/*$', 'profile.camera.save'),
    (r'^camera/apply/*$', 'profile.camera.apply_profile'),
    (r'^camera/addprofile/*$', 'profile.camera.add_profile'),
    (r'^camera/delete/*$', 'profile.camera.delete'),
    #(r'^.*$', include('videoclient.urls')),
)