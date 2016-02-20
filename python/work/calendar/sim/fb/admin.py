#from statistics.models import *
from django.contrib import admin

from sim.adm.models import *
#from sim.wizers.models import Wizer, WizerGroup
from sim.statistic.models import *


class WiserAdmin(admin.ModelAdmin):
    change_form_template = 'wizer_new.html'
    change_list_template = 'wizer_list_new.html'
    list_display = ('thumb', 'group', 'code', 'rate')
    search_fields = ['code']
    list_filter = ('group','public')
    list_per_page = 500

class StoredFrameAdmin(admin.ModelAdmin):
    list_display = ('frame_id', 'image','user_id', 'is_public')

class StoredImageAdmin(admin.ModelAdmin):
    list_display = ('code',)

#######################

"""
admin.site.register( ByDay, StatAdmin)
admin.site.register( ByWeek, StatAdmin)
admin.site.register( ByMonth, StatAdmin)
admin.site.register( AllTime, StatAdmin)
admin.site.register( StatVisit, StatVisitAdmin)
"""

######################
admin.site.register( BuyStat, StatShablon)
#admin.site.register( Wizer, WiserAdmin)
#admin.site.register( EditablePage)
#admin.site.register( News)
#admin.site.register( WizerGroup)
#admin.site.register( StoredFrame, StoredFrameAdmin)

#admin.site.register( StoredImage, StoredImageAdmin)

#####################
#admin.site.register( DispatchEvent, DispatchEventAdmin)
