from django.conf.urls.defaults import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.turnstiles_list, {}, 'turnstiles_list'),
    url(r'^edit/', views.turnstile_edit, {}, 'turnstile_edit'),
    url(r'^command/', views.turnstile_command, {}, 'turnstiles_command'),
    #url(r'^settings/', views.turnstile_settings, {}, 'turnstile_settings'),
)
