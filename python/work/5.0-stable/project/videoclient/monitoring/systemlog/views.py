#coding=utf-8
from django.shortcuts import render_to_response
from videoclient import utils as vUtils
from monitoring import utils
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from videoclient.views import initBalancer, initCommunicators, tester, render_to_response_ex, video, getAllActiveCameras, getActiveSystemCameras
from videoclient.utils import get_value_defaultparams, VERSION
from videoclient.monitoring.systemlog import models
from videoclient.communicator import Communicator
import settings
import commands
import logging
import json
import sys
import re
from django.template.loader import render_to_string
import os
from django.utils.safestring import mark_safe
import zipfile
from videoclient.utils import dataNavigation
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
import videoclient
import math
from videoclient.communicator.models import Camera
from django import forms
from videoarchive.utils import getNavigation
from django.contrib.auth.decorators import permission_required
import datetime
from django.db import connections, transaction

CRITICAL_INDEX = 5
priority_map = {0: "EMERGENCY", 1: "ALERT", 2: "CRITICAL", 3: "ERROR", 4: "WARNING", 5: "NOTICE", 6: "INFO", 7: "DEBUG"}
facility_names = {0: "kern", 1: "user", 2: "mail", 3: "daemon", 4: "auth", 5: "syslog", 6: "lpr", 7: "news", 8: "uucp", 9: "cron", 10: "authpriv", 11: "ftp", 
                  16: "kpp", 17: "archive", 18: "local2", 19: "local3", 20: "local4", 21: "local5", 22: "local6", 23: "local7"}

order_list = ["id", "id", "receivedat",  "receivedat", "facility", "priority", "fromhost", "message", "eventsource", "syslogtag"]

def setFullInfo(row):
    data = {"id":row[0], "receivedat": row[2], "facility_id":row[4], "priority_id":row[5], "message":row[7], 
            "priority": priority_map.get(row[5], ""), "facility": facility_names.get(row[4], ""), "hostname": row[6],
            "eventsource": row[8], "syslogtag": row[9]}
    return data

class CheckLogForm(forms.Form):
    id_record = forms.IntegerField(required=False)
    facility = forms.IntegerField(required=False)
    priority = forms.IntegerField(required=False)
    dateBegin = forms.DateField(required=False)
    dateEnd = forms.DateField(required=False)
    hour1 = forms.IntegerField(required=False)
    hour2 = forms.IntegerField(required=False)
    minute1 = forms.IntegerField(required=False)
    minute2 = forms.IntegerField(required=False)
    second1 = forms.IntegerField(required=False)
    second2 = forms.IntegerField(required=False)
    description = forms.CharField(max_length=128, required=False)
    
    up = forms.IntegerField(required=False)
    sorto = forms.IntegerField(required=False)
    
    all_pages = forms.CharField(required=False)

