# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from django.db import models
from videoclient import models as VModels
from django.db.models.signals import post_save, pre_save      
#from django.contrib.auth.models import User

class CamerasProfile(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'Имя профиля', null=False, unique=True)
    text = models.TextField(null=True, verbose_name=u'Данные профиля', help_text=u"В JSON формате")
    
    def __unicode__(self):
        return self.name   
    
    class Meta:
        verbose_name="Профиль камеры"
        verbose_name_plural="Профили камер"

"""
class ProfileToCamera(models.Model):
    camera = models.ForeignKey(VModels.Camera, null=False)
    profile = models.ForeignKey(CamerasProfile, null=False)
    
    class Meta:
        verbose_name="Связь профиля и камеры"
        verbose_name_plural="Связь профилей и камер"
""" 