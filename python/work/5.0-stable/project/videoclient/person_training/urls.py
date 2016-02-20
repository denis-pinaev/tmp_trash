from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^person/(?P<local_person_id>[\d\w-]+)/$', views.training, {}, 'person_training'),
    url(r'^params/(?P<uuid>[\d\w-]+)/(?P<local_person_id>[\d\w-]+)/$', views.training, {}, 'person_training2'),
    url(r'^training/$', views.get_training_photos, {}, 'get_training_photos'),
    url(r'^edit/(?P<uuid>[\d\w-]+)/(?P<local_person_id>[\d\w-]+)/$', views.edit_photos, {}, 'edit_photos'),
    url(r'^persons/$', views.edit_persons, {}, 'edit_persons'),
    url(r'^person-form/$', views.person_form, {}, 'get-create-person-for-training'),
    url(r'^get-or-create-person/$', views.get_or_create_person, {}, 'get-or-create-person'),
    url(r'^result/$', views.training_result, {}, 'training-result'),
)