@tester
@permission_required('user_perms.perm_monitoring')
def syslog_journal(request):
    data = dict()
    data.update(vUtils.getDefaultParams(request, 'monitoring_syslog_journal'))

    order_str = ""
    where_str = ""
    
    form = CheckLogForm(request.GET)
    if form.is_valid():
        # Сортировка
        try:
            order = form.cleaned_data.get("up", 0) or 0
            sort = form.cleaned_data.get("sorto", 0) or 0
            data["up"] = order
            data["sorto"] = sort
            order_str = "order by %s %s" % (order_list[sort], "asc" if str(order)=="1" else "desc")
        except:
            order_str = ""
        # Фильтр по id
        id_record = form.cleaned_data.get("id_record", 0)
        if id_record:
            data["id_record"] = id_record
            where_str = "id=%s" % id_record
        # Фильтра по источнику
        facility = form.cleaned_data.get("facility", -1)
        if facility != None  and int(facility) >= 0 and int(facility) in facility_names:
            data["facility"] = facility
            where_str = "%s%s facility=%s" % (where_str, "" if len(where_str)==0 else " and", facility)
        # Фильтра по приоритету
        priority = form.cleaned_data.get("priority", -1)
        if priority != None and int(priority) >= 0 and int(priority) in priority_map:
            data["priority"] = priority
            where_str = "%s%s priority='%s'" % (where_str, "" if len(where_str)==0 else " and", priority)
        # Фильтры по дате        
        dateBegin = form.cleaned_data.get("dateBegin", datetime.datetime.now()) or datetime.datetime.now()
        data["dateBegin"] = dateBegin
        param = {"where": where_str, 
                 "and": "" if len(where_str)==0 else " and", 
                 "date": dateBegin.strftime("%Y-%m-%d")}
        where_str = "%(where)s%(and)s receivedat>=(('%(date)s' || ' ' || '00:00:00')::timestamp)" % param               

        dateEnd = form.cleaned_data.get("dateEnd", datetime.datetime.now()) or datetime.datetime.now()
        data["dateEnd"] = dateEnd
        param = {"where": where_str, 
                 "and": "" if len(where_str)==0 else " and", 
                 "date": dateEnd.strftime("%Y-%m-%d")}
        where_str = "%(where)s%(and)s receivedat<=(('%(date)s' || ' ' || '23:59:59')::timestamp)" % param               
        # Фильтры по времени
        hour1 = form.cleaned_data["hour1"] if "hour1" in form.cleaned_data and form.cleaned_data["hour1"]>=0 else 0
        minute1 = form.cleaned_data["minute1"] if "minute1" in form.cleaned_data and form.cleaned_data["minute1"]>=0 else 0 
        second1 = form.cleaned_data["second1"] if "second1" in form.cleaned_data and form.cleaned_data["second1"]>=0 else 0        
        data["hour1"] = hour1
        data["minute1"] = minute1
        data["second1"] = second1
        if hour1+minute1+second1>0:
            data["time_check"] = True
            param = {"where": where_str, 
                 "and": "" if len(where_str)==0 else " and", 
                 "time": "%s:%s:%s" % (hour1, minute1, second1)}                
            where_str = "%(where)s%(and)s receivedat::time>='%(time)s'::time" % param               

        hour2 = form.cleaned_data["hour2"] if "hour2" in form.cleaned_data and form.cleaned_data["hour1"]>=0 else 23 
        minute2 = form.cleaned_data["minute2"] if "minute2" in form.cleaned_data and form.cleaned_data["minute2"]>=0 else 59 
        second2 = form.cleaned_data["second2"] if "second2" in form.cleaned_data and form.cleaned_data["second2"]>=0 else 59 
        data["hour2"] = hour2
        data["minute2"] = minute2
        data["second2"] = second2            
        if hour2+minute2+second2<141:
            data["time_check"] = True
            param = {"where": where_str, 
                  "and": "" if len(where_str)==0 else " and", 
                  "date": dateEnd.strftime("%Y-%m-%d"), 
                  "time": "%s:%s:%s" % (hour2, minute2, second2)}
            where_str = "%(where)s%(and)s receivedat::time<='%(time)s'::time" % param
        # Фильтры по описанию                 
        message = form.cleaned_data.get("description", "") or ""
        if message:
            data["description"] = message
            where_str = "%s%s message like '%s'" % (where_str, "" if len(where_str)==0 else " and", "%%"+message+"%%")
            
        if len(where_str) > 0: where_str = "where %s" % where_str

    params = {"fields": ",".join(order_list),
              "order": order_str,
              "start": "0",
              "limit": "10",
              "where": where_str}
    
    cursor = connections['systemlog'].cursor()

    cursor.execute('SELECT max(id)-min(id) FROM systemevents;')
    data["count"] = cursor.fetchall()[0][0]

    COL_JOURNAL_PAGES = 3
    limits = [15,20,25,30]
    if request.GET.has_key('per_page'):
        try:
            limit = int(request.GET['per_page'])
        except:
            limit = limits[0]
    else:
        limit = limits[0]
        
    journals = None
    params["limit"] = limit
         
    if form.cleaned_data["all_pages"]:
        cursor.execute('SELECT count(*) FROM systemevents %(where)s;' % params)
        len_data_list = cursor.fetchall()[0][0]
        data["find_events"] = len_data_list
        data["all_users"] = len_data_list
        data["all_pages"] = form.cleaned_data["all_pages"]
        if data["all_users"] > COL_JOURNAL_PAGES * limit:
           data["need_button"] = True
    else:
        params["limit"] = COL_JOURNAL_PAGES * limit + 1
        cursor.execute('SELECT %(fields)s FROM systemevents %(where)s %(order)s limit %(limit)s offset %(start)s;' % params)
        journals = cursor.fetchall()
        if len(journals) > COL_JOURNAL_PAGES * limit:
            data["all_users"] = COL_JOURNAL_PAGES * limit
            data["need_button"] = True
        else:
            data["all_pages"] = 'True'
            data["all_users"] = len(journals)
     
    data.update(dataNavigation(request, data['all_users'], limits=limits))
    if form.cleaned_data["all_pages"]:
        params["start"] = data['start'] - 1
        cursor.execute('SELECT %(fields)s FROM systemevents %(where)s %(order)s limit %(limit)s offset %(start)s;' % params)
        journals = cursor.fetchall()
    else: journals = journals[data['start'] - 1:data['finish'] - 1]
    journals = [setFullInfo(row) for row in journals]
    data["events"] = journals
    data["facility_list"] = facility_names
    data["priority_list"] = priority_map
    
    data.update(vUtils.dataGet(request, ignore_list=["page", "all_pages", "sorto", "up"]))
    data.update(dataGet(request, "sortvars", ["page", "all_pages"]))
    return render_to_response_ex(request, 'syslog_journal.html', data, context_instance=RequestContext(request))

def getMaxSyslogId():
    try:
        cursor = connections['systemlog'].cursor()
        cursor.execute('SELECT max(id) FROM systemevents;')
        return cursor.fetchall()[0][0]
    except:
        return None    

def getSyslogEvents(id):
    try:
        cursor = connections['systemlog'].cursor()
        params = {"fields": ",".join(order_list),
                  "order": "order by id desc ",
                  "id": id,
                  "priority": CRITICAL_INDEX}
        cursor.execute('SELECT %(fields)s FROM systemevents where id>%(id)s and priority<=%(priority)s %(order)s;' % params)
        return cursor.fetchall()
    except:
        return None    

def getSyslogEventsContent(event):
    contents = []
    if event[5] and priority_map.get(event[5], ""): contents.append("Статус: %s" % priority_map.get(event[5], ""))
    if event[4] and facility_names.get(event[4], ""): contents.append("Объект: %s" % facility_names.get(event[4], ""))
    if event[8]: contents.append("Источник: %s" % event[8])
    if event[9]: contents.append("Тэг: %s" % event[9])
    if event[6]: contents.append("Сервер: %s" % event[6])
    if event[7]: contents.append("Описание: %s" % event[7][:200]+"..." if len(event[7]) > 203 else event[7])
    date = event[2].strftime("%d.%m.%Y %H:%M:%S")
    content = "<br>".join(contents)
    return date, content    

@tester
@permission_required('user_perms.perm_monitoring')
def dataGet(request, name="getvars", list={}):
    data = dict()
    result = []
    get = request.GET
    for g in list:
        if g in get: result.append("%s=%s" % (g, get[g]))
    get_result = "&".join(result)
    data[name] = get_result
    return data