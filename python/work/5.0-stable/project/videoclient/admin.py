# charset=utf-8
from videoclient.models import *
from django.contrib import admin, auth
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from videoclient.forms import *
from videoclient.control_settings.models import Params, NotEditableParams
from videoarchive import admin as v_admin
from videoclient.communicator.models import Communicator, Kpp, Camera

class TranslationAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'language', 'translate', 'group', 'active')
    list_filter = ('group', 'active', 'language')
    search_fields = ['phrase']
    fields = ('group', 'phrase', 'language', 'translate','active')
    list_per_page = 20

class UserAdmin(auth.admin.UserAdmin):
       
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name', 'birthday', 'email')}),
        (_('Passport'), {'fields': ('passport_series', 'passport_number', 'passport_note', 'passport_date')}),
        (_('Contacts'), {'fields': ('address', 'phone_work', 'phone_home', 'phone_mobile', 'division', 'position')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('Note'), {'fields': ('note',)}),
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'middle_name', 'email')
    
    form = UserUserChangeForm
    add_form = UserUserCreationForm
    change_password_form = UserAdminPasswordChangeForm
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'middle_name', 'is_staff')
    
class StatusUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'division')
    list_filter = ['division']
    #search_fields = ['phrase']
    #fields = ('group', 'phrase', 'language', 'translate','active')
    #list_per_page = 20
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'discription', 'group', 'type', 'level', 'active')    

class ParamsAdmin(admin.ModelAdmin):
    list_display = ('code', 'permit')
    
#admin.site.register(DivisionUser)
#admin.site.register(PositionUser)
admin.site.register(DefaultParams)
admin.site.register(StatusUser, StatusUserAdmin)
admin.site.register(Document)
#admin.site.register(User, UserAdmin)
#admin.site.register(Rule)
#admin.site.register(RuleGroup)
#admin.site.register(Person)
admin.site.register(GroupPerson)

admin.site.register(Translation, TranslationAdmin)
admin.site.register(Language)
admin.site.register(Group)

admin.site.register(Communicator)
#admin.site.register(Kpp)
#admin.site.register(Camera)
admin.site.register(Balancer)
admin.site.register(Article)
admin.site.register(ArticleItem)
admin.site.register(ArticlePart)
admin.site.register(Params)
admin.site.register(NotEditableParams, ParamsAdmin)
#admin.site.register(Sound)
#admin.site.register(List, ListAdmin)