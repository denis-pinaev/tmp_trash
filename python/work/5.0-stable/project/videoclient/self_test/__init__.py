#coding=utf-8

from django.conf import settings
from videoclient import settings as vaSettings
from videoclient.views import initBalancer, initCommunicators
from videoclient.balancer import Balancer
from videoclient.communicator import Communicator
from videoclient import models as vModels
from videoclient.communicator.models import Camera
from videoclient.utils import get_value_defaultparams
import sys
import os
import monitoring
from videoclient.settings import log_self_test as logging
import models
import datetime
from django.utils.translation import ugettext as _
from django.utils import simplejson
from monitoring.utils import saveMonitoringMessage

DEFAULT_FACES_PATH = getattr(settings, 'FACES_PATH', os.path.join( os.path.dirname(__file__), 'faces/'))
DEFAULT_FACES_3_PATH = getattr(settings, 'FACES_PATH', os.path.join(DEFAULT_FACES_PATH, '3/'))
DEFAULT_FACES_5_PATH = getattr(settings, 'FACES_PATH', os.path.join(DEFAULT_FACES_PATH, '5/'))
DEFAULT_FACES_RESAULT = getattr(settings, 'FACES_PATH', os.path.join(DEFAULT_FACES_PATH, 'resault.json'))



if int(get_value_defaultparams(vaSettings.self_test, default_value = 0)):
    START_TESTING_WITH_START_SYSTEM = True
else:
    START_TESTING_WITH_START_SYSTEM = False
DEFAULT_FD_PHOTOS = getattr(settings, 'SELF_TEST_DEFAULT_FD_PHOTOS', os.path.join( os.path.dirname(__file__), 'FD_photos/'))
DEFAULT_EXT = getattr(settings, 'SELF_TEST_DEFAULT_EXT', ['.jpg', '.png'])
DEFAULT_INFO_TEMPERATURE = getattr(settings, 'SELF_TEST_DEFAULT_INFO_TEMPERATURE', 90)
DEFAULT_WARNING_TEMPERATURE = getattr(settings, 'SELF_TEST_DEFAULT_WARNING_TEMPERATURE', 97)
DEFAULT_DELAY_CRON_FOR_TEMPERATURE_TESTING = getattr(settings, 'SELF_TEST_DEFAULT_DELAY_CRON_FOR_TEMPERATURE_TESTING', 1800)
DEFAULT_DAYS_LIMIT_FOR_LICENSE = getattr(settings, 'SELF_TEST_DAYS_LIMIT_FOR_LICENSE', 30)


def testing():
    try:
        res = True
        if not testing_time(): return False
        
        if res:
            #monitoring.info(type='testing', description=_("Начало тестирования"))
            saveMonitoringMessage(error_level=1, action='info', type='testing', description=_("Начало тестирования"), id='start_testing')
        us = True
        if not testing_US():
            us = False 
            res = False
        elif not testing_FD():
            res = False
        if not testing_comunicators_cameras(): res = False
        if us and not testing_balancer():
            res = False
            
        if res:
            #monitoring.info(type='testing', description=_("Тестирование выполнено успешно"))
            saveMonitoringMessage(error_level=1, action='info', type='testing', description=_("Тестирование выполнено успешно"), id='finish_testing')
        else:
            saveMonitoringMessage(error_level=1, action='info', type='testing', description=_("Тестирование завершено с ошибками"), id='finish_testing') 
        return res
    except:
        logging.exception("testing: "+str(sys.exc_info()))

def testing_US():
    try:
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        b.open()
        b.close()
        del b
        return True
    except:
        logging.exception("testingUS: "+str(sys.exc_info()))
        params = {'host':HOST, 'port':PORT}
        #monitoring.warning(type='accident_components', description=_("Управляющая система %(host)s:%(port)s недоступна") % params )
        saveMonitoringMessage(error_level=0, type='accident_components', description=_("Управляющая система %(host)s:%(port)s недоступна") % params, params = params, id='cs_unavailable')
    return False
    

