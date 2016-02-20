#coding=utf-8
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

class LeftThingsDetectorForm(forms.Form):
    hour = forms.IntegerField()
    minutes = forms.IntegerField()
    seconds = forms.IntegerField()
    cam_id = forms.IntegerField()
    com_id = forms.IntegerField()
    diffColorThreshold = forms.IntegerField()
    diffGrayThreshold = forms.IntegerField()
    diffMotionThreshold = forms.IntegerField()
    minPixelObject = forms.IntegerField()
    minPixelMove = forms.IntegerField()
    check_thingsDetector = forms.BooleanField(required=False)

class BackgroundDetectorForm(forms.Form):
    bg_minutes = forms.IntegerField()
    bg_seconds = forms.IntegerField()
    cam_id = forms.IntegerField()
    com_id = forms.IntegerField()

class TestFromLogDetect(forms.Form):
    data = forms.CharField(required=True)
    frame = forms.ImageField(required=True)
    preview = forms.ImageField(required=False)

class TestClearDataJournal(forms.Form):
    dataClear = forms.DateField(required=False, input_formats=('%d.%m.%Y',),)
    period = forms.IntegerField(required = True) 
