#coding=utf-8

from django.db import models
from videoclient import settings
from django.utils.translation import ugettext as _
from videoclient.models import Lens
from videoclient.communicator.models import Camera

class Direction(models.Model):
    name = models.CharField(max_length=250, null=True, blank=False, verbose_name=_('Направление'))

    def __unicode__(self):
        return u'%s' % (self.name)

class MapCity(models.Model):
    name = models.CharField(max_length=250, null=True, blank=False)

    def __unicode__(self):
        return self.name

class MapObjectType(models.Model):
    name = models.CharField(max_length=250, null=True, blank=False)

    def __unicode__(self):
        return self.name

class MapObject(models.Model):
    name = models.CharField(max_length=250, null=True, blank=False)
    map_object_type = models.ForeignKey(MapObjectType, null=True)
    city = models.ForeignKey(MapCity, null=True)

    def __unicode__(self):
        return self.name

def map_image(self):
    return u'%s%s' % (settings.MAP_IMAGES, 'test.jpg')

class Map(models.Model):
    city = models.ForeignKey(MapCity, null=True, verbose_name=_('Название города'))
    obj_type = models.ForeignKey(MapObjectType, null=True, verbose_name=_('Тип объекта'))
    obj_name = models.ForeignKey(MapObject, null=True, verbose_name=_('Название объекта'))
    image = models.ImageField(upload_to=map_image, null=True, blank=False, verbose_name=_('Изображение карты'))
    def __unicode__(self):
        return u'%s %s %s' % (self.city, self.obj_type, self.obj_name)

class MapTerminalType(models.Model):
    name = models.CharField(max_length=250, null=True, blank=False, verbose_name=_('Тип терминала'))

    def __unicode__(self):
        return u'%s' % (self.name)

#class MapTerminalSensor(models.Model):
#    name = models.CharField(max_length=250, null=True, blank=False, verbose_name=_('Название датчика'))

#    def __unicode__(self):
#        return u'%s' % (self.name)

class MapTerminal(models.Model):
    name = models.CharField(max_length=250, null=True, blank=False, verbose_name=_('Название терминала'))
    model = models.ForeignKey(MapTerminalType, null=True, verbose_name=_('Модель терминала'))
    number = models.IntegerField(null=False, verbose_name=_('Номер терминала'))
    direction = models.ForeignKey(Direction, null=True, verbose_name=_('Направление'))
    #sensors = models.ManyToManyField(MapTerminalSensor, null=False, blank=True, verbose_name=_('Датчик'))
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Описание'))
    map = models.ForeignKey(Map, null=True, verbose_name=_('Название карты'))
    x = models.IntegerField(null=False, blank=True, verbose_name=_('Х - координата'))
    y = models.IntegerField(null=False, blank=True, verbose_name=_('Y - координата'))

    def __unicode__(self):
        return u'%s' % (self.name)

class MapCamera(models.Model):
    map = models.ForeignKey(Map, null=True, verbose_name=_('Карта'))
    terminal = models.ForeignKey(MapTerminal, null=True, verbose_name=_('Терминал'))
    camera = models.ForeignKey(Camera, null=True, verbose_name=_('Камера'))
    lens =  models.ForeignKey(Lens, null=True, verbose_name=_('Объектив'))
    direction = models.ForeignKey(Direction, null=True, verbose_name=_('Направление'))
    visible_objects = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Видимые объекты'))
    visibility = models.FloatField(null=False, blank=True, default=0, verbose_name=_('Видимость'))
    range = models.FloatField(null=False, blank=True, default=0, verbose_name=_('Детектирование'))
    recognition = models.FloatField(null=False, blank=True, default=0, verbose_name=_('Распознавание'))
    focal = models.FloatField(null=False, blank=True, default=0, verbose_name=_('Фокальное число'))
    angle = models.FloatField(null=False, blank=True, default=0, verbose_name=_('Угол обзора'))
    
    
    def __unicode__(self):
        return u'%s' % (self.name)