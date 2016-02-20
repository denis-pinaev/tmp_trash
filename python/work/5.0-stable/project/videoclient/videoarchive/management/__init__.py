#coding=utf-8
import sys
from django.db.models import signals
from videoarchive import models
from videoarchive.archive import models as archiveModels
from videoarchive.va import models as vaModels

        
def default_settings(app, created_models, verbosity, **kwargs):
    from django.core.management import call_command
    #print "default_settings"
    if not kwargs.get('interactive', True):
        return 0
    
    if models.Week in created_models:
        try:
            day, create = models.Week.objects.get_or_create(id=1)
            all_cerate = False
            if create:
                all_cerate = True
                day.str_id = 'mon'
                day.number = day.id
                day.name = 'Понедельник'
                day.short_name = 'Пн'
                day.is_work = True
                day.save()
            day, create = models.Week.objects.get_or_create(id=2)
            if create:
                all_cerate = True
                day.str_id = 'tue'
                day.number = day.id
                day.name = 'Вторник'
                day.short_name = 'Вт'
                day.is_work = True
                day.save()
            day, create = models.Week.objects.get_or_create(id=3)
            if create:
                all_cerate = True
                day.str_id = 'wed'
                day.number = day.id
                day.name = 'Среда'
                day.short_name = 'Ср'
                day.is_work = True
                day.save()
            day, create = models.Week.objects.get_or_create(id=4)
            if create:
                all_cerate = True
                day.str_id = 'thu'
                day.number = day.id
                day.name = 'Четверг'
                day.short_name = 'Чт'
                day.is_work = True
                day.save()
            day, create = models.Week.objects.get_or_create(id=5)
            if create:
                all_cerate = True
                day.str_id = 'fri'
                day.number = day.id
                day.name = 'Пятница'
                day.short_name = 'Пт'
                day.is_work = True
                day.save()
            day, create = models.Week.objects.get_or_create(id=6)
            if create:
                all_cerate = True
                day.str_id = 'sat'
                day.number = day.id
                day.name = 'Суббота'
                day.short_name = 'Сб'
                day.is_work = False
                day.save()
            day, create = models.Week.objects.get_or_create(id=7)
            if create:
                all_cerate = True
                day.str_id = 'sun'
                day.number = day.id
                day.name = 'Воскресенье'
                day.short_name = 'Вс'
                day.is_work = False
                day.save()
            if all_cerate: print "Initialization Week"
        except:
            print "ERROR %s %s" %("Week", str(sys.exc_info()))
        
    if models.Codecs in created_models:
        try:
            all_cerate = False
            codec, create = models.Codecs.objects.get_or_create(name = 'mpeg4')
            if create:
                all_cerate = True
                codec.number = 3
                codec.save()
            codec, create = models.Codecs.objects.get_or_create(name = 'mjpeg')
            if create:
                all_cerate = True
                codec.number = 2
                codec.save()
            if all_cerate: print "Initialization Codecs"
        except:
            print "ERROR %s %s" %("Codecs", str(sys.exc_info()))
    
    if models.Resolutions in created_models:    
        try:
            all_cerate = False
            resol, create = models.Resolutions.objects.get_or_create(name="1280*1024")
            if create: all_cerate = True
            resol, create = models.Resolutions.objects.get_or_create(name="800*600")
            if create: all_cerate = True
            resol, create = models.Resolutions.objects.get_or_create(name="640*480")
            if create: all_cerate = True
            resol, create = models.Resolutions.objects.get_or_create(name="320*240")
            if all_cerate: print "Initialization Resolutions"
        except:
            print "ERROR %s %s" %("Resolutions", str(sys.exc_info()))
            
    if models.Signals in created_models:    
        try:
            all_cerate = False
            signal, create = models.Signals.objects.get_or_create(str_id = "simple")
            if create:
                all_cerate = True
                signal.short_name = "simple"
                signal.name = "Запись"
                signal.save()
            signal, create = models.Signals.objects.get_or_create(str_id = "facedetect")
            if create:
                all_cerate = True
                signal.short_name = "facedetect"
                signal.name = "Детектирование лица"
                signal.save()
            signal, create = models.Signals.objects.get_or_create(str_id = "identification")
            if create:
                all_cerate = True
                signal.short_name = "identification"
                signal.name = "Идентификация"
                signal.save()
            signal, create = models.Signals.objects.get_or_create(str_id = "motion")
            if create:
                all_cerate = True
                signal.short_name = "motion"
                signal.name = "Движение"
                signal.save()
            signal, create = models.Signals.objects.get_or_create(str_id = "sensor1")
            if create:
                all_cerate = True
                signal.short_name = "sensor"
                signal.name = "Запись по датчику"
                signal.save()
            if all_cerate: print "Initialization Signals"
        except:
            print "ERROR %s %s" %("Signals", str(sys.exc_info()))
            
    if models.Settings in created_models:
        try:
            all_cerate = False
            param, create = models.Settings.objects.get_or_create(name=settings.CRON_DELAY_FOR_PROCESS)
            if create or (not create and not param.value):
                all_cerate = True
                param.value = "600"
                param.info = "Интеревал выполнение задачи крон на добовление процессов"
                param.save()
            param, create = models.Settings.objects.get_or_create(name=settings.RES_INTERFACE)
            if create or (not param.value):
                all_cerate = True
                param.value = "0"
                param.info = '1280x1024 - 0, 1920x1200 - 1. Разрешение экрана'
                param.save()            
                
            if all_cerate: print "Initialization Settings"
        except:
            print "ERROR %s %s" %("Settings", str(sys.exc_info()))
        
    if models.PositionUser in created_models:
        try:
            all_cerate = False
            position, create = models.PositionUser.objects.get_or_create(name='Адвокат')
            if create: all_cerate = True
            position, create = models.PositionUser.objects.get_or_create(name='Следователь')
            if create: all_cerate = True
            position, create = models.PositionUser.objects.get_or_create(name='Секретарь')
            if create: all_cerate = True
            if all_cerate: print "Initialization PositionUser"
        except:
            print "ERROR %s %s" %("PositionUser", str(sys.exc_info()))
    
    if models.AccessUser in created_models:    
        try:
            all_cerate = False
            access, create = models.AccessUser.objects.get_or_create(str_id='denied')
            if create:
                all_cerate = True
                access.name="Доступ запрещен"
                access.save()
            access, create = models.AccessUser.objects.get_or_create(str_id='operator')
            if create:
                all_cerate = True
                access.name="Оператор"
                access.save()
            access, create = models.AccessUser.objects.get_or_create(str_id='moderator')
            if create:
                all_cerate = True
                access.name="Модератор"
                access.save()
            access, create = models.AccessUser.objects.get_or_create(str_id='admin')
            if create:
                all_cerate = True
                access.name="Администратор"
                access.save()
            if all_cerate: print "Initialization AccessUser"
        except:
            print "ERROR %s %s" %("AccessUser", str(sys.exc_info()))

signals.post_syncdb.connect(default_settings, 
    dispatch_uid = "videoarchive.management.default_settings")
