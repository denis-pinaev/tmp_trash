#coding=utf-8

from django.db import models
import json
from videoclient.models import PersonId,User
from videoclient.communicator.models import Camera

class Decision(models.Model):
    person = models.ForeignKey(PersonId, null=True, verbose_name=u'ID персоны', db_index=True)
    state = models.CharField( max_length=32, verbose_name=u'Статус')
    operator = models.ForeignKey(User, null=True, verbose_name=u'Оператор')  
    camera = models.ForeignKey(Camera, null=True, verbose_name=u'Камера')
    dt = models.DateTimeField(auto_now_add=True)