#!/usr/bin/env python
#coding=utf-8
from django.core.management import setup_environ
import settings
setup_environ(settings)
import logging
import sys
from django.utils.translation import ugettext as _
from videoclient.models import Article, ArticlePart, ArticleItem, Document, DivisionUser, PositionUser, StatusUser, Category, Ground, PositionsStatus, DefaultParams, Types, List, GroupPerson, ProfileEvent, Event, Signal, Balancer
from videoclient.settings import last_journal_update, wait_unidentified_person, reaction_time, journalBoundCoeff, count_time_test, time_span_time_test, add_not_ident_person, transfer_alerts, transfer_alerts_url, self_learning, show_ident_window_recogn_only, noise_learning, local_host_name, delay_for_create_new_group
from videoclient import models as vcModels
from videoclient.communicator.models import Kpp, Communicator
#from videoclient.models import InitBase
from smilart_cron.views import initTaskList


SHOW_VIDEOARCHIVE = '1'
SHOW_VIDEOANALITYCS = '1'
SHOW_RECOGNITION = '1'


def create_list(id, name, type, level, id_required=False):
    try:
        if GroupPerson.objects.filter(id=id).count() == 0:
            if id_required:
                g = GroupPerson.objects.create(id=id, name=name)
            else:
                g = GroupPerson.objects.create(name=name)
        else: 
            g = GroupPerson.objects.get(id=id)    
        if List.objects.filter(id=id).count() == 0:
            if id_required: 
                List.objects.create(id=id, name=name, type=type, group=g, discription=name, level=level)
            else:
                List.objects.create(name=name, type=type, group=g, discription=name, level=level)
    except:
        logging.exception(str(sys.exc_info()))

def InitBase(update = False):
    try:
#    if True:
        i = 1
        while i <= 390:
            try:
                Article.objects.get_or_create(name = str(i))
            except:
                print "Article: name = %s, Error: %s" %(i, str(sys.exc_info()))
            i=i+1
        print "Articles was added"
            
        i = 1
        while i <= 20:
            try:
                ArticlePart.objects.get_or_create(name = str(i))
            except:
                print "ArticlePart: name = %s, Error: %s" %(i, str(sys.exc_info()))
            i=i+1
        
        print "ArticleParts was added"
            
        try:    
            ArticleItem.objects.get_or_create(name = 'а')
            ArticleItem.objects.get_or_create(name = 'б')
            ArticleItem.objects.get_or_create(name = 'в')
            ArticleItem.objects.get_or_create(name = 'г')
            ArticleItem.objects.get_or_create(name = 'д')
            ArticleItem.objects.get_or_create(name = 'е')
            ArticleItem.objects.get_or_create(name = 'ж')
            ArticleItem.objects.get_or_create(name = 'з')
            ArticleItem.objects.get_or_create(name = 'и')
            ArticleItem.objects.get_or_create(name = 'к')
            ArticleItem.objects.get_or_create(name = 'л')
            ArticleItem.objects.get_or_create(name = 'м')
            ArticleItem.objects.get_or_create(name = 'н')
            ArticleItem.objects.get_or_create(name = 'о')
            ArticleItem.objects.get_or_create(name = 'п')
            ArticleItem.objects.get_or_create(name = 'р')
            ArticleItem.objects.get_or_create(name = 'с')
            ArticleItem.objects.get_or_create(name = 'т')
            ArticleItem.objects.get_or_create(name = 'у')
            ArticleItem.objects.get_or_create(name = 'ф')
            ArticleItem.objects.get_or_create(name = 'х')
            ArticleItem.objects.get_or_create(name = 'ц')
            ArticleItem.objects.get_or_create(name = 'ч')
            ArticleItem.objects.get_or_create(name = 'ш')
            ArticleItem.objects.get_or_create(name = 'щ')
            ArticleItem.objects.get_or_create(name = 'э')
            ArticleItem.objects.get_or_create(name = 'ю')
            ArticleItem.objects.get_or_create(name = 'я')
            print "ArticleItems was added"
        except:
            print "ArticleItem Error: %s" %str(sys.exc_info())
            
        try:
            Document.objects.get_or_create(name = _('Паспорт'))
            Document.objects.get_or_create(name = _('Удостоверение'))
            print "Document was added"
        except:
            print "Document Error: %s" %str(sys.exc_info())
        
        try:
            Kpp.objects.get_or_create(name = _('Главный вход'))
            print "Kpp was added"
        except:
            print "Kpp Error: %s" %str(sys.exc_info())
        
        try:
            d1 = DivisionUser.objects.get_or_create(name = _('Операторы'))
            d2 = DivisionUser.objects.get_or_create(name = _('Посетители'))
            d3 = DivisionUser.objects.get_or_create(name = _('Персоны'))
            d4 = DivisionUser.objects.get_or_create(name = _('Сотрудники'))
            d5 = DivisionUser.objects.get_or_create(name = _('Автообученные'))
            print "DivisionUser was added"
        except:
            print "DivisionUser Error: %s" %str(sys.exc_info())
        
        try:
            PositionUser.objects.get_or_create(name = _('Программист'))
            PositionUser.objects.get_or_create(name = _('Охранник'))
            PositionUser.objects.get_or_create(name = _('Адвокат'))
            PositionUser.objects.get_or_create(name = _('Следователь'))
            PositionUser.objects.get_or_create(name = _('Секретарь'))
            print "PositionUser was added"
        except:
            print "PositionUser Error: %s" %str(sys.exc_info())
            
        #try:
        #    c, create = Communicator.objects.get_or_create(id = 1)
        #    if create:
        #        c.host = '127.0.0.1'
        #        c.port = 12600
        #        c.active = True
        #        c.save() 
        #        print "Communicator was added"
        #except:
        #    print "Communicator Error: %s" %str(sys.exc_info())
        
