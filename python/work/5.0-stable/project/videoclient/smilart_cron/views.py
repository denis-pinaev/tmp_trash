#coding=utf-8
import datetime
from smilart_cron.models import Task as TableTask
from smilart_cron.utils import getClassByName 
import sys
from settings import MODULE_TASK_LIST

def initTaskList():
    module = MODULE_TASK_LIST
    imported_module_object = __import__(module)
    BaseTask = getClassByName(module, 'Task')
    for class_name in dir(imported_module_object):
        c = getClassByName(module, class_name)
        try:
            if c and isinstance(c(), BaseTask) and c!=BaseTask:
                auto_run = False
                if c.__dict__.has_key('AUTO_RUN'):
                    auto_run = c.__dict__['AUTO_RUN']   
                if auto_run:
                    frequency = 0
                    if c.__dict__.has_key('FREQUENCY_AUTO_RUN'):
                        frequency = c.__dict__['FREQUENCY_AUTO_RUN']                    
                    params_auto_run = ''
                    if c.__dict__.has_key('PARAMS_AUTO_RUN'):
                        params_auto_run = c.__dict__['PARAMS_AUTO_RUN']

                    t = TableTask.objects.get_or_create(title=class_name, auto_run=True)
                    if t:
                        t[0].title = class_name
                        t[0].frequency = frequency
                        t[0].params = params_auto_run
                        t[0].save()
               
                manual_run = False
                if c.__dict__.has_key('MANUAL_RUN'):
                    manual_run = c.__dict__['MANUAL_RUN']
                if manual_run:
                    t = TableTask.objects.get_or_create(title=class_name, auto_run=False)
                    if t:
                        t[0].title = class_name
                        t[0].frequency = 0
                        t[0].params = 0
                        t[0].save()
        except:
            pass
    return True
