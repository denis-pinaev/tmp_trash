# coding:utf-8
from django.db import models

# Create your models here.

class Balancer(models.Model):
    host = models.CharField( max_length = 32, null=False, verbose_name=u'Хост')
    port = models.IntegerField(null=False, verbose_name=u'Порт')
    login = models.CharField( max_length = 32, verbose_name = u'Логин')
    passwd = models.CharField( max_length = 32, verbose_name = u'Пароль')
    user = models.CharField( max_length = 32, verbose_name = u'Пользователь')
    active = models.BooleanField(default = True, verbose_name=u'Активность')

    def __unicode__(self):
        return "%s:%s %s %s %s" %(self.host if self.host is not None else "", self.port if self.port is not None else "", self.login if self.login is not None else "", self.passwd if self.passwd is not None else "", self.user if self.user is not None else "")
    class Meta:
        verbose_name="Управляющую систему"
        verbose_name_plural="Управляющая система"
