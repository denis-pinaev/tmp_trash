#!/usr/bin/env python
#coding=utf-8
from django.core.management import setup_environ
from videoclient import settings
from videoarchive import settings as vaSettings
setup_environ(settings)
import sys

from videoarchive import models
from videoarchive.archive import models as archiveModels
from videoarchive.va import models as vaModels
from videoclient import models as vcModels 

def InitBase(update = False):
    try:
        day, create = models.Week.objects.get_or_create(id=1)
        if create:
            day.str_id = 'mon'
            day.number = day.id
            day.name = 'Понедельник'
            day.short_name = 'Пн'
            day.is_work = True
            day.save()
        day, create = models.Week.objects.get_or_create(id=2)
        if create:
            day.str_id = 'tue'
            day.number = day.id
            day.name = 'Вторник'
            day.short_name = 'Вт'
            day.is_work = True
            day.save()
        day, create = models.Week.objects.get_or_create(id=3)
        if create:
            day.str_id = 'wed'
            day.number = day.id
            day.name = 'Среда'
            day.short_name = 'Ср'
            day.is_work = True
            day.save()
        day, create = models.Week.objects.get_or_create(id=4)
        if create:
            day.str_id = 'thu'
            day.number = day.id
            day.name = 'Четверг'
            day.short_name = 'Чт'
            day.is_work = True
            day.save()
        day, create = models.Week.objects.get_or_create(id=5)
        if create:
            day.str_id = 'fri'
            day.number = day.id
            day.name = 'Пятница'
            day.short_name = 'Пт'
            day.is_work = True
            day.save()
        day, create = models.Week.objects.get_or_create(id=6)
        if create:
            day.str_id = 'sat'
            day.number = day.id
            day.name = 'Суббота'
            day.short_name = 'Сб'
            day.is_work = False
            day.save()
        day, create = models.Week.objects.get_or_create(id=7)
        if create:
            day.str_id = 'sun'
            day.number = day.id
            day.name = 'Воскресенье'
            day.short_name = 'Вс'
            day.is_work = False
            day.save()
        print "Week was created"
    except:
        print "Week: "+str(sys.exc_info())
        
    try:        
        codec, create = models.Codecs.objects.get_or_create(name = 'h264')
        if create:
            codec.number = 0
            codec.save()
        codec, create = models.Codecs.objects.get_or_create(name = 'mpeg4')
        if create:
            codec.number = 3
            codec.save()
        codec, create = models.Codecs.objects.get_or_create(name = 'mjpeg')
        if create:
            codec.number = 2
            codec.save()
        print "Codecs was created"
    except:
        print "Codecs: "+str(sys.exc_info())
        
        
        #320*240, 640*480,800*600, 1024*1280 по умолч 1024*1280
    try:
        models.Resolutions.objects.get_or_create(name="2560*1600")
        models.Resolutions.objects.get_or_create(name="2272*1704")
        models.Resolutions.objects.get_or_create(name="2048*1536")
        models.Resolutions.objects.get_or_create(name="1600*1200")
        models.Resolutions.objects.get_or_create(name="1280*1024")
        models.Resolutions.objects.get_or_create(name="800*600")
        models.Resolutions.objects.get_or_create(name="640*480")
        models.Resolutions.objects.get_or_create(name="320*240")
        print "Resolutions was created"
    except:
        print "Resolutions: "+str(sys.exc_info())
        
    try:

        dp = vcModels.DefaultParams.objects.get_or_create(name="gop_size")
        if dp[1] or update:
            dp[0].value = "5"
            dp[0].info = 'Расстояние между ключевыми кадрами.'
            dp[0].save()
                                      
        dp = vcModels.DefaultParams.objects.get_or_create(name="compress")
        if dp[1] or update:
            dp[0].value = "0.8"
            dp[0].info = 'Степень сжатия видеоролика, влияет на кач-во и размер видеоролика(0..1).'
            dp[0].save()
            
        dp = vcModels.DefaultParams.objects.get_or_create(name="bitrate")
        if dp[1] or update:
            dp[0].value = "1500"
            dp[0].info = 'Пропускная способность при записи видеоролика(100...).'
            dp[0].save()
            
        dp = vcModels.DefaultParams.objects.get_or_create(name="blur")
        if dp[1] or update:
            dp[0].value = "0.6"
            dp[0].info = 'Коэффициент сглаживания изображения(0..1).'
            dp[0].save()             
        print "DefaultArchiveParams was add"    
    except:
        print "DefaultArchiveParams Error: %s" %str(sys.exc_info())            
        
    try:
        signal, create = models.Signals.objects.get_or_create(str_id = "simple")
        if create:
            signal.short_name = "simple"
            signal.name = "По расписанию"
            signal.save()
        signal, create = models.Signals.objects.get_or_create(str_id = "facedetect")
        if create:
            signal.short_name = "facedetect"
            signal.name = "Детектирование лица"
            signal.save()
        signal, create = models.Signals.objects.get_or_create(str_id = "identification")
        if create:
            signal.short_name = "identification"
            signal.name = "Идентификация"
            signal.save()
        signal, create = models.Signals.objects.get_or_create(str_id = "motion")
        if create:
            signal.short_name = "motion"
            signal.name = "Движение"
            signal.save()
        signal, create = models.Signals.objects.get_or_create(str_id = "sensor1")
        if create:
            signal.short_name = "sensor"
            signal.name = "Запись по датчику"
            signal.save()
        signal, create = models.Signals.objects.get_or_create(str_id = "import")
        if create:
            signal.short_name = "import"
            signal.name = "Импорт"
            signal.save()            
        print "Signals was created"
    except:
        print "Signals: "+str(sys.exc_info())
        
        
    try:
        param, create = models.Settings.objects.get_or_create(name=vaSettings.CRON_DELAY_FOR_PROCESS)
        if create or (not create and not param.value):
            param.value = "600"
            param.info = "Интервал выполнение задачи крон на добовление процессов"
            param.save()
        print "Settings was created"
    except:
        print "Settings: "+str(sys.exc_info())
        
    try:
        position, create = models.PositionUser.objects.get_or_create(name='Адвокат')
        position, create = models.PositionUser.objects.get_or_create(name='Следователь')
        position, create = models.PositionUser.objects.get_or_create(name='Секретарь')
        print "PositionUser was created"
    except:
        print "PositionUser: "+str(sys.exc_info())
        
    try:
        access, create = models.AccessUser.objects.get_or_create(str_id='denied')
        if create:
            access.name="Доступ запрещен"
            access.save()
        access, create = models.AccessUser.objects.get_or_create(str_id='operator')
        if create:
            access.name="Оператор"
            access.save()
        access, create = models.AccessUser.objects.get_or_create(str_id='moderator')
        if create:
            access.name="Модератор"
            access.save()
        access, create = models.AccessUser.objects.get_or_create(str_id='admin')
        if create:
            access.name="Администратор"
            access.save()
        print "AccessUser was created"
    except:
        print "AccessUser: "+str(sys.exc_info())
        
    #try:
    #    from videoarchive.communicator import models as cModels
    #    com, create = cModels.Communicator.objects.get_or_create(host='127.0.0.1', port=12600)
    #    if create:
    #        com.active=True
    #        com.save()
    #    print "Communicator was created"
    #except:
    #    print "Communicator: "+str(sys.exc_info())
        
        
#    try:
#        pass
#        print "pass was created"
#    except:
#        print "pass: "+str(sys.exc_info())  

    from videoarchive.upload import config
    from videoarchive.upload import models as uploadModels
    for param in config.default_settings:
        try:
            if uploadModels.Settings.objects.filter(name = param["name"]).count() == 0:
                uploadModels.Settings.objects.create(name = param["name"], value=param["value"], info=param["info"])
                print "Creating param %s" %param["name"]
        except:
            print "ERROR %s %s" %( param["name"], str(sys.exc_info()))        
        
#InitBase(False)
 