def r_testing_FD(path = DEFAULT_FD_PHOTOS):
    all = 0
    test = 0
    for file in os.listdir(path):
        try:
            filename = os.path.join(path, file)
            if os.path.isdir(filename):
                add_test, add_all= r_testing_FD(filename)
                all+=add_all
                test+=add_test
            elif filename[-4:] in DEFAULT_EXT and os.path.isfile(filename):
                logging.info(filename)
                all+=1
                f = open(filename, 'r+b')
                data = f.read()
                f.close()
                HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
                b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
                b.faceDetect(data)
                b.close()
                del b
                test+=1
            
        except:
            logging.exception("r_testing_FD: "+str(sys.exc_info()))
    return (test, all)
            
    
def testing_FD():
    path = DEFAULT_FD_PHOTOS
    if not os.path.exists(path):
        #monitoring.warning(type='accident_components', description=_("Путь к фотографиям не найден, тестирование FaceDetect невозможно продолжить."))
        saveMonitoringMessage(error_level=0, type='accident_components', description=_("Путь к фотографиям не нейден, тестирование FaceDetect невозможно продолжить."), id='wrong_path')
        return False
    else:
        test, all = r_testing_FD(path)
    
    if test == all:
        return True

    params = {'count':test, 'all':all}
    #monitoring.warning(type='accident_components', description=_("Нестабильная работа FaceDetect, успешных тестов %(count)s из %(all)s.") % params)
    saveMonitoringMessage(error_level=0, type='accident_components', description=_("Нестабильная работа FaceDetect, успешных тестов %(count)s из %(all)s.") % params, params = params, id = 'unstable_facedetect')
    
    return False

def testing_comunicators_cameras():

    res = True
    
    c = Communicator()
    res_cameras = c.getCameras(filter_active=True)
    c.close()
    del c
    
    if res_cameras["success"]:
        disappered_cams = res_cameras["disappeared_cams"]
        communicator_errors_info = res_cameras["communicator_errors_info"]
        
        for d_cam in disappered_cams:
            res = False
            params = {'ip': d_cam.ip, 'type': d_cam.type, 'uuid': d_cam.uuid}
            saveMonitoringMessage(error_level=0, type='accident_components', description=_("Камера %(ip)s %(type)s %(uuid)s недоступна") % params, params = params, id = 'camera_unavailable' )
            logging.info("Camera %(ip)s %(type)s %(uuid)s is unavailable" % params)
        
        for com_error in communicator_errors_info:
            res = False
            params = {'HOST': com_error["host"], 'PORT': com_error["port"]}
            saveMonitoringMessage(error_level=0, id = 'communicator_unavailable', params = params, type='accident_components', description=_("Коммуникатор %(HOST)s:%(PORT)s недоступен") % params )
            logging.info("Communicator %(HOST)s:%(PORT)s is unavailable" % params)
    else:
        logging.info("Testing_comunicators_cameras method c.getCameras result: False")

    return res 


