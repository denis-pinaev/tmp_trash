#coding=utf-8

import models
import logging
import datetime
import settings
import commands
import forms
import sys
import re
from videoclient.views import initBalancer, initCommunicators, tester
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.utils import simplejson


def getSystemData(request):
    data = dict()
    #data.update(vUtils.getDefaultParams(request, 'monitoring_system', None))
    
    if settings.space:    
        s = commands.getoutput(settings.space)
        s = s.replace("\n", "")
        m = re.match(r".*G *([0-9]+)%.*", s)
        if m and m.group(1):
            data["space"] = 100-int(m.group(1))
    if settings.raid_status:    
        s = commands.getoutput(settings.raid_status)
        data["raid_status"] = s            
    try:
   
        from videoclient.balancer import Balancer
        
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        data['balancers'] = b.getSystemInfo()
        b.close()
        del b
    except:
        logging.exception("monitoring_system "+str(sys.exc_info()))
    return data

def getEventsData(request, last=False):
    data = dict()
    data['MONITORING_STATUS_CHOICES'] = models.MONITORING_STATUS_CHOICES
    data['MONITORING_TYPE_CHOICES'] = models.MONITORING_TYPE_CHOICES
    sort = [[],["id"],
            ["date"],
            ["time"],
            ["status"],
            ["type"],
            ["description"],
            ]

    s = 0
    up = 0
    
    events = models.Events.objects.all().order_by('-id')
    data["count"] = len(events)
    form = forms.CheckEventsFilterForm(request.REQUEST)
    if form.is_valid():
        now = datetime.datetime.now()
        today = datetime.date(year=now.year, month=now.month, day = now.day)
        
        if form.cleaned_data["dateBegin"]:
            dateBegin = form.cleaned_data["dateBegin"]
        else:
            dateBegin = today
        data["dateBegin"] = dateBegin
        events = events.filter(date__gte=dateBegin)
          
        if form.cleaned_data["dateEnd"]:
            dateEnd = form.cleaned_data["dateEnd"]
        else:
            dateEnd = today
        data["dateEnd"] = dateEnd
        events = events.filter(date__lte=dateEnd)  
        
        timeBegin = datetime.time (0,0,0)        
        if form.cleaned_data["hour_beg"]:
            timeBegin = datetime.time (int(form.cleaned_data["hour_beg"]),0,0)
        if form.cleaned_data["min_beg"]:
            timeBegin = datetime.time (timeBegin.hour, int(form.cleaned_data["min_beg"]),0)
        data["timeBegin"]= {"hour":str(timeBegin.hour),"minute":str(timeBegin.minute)}  
        if timeBegin.hour!=0 or timeBegin.minute!=0:
            events = events.filter(time__gte=timeBegin)
            data["time_check"] = True
            
        timeEnd = datetime.time (23,59,59)        
        if form.cleaned_data["hour_end"]!=None:
            timeEnd = datetime.time (int(form.cleaned_data["hour_end"]),59,59)
        if form.cleaned_data["min_end"]!=None:
            timeEnd = datetime.time (timeEnd.hour, int(form.cleaned_data["min_end"]),59) 
        data["timeEnd"]={"hour":str(timeEnd.hour),"minute":str(timeEnd.minute)}  
        if timeEnd.hour!=23 or timeEnd.minute!=59:
            events = events.filter(time__lte=timeEnd)
            data["time_check"] = True
               
        if form.cleaned_data["id_record"]:
            id = form.cleaned_data["id_record"]
            if id.isdigit():
                events = events.filter(id=id)
                data["id_record"] = form.cleaned_data["id_record"]
 
        if form.cleaned_data["status"]:
            status = form.cleaned_data["status"]
            if status != "0": 
                data["status"] = status
                events = events.filter(status=status)            
          
        if form.cleaned_data["type"]:
            type = form.cleaned_data["type"]
            if type != "0": 
                data["type"] = type
                events = events.filter(type=type) 
            
        
        if form.cleaned_data["description"]:
            data["description"] = form.cleaned_data["description"]
            fs = u""+form.cleaned_data["description"]
            fs = fs.split()
            i = 0
            while i<len(fs):
                f = fs[i]
                events = events.filter(Q(description__icontains=f))
                i = i+1
                
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"]==1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"]>0 and form.cleaned_data["sorto"]<=len(sort): s = form.cleaned_data["sorto"]
        else: 
            s = 1
            up = 1      
        events = events.order_by("%s%s" % ("-" if up==1 else "", sort[s][0]))        
        data["up"] = up
        data["sorto"] = s
    else:
        logging.info("getDataVideo:" + str(form.errors))
    data["found"] = events.count()
    data["events"] = events
    if last:
        from videoclient.self_test import models as sModels
        datetimes = sModels.TimeControl.objects.all().order_by('-id')
        if datetimes.count()>0:
            datetimes = datetimes[0].datetime
        else:
            datetimes = datetime.datetime.now()
        date = datetime.date(year=datetimes.year, month=datetimes.month, day=datetimes.day)
        events = events.filter(date=date)
        
        time1 = datetime.time(hour = datetimes.hour, minute=datetimes.minute, second=datetimes.second)
        as1 = (time1.hour*60+time1.minute)*60+time1.second
        
        start = 0
        i = 0
        finish = len(events)-1
        
        events_j = []
        while i<len(events):
            #time1 = events[i-1].time
            events_j.append(events[i].getDict())
            time2 = events[i].time
            as2 = (time2.hour*60+time2.minute)*60+time2.second
            if as2-as1>60:
                start = i
            elif as1 > as2 or as2-60>as1:
                finish = i-1
                break
            i = i+1
        if finish>start:
            data["events"] = events_j[start:finish]
        else:
            data["events"] = []
    else:
        events_b = []
        for event in events:
            events_b.append(event.getDict())  
        data["events"] = events_b

    return data

def saveMonitoringMessage(**kwargs):
    import monitoring
    action = kwargs["action"] if 'action' in kwargs else 'warning'
    
    nkwargs = dict()
    if 'id' in kwargs:
        params = kwargs["params"] if 'params' in kwargs else dict()
        json_description = {"id":kwargs["id"],"params":params}
        kwargs["json_description"] = simplejson.dumps(json_description)
        nkwargs["message_id"] = kwargs["id"]
    
    #TODO: получать список полей таблицы
    allow_keys = [field.name for field in monitoring.models.Events._meta.fields]
    #allow_keys = ['date', 'description', 'error_file', 'events_sessions', 'json_description', 'sessions', 'show', 'status', 'time', 'type']
    nkwargs = {"message_id": kwargs["id"]}
    for key in kwargs:
        if key in allow_keys and not key == "id":
            nkwargs[key] = kwargs[key]
        
    logging.info('%s %s'%(action, nkwargs["json_description"]))
    
    if action == 'warning':
        monitoring.warning(**nkwargs)
    elif action == 'info':
        monitoring.info(**nkwargs)
    else:
        monitoring.action(**nkwargs)
        
def getMonitoringMessage(description, json_description):
    if not json_description: return _(description)
    try:
        json = simplejson.loads(json_description)
    except:
        return _(description)
    
    
    
    params = json['params']
    logging.info('%s %s'%(json["id"], json['params']))
    if json["id"] == 'update_ok': return _('Обновление для ревизии %(version)s')%params
    if json["id"] == 'update_no': return _('Ошибка обновления для ревизиии %(version)s')%params
    if json["id"] == 'space_info_videoarchive_critical': return _("Видеоархив: %(host)s:%(port)s. Свободного места на диске: %(free)s%%, некоторые ролики будут удалены.")%params
    if json["id"] == 'space_info_videoarchive': return _("Видеоархив: %(host)s:%(port)s. Свободного места на диске: %(free)s%%.")%params
    if json["id"] == 'space_info_critical': return _("Свободного места на диске: %(free)s%%, некоторые ролики будут удалены")%params
    if json["id"] == 'space_info': return _("Свободного места на диске: %(free)s%%")%params
    if json["id"] == 'import_error_videoarchive': return _("Видеоархив: %(host)s:%(port)s. Ошибка импорта")%params
    if json["id"] == 'import_error': return _("Ошибка импорта")%params
    if json["id"] == 'videoarchive_error': return _("Ошибка подключения к демону видеоархива, демон %(host)s:%(port)s.") % params
    if json["id"] == 'start_testing': return _(description)# + _("Начало тестирования")#not used???
    if json["id"] == 'finish_testing': return _("Тестирование выполнено успешно")#not used
    if json["id"] == 'wrong_path': return _("Путь к фотографиям не найден, тестирование FaceDetect невозможно продолжить.")#not used
    if json["id"] == 'cs_unavailable': return _("Управляющая система %(host)s:%(port)s недоступна") % params
    if json["id"] == 'unstable_facedetect': return _("Нестабильная работа FaceDetect, успешных тестов %(count)s из %(all)s.") % params
    if json["id"] == 'camera_unavailable': return _("Камера %(ip)s %(type)s %(uuid)s недоступна") % params
    if json["id"] == 'communicator_unavailable': return _("Коммуникатор %(HOST)s:%(PORT)s недоступен") % params
    if json["id"] == 'cs_unavailable_test': return _("Управляющая система %(HOST)s:%(PORT)s недоступна, тестирование балансировщиков невозможно продолжить.") % params
    if json["id"] == 'balancer_unavailable': return _("Балансировщик %(HOST)s:%(PORT)s недоступен") % params
    if json["id"] == 'daemon_unavailable': return _("Демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s недоступен") % params
    if json["id"] == 'license_incorrect': return _("Не верный формат даты лицензии, поддерживаемый формат '%(format)s', текущее значение: %(days)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params
    if json["id"] == 'license_finished': return _("Закончился срок действия лицензии, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params
    if json["id"] == 'license_finishing': return _("Заканчивается срок действия лицензии, осталось %(days)s день/дней, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params
    if json["id"] == 'temperature_overloaded': return _("Перегрузка по температуре, текущее значение: %(temp)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params
    if json["id"] == 'temperature_overloading': return _("Возможно перегрузка по температуре, текущее значение: %(temp)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params
    if json["id"] == 'import_error': return _("Ошибка импорта")
    if json["id"] == 'cs_connect_error': return _("Ошибка подключения к Управляющей системе %(host)s:%(port)s") % params
    if json["id"] == 'communicator_timeout': return _("Превышено время ожидания соединения с Коммуникатором %(host)s:%(port)s") % params
    if json["id"] == 'communicator_connect_error': return _("Ошибка подключения к Коммуникатору %(host)s:%(port)s") % params
    if json["id"] == 'videoarchive_settings_error': return _("Ошибка задания параметров демона видеоархива, демон %(host)s:%(port)s") % params
    #if json["id"] == : return
    
    return _(description)
    