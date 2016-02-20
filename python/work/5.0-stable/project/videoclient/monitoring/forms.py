from django import forms

class CheckEventsFilterForm(forms.Form):
    filter = forms.CharField(required=False)
    
    dateBegin = forms.DateField(required=False, input_formats=('%d.%m.%Y',),)
    dateEnd = forms.DateField(required=False, input_formats=('%d.%m.%Y',),)
    
    hour_beg = forms.IntegerField(required=False)
    min_beg = forms.IntegerField(required=False)
    hour_end = forms.IntegerField(required=False)
    min_end = forms.IntegerField(required=False)
    
    id_record = forms.CharField(required=False)
    
    status = forms.CharField(required=False)
    
    type = forms.CharField(required=False)
    
    description = forms.CharField(required=False)
    
    up = forms.IntegerField(required=False)
    sorto = forms.IntegerField(required=False)
    
class CheckForm(forms.Form):
    check = forms.IntegerField(required=False)
    syscheck = forms.IntegerField(required=False)