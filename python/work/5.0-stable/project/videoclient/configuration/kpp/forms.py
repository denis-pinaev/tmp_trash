# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from django import forms

class CheckID(forms.Form):
    id = forms.IntegerField(required=True)
    
class CheckKpp(forms.Form):
    name = forms.CharField(max_length=32, required=True)
    location = forms.CharField(max_length=128, required=False)
    
class ChangeCameraKpp(forms.Form):
    camera_id = forms.IntegerField(required=True)
    kpp_id = forms.IntegerField(required=True)    