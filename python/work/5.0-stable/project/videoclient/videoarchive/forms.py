#coding=utf-8

from django import forms
from videoarchive import models
from django.utils.translation import ugettext, ugettext_lazy as _

SVN_REVISION = '$Revision: 4946 $'#

class TaskForm(forms.ModelForm):
    start_date = forms.DateField(input_formats=('%d.%m.%Y',))
    stop_date = forms.DateField(input_formats=('%d.%m.%Y',))
    repeat_start_date = forms.DateField(input_formats=('%d.%m.%Y',))
    repeat_stop_date = forms.DateField(input_formats=('%d.%m.%Y',))
    repeat_start_time = forms.TimeField(input_formats=('%H:%M',))
    repeat_stop_time = forms.TimeField(input_formats=('%H:%M',))
    class Meta:
        model = models.Tasks
        
class UserForm(forms.ModelForm):
    first_name = forms.CharField( max_length=30, label=u'Имя', required=True)
    last_name =  forms.CharField( max_length=30, label=u'Фамилия', required=True)
    middle_name = forms.CharField( max_length=32, label=u'Отчество', required=True)    
    last_login = forms.DateTimeField(input_formats=('%d.%m.%Y',))
    date_joined = forms.DateTimeField(input_formats=('%d.%m.%Y',))
    password = forms.CharField( max_length=128, label=u'Пароль1', required=False)
    password2 = forms.CharField( max_length=128, label=u'Пароль2', required=False)
    
    def clean_password2(self):
        password = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data["password2"]
        if password != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
    
    class Meta:
        model = models.Users        
 
class NavigationDataForm(forms.Form):
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)
    
        
class RollerDataForm(forms.Form):
    id = forms.IntegerField()
    frame = forms.IntegerField(required=False)
    count = forms.IntegerField(required=False)
    
class CheckCalendarForm(forms.Form):
    year = forms.IntegerField(required=False)
    date_from = forms.DateField(required=False, input_formats=('%d.%m.%Y',))
    date_to = forms.DateField(required=False, input_formats=('%d.%m.%Y',))
    camera = forms.IntegerField(required=False)
    
class CheckTablesVideoForm(forms.Form):
    date = forms.DateField(required=True, input_formats=('%d.%m.%Y',))
    camera = forms.IntegerField(required=False)
    
class CheckTablesDataForm(forms.Form):
    startTime = forms.DateTimeField(required=True, input_formats=('%d.%m.%Y',)) #, input_formats=('%Y-%m-%d 00:00:00',)
    endTime = forms.DateTimeField(required=True, input_formats=('%d.%m.%Y',)) #, input_formats=('%Y-%m-%d 00:00:00',)
    id = forms.IntegerField(required=False)    

class CheckRenameCameraForm(forms.Form):
    id = forms.IntegerField(required=True)
    name = forms.CharField(max_length = 128, required=True)
    
class CheckImportRollerForm(forms.Form):
    path = forms.CharField(max_length = 512, required=True)
    source = forms.IntegerField(required=True)
    new_name_source = forms.CharField(max_length = 128, required = False)
    date_imp = forms.DateTimeField(required = True, input_formats=('%d.%m.%Y',))
    hour_imp = forms.IntegerField(required = True)
    minute_imp = forms.IntegerField(required = True)
    second_imp = forms.IntegerField(required = True)
    fd = forms.BooleanField(required = False)
    fr = forms.BooleanField(required = False)
    fps_imp = forms.BooleanField(required = False)
    enter_fps_imp = forms.IntegerField(required = False)
    convert = forms.IntegerField(required = False)
    interval = forms.IntegerField(required = False)
    time = forms.IntegerField(required = False)
    resol = forms.CharField(max_length = 128, required = False)
    codec = forms.IntegerField(required=False)
    gop = forms.IntegerField(required=False)
    compress = forms.FloatField(required=False)
    
class CheckInfoRollerForm(forms.Form):
    id = forms.IntegerField()
    
class CheckIdForm(forms.Form):
    id = forms.IntegerField(required=True)    
    
