#coding=utf-8
from django.contrib import admin
from videoarchive.person import models as pModels
from videoarchive.archive import models as aModels
from videoarchive.va import models as VaModels
#from videoarchive.communicator import models as CommunicatorModels
from videoarchive import models

class TranslationAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'language', 'translate', 'group', 'active')
    list_filter = ('group', 'active', 'language')
    search_fields = ['phrase']
    fields = ('group', 'phrase', 'language', 'translate','active')
    list_per_page = 20
    



# Переводы
admin.site.register(models.Translation, TranslationAdmin)
admin.site.register(models.Language)
admin.site.register(models.Group)

# Настройки
admin.site.register(models.Settings)
#admin.site.register(CommunicatorModels.Communicator)
admin.site.register(VaModels.VaArchive)
#admin.site.register(VaModels.VaCamera)
admin.site.register(models.Signals)
admin.site.register(models.Week)

#Временные
admin.site.register(pModels.Person)
admin.site.register(pModels.Document)