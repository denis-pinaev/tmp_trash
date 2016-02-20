#coding=utf-8
from models import Map, MapTerminal
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django import forms
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
import logging
import sys
import re
import settings

class MapForm(forms.Form):
    city = forms.CharField(max_length=250, required=True)
    obj_type = forms.CharField(max_length=250, required=True)
    obj_name = forms.CharField(max_length=250, required=True)

class MapImageForm(forms.Form):    
    image = forms.FileField(required=True)

class MapTerminalForm(forms.ModelForm):
    #password2 = forms.CharField(widget=forms.PasswordInput())
  
    class Meta:
        model = MapTerminal
        fields = ('name', 'model', 'number', 'direction', 'description')
        widgets = {
            'name': forms.TextInput(),
            'model': forms.Select(),
            'number': forms.TextInput(),
            'direction': forms.Select(),
            'description': forms.widgets.Textarea()
        }

class MapCameraForm(forms.Form):
    terminal = forms.IntegerField(required = True)
    camera = forms.IntegerField(required = True)
    lens = forms.IntegerField(required = True)
    direction = forms.IntegerField(required = True)
    visible_objects = forms.CharField(max_length=250, required=False)
    visibility = forms.FloatField(required = True)
    range = forms.FloatField(required = True)
    recognition = forms.FloatField(required = True)
    focal = forms.FloatField(required = True)
    angle = forms.FloatField(required = True)