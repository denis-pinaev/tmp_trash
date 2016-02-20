# coding=utf-8
from django.db import models
import json
import sys
import datetime

STATE_PENDING = "pending"
STATE_RUNNING = "running"

class Task(models.Model):
    STATE_CHOICES = (
        (0, STATE_PENDING),
        (1, STATE_RUNNING),
    )
    title = models.CharField( max_length=64, null=False, verbose_name=u'Имя задачи')
    auto_run = models.BooleanField(default=False, null=False, verbose_name=u'Автоматический запуск')
    params = models.TextField(null=True, blank=True, verbose_name=u'Параметры автоматического запуска задачи') 
    percent = models.IntegerField(default=0, verbose_name=u'Процент выполнения задачи')
    state = models.IntegerField(choices=STATE_CHOICES, default=0, verbose_name=u'Статус задачи')
    frequency = models.IntegerField(default=0, null=False, verbose_name=u'Частота запуска (сек.)')
    dt_last_run = models.DateTimeField(auto_now_add=True, verbose_name=u'Время последнего запуска')
    dt_update = models.DateTimeField(auto_now=True, auto_now_add=True, verbose_name=u'Время последнего обновления')
    result = models.TextField(null=True)
            
    def setState(self, state):
        self.state = state
        self.save()

    def setPercent(self, percent):
        self.percent = percent
        self.save()
        
    def setResult(self, result):
        if isinstance(result, dict):
            result = json.dumps(result)
        else:
            result = str(result)
        self.result = result
        self.save()

    def setDtLastRun(self,dt_last_run):
        self.dt_last_run = dt_last_run
        self.save()