class CheckPageVideoForm(forms.Form):
    date = forms.DateField(required=True, input_formats=('%d.%m.%Y',))
    
class CheckCameraPageVideoForm(forms.Form):
    camera = forms.IntegerField(required=False)    
    
class CheckSaveRollersForm(forms.Form):
    rollers = forms.CharField(required=True)    
    
class CheckProcessRollerForm(forms.Form):
    id = forms.IntegerField(required=True)
    mode = forms.IntegerField(required=True)
    diffFramesProc = forms.IntegerField(required=False)
    
class CheckSetResolutionInterfaceForm(forms.Form):
    resol = forms.IntegerField(required=True)    

class CheckJournalSortForm(forms.Form):
    sort = forms.IntegerField(required=True)
    order = forms.IntegerField(required=True)
    filter = forms.CharField(max_length=256, required=False)
    
class CheckRollerSearchForm(forms.Form):
    source = forms.IntegerField(required=False)
    cr = forms.IntegerField(required=False)
    signal = forms.IntegerField(required=False)
    interval = forms.ChoiceField(choices=((0,0), (1,1)), required=False)
    dateBegin = forms.DateTimeField(required=False, input_formats=('%d.%m.%Y',))
    dateEnd = forms.DateTimeField(required=False, input_formats=('%d.%m.%Y',))
    date = forms.DateField(required=False, input_formats=('%d.%m.%Y',))
    period_date = forms.ChoiceField(choices = ((0,0),(1,1)), required=False)
    hour1 = forms.IntegerField(required=False)
    minute1 = forms.IntegerField(required=False)
    second1 = forms.IntegerField(required=False)
    hour2 = forms.IntegerField(required=False)
    minute2 = forms.IntegerField(required=False)
    second2 = forms.IntegerField(required=False)    
    
class CheckDatePeriodForm(forms.Form):
    dateBegin = forms.DateField(required=True, input_formats=('%d.%m.%Y',))
    dateEnd = forms.DateField(required=False, input_formats=('%d.%m.%Y',))
    source = forms.IntegerField(required=False)

class SetSettingsForm(forms.Form):                                                                                                                                                                                                                     
    id = forms.IntegerField(required=True)                                                                                                                                                                                                             
    thresholdDays = forms.IntegerField(required=False)                                                                                                                                                                                                 
    thresholdAlerts = forms.IntegerField(required=False)                                                                                                                                                                                               
    thresholdRemove = forms.IntegerField(required=False)                                                                                                                                                                                               
    checkIntervalThresholds = forms.IntegerField(required=False)                                                                                                                                                                                       
    rollerCapacity = forms.IntegerField(required=False)                                                                                                                                                                                                
    rollerCompression = forms.FloatField(required=False)                                                                                                                                                                                               
    rollerBlur = forms.FloatField(required=False)                                                                                                                                                                                                      
    rollerDistance = forms.IntegerField(required=False)                                                                                                                                                                                                
    rollerIdent = forms.FloatField(required=False)                                                                                                                                                                                                     
    domen = forms.CharField(max_length=200, required=False)                                                                                                                                                                                            
    domenAlert = forms.CharField(max_length=200, required=False)                                                                                                                                                                                       
    timeout = forms.IntegerField(required=False)                                                                                                                                                                                                       
    url = forms.CharField(max_length=150, required=False)                                                                                                                                                                                              
    save_dir = forms.CharField(max_length=150, required=False)                                                                                                                                                                                         

class SetDefaultArchiveSettingsForm(forms.Form):
    gop_size = forms.IntegerField()
    compress = forms.FloatField()
    bitrate = forms.IntegerField()
    blur = forms.FloatField()

class CheckTaskNameForm(forms.Form):
    name = forms.CharField(max_length = 128, required=True)
    id = forms.IntegerField(required=False)
    
class TestDeleteCamerasForm(forms.Form):                                                                                                                                                                                       
    ids = forms.RegexField(max_length=1024, regex=r'^[\d+,]+$',
        help_text = _("Required. Digits and ',' only."), error_messages = {'invalid': _("This value may contain only numbers and ',' characters.")})