def testing_balancer():
    res = True
    try:
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        balancers = b.getSystemInfo()
        b.close()
    except:
        params = {'HOST':HOST, 'PORT':PORT}
        #monitoring.warning(type='accident_components', description=_("Управляющая система %(HOST)s:%(PORT)s недоступна, тестирование балансировщиков невозможно продолжить.") % params )
        saveMonitoringMessage(error_level=0, id = 'cs_unavailable_test', params = params, type='accident_components', description=_("Управляющая система %(HOST)s:%(PORT)s недоступна, тестирование балансировщиков невозможно продолжить.") % params )
        return False
    if not ('balancer' in balancers):
        return res
    for balancer in balancers["balancer"]:
        if not ('active' in balancer):
            continue
        if balancer["active"] != "true":
            res = False
            params = {'HOST':balancer["address"], 'PORT':balancer["port"]}
            #monitoring.warning(type='accident_components', description=_("Балансировщик %(HOST)s:%(PORT)s недоступен") % params )
            saveMonitoringMessage(error_level=0, id = 'balancer_unavailable', params = params, type='accident_components', description=_("Балансировщик %(HOST)s:%(PORT)s недоступен") % params )
        elif 'daemons' in balancer:
            for daemons in balancer['daemons']:
                for daemon in daemons["daemon"]:
                    if not ('active' in daemon):
                        continue
                    if daemon["active"] != "true":
                        res = False
                        params = {'type':daemon["type"], 'daddress':daemon["address"], 'dport':daemon["port"], 'baddress':balancer["address"], 'bport':balancer["port"] }
                        #monitoring.warning(type='accident_components', description=_("Демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s недоступен") % params )
                        saveMonitoringMessage(error_level=0, id = 'daemon_unavailable', params = params, type='accident_components', description=_("Демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s недоступен") % params )
                    if daemon.has_key("license_days"):
                        license_days = None
                        license_days_format = '%Y-%m-%d %H:%M:%S'
                        try:
                            license_days = datetime.datetime.strptime(daemon["license_days"], license_days_format)
                        except ValueError:
                            params = {'format':license_days_format, 'days':daemon['license_days'], 'type':daemon["type"], 'daddress':daemon["address"], 'dport':daemon["port"], 'baddress':balancer["address"], 'bport':balancer["port"] }
                            #monitoring.warning(type='license_testing', description=_("Не верный формат даты лицензии, поддерживаемый формат '%(format)s', текущее значение: %(days)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=False )
                            saveMonitoringMessage(error_level=0, id = 'license_incorrect', params = params, type='license_testing', description=_("Не верный формат даты лицензии, поддерживаемый формат '%(format)s', текущее значение: %(days)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=False )
                        except:
                            logging.exception(str(sys.exc_info()))
                        if license_days:
                            now =  datetime.datetime.now()
                            days = license_days - now
                            if days.days <= DEFAULT_DAYS_LIMIT_FOR_LICENSE:
                                if days.days < 0:
                                    params = {'type':daemon["type"], 'daddress':daemon["address"], 'dport':daemon["port"], 'baddress':balancer["address"], 'bport':balancer["port"] }
                                    #monitoring.warning(type='license_testing', description=_("Закончился срок действия лицензии, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=True )
                                    saveMonitoringMessage(error_level=0, id = 'license_finished', params = params, type='license_testing', description=_("Закончился срок действия лицензии, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=True )
                                else:
                                    params = {'days':days.days, 'type':daemon["type"], 'daddress':daemon["address"], 'dport':daemon["port"], 'baddress':balancer["address"], 'bport':balancer["port"] }
                                    #monitoring.warning(type='license_testing', description=_("Заканчивается срок действия лицензии, осталось %(days)s день/дней, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=True )
                                    saveMonitoringMessage(error_level=0, id = 'license_finishing', params = params, type='license_testing', description=_("Заканчивается срок действия лицензии, осталось дней: %(days)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=True )
                    if 'temperature' in daemon:
                        if int(daemon['temperature'])>DEFAULT_WARNING_TEMPERATURE:
                            params = {'temp':daemon['temperature'], 'type':daemon["type"], 'daddress':daemon["address"], 'dport':daemon["port"], 'baddress':balancer["address"], 'bport':balancer["port"] }
                            #monitoring.warning(type='overload_temperatures', description=_("Перегрузка по температуре, текущее значение: %(temp)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=True )
                            saveMonitoringMessage(error_level=0, id = 'temperature_overloaded', params = params, type='overload_temperatures', description=_("Перегрузка по температуре, текущее значение: %(temp)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=True )
                            res = False
                        elif int(daemon['temperature'])>DEFAULT_INFO_TEMPERATURE:    
                            params = {'temp':daemon['temperature'], 'type':daemon["type"], 'daddress':daemon["address"], 'dport':daemon["port"], 'baddress':balancer["address"], 'bport':balancer["port"] }
                            #monitoring.info(action='info', type='overload_temperatures', description=_("Возможно перегрузка по температуре, текущее значение: %(temp)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=True )
                            saveMonitoringMessage(error_level=0, id = 'temperature_overloading', params = params, type='overload_temperatures', description=_("Возможно перегрузка по температуре, текущее значение: %(temp)s, демон %(type)s %(daddress)s:%(dport)s на балансировщике %(baddress)s:%(bport)s.") % params, show=True )
    return re