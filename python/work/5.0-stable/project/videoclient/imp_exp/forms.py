#coding=utf-8
from django import forms

class ImportPersonForm(forms.Form):    
    file = forms.FileField(label=u'Файл импорта', required=True)