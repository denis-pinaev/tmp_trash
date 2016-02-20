#coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import sys
import json
import datetime
from videoclient.settings import log_videoclient as logging
from smilart_cron.utils import getClassByName,getDictFromString
from django.core.management.base import AppCommand
from optparse import make_option
from smilart_cron.models import Task
from django.utils.translation import ugettext as _

MODULE_TASKS = 'tasks'

class Command(BaseCommand):

    option_list = AppCommand.option_list + (
        make_option('--task', action='store', dest='task', type="string",  default= False ,help='Название запускаемой задачи' ),
        make_option('--params', action='store', dest='params', type="string", default= False, help='Параметры, с которыми запускается задача' ),
    )

    help = 'Запуск задачи на выполнение.'

    #example 
    #./manage.py run_task --task=CheckOpenTime --params='{"file":"/tmp/result.txt", "page":"journl/"}'

    requires_model_validation = True

    def handle(self, *args, **options):
        name_task = options.get("task", False)
        if not name_task:
            print 'Для запуска задачи вручную необходимо указать её название (--task)'
        task_nodes = Task.objects.filter(title=name_task, auto_run=False)
        if len(task_nodes)>0:
            task_node = task_nodes[0]
            t = getClassByName(MODULE_TASKS, task_node.title)#получаем класс-задачу
            if t:
                str_params = options.get("params", False)#получаем параметры запуска задачи
                task_params = getDictFromString(str_params)
                task_node.setDtLastRun(datetime.datetime.now())
                amount = 0
                curr_task = t()
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
                print name_task, 'class not found'
        else:
            print 'Task not found'
            logging.info('Task '+name_task+' not found')