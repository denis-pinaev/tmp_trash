# coding=utf-8

from django.db import models
from videoclient.communicator.models import Camera

class Turnstile(models.Model):
    turn_id = models.IntegerField(null=False)
    ip = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    enable = models.BooleanField(default=True)
    
class TurnstileCamera(models.Model):    
    camera = models.ForeignKey(Camera, null=False, verbose_name=u'Камера')
    turnstile = models.ForeignKey(Turnstile, null=False, verbose_name=u'Турникет')
    inside = models.BooleanField(default=True)