#        try:
#            b, create = Balancer.objects.get_or_create(id = 1)
#            if create:
#                b.host = '127.0.0.1'
#                b.port = 16544
#                b.login = 'lLogin'
#                b.passwd = 'pPassword'
#                b.user = 'communicator'
#                b.active = True
#                b.save() 
#                print "Balancer was added"
#        except:
#            print "Balancer Error: %s" %str(sys.exc_info())
        
        try:
            StatusUser.objects.get_or_create(name = _('Администратор'), division=d1[0])
            StatusUser.objects.get_or_create(name = _('Оператор'), division=d1[0])
            StatusUser.objects.get_or_create(name = _('Модератор'), division=d1[0])
            StatusUser.objects.get_or_create(name = _('Охранник'), division=d1[0])
            StatusUser.objects.get_or_create(name = _('Доступ запрещен'), division=d1[0])
            
            StatusUser.objects.get_or_create(name = _('Подследственный'), division=d3[0])
            StatusUser.objects.get_or_create(name = _('Осужденный'), division=d3[0])
            
            StatusUser.objects.get_or_create(name = _('Адвокат'), division=d2[0])
            StatusUser.objects.get_or_create(name = _('Следователь'), division=d2[0])
            StatusUser.objects.get_or_create(name = _('Родственник'), division=d2[0])
            
            StatusUser.objects.get_or_create(name = _('Адвокат'), division=d4[0])
            StatusUser.objects.get_or_create(name = _('Следователь'), division=d4[0])
            StatusUser.objects.get_or_create(name = _('Секретарь'), division=d4[0])
            
            StatusUser.objects.get_or_create(name = _('Автообученный'), division=d5[0])
            print "StatusUser was added"
        except:
            print "StatusUser Error: %s" %str(sys.exc_info())

        try:        
            Category.objects.get_or_create(name = _('Опасен'))
            Category.objects.get_or_create(name = _('Особо опасен'))
            Category.objects.get_or_create(name = _('Рецидивист'))
            print "Category was added"
        except:
            print "Category Error: %s" %str(sys.exc_info())
        
        try:
            Ground.objects.get_or_create(name = _('Личные вопросы'))
            Ground.objects.get_or_create(name = _('Посещение'))
            Ground.objects.get_or_create(name = _('Допрос'))
            Ground.objects.get_or_create(name = _('Свидание'))
            Ground.objects.get_or_create(name = _('Ремонтные работы'))
            Ground.objects.get_or_create(name = _('Следственный эксперимент'))
            Ground.objects.get_or_create(name = _('Очная ставка'))
            print "Ground was added"
        except:
            print "Ground Error: %s" %str(sys.exc_info())
        
        #PositionsStatus.objects.get_or_create(name = "Вход")
        #PositionsStatus.objects.get_or_create(name = "Выход")
        #PositionsStatus.objects.get_or_create(name = "Запрещено")
        
        try:
