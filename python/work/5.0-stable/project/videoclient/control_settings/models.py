# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from django.db import models
#from django.contrib.auth.models import User

TYPES = (
    (0, "text"),
    (1, "choice"),
    (2, "number"),
)

class Params(models.Model):
    code = models.CharField( max_length=255, unique=True, verbose_name=u'Код параметра', help_text=u'Короткое имя языка. Например: Russian(Русский) - ru', null=False)
    name = models.TextField( verbose_name=u'Описание', help_text=u'Описание параметра', null=True, default=None, blank = True)
    min_val = models.CharField( max_length=255, verbose_name=u'Минимальное значение', help_text=u'Минимальное значение параметра', default='0')
    max_val = models.CharField( max_length=255, verbose_name=u'Максимальное значение', help_text=u'Максимальное значение параметра', default='20120000')
    step = models.CharField( max_length=255, verbose_name=u'Шаг', help_text=u'Шаг изменения значения параметра', default='1')
    type = models.PositiveIntegerField(default = 2, verbose_name=u'Минимальное значение', help_text=u'Минимальное значение параметра', choices = TYPES)
    def __unicode__(self):
        return "%s (%s)" % (self.code, self.name)
    class Meta:
        verbose_name="Параметр УС"
        verbose_name_plural="Параметры УС"


class NotEditableParams(models.Model):
    code = models.CharField( max_length=255, unique=True, verbose_name=u'Код параметра', help_text=u'Короткое имя языка. Например: Russian(Русский) - ru', null=False)
    value = models.CharField( max_length=255, verbose_name=u'Значение параметра', null=True)
    permit = models.BooleanField(default=False, verbose_name=u'Разрешать?', help_text=u"Разрешать заменять параметр или нет (да - разрешить, нет - запретить изменение параметра)")
    def __unicode__(self):
        return "%s" % (self.code)
    class Meta:
        verbose_name="Нередактируемый параметр УС"
        verbose_name_plural="Нередактируемые параметры УС"      