#coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _


class WebApiSetting(models.Model):
    host = models.CharField( max_length = 250,  verbose_name=u'Хост', help_text=u'Например: 127.0.0.1')
    port = models.CharField( max_length = 250,  verbose_name=u'Порт', help_text=u'Например: 8080')
    users_url = models.CharField( max_length = 250,  verbose_name=u'Адрес для получения информации о пользователях', help_text=u'Например: /web_api/users')
    stat_url = models.CharField( max_length = 250,  verbose_name=u'Адрес для получения статистики', help_text=u'Например: /charts/stat')

    def __unicode__(self):
        return self.host