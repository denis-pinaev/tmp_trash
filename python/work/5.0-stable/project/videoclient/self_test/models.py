#coding=utf-8

from django.db import models
import datetime

class TimeControl(models.Model):
    datetime = models.DateTimeField(auto_now=True, auto_now_add=True)

def getDateTime():
    tc = TimeControl.objects.all().order_by('-id')
    count = tc.count()
    if count == 0:
        return None
    tc = tc[0]
    return tc.datetime

def setDateTime():
    tc = TimeControl.objects.all().order_by('-id')
    count = tc.count()
    if count == 0:
        TimeControl.objects.create()
    tc.update(datetime=datetime.datetime.now())


     