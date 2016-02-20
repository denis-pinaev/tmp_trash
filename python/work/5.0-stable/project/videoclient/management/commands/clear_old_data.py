#coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import settings
import sys
import os
import logging
from utils import get_value_defaultparams



class Command(BaseCommand):
    help = 'Очистка устаревших данных журнала и системных логов.'

    def handle(self, *args, **options):
        period=get_value_defaultparams("period_storage_data")
        try:
            query = 'cd %s;python ./manage.py clear_journal --days=%s' % (settings.PROJECT_ROOT+'project/videoclient/', period)
            pid = os.spawnvp(os.P_NOWAIT, 'sh', ['sh',  '-c', query])
            query = 'cd %s;python ./manage.py clear_syslog_journal --days=%s' % (settings.PROJECT_ROOT+'project/videoclient/', period)
            pid = os.spawnvp(os.P_NOWAIT, 'sh', ['sh',  '-c', query])
        except:
            logging.exception("clear old data: "+str(sys.exc_info()))