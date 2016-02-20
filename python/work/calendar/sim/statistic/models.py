#!/usr/bin/python 
# -*- coding: utf-8 -*- 
from django.db import models
from django.conf import settings
from django.db.models import ImageField, signals
from django.dispatch import dispatcher
from django.contrib import admin
from sim import settings


class BuyStat( models.Model):
    date = models.DateField(null=False, verbose_name=u'Дата')
    count_vote = models.PositiveIntegerField( null=True, default=0, verbose_name=u'Оплаченные 10-ть голосов')
    count_up = models.PositiveIntegerField( null=True, default=0, verbose_name=u'Оплаченные поднятия наверх')

#    thumb.allow_tags = True
#    thumb.short_description = 'Preview'

    def __unicode__(self):
        return u'%s (%s, %s)' % (self.date, self.count_vote, self.count_up)

class StatShablon(admin.ModelAdmin):
    list_display = ( 'date', "count_vote", 'count_up')
    list_per_page = 100
    date_hierarchy = 'date'
