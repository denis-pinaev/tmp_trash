#coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import settings
import sys
import os
import logging
import datetime
from videoclient import models
from utils import queryset_iterator
from django.utils.translation import ugettext as _
from status_thread.models import Status
from django.db import connection, transaction
from django.core.management.base import AppCommand
from optparse import make_option
import re

def UnlinkFileDir(d):
    try:
        if os.path.exists(d): os.unlink(d)
        for i in range(4):
            d = os.path.dirname(d)
            os.rmdir(d)
        return True
    except:
        return False  

class Command(BaseCommand):
    option_list = AppCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default= False, help='Очистка всего журнала' ),
        make_option('--datetime', action='store', dest='datetime', type="string", default= False, help='Удалить логи старше заданной зады, с указанием времени. Формат "%Y-%m-%d %H:%M:%S".' ),
        make_option('--date', action='store', dest='date', type="string", default= False, help='Удалить логи старше заданной даты. Формат "%Y-%m-%d".' ),
        make_option('--days', action='store', dest='days', type='int', default= False, help='Удалить логи старше заданного периода в днях' ),
        make_option('--id', action='store', dest='id', type='int', default=0, help='ID status-потока' ),
    )
    help = 'Очистка журнала идентификаций.'

    requires_model_validation = True

    def handle(self, *args, **options):
        try:
            dt = self.getDeleteDay(options)
            if dt == None: return
        except:
            return
 
        thread_id = options.get("id", 0)
        thread = ''
        if thread_id > 0:
            try:
                thread = Status.objects.get(id=thread_id)
            except:
                thread = False

        data = dict()
        data["status"] = False
                
        param_aggregator = models.ParamAggregator.getRecord()
        if dt == 'all':
            journals = models.Journal.objects.filter(id__lte = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID),id__gt = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID)).order_by('-id')
        else:
            journals = models.Journal.objects.filter(dt_first_fixed__lt=dt, id__lte = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID), id__gt = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID)).order_by('-id')
        journal_len = int(journals.count())
        
        if thread:
            thread.setRunning()
        if journal_len>0:
            journals_count = journals.extra(where=['videoclient_journal.id = videoclient_journal.agregate_id'])
            journals_count = journals_count.filter(id__gt=param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID))
            param_aggregator.setParam(models.ParamAggregator.PARAM_JOURNAL_COUNT, param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_COUNT) - journals_count.count())
            journals_count = journals_count.exclude(person=None)
            param_aggregator.setParam(models.ParamAggregator.PARAM_JOURNAL_IDENT_COUNT, param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_IDENT_COUNT) - journals_count.count())            
            param_aggregator.setParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID, journals[0].id)            
            
            count_j=0
            percent = 0
            
            generator = queryset_iterator(journals) # создаём генератор
            for journal in generator:
                if journal.original:
                    logging.info(journal.original.path)
                    if os.path.exists(journal.original.path): UnlinkFileDir(journal.original.path)
                if journal.finded:
                    if os.path.exists(journal.finded.path): UnlinkFileDir(journal.finded.path)
                count_j+=1                
                if thread:
                    current_percent = count_j*100/journal_len
                    if current_percent != percent:
                        if current_percent>100:
                            current_percent = 100
                        percent = current_percent
                        thread.setPercent(percent)
            from django.db import connection, transaction
            cursor = connection.cursor()
            try:
                last_id = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID)
                first_id = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID)
                if dt == 'all':
                    query = " ".join(["delete from videoclient_lastident where agregate_id <= '%(last_id)s' and agregate_id > '%(first_id)s';",
                                      "delete from videoclient_journal where id <= '%(last_id)s' and id > '%(first_id)s';"
                                      ]) % ({"last_id": last_id, "first_id": first_id})
                                      
                else:
                    query = " ".join(["delete from videoclient_lastident where time<'%(dt)s' and agregate_id <= '%(last_id)s' and agregate_id > '%(first_id)s';",
                                      "delete from videoclient_journal where dt_first_fixed<'%(dt)s' and id <= '%(last_id)s' and id > '%(first_id)s';"
                                      ]) %({"dt": dt, "last_id": last_id, "first_id": first_id})
                cursor.execute(query)
            except:
                logging.exception("clear_journal")

            transaction.commit_unless_managed()

        data["status"] = True
        print 'data=',data
        if thread:
            thread.setFinished()
            thread.setAnswer(data)
            
    def getDeleteDay(self, options=None):
        clear_day = None
        
        all = options.get("all", False)
        if all: return 'all'
 
        date_time = options.get("datetime", False)
        if date_time:
            if re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", date_time):
                clear_day = date_time
        else:
            date = options.get("date", False)
            if date:
                m = re.match(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", date)
                if m:
                    clear_day = datetime.datetime(int(m.group("year")), int(m.group("month")), int(m.group("day"))).strftime("%Y-%m-%d")
            else:
                days = options.get("days", False)
                if days or days==0:
                    clear_day = (datetime.datetime.now()-datetime.timedelta(days=int(days))).strftime("%Y-%m-%d %H:%M:%S")

        return clear_day            