from django.conf.urls.defaults import *
from sim.fb.views import *


urlpatterns = patterns('',
    url(r'iframe/$', 'sim.fb.views.iframe'),
    
   # url(r'^upload/$', upload, name = "fb_upload"),
   # url(r'^upload_url/$', upload_url, name = 'fb_upload_url'),
   # url(r'^process/$', process, name = 'fb_process'),
   # url(r'^delete/*$', delete, name = 'fb_delete'),

   # url(r'^getframes/$', getcontest, name = 'fb_process_getcontest'),
   # url(r'^savecontest/$', savecontest, name = 'fb_process_savecontest'),
   # url(r'^getcontest/$', getcontest, name = 'fb_process_getcontest'),
   # url(r'^getvote/$', getvote, name = 'fb_process_getvote'),
   # url(r'^getcabinet/$', getcabinet, name = 'fb_process_getcabinet'),
   # url(r'^setvote/$', setvote, name = 'fb_process_setvote'),
   url(r'^del_meeting/$', delMeeting, name = 'fb_getm'),
   url(r'^get_meeting/$', getMeetings, name = 'fb_getm'),
   url(r'^set_meeting/$', createSaveMeeting, name = 'fb_setm'),
    
    url(r'^get_money/', get_money ,name='fb_get_money'),
    url(r'^from_payment/', from_payment, name='fb_from_payment'),
    #url(r'^pay_contest/', pay_contest, name='fb_pay_contest'),
    #url(r'^pay_collage_set/', pay_collage_set, name='pay_collage_set'),
    #url(r'^pay_collage_get/', pay_collage_get, name='pay_collage_get'),
    
    #url(r'^test/$', test, name = 'fb_test'),

)

