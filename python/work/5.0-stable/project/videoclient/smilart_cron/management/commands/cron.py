#coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import sys
import json
import logging
from django.core.management.base import AppCommand
import datetime, time
from optparse import make_option
from smilart_cron.utils import getClassByName,getDictFromString
from smilart_cron.views import initTaskList
from smilart_cron.models import Task
from django.utils.translation import ugettext as _
import re
from settings import MODULE_TASK_LIST

STATE_PENDING = 0
STATE_RUNNING = 1

TIME_PROCESS = 60 #seconds

TIME_OUT_UPDATE_MINUTE = 5 # по истечению данного периода с момента последнего обновления данных по задаче, считается, что выполнение завершилось ошибкой 

def getPriorityTask(ids_exclude_task=False):
    #Выбираем задачу исходя из её продолжительности, приоритета, как давно запускалась, статуса выполнения(включая задачи "завершённые" по таймауту)
    now = datetime.datetime.now() 
    time_delta = datetime.timedelta(minutes=TIME_OUT_UPDATE_MINUTE)    
    tasks = Task.objects.exclude(auto_run=False)
    if ids_exclude_task:
        tasks = tasks.exclude(id__in=ids_exclude_task)
    tasks = tasks.exclude(state=STATE_RUNNING, dt_update__lt = now - time_delta)
    tasks = list(tasks)    
    filtered_task = filter(lambda x: x.dt_last_run < now - datetime.timedelta(seconds=x.frequency), tasks)    
    filtered_task = sorted(filtered_task, key=lambda x: x.dt_last_run)
    
    task = False
    if len(filtered_task)>0:
        task = filtered_task[0] 
    return task


class Command(BaseCommand):
    
    help = 'Запуск задач на выполнение.'

    requires_model_validation = True

    def handle(self, *args, **options):
        error_ids = [] #id записей в таблице задач с ошибками запуска, чтобы такие задачи повторно не учавствовали в выборе приоритетной
        time_start = time.time()
        while time.time() - time_start < TIME_PROCESS:
            task_node = getPriorityTask(ids_exclude_task=error_ids)
            if task_node:
                t = getClassByName(MODULE_TASK_LIST, task_node.title)#получаем класс-задачу
                if t:
                    task_params = getDictFromString(task_node.params)
                    curr_task = t()
                    amount = 0
                    task_node.setDtLastRun(datetime.datetime.now())
                    for item in curr_task.get_instances(**task_params):
                        if item.has_key('amount'):
                            amount = item['amount']   
                        if item.has_key('count') and amount>0:
                            curr_percent = item['count']*100/amount
                            if curr_percent != task_node.percent:
                                 task_node.setPercent(curr_percent)
                        if item.has_key('state') and item['state'] != task_node.state:
                            task_node.setState(item['state'])     
                        if item.has_key('result') and item['result'] != task_node.result:
                            task_node.setResult(item['result'])
                else:
                    error_ids.append(task_node.id)
            else:
                time.sleep(1)