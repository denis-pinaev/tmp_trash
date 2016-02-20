# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Document(models.Model):
    name = models.CharField(max_length = 32, null = False, verbose_name=u'Имя документа')
    def __unicode__(self):
        return "%s" %(self.name if self.name is not None else "")
    class Meta:
        verbose_name="Вид документа"
        verbose_name_plural="Виды документов"

class Person(models.Model):
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
    active = models.BooleanField(default=1, null=False, verbose_name=u'Активированность пользователя')
    bal_id = models.IntegerField(null=True, unique=True)
    user = models.ForeignKey(User, null=True)
    first_name = models.CharField( max_length=32, verbose_name=u'Фамилия')
    last_name = models.CharField( max_length=32, verbose_name=u'Имя')
    middle_name = models.CharField( max_length=32, verbose_name=u'Отчество')
    birthday = models.DateField(null=True)
    passport_series = models.CharField(max_length = 8, verbose_name=u'Серия', null=True)
    passport_number = models.CharField(max_length = 16, verbose_name=u'Номер', null=True)
    passport_note = models.TextField(verbose_name=u'Выдан', null=True)
    passport_date = models.DateField(verbose_name=u'Дата выдачи', null=True)
    address = models.TextField(verbose_name=u'Адрес', null=True)
    phone_work = models.CharField( max_length=32, verbose_name=u'Служебный телефон', null=True)
    phone_home = models.CharField( max_length=32, verbose_name=u'Домашний телефон', null=True)
    phone_mobile = models.CharField( max_length=32, verbose_name=u'Мобильный телефон', null=True)
    note = models.TextField(verbose_name=u'Примечание', null=True)
    document = models.ForeignKey(Document, null=True, verbose_name=u'Документ')
    