#            p = PositionsStatus.objects.get_or_create(id=1)
#            if p[1] or update:
#                p[0].name = "Разрешен проход"
#                p[0].save()
#            p = PositionsStatus.objects.get_or_create(id=2)
#            if p[1] or update:
#                p[0].name = "Разрешен проход"
#                p[0].save()
#            p = PositionsStatus.objects.get_or_create(id=3)
#            if p[1] or update:
#                p[0].name = "Запрещен проход"
#                p[0].save()
                
            p = PositionsStatus.objects.get_or_create(id=1)
            if p[1] or update:
                p[0].name = _("Вход")
                p[0].save()
            p = PositionsStatus.objects.get_or_create(id=2)
            if p[1] or update:
                p[0].name = _("Выход")
                p[0].save()
            p = PositionsStatus.objects.get_or_create(id=3)
            if p[1] or update:
                p[0].name = _("Запрещено")
                p[0].save()
            print "PositionsStatus was added"
        except:
            print "PositionsStatus Error: %s" %str(sys.exc_info())    
 
        try:
#            dp = DefaultParams.objects.get_or_create(name=last_journal_update)
#            if dp[1] or update:
#                dp[0].value = "30"
#                dp[0].info = "Измеряется в секундах. Если время между идентификациями меньше этого времени, то считается что человек все еще стоит перед камерой и считается одной записью в журнале."
#                dp[0].save()
#            dp = DefaultParams.objects.get_or_create(name=wait_unidentified_person)  
#            if dp[1] or update:
#                dp[0].value = "15"
#                dp[0].info = "Измеряется в секундах. Время выделенное на идентификацию. Если за это время человек не идентифицирован, об этом сообщается. ( Строго меньше параметра reaction_time )"
#                dp[0].save()
#            dp = DefaultParams.objects.get_or_create(name=reaction_time)        
#            if dp[1] or update:
#                dp[0].value = "30"
#                dp[0].info = "Измеряется в секундах. Время реакции на сообщения. Если идентифицированному лицу было 'запрещено', но оно все еще находится перед камерой,  или окно было открыто дольше этого времени, то создается новая запись в журнале о неопознанном лице."
#                dp[0].save()
#            dp = DefaultParams.objects.get_or_create(name="pause_time")
#            if dp[1] or update:
#                dp[0].value = "10"
#                dp[0].info = "Cек. Пауза между идентификацией"
#                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="draw_frame_leftthings_delay")        
            if dp[1] or update:
                dp[0].value = "1000"
                dp[0].info = _("Время отображения рамки детектированной области оставленной вещи(.мс)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="draw_frame_fire_delay")        
            if dp[1] or update:
                dp[0].value = "1000"
                dp[0].info = _("Время отображения рамки детектированной области огня(.мс)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="draw_frame_smoke_delay")        
            if dp[1] or update:
                dp[0].value = "1000"
                dp[0].info = _("Время отображения рамки детектированной области дыма(.мс)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="draw_frame_flash_delay")        
            if dp[1] or update:
                dp[0].value = "1000"
                dp[0].info = _("Время отображения рамки детектированной области вспышки(.мс)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="draw_frame_face_delay")        
            if dp[1] or update:
                dp[0].value = "300"
                dp[0].info = _("Время отображения рамки детектированной области лица(.мс)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="use_color_style_security")        
            if dp[1] or update:
                dp[0].value = "1"
                dp[0].info = _("Использовать цветную версию интерфейса охранника (1 - Вкл. 0 - Выкл)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="show_buttons_for_security")        
            if dp[1] or update:
                dp[0].value = "0"
                dp[0].info = _("Отображать кнопки для принятия решения в интерфейсе охранника (1 - Вкл. 0 - Выкл)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="show_detect_alerts")        
            if dp[1] or update:
                dp[0].value = "1"
                dp[0].info = _("Показывать окно оперативного реагирования (1 - Вкл. 0 - Выкл)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="add_to_carousel_fire_delay")        
            if dp[1] or update:
                dp[0].value = "2000"
                dp[0].info = _("Задержка при добавлении областей детектов огня в карусель (.мс)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="add_to_carousel_flash_delay")        
            if dp[1] or update:
                dp[0].value = "2000"
                dp[0].info = _("Задержка при добавлении областей детектов вспышки в карусель (.мс)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="add_to_carousel_smoke_delay")        
            if dp[1] or update:
                dp[0].value = "2000"
                dp[0].info = _("Задержка при добавлении областей детектов дыма в карусель (.мс)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="add_to_carousel_leftthings_delay")        
            if dp[1] or update:
                dp[0].value = "2000"
                dp[0].info = _("Задержка при добавлении областей детектов оставленных вещей в карусель (.мс)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="show_videoanalitycs")        
            if dp[1] or update:
                dp[0].value = SHOW_VIDEOANALITYCS
                dp[0].info = _("Отображать настройки видеоаналитики (1 - Вкл. 0 - Выкл)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="show_maps")        
            if dp[1] or update:
                dp[0].value = "0"
                dp[0].info = _('Отображать вкладку "Карты" (1 - Вкл. 0 - Выкл)')            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="self_test")        
            if dp[1] or update:
                dp[0].value = "1"
                dp[0].info = _("Самотестирование системы (1 - Вкл. 0 - Выкл)")            
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="testing_balancer")        
            if dp[1] or update:
                dp[0].value = "1"
                dp[0].info = "Тестирование УС, балансировщиков, демонов, температуры видеокарт. Актуально только при выключенном самотестировании. (1 - Вкл. 0 - Выкл)"            
                dp[0].save()    
            dp = DefaultParams.objects.get_or_create(name=journalBoundCoeff)        
            if dp[1] or update:
                dp[0].value = "0.42"
                dp[0].info = _("Порог идентификации (Csm)")            
                dp[0].save()                    
            dp = DefaultParams.objects.get_or_create(name="login_timeout")
            if dp[1] or update:
                dp[0].value = "1800"
                dp[0].info = _("Период бездействия, после которого совершается автовыход.")
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="show_ident_window")
            if dp[1] or update:
                dp[0].value = "0"
                dp[0].info = _("Вкл./Выкл. окна идентификации (1 - Вкл. 0 - Выкл)")
                dp[0].save()
                
            dp = DefaultParams.objects.get_or_create(name="ident_window_position")
            if dp[1] or update:
                dp[0].value = "1"
                dp[0].info = _("Позиция окна идентификации (0 - В центре. 1 - В правом нижнем углу)")
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name=count_time_test)
            if dp[1] or update:
                dp[0].value = "1"
                dp[0].info = _("Количество запросов идентификации в заданный интервал времени при котором запрос считаем истинным (Временная проверка)")
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name=time_span_time_test)
            if dp[1] or update:
                dp[0].value = "1500"
                dp[0].info = _('мс. Интервал времени для "count_time_test" (Временная проверка)')
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name=add_not_ident_person)
            if dp[1] or update:
                dp[0].value = "1"
                dp[0].info = _('Добавление неопознанных записей в журнал (1 - добавляются, 0 - не добавляются)')
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name=transfer_alerts)
            if dp[1] or update:
                dp[0].value = "0"
                dp[0].info = _('Пересылка оповещений (1 - пересылать, 0 - не пересылать)')
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name=transfer_alerts_url)
            if dp[1] or update:
                dp[0].value = ""
                dp[0].info = _('Адрес пересылки оповещений (Пример: 127.0.0.1:14600)')
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name="res_interface")
            if dp[1] or update:
                dp[0].value = "0"
                dp[0].info = _('1280x1024 - 0, 1920x1200 - 1. Разрешение экрана')
                dp[0].save()
            dp = DefaultParams.objects.get_or_create(name=show_ident_window_recogn_only)
            if dp[1] or update:
                dp[0].value = "1"
                dp[0].info = _('Вывод окна только при успешной идентификации (1 - вкл., 0 - выкл. (вывод независимо от результата))')
                dp[0].save()
                
            dp = DefaultParams.objects.get_or_create(name="timeout_for_record_roller")
            if dp[1] or update:
                dp[0].value = "10"
                dp[0].info = _('мин. Таймаут для записи ролика с камеры.')
                dp[0].save()    
            
            dp = DefaultParams.objects.get_or_create(name="period_storage_data")        
            if dp[1] or update:
                dp[0].value = "30"
                dp[0].info = _("Период хранения данных  (журнал идентификаций, логи ошибок)(в днях):")            
                dp[0].save()
            
            dp = DefaultParams.objects.get_or_create(name="time_opened_turnstiles")        
            if dp[1] or update:
                dp[0].value = "15"
                dp[0].info = _("Время открывания турникета (в секундах):")            
                dp[0].save()            
            
            dp = DefaultParams.objects.get_or_create(name="permit_control_system_params")
            if dp[1] or update:
                dp[0].value = "0"
                dp[0].info = _('Разрешить редактировать все параметры управляющей системы (1 - разрешить редактировать все, 0 - запретить редактировать параметры из списка "Не редактируемые параметры УС").')
                dp[0].save()  
            
            dp = DefaultParams.objects.get_or_create(name="add_report_export_journal")        
            if dp[1] or update:
                dp[0].value = "1"
                dp[0].info = _("Добавлять отчет в экспортируемый архив записей журнала (1 - Вкл. 0 - Выкл)")
                dp[0].save()
          
            dp = DefaultParams.objects.get_or_create(name=local_host_name)
            if dp[1] or update:
                dp[0].value = "0"
                dp[0].info = _('Адрес основного компьютера.')
                dp[0].save()
                
            dp = DefaultParams.objects.get_or_create(name="fps_of_the_cameras")
            if dp[1] or update:
                dp[0].value = "5"
                dp[0].info = _('Количество отображаемых кадров в видеопотоке.')
                dp[0].save()
                
            dp = DefaultParams.objects.get_or_create(name="show_recognition")
            if dp[1] or update:
                dp[0].value = SHOW_RECOGNITION
                dp[0].info = _('Отображать детектор для включения рекогнишена (1 - Вкл. 0 - Выкл)')
                dp[0].save()
                
            dp = DefaultParams.objects.get_or_create(name="show_videoarchive")
            if dp[1] or update:
                dp[0].value = SHOW_VIDEOARCHIVE
                dp[0].info = _('Отображать вкладку видеоархива (1 - Вкл. 0 - Выкл)')
                dp[0].save()
            
            dp = DefaultParams.objects.get_or_create(name=delay_for_create_new_group)
            if dp[1] or update:
                dp[0].value = 30
                dp[0].info = _('Задержка в секундах для создания новой группы в журнале')
                dp[0].save()

            print "DefaultParams was added"    
        except:
            print "DefaultParams Error: %s" %str(sys.exc_info())    
        
        try:
            p = ProfileEvent.objects.get_or_create(name_id="default")
            if p[1] or update:
                p[0].name = _("По умолчаню")
                p[0].save()
            print "ProfileEvent was added"
        except:
            print "ProfileEvent Error: %s" %str(sys.exc_info())

        try:        
            s = Event.objects.get_or_create(name_id="on_ident", profile=None)
            if s[1] or update:
                s[0].name = _("Лицо идентифицировано")
                s[0].save()
                if p[1] or update:
                    e = Event(object = s[0])
                    e.profile = p[0]
                    e.save()
                
            s = Event.objects.get_or_create(name_id="on_no_ident", profile=None)
            if s[1] or update:
                s[0].name = _("Лицо не идентифицировано")
                s[0].save()
                if p[1] or update:
                    e = Event(object = s[0])
                    e.profile = p[0]
                    e.save()
            print "Event was added"
        except:
            print "Event Error: %s" %str(sys.exc_info())
        
        try:
            s = Signal.objects.get_or_create(name_id="show_light")
            if s[1] or update:
                s[0].name = _("Зажечь лампочку")
                s[0].save()
            
            s = Signal.objects.get_or_create(name_id="show_red_light")
            if s[1] or update:
                s[0].name = _("Зажечь красную лампочку")
                s[0].save()
            print "Signal was added"
        except:
            print "Signal Error: %s" %str(sys.exc_info())
        
        try:
            t1 = Types.objects.get_or_create(url="/visitorslist/")
            if t1[1] or update:
                t1[0].name = _("Посетители")
                t1[0].division = d2[0]
                t1[0].save()
                
            t2 = Types.objects.get_or_create(url="/persons/")
            if t2[1] or update:
                t2[0].name = _("Персоны")
                t2[0].division = d3[0]
                t2[0].save()
                
            t3 = Types.objects.get_or_create(url="/stafflist/")
            if t3[1] or update:
                t3[0].name = _("Сотрудники")
                t3[0].division = d4[0]
                t3[0].save()
            t4 = Types.objects.get_or_create(url="/autolist/")
            if t4[1] or update:
                t4[0].name = _("Автообученные")
                t4[0].division = d5[0]
                t4[0].save()
            print "Types was added"
        except:
            print "Types Error: %s" %str(sys.exc_info())
        
        try:
            create_list(1, _("Руководство"), t3[0], "Level0")
            create_list(2, _("Cотрудники"), t3[0], "Level1")
            create_list(3, _("Технический персонал"), t3[0], "Level2")
            create_list(4, _("Важная персона"), t3[0], "Level3")
            create_list(5, _("Оперативный розыск"), t2[0], "Level4")
            create_list(6, _("Террористы"), t2[0], "Level5")
            create_list(7, _("Тестирование"), t3[0], "Level1")
            create_list(noise_learning, _("Шум"), t4[0], "Level1", id_required=True)
            #create_list(self_learning, "Автообученные", t4[0], "Level1", id_required=True)
            print "Lists was added"
        except:
            print "Lists Error: %s" %str(sys.exc_info())
      
        #videoclient lens
        try:
            from videoclient.models import Lens
            t1 = Lens.objects.get_or_create(name='Lens12.0')
            if t1[1] or update:
                t1[0].name = 'Lens12.0'
                t1[0].v = 12.0
                t1[0].save()
            t2 = Lens.objects.get_or_create(name='Lens4.0')
            if t2[1] or update:
                t2[0].name = 'Lens4.0'
                t2[0].v = 4.0
                t2[0].save()
            t3 = Lens.objects.get_or_create(name='Lens2.0')
            if t3[1] or update:
                t3[0].name = 'Lens2.0'
                t3[0].v = 2.0
                t3[0].save()
            print "Lens has been added"
        except:
            print "Lens Error: %s" % str(sys.exc_info())
        
        #map terminal models
        try:
            from videoclient.maps.models import MapTerminalType
            t1 = MapTerminalType.objects.get_or_create(name='Терминал "Оксион"')
            if t1[1] or update:
                t1[0].name = _('Терминал "Оксион"')
                t1[0].save()
            t2 = MapTerminalType.objects.get_or_create(name='Терминал "Оксион" 2')
            if t2[1] or update:
                t2[0].name = _('Терминал "Оксион" 2')
                t2[0].save()
            t3 = MapTerminalType.objects.get_or_create(name='Терминал "Digital Signage"')
            if t3[1] or update:
                t3[0].name = _('Терминал "Digital Signage"')
                t3[0].save()
            print "MapTerminalType has been added"
        except:
            print "MapTerminalType Error: %s" % str(sys.exc_info())
        
        #map direction models
        try:
            from videoclient.maps.models import Direction
            t1 = Direction.objects.get_or_create(name='Юг')
            if t1[1] or update:
                t1[0].name = _('Юг')
                t1[0].save()
            t2 = Direction.objects.get_or_create(name='Север')
            if t2[1] or update:
                t2[0].name = _('Север')
                t2[0].save()
            t3 = Direction.objects.get_or_create(name='Запад')
            if t3[1] or update:
                t3[0].name = _('Запад')
                t3[0].save()
            t4 = Direction.objects.get_or_create(name='Восток')
            if t4[1] or update:
                t4[0].name = _('Восток')
                t4[0].save()
            print "Map directions has been added"
        except:
            print "Map directions Error: %s" % str(sys.exc_info())
        
        #videoanalytics detector
        try:
            from videoclient.videoanalytics.models import Detector
            t1 = Detector.objects.get_or_create(dtype = 'leftThings')
            if t1[1] or update:
                t1[0].name = _('Оставленные вещи')
                t1[0].save()
            t2 = Detector.objects.get_or_create(dtype = 'background')
            if t2[1] or update:
                t2[0].name = _('Фон')
                t2[0].dtype = 'background'
                t2[0].save()
            t3 = Detector.objects.get_or_create(dtype = 'fireDetect')
            if t3[1] or update:
                t3[0].name = _('Огонь')
                t3[0].save()
            t4 = Detector.objects.get_or_create(dtype = 'smokeDetect')
            if t4[1] or update:
                t4[0].name = _('Дым')
                t4[0].save()
            t5 = Detector.objects.get_or_create(dtype = 'flashDetect')
            if t5[1] or update:
                t5[0].name = _('Вспышка')
                t5[0].save()
            t6 = Detector.objects.get_or_create(dtype = 'crowdDetect')
            if t6[1] or update:
                t6[0].name = _('Скопление людей')
                t6[0].save()
            print "Detectors has been added"
        except:
            print "Detectors Error: %s" % str(sys.exc_info())
            
        from videoclient.maps import models as mapModels
        try:
            city, create = mapModels.MapCity.objects.get_or_create(name=_('Москва'))
            print "MapCity has been added"
        except:
            print "MapCity Error: %s" % str(sys.exc_info())
        
        try:
            objType, create = mapModels.MapObjectType.objects.get_or_create(name=_('Торговые центры'))
            print "MapObjectType has been added"
        except:
            print "MapObjectType Error: %s" % str(sys.exc_info())
            
        try:
            obj, create = mapModels.MapObject.objects.get_or_create(name=_('Торговый центр'), map_object_type=objType, city=city)
            print "MapObject has been added"
        except:
            print "MapObject Error: %s" % str(sys.exc_info())
        try:
            map, create = mapModels.Map.objects.get_or_create(city_id=city.id, obj_type_id=objType.id, obj_name_id=obj.id)
            if create:
                import os
                import settings
                path = os.path.join(settings.SRC_ROOT, 'maps/resources/default_map.jpg')
                try:
                    from videoclient.maps import views as mapViews
                    
                    mapImage = mapViews.mapthumbnail(path, mapViews.MAP_IMAGE_SIZE)
                    map.image=mapImage
                    map.save()
                except:
                    print "SaveImage: %s" %str(sys.exc_info())
            print "Map has been added"
        except:
            print "Map Error: %s" % str(sys.exc_info())
            
        try:        
            vcModels.Group.objects.get_or_create(title = 'trans')
            vcModels.Group.objects.get_or_create(title = 'help')
            print "Group was added"
        except:
            print "Group Error: %s" %str(sys.exc_info())
            
        try:        
            vcModels.Language.objects.get_or_create(name = 'ru', title = 'Russian')
            vcModels.Language.objects.get_or_create(name = 'en', title = 'English')
            print "Language was added"
        except:
            print "Language Error: %s" %str(sys.exc_info())
        
        
        try:
            from django.db import connection, transaction
            cursor = connection.cursor()
            cursor.execute('ALTER TABLE va_archives alter column active set default true;')       
            transaction.commit_unless_managed()
        except:
            print "Videoarchive active update: %s" %str(sys.exc_info())
            
        try:
            import user_perms
            user_perms.create_groups()
            print "Django group was added"
        except:
            print "Django group Error: %s " %str(sys.exc_info())
        initTaskList()
    except:
        print sys.exc_info()

#InitBase(False)
 
