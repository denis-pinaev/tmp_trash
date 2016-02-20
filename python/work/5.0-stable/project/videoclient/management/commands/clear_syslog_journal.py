#coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import settings
import sys
import os
import datetime
from utils import queryset_iterator
from django.utils.translation import ugettext as _
from django.db import connections, transaction
from django.core.management.base import AppCommand
from optparse import make_option
import re

class Command(BaseCommand):
    option_list = AppCommand.option_list + (
        make_option('--datetime', action='store', dest='datetime', type="string", default= False, help='Удалить логи старше заданной зады, с указанием времени. Формат "%Y-%m-%d %H:%M:%S".' ),
        make_option('--date', action='store', dest='date', type="string", default= False, help='Удалить логи старше заданной даты. Формат "%Y-%m-%d".' ),
        make_option('--days', action='store', dest='days', type='int', default= False, help='Удалить логи старше заданного периода в днях' ),
    )
    help = 'Очистка журнала syslog.'

    requires_model_validation = True

    def handle(self, *args, **options):
        return self.deleteEvents(self.getDeleteDay(options))
        
    def getDeleteDay(self, options=None):
        clear_day = None

        date_time = options.get("datetime", False)
        if date_time:
            if re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", date_time):
                clear_day = date_time
        else:
            date = options.get("date", False)
            if date:
                m = re.match(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", date)
                if m:
                    clear_day = datetime.datetime(int(m.group("year")), int(m.group("month")), int(m.group("day")), 0, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
            else:
                days = options.get("days", False)
                if days or days==0:
                    clear_day = (datetime.datetime.now()-datetime.timedelta(days=int(days))).strftime("%Y-%m-%d %H:%M:%S")

        return clear_day
    
    def deleteEvents(self, day=None):
        if day:
            print "Delete data from the log of the date earlier than %s" % day    
            cursor = connections['systemlog'].cursor()
            cursor.execute("delete FROM systemevents where receivedat <= '%s'::timestamp;" %day)
            transaction.commit_unless_managed('systemlog')
        return

    