#coding=utf-8
import sys
import os
import re
import datetime
from settings import PROJECT_ROOT
from django.utils.translation import ugettext as _
from django.db import connection, transaction
from videoclient import models
import logging
import json
from videoclient.utils import clearForCron, updateJournalStatistic
from utils import get_value_defaultparams
import httplib
import time
from urllib import urlencode
from videoclient import self_test
from views import initBalancer, initCommunicators 

STATE_PENDING = 0
STATE_RUNNING = 1

        
LOGIN = 'admin'
PASSWORD = 'eghfdkz.ofz cbcntvf'

def UnlinkFileDir(d):
    try:
        if os.path.exists(d): os.unlink(d)
        for i in range(4):
            d = os.path.dirname(d)
            os.rmdir(d)
        return True
    except:
        return False  

class Task(object):

    def get_instances(self,*arg,**kwargs):
        return True
    
#Очистка журнала
class ClearJournal(Task):
    
    AUTO_RUN = False #Параметр, отвечающий за автозапуск задачи
    PARAMS_AUTO_RUN = '{"all":true}' #Параметры автоматического запуска задачи
    FREQUENCY_AUTO_RUN = 10 #Промежуток между запусками задачи в секундах.
    
    MANUAL_RUN = True #Если MANUAL_RUN = True, то задачу можно запустить консольной командой через manage.py run_task
    
    #Параметры:
    #all : Очистка всего журнала
    #datetime : Удалить логи старше заданной зады, с указанием времени. Формат "%Y-%m-%d %H:%M:%S".
    #date : Удалить логи старше заданной даты. Формат "%Y-%m-%d".
    #days : Удалить логи старше заданного периода в днях
    def get_instances(self,*arg,**kwargs):
        print 'ClearJournal'
        try:
            dt = getDeleteDay(kwargs)
            if dt == None: return
        except:
            return
        data = dict()
        data["status"] = False         
        param_aggregator = models.ParamAggregator.getRecord()
        if dt == 'all':
            journals = models.Journal.objects.filter(id__lte = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID),id__gt = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID)).order_by('-id')
        else:
            journals = models.Journal.objects.filter(dt_first_fixed__lt=dt, id__lte = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID), id__gt = param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID)).order_by('-id')
        journal_len = int(journals.count())

        result = {'state': STATE_RUNNING, 'amount':journal_len}
        yield result
        if journal_len>0:
            journals_count = journals.extra(where=['videoclient_journal.id = videoclient_journal.agregate_id'])
            journals_count = journals_count.filter(id__gt=param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID))
            param_aggregator.setParam(models.ParamAggregator.PARAM_JOURNAL_COUNT, param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_COUNT) - journals_count.count())
            journals_count = journals_count.exclude(person=None)
            param_aggregator.setParam(models.ParamAggregator.PARAM_JOURNAL_IDENT_COUNT, param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_IDENT_COUNT) - journals_count.count())            
            param_aggregator.setParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID, journals[0].id)            
            
            count_j=0
            percent = 0
            from videoclient.utils import queryset_iterator
            generator = queryset_iterator(journals)
            for journal in generator:
                if journal.original:
                    logging.info(journal.original.path)
                    if os.path.exists(journal.original.path): UnlinkFileDir(journal.original.path)
                if journal.finded:
                    if os.path.exists(journal.finded.path): UnlinkFileDir(journal.finded.path)
                count_j+=1                
                #current_percent = count_j*100/journal_len
                #if current_percent != percent:
                    #percent = current_percent
                yield {'count':count_j}
                        
            from django.db import connection, transaction
            cursor = connection.cursor()
            
            repeat = 3
            while repeat>0:
                try:
                    if dt == 'all':
                        query = "delete from videoclient_lastident where agregate_id <= '%s' and agregate_id > '%s'" %(dt, param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID),param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID))
                    else:
                        query = "delete from videoclient_lastident where time<'%s' and agregate_id <= '%s' and agregate_id > '%s'" %(dt, param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID),param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID))
                    cursor.execute(query)
                    if dt == 'all':
                        query = "delete from videoclient_journal id <= '%s' and id > '%s'" %(dt, param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID),param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID))
                    else:                           
                        query = "delete from videoclient_journal where dt_first_fixed<'%s' and id <= '%s' and id > '%s' " %(dt, param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID),param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID))
                    cursor.execute(query)
                    repeat = 0
                except:
                    repeat-=1
                
            transaction.commit_unless_managed()

        result['state'] = STATE_PENDING
        result["result"] = json.dumps(data)
        yield result


#Очистка журнала syslog
class ClearSyslogJournal(Task):
    
    AUTO_RUN = False
    PARAMS_AUTO_RUN = '{"days":10}'
    FREQUENCY_AUTO_RUN = 10
    
    MANUAL_RUN = True 
    
    #Параметры:
    #datetime : Удалить логи старше заданной зады, с указанием времени. Формат "%Y-%m-%d %H:%M:%S".
    #date : Удалить логи старше заданной даты. Формат "%Y-%m-%d".
    #days : Удалить логи старше заданного периода в днях
    def get_instances(self,*arg,**kwargs):
        print 'ClearSyslogJournal'
        yield {'state': STATE_RUNNING, 'count':0, 'amount':1}     
        logging.info("ClearSyslogJournal")
        self.deleteEvents(getDeleteDay(kwargs))  
        yield {'state': STATE_PENDING, 'count':1} 

    
    def deleteEvents(self, day=None):
        if day:
            print "Delete data from the log of the date earlier than %s" % day    
            from django.db import connections, transaction
            cursor = connections['systemlog'].cursor()
            cursor.execute("delete FROM systemevents where receivedat <= '%s'::timestamp;" %day)
            transaction.commit_unless_managed('systemlog')

    
def getDeleteDay(options):
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


#Очистка устаревших данных журнала и системных логов.
class ClearOldData(Task):
   
    AUTO_RUN = True #Параметр, отвечающий за автозапуск задачи
    FREQUENCY_AUTO_RUN = 86400 #Промежуток между запусками задачи в секундах. (раз в сутки)
    MANUAL_RUN = False #Если MANUAL_RUN = True, то задачу можно запустить консольной командой через manage.py run_task
    
    #запускается без параметров, данные о количестве дней берутся из базы.
    def get_instances(self,*arg,**kwargs):
        print 'ClearOldData'
        yield {'state': STATE_RUNNING, 'count':0, 'amount':1}  
        logging.info('ClearOldData')
        
        period=get_value_defaultparams("period_storage_data")
        os.system('cd %s;python ./manage.py run_task --task=ClearJournal --params={"days":%s}' % (PROJECT_ROOT+'project/videoclient/', period))
        os.system('cd %s;python ./manage.py run_task --task=ClearSyslogJournal --params={"days":%s}' % (PROJECT_ROOT+'project/videoclient/', period))
        yield {'state': STATE_PENDING, 'count':1}   
  
        
class TestingTemperature(Task):
    AUTO_RUN = False #Если AUTO_RUN = True, то задача будет запускаться автоматически
    FREQUENCY_AUTO_RUN = 10 #Промежуток между запусками задачи в секундах.
    
    def get_instances(self,*arg,**kwargs):
        print 'TestingTemperature'
        yield {'state': STATE_RUNNING, 'count':0, 'amount':1}
        
        # Проверяем настроена система или нет перед запуском тестирования
        HOST, PORT, LOGIN, PASSWD, USER, check = initBalancer(True)
        if check:
            SERVERC, PORTC, COMMUNICATORS = initCommunicators()
            if len(COMMUNICATORS) == 0:
                yield {'state': STATE_PENDING, 'count':1}
        
        logging.info('TestingTemperature')
        st=get_value_defaultparams("self_test")
        if st == "1":
            self_test.testing()
        else:
            tb=get_value_defaultparams("testing_balancer")
            if tb == "1":
                self_test.testing_balancer()
        yield {'state': STATE_PENDING, 'count':1} 
  
        
class UpdateJournalStatistic(Task):
    AUTO_RUN = True #Если AUTO_RUN = True, то задача будет запускаться автоматически
    FREQUENCY_AUTO_RUN = 15 #Промежуток между запусками задачи в секундах.
        
    def get_instances(self,*arg,**kwargs):
        print 'UpdateJournalStatistic'
        yield {'state': STATE_RUNNING, 'count':0, 'amount':1}     
        logging.info("UpdateJournalStatistic")
        updateJournalStatistic()   
        yield {'state': STATE_PENDING, 'count':1} 
        
        
class CheckClear(Task):
    AUTO_RUN = True #Если AUTO_RUN = True, то задача будет запускаться автоматически
    FREQUENCY_AUTO_RUN = 60 #Промежуток между запусками задачи в секундах.
        
    def get_instances(self,*arg,**kwargs):
        print 'CheckClear'
        yield {'state': STATE_RUNNING, 'count':0, 'amount':1}     
        logging.info("CheckClear")
        clearForCron()  
        yield {'state': STATE_PENDING, 'count':1}
        

def init_connection(host, port):
    try:
        return httplib.HTTPConnection(host, port)
    except Exception as http_exception:
        print 'error init_connection'

def get_login_token(connection, login, password):
    # Формируем url для входа
    url = '/'
    parameters = urlencode({
                            'login': login,
                            'password': password,
                            })    
    # Отправляем запрос
    connection.request('POST', url, parameters)
    response = connection.getresponse()
    
    if response.status == 200:
        print 'Login fault. Password rejected'
    
    if response.status <> 302:
        print 'Login fault. Unsupported request.status'
    
    # Вычитываем переданные данные, чтобы освободить сокет
    response.read()
    
    # Получаем и обрабатываем cookies
    if 'set-cookie' not in response.msg:
        print 'Login fault. No set-cookie in response header'
        
    set_cookie = response.msg['set-cookie']
    
    cookies_list = [cookie.lstrip().rstrip().split('=') for cookie in set_cookie.split(';')]
    
    cookies = {}
    for cookie in cookies_list:
        cookies[cookie[0]] = cookie[1]
    
    # Получаем id сессии
    if 'sessionid' not in cookies:
        print 'Login fault. No sessionid in cookies'
    
    # Формируем токен
    sessionid = '%s=%s' % ('sessionid', cookies['sessionid'])
    return sessionid
    
    
def http_send(connection, url, parameters, auth_token):
    try:
        # Формируем header с id сессии
        headers = {
                   'Cookie': auth_token,
                   }
        # Формируем строку параметров
        params_url = urlencode(parameters)
        
        # Для GET запроса все параметры передаются в url
        if len(params_url) > 0:
            full_url = '%s?%s' % (url, params_url)
        else:
            full_url = url
        
        # Отправляем запрос
        connection.request('GET', full_url, '', headers)
        
    except Exception as http_exception:
        print 'error http_send'


def http_recv(connection):
    try:
        # Получаем статус и данные
        response = connection.getresponse()
        response_data = response.read()
         
        # Возвращаем кортеж
        return response.status, response_data 
    
    except Exception as http_exception:
        print 'http_recv'
    

#Измерение времени отлика системы.
class CheckOpenTime(Task):
    
    AUTO_RUN = False
    FREQUENCY_AUTO_RUN = 10
    
    MANUAL_RUN = False 
    
    #Параметры:
    #file : Название файла для записи результатов.
    #page : Страница, на которой будут замеряться время
    def get_instances(self,*arg,**kwargs):
        print 'CheckOpenTime'
        yield {'state': STATE_RUNNING, 'count':0, 'amount':1}    
        logging.info("CheckOpenTime")
        file_name = kwargs.get("file", False)
        if not file_name:
            print 'Необходимо указать файл для записи результатов'
            return
        try:
            f = open(file_name, 'a')
        except:
            print 'Неверно указан файл'
            return        
        page = kwargs.get("page", 'ident/')
        request_url = 'http://127.0.0.1/' + page 
        conn = init_connection('127.0.0.1', 80)
        auth_token = get_login_token(conn, LOGIN, PASSWORD)
        t1 = time.time()
        http_send(conn, request_url, '', auth_token)
        status, json = http_recv(conn)
        t2 = time.time()
        f.write(str(datetime.datetime.now()) + ' ' + str(t2 - t1) + '\n')
        f.close
        print str(datetime.datetime.now()) + ' ' + str(t2 - t1)
        yield {'state': STATE_PENDING, 'count':1}
         

#Самотестирование         
class SelfTest(Task):
    
    AUTO_RUN = True
    FREQUENCY_AUTO_RUN = 1200
    
    MANUAL_RUN = True 
    
    def get_instances(self,*arg,**kwargs):
        print 'SelfTest'
        yield {'state': STATE_RUNNING, 'count':0, 'amount':1}
        
        # Проверяем настроена система или нет перед запуском тестирования
        HOST, PORT, LOGIN, PASSWD, USER, check = initBalancer(True)
        if check:
            SERVERC, PORTC, COMMUNICATORS = initCommunicators()
            if len(COMMUNICATORS) == 0:
                yield {'state': STATE_PENDING, 'count':1}
        
        from django.db import connection
        cur = connection.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('self_test_timecontrol',))
        if bool(cur.rowcount):
            self_test.testing()
        yield {'state': STATE_PENDING, 'count':1}