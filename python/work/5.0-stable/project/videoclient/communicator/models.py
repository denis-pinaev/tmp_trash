# coding=utf-8

from django.db import models
from django.utils import translation
from videoclient.settings import *

class Kpp(models.Model):
    name = models.CharField(max_length = 32, null = False, verbose_name=u'Имя КПП')
    location = models.CharField(max_length = 128, blank=True, null=True, verbose_name=u'Расположение КПП')
    
    def __unicode__(self):
        return "%s" %(self.name if self.name is not None else "")
    class Meta:
        verbose_name="КПП"
        verbose_name_plural="КПП"
        
class Communicator(models.Model):
    host = models.CharField( max_length = 255, null=False, verbose_name=u'Хост')
    port = models.IntegerField(null=True, verbose_name=u'Порт')
    mjpeg_port = models.IntegerField(null=True, verbose_name=u'Порт для потока mjpeg')
    active = models.BooleanField(default = True, verbose_name=u'Активность')
    def __unicode__(self):
        return "%s:%s" %(self.host if self.host is not None else "", self.port if self.port is not None else "")
    class Meta:
        verbose_name="Коммуникатор"
        verbose_name_plural="Коммуникаторы"
        
POSITIONS = (
    (0, "Вход"),
    (1, "Выход"),
    (2, "Вход/Выход"),
)           
        
class Camera(models.Model):
    ip = models.CharField(max_length = 255, null = False, verbose_name=u'IP')
    port = models.IntegerField(null=True, verbose_name=u'Порт')
    url = models.CharField(max_length = 255, null = True, verbose_name=u'URL')
    type = models.CharField(max_length = 64, null = False, verbose_name=u'Тип')
    kpp = models.ForeignKey(Kpp, null = True, verbose_name=u'КПП', help_text=u'Контрольно пропускной пункт')
    position = models.PositiveIntegerField(default = 2, verbose_name="Размещение", choices = POSITIONS)
    name = models.CharField(max_length = 128, null = True, verbose_name=u'Название камеры', blank=True)
    commun = models.ForeignKey(Communicator, null=True, verbose_name=u'Коммуникатор')
    active = models.BooleanField(default=True, verbose_name=u'Активность')
    uuid = models.CharField(max_length = 255, unique=True, verbose_name=u'UUID камеры')
    available = models.BooleanField(default=True, verbose_name=u'Доступность')
    delete = models.BooleanField(default=True, verbose_name=u'Некорректно удалена')
    
    # для отображения имени камеры, возможно использовать так же и в шаблонах
    def __unicode__(self):
        if self.name is not None and self.name:
            return self.name
        answer = []
        if self.ip: answer.append(self.ip)
        if self.type: answer.append(self.type)
        return " ".join(answer)

    class Meta:
        verbose_name="Камеру"
        verbose_name_plural="Камеры"
        
    def display_name(self):
        if self.name is not None and self.name:
            return self.name
        answer = []
        if self.ip: answer.append(self.ip)
        if self.type: answer.append(self.type)
        return " ".join(answer)
    
    def full_name(self):
        answer = []
        if self.ip: answer.append(self.ip)
        if self.type: answer.append(self.type)
        if self.name is not None and self.name:
            return " ".join([self.name, "(%s)" % " ".join(answer)])
        else:
            return " ".join(answer) 
