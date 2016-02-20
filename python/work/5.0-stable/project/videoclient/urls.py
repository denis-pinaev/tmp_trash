# coding=utf-8
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from videoclient.settings import *
import views
from videoclient.videoanalytics import views as viViews

urlpatterns = patterns('',
    (r'^api/', include('videoclient.api.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^status_thread/', include('videoclient.status_thread.urls')),
    (r'^flashpolicy.xml$', 'django.views.static.serve', {'document_root': WWW_ROOT, 'show_indexes': True, 'path': 'flashpolicy.xml'}),
    (r'^crossdomain.xml$', 'django.views.static.serve', {'document_root': WWW_ROOT, 'show_indexes': True, 'path': 'crossdomain.xml'}),
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/translations/', include('videoclient.rosetta.urls')),
    #(r'^localeurl/', include('videoclient.localeurl.urls')),
    url(r'^map/', include('videoclient.maps.urls')),
    
    (r'^settings/', include('videoclient.configuration.urls')),
    (r'^settings/videoanalytics/', include('videoclient.videoanalytics.urls')),
    (r'^settings/recognition/$', 'videoclient.views.settings_recognition', {}, 'settings_recognition'),
    (r'^settings/users/', 'videoclient.po4.views.users', {}, 'settings_user'),
    (r'^control_settings/', include('videoclient.control_settings.urls')),  # необходимо перенести url в settings
    (r'^settings/interface/$', 'videoclient.po4.views.settings_interface', {}, 'settings_interface'),
    
    # Вынесено в основной urls.py для того что бы префикс урла был journal а не settings, было бы неплохо вынести его в отдельный модуль и назвать его logs
    (r'^journal/videoanalytics/', 'videoclient.videoanalytics.views.journal_videoanalytics', {}, 'journal-videoanalytics'), 
    
    
    (r'^training/', include('videoclient.person_training.urls')),
    url(r'^logdetector/$', viViews.log_detect, {}, 'log_detect'),
    url(r'^logdetector_package/$', viViews.log_detect_package, {}, 'log_detect_package'),
    (r'^archive/', include('videoclient.videoarchive.urls')),    
    (r'^security/', include('videoclient.security.urls')),
    (r'^image/', 'videoclient.views.image'),
    (r'^settings/(?P<uuid>[\d\w-]+)/', 'videoclient.views.camera', {}, 'camera-settings'),
    (r'^settings/', 'videoclient.views.settings', {}, 'communicator_settings'),
    (r'^$', 'videoclient.views.login'),
    (r'^login/$', 'videoclient.views.login'),
    (r'^logout/$', 'videoclient.views.logout'),
    (r'^execute_method/$', 'videoclient.views.execute_method'),
    (r'^addphotoperson/(?P<select_page>.+)/(?P<id>.+)/upload_multiple/resault/', 'videoclient.views.upload_multiple_resault', {}, 'upload_multiple_resault'),
    (r'^addphotoperson/(?P<select_page>.+)/(?P<id>.+)/upload_multiple/', 'videoclient.views.upload_multiple', {}, 'upload_multiple'),
    (r'^get_upload_image/(?P<path>.+)/', 'videoclient.views.get_upload_image', {}, 'get_upload_image'),
    (r'^set_default_params/', 'videoclient.views.set_default_params', {}, 'set_default_params'),
    (r'^json_sdk/', 'videoclient.views.json_sdk', {}, 'json_sdk'),
    (r'^logperson_package', 'videoclient.views.logperson_package', {}, 'logperson_package'),
    
    
    #(r'^logperson/', 'videoclient.views.logperson'),
    (r'^checkjournal/*', 'videoclient.views.checkjournal'),
    (r'^ident/$', 'videoclient.views.ident'),
    (r'^ident/(?P<uuid>[\d\w-]+)/$', 'videoclient.views.ident', {}, 'js_ident'),
    (r'^get-ident-video-frame/', 'videoclient.views.get_ident_video_frame', {}, 'get-ident-video-frame'),
    (r'^get-ident-video-frame-detects-free/', 'videoclient.views.get_ident_video_frame_detects_free', {},'get-ident-video-frame-detects-free'),
    (r'^get-all-video-frames/', 'videoclient.views.get_all_video_frames', {}, 'get-all-video-frames'),
    (r'^get-ident-person-info/', 'videoclient.views.get_ident_person_info', {}, 'get-ident-person-info'),
    (r'^execute-communicator-method/', 'videoclient.views.executeCommunicatorMethod', {}, 'execute-communicator-method'),
    (r'^get-extended-video-info/', 'videoclient.views.get_extended_video_info', {}, 'get-extended-video-info'),
    (r'^big-video-frame-info/$', 'videoclient.views.big_video_frame_info', {}, 'big-video-frame-info'),
    (r'^help/$', 'videoclient.views.help'),
    (r'^set_alias_camera/*', 'videoclient.views.set_alias_camera'),
    (r'^check_similar_camera/*', 'videoclient.views.check_similar_camera', {}, 'check_similar_camera'),
    (r'^delete_person/$', 'videoclient.views.delete_person', {}, 'vc_delete_person'),
    (r'^execute_method_balancer/$', 'videoclient.views.execute_method_balancer'),
    (r'^change_language/', 'videoclient.views.change_language'),
    (r'^distortion_settings/(?P<communicator>\d+)/(?P<numcamera>\d+)/(?P<cameramode>\d+)/', 'videoclient.views.distortion_settings'),
    (r'^admin/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ADMIN, 'show_indexes': True}),
    (r'^admin_tools/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ADMIN_TOOLS, 'show_indexes': True}),
    (r'^admin/', include(admin.site.urls)),
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True}),
    (r'^employee/*(?P<journalid>.*)$', 'videoclient.views.employee'),
    (r'^journal/(?P<journal_id>[\d\w-]+)/(?P<ptype>\w+)/$', views.get_journal_photo, {}, 'get-journal-photo'),
    (r'^journal/', 'videoclient.views.journal', {}, 'ident-journal'),
    url(r'^person_autocomplete/$', 'videoclient.views.journal_person_autocomplete', name='person_autocomplete'),

    (r'^clearjournal/', 'videoclient.views.clearjournal'),
    (r'^(?P<project>.*)/journal/', 'videoclient.views.journal'),
    
    (r'^addphotoperson/(?P<select_page>.+)/(?P<id>.+)/(?P<distortion>.+)/', 'videoclient.po4.views.addphotoperson'),
    (r'^addphotoperson/(?P<select_page>.+)/(?P<id>.+)/', 'videoclient.po4.views.addphotoperson'),
    (r'^(?P<project>.*)/addphotoperson/(?P<select_page>.+)/(?P<id>.+)/', 'videoclient.po4.views.addphotoperson'),
    
    (r'^choose_camera/(?P<select_page>.+)/(?P<id>.+)/', 'videoclient.po4.views.choose_camera'),
    #(r'^choose_camera/(?P<person>.*)/', 'videoclient.views.choose_camera'),
    (r'^(?P<project>.*)/choose_camera/(?P<select_page>.+)/(?P<id>.+)/', 'videoclient.po4.views.choose_camera'),
    
    (r'^learn_camera/(?P<select_page>.+)/(?P<communicator>\d+)/(?P<numcamera>\d+)/(?P<person>.*)/', 'videoclient.po4.views.learn_camera'),
    (r'^(?P<project>.*)/learn_camera/(?P<select_page>.+)/(?P<communicator>\d+)/(?P<numcamera>\d+)/(?P<person>.*)/', 'videoclient.po4.views.learn_camera'),
    
    (r'^visitors/', 'videoclient.po4.views.visitors'),
    (r'^(?P<project>.*)/visitors/', 'videoclient.po4.views.visitors'),
    (r'^visitorslist/', 'videoclient.po4.views.visitorslist'),
    (r'^(?P<project>.*)/visitorslist/', 'videoclient.po4.views.visitorslist'),
    (r'^visitorcard/*(?P<vcid>\d+)*', 'videoclient.po4.views.visitorcard'),
    (r'^(?P<project>.*)/visitorcard/*(?P<vcid>\d+)*', 'videoclient.po4.views.visitorcard'),
    
    (r'^(?P<project>.*)/anketavisitor/(?P<id>\d+)/(?P<id2>\d+)/', 'videoclient.po4.views.anketavisitor'),
    (r'^(?P<project>.*)/anketavisitor/(?P<id>\d+)/', 'videoclient.po4.views.anketavisitor'),
    (r'^(?P<project>.*)/anketavisitor/', 'videoclient.po4.views.anketavisitor'),
    (r'^anketavisitor/(?P<id>\d+)/(?P<id2>\d+)/', 'videoclient.po4.views.anketavisitor'),
    (r'^anketavisitor/(?P<id>\d+)/', 'videoclient.po4.views.anketavisitor'),
    (r'^anketavisitor/', 'videoclient.po4.views.anketavisitor'),
    
    (r'^(?P<project>.*)/anketastaff/(?P<id>\d+)/(?P<id2>\d+)/', 'videoclient.po4.views.anketastaff'),
    (r'^(?P<project>.*)/anketastaff/(?P<id>\d+)/', 'videoclient.po4.views.anketastaff'),
    (r'^(?P<project>.*)/anketastaff/', 'videoclient.po4.views.anketastaff'),    
    (r'^anketastaff/(?P<id>\d+)/(?P<id2>\d+)/', 'videoclient.po4.views.anketastaff'),
    (r'^anketastaff/(?P<id>\d+)/', 'videoclient.po4.views.anketastaff'),
    (r'^anketastaff/', 'videoclient.po4.views.anketastaff'),
    
    (r'^(?P<project>.*)/anketaauto/(?P<id>\d+)/(?P<id2>\d+)/', 'videoclient.po4.views.anketaauto'),
    (r'^(?P<project>.*)/anketaauto/(?P<id>\d+)/', 'videoclient.po4.views.anketaauto'),
    (r'^(?P<project>.*)/anketaauto/', 'videoclient.po4.views.anketaauto'),    
    (r'^anketaauto/(?P<id>\d+)/(?P<id2>\d+)/', 'videoclient.po4.views.anketaauto'),
    (r'^anketaauto/(?P<id>\d+)/', 'videoclient.po4.views.anketaauto'),
    (r'^anketaauto/', 'videoclient.po4.views.anketaauto'),
    
    
    
    (r'^anketalist/$', 'videoclient.views.anketalist'),
    (r'^anketalist/(?P<id>-?\d+)/', 'videoclient.views.anketalist'),
    
    (r'^delete_list/$', 'videoclient.views.delete_list'),
    
    (r'^auto/', 'videoclient.po4.views.staff'),
    (r'^(?P<project>.*)/staff/', 'videoclient.po4.views.staff'),
    
    (r'^stafflist/', 'videoclient.po4.views.stafflist'),
    (r'^(?P<project>.*)/stafflist/', 'videoclient.po4.views.stafflist'),
    
    (r'^autolist/', 'videoclient.po4.views.autolist'),
    (r'^(?P<project>.*)/autolist/', 'videoclient.po4.views.autolist'),
    
    (r'^(?P<project>.*)/persons/', 'videoclient.po4.views.persons'),
    (r'^persons/', 'videoclient.po4.views.persons'),
    
    (r'^(?P<project>.*)/kpp/', 'videoclient.po4.views.kpp'),
    (r'^kpp/', 'videoclient.po4.views.kpp'),
    
    (r'^(?P<project>.*)/historychange/', 'videoclient.po4.views.historychange'),
    (r'^historychange/', 'videoclient.po4.views.historychange'),
    
    (r'^(?P<project>.*)/special/$', 'videoclient.po4.views.special'),
    (r'^special/$', 'videoclient.po4.views.special'),
    
    (r'^(?P<project>.*)/anketauser/(?P<id>\d+)/', 'videoclient.po4.views.anketauser'),
    (r'^(?P<project>.*)/anketauser/', 'videoclient.po4.views.anketauser'),
    (r'^anketauser/(?P<id>\d+)/', 'videoclient.po4.views.anketauser'),
    (r'^anketauser/', 'videoclient.po4.views.anketauser'),
    
    (r'^(?P<project>.*)/anketaperson/(?P<id>\d+)/(?P<id2>\d+)/', 'videoclient.po4.views.anketaperson'),
    (r'^(?P<project>.*)/anketaperson/(?P<id>\d+)/', 'videoclient.po4.views.anketaperson'),
    (r'^(?P<project>.*)/anketaperson/', 'videoclient.po4.views.anketaperson'),
    (r'^anketaperson/(?P<id>\d+)/(?P<id2>\d+)/', 'videoclient.po4.views.anketaperson'),
    (r'^anketaperson/(?P<id>\d+)/', 'videoclient.po4.views.anketaperson'),
    (r'^anketaperson/', 'videoclient.po4.views.anketaperson'),
    
    (r'^(?P<project>.*)/photosperson/(?P<id>\d+)/', 'videoclient.po4.views.photosperson'),
    (r'^photosperson/(?P<id>\d+)/', 'videoclient.po4.views.photosperson'),
    
    
    (r'^po1/', include('videoclient.po1.urls')),
    (r'^po2/', include('videoclient.po2.urls')),
    (r'^po3/', include('videoclient.po3.urls')),
    (r'^po4/', include('videoclient.po4.urls')),
    (r'^wizard/', include('videoclient.wizard.urls')),
    (r'^showjournalphoto/*(?P<journalid>.*)$', 'videoclient.views.showjournalphoto'),
    (r'^rename_person/', 'videoclient.views.rename_person'),
    (r'^export/', 'videoclient.views.export'),
    (r'^exportfile/', 'videoclient.views.exportfile'),
    (r'^export_journalphotos/', 'videoclient.views.export_journalphotos'),
    (r'^save_distortion/', 'videoclient.views.save_distortion'),
    (r'^delete_distortion/', 'videoclient.views.delete_distortion'),
    (r'^rebootdaemon/*', 'videoclient.views.rebootdaemon'),
    (r'^set_balancer_state/*', 'videoclient.views.set_balancer_state'),
    (r'^get_balancer_statistics/*', 'videoclient.views.get_balancer_statistics'),
    (r'^get_balancers_statistics/*', 'videoclient.views.get_balancers_statistics'),
    url(r'^get_camera_statistics_js/*', views.get_camera_statistics_js, name='get_camera_statistics_js'),
    url(r'^get_balancer_daemons_statistics_js/*', views.get_balancer_daemons_statistics_js, name='get_balancer_daemons_statistics_js'),
    url(r'^get_balancer_daemons_statistics/*', views.get_balancer_daemons_statistics, name='get_balancer_daemons_statistics'),
    url(r'^get_communicator_statistics_js/*', views.get_communicator_statistics_js, name='get_communicator_statistics_js'),
    url(r'^get_detect_coefficients/*', views.get_detect_coefficients, name='get_detect_coefficients'),
    (r'^get_communicator_statistics/*', 'videoclient.views.get_communicator_statistics'),
    (r'^set_self_learning/*', 'videoclient.views.set_self_learning'),
    (r'^self_learning/*', 'videoclient.views.self_learning'),
    (r'^delete_camera/*', 'videoclient.views.delete_camera', {}, 'delete_camera'),
    (r'^delete_self_person/*', 'videoclient.views.delete_self_person'),
    (r'^view/all/', 'videoclient.views.security_main'),
    (r'^get_photo_meta/', 'videoclient.views.get_photo_meta'),
    (r'^get_journal_training_form/', 'videoclient.views.get_journal_training_form'),
    url(r'^lists/', views.lists, name="lists"),
    url(r'^url_name_person/', views.url_name_person, name='url_name_person'),
    url(r'^person_info_url/', views.person_info_url, name='person_info_url'),

    (r'^distortion/', include('videoclient.distortion.urls')),
    (r'^profile/', include('videoclient.profile.urls')),
    (r'^monitoring/', include('videoclient.monitoring.urls')),
    (r'^imp_exp/', include('videoclient.imp_exp.urls')),
    (r'^video/', 'videoclient.views.video', {}, 'video-clips'),
    (r'^videoclip_download/', 'videoclient.views.videoclip_download'),
    (r'^start_record/', 'videoclient.views.startRecord', {}, 'start-record'),
    (r'^status_record/', 'videoclient.views.statusRecord', {}, 'status-record'),
    #(r'^test/', 'videoclient.views.testform'),
    
    (r'^template_new/$', 'videoclient.views.template_new'),
    (r'^noiselist_result/$', 'videoclient.views.noiselist_result'),
    (r'^translation-convert/$', 'videoclient.views.translation_convert'),
)
