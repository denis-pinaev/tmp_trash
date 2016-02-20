# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.db.models import ImageField, signals
from django.dispatch import dispatcher

from django.contrib import admin
from django.db.models.signals import post_save, pre_save
import datetime


class DispatchEventAdmin(admin.ModelAdmin):
    list_display = ( 'message', 'status', 'active',  'dt_open', 'copies', 'send_copies', 'received_copies')

class DispatchEvent(models.Model):
    message = models.TextField( verbose_name="Текст сообщения" )
    mode = models.IntegerField( verbose_name="Повторять через кол-во дней", default = 0)
    dt_start = models.DateField(verbose_name="Ближайшая дата выполнения", default = datetime.date.today() )
    dt_open = models.DateTimeField(auto_now=True, auto_now_add=True)
    dt_last = models.DateField(default = datetime.date(2000, 01, 01), verbose_name = "Дата последнего выполнения")
    active = models.BooleanField( verbose_name="Включить", default=False)
    status = models.IntegerField( verbose_name="Статус обработки", default = 0)
    copies = models.IntegerField( verbose_name="Всего экземпляров", default = 0, editable = False)
    send_copies = models.IntegerField( verbose_name="Отправлено экземпляров", default = 0, editable = False)
    received_copies = models.IntegerField( verbose_name="Получено экземпляров", default = 0, editable = False)
    
    def __unicode__(self):
        return u'%s %s' % ( str( self.dt_open), self.message[128:], )
    class Meta:
        verbose_name="Оповещения"
        verbose_name_plural="Оповещения"

class MessageSent(models.Model):
    user = models.IntegerField( db_index=True)
    code =  models.CharField( max_length = 64, db_index=True)
    dt_open = models.DateTimeField( auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.user)

def dispatch_pre_save(sender, **kwargs):
    from wizer.vkontakte import vkontakte
    message = kwargs['instance']
    vkontakte.sendAll( message.message)

def dispatch_pre_save2(sender, **kwargs): 
    from wizer.vkontakte import scheduler
    scheduler.scheduler_send_message()

#pre_save.connect( dispatch_pre_save2, sender=DispatchEvent)

