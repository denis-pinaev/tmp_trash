#coding=utf-8
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django import forms
from django.core.exceptions import ValidationError

class ImageFileForm(forms.Form):    
    image_file = forms.FileField(required=True) 
