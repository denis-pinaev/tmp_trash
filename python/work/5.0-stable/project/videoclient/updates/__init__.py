#coding=utf-8

import models
from videoclient import utils
import updates 
import logging
import sys
from django.core.management.commands import syncdb
from videoclient.management.commands import initbase

NO_UPDATE_FOUND = "No update found"
UPDATE_ERROR = "Update error"
monitoring_events = []

def run_syncdb():
    print "syncdb"
    command = syncdb.Command()
    command.handle_noargs()
    
def run_initbase():
    print "initbase"
    command = initbase.Command()
    command.handle()
    

def update(r):
    answer = False
    try:
        if r is None:
            print NO_UPDATE_FOUND
            return False
        
        import exceptions
        is_updated = False
        try:
            answer = eval("updates.update_from_revision_%s()" %(r))
            is_updated = True
        except exceptions.AttributeError:
            answer = True
            is_updated = False
        except:
            answer = False # Значение False для того что бы все обновления выполнились без ошибок, иначе будет считаться что обновление не выполнено
            #answer = True # Предполагается что не зависимо от ошибок обновление выполнено успешно 
            is_updated = True
            print str(sys.exc_info())

        if is_updated:
            try:
                #import monitoring
                if answer:
                    monitoring_events.append({"action":"action", "type":'update', "message_id":"update_ok", "description":'Обновление для ревизии %s'%(r+1), "json_description":'{"id":"update_ok","params":{"version":"%s"}}'%(r+1)})
                    #monitoring.action(type='update', description='Обновление для ревизии %s'%(r+1)) # +1 для того что бы указать конкретную ревизию в которой были изменения. 
                else:
                    monitoring_events.append({"action":"warning", "type":'update', "message_id":"update_no", "description":'Ошибка обновления для ревизии %s'%(r+1), "json_description":'{"id":"update_no","params":{"version":"%s"}}'%(r+1)})
                    #monitoring.warning(type='update', description='Ошибка обновления для ревизии %s'%(r+1)) # +1 для того что бы указать конкретную ревизию в которой были изменения. 
            except:
                print "Ошибка записи в журнал событий"
                
            if answer:
                print 'Обновление для ревизии %s' %(r+1)
            else:
                print 'Ошибка обновление для ревизии %s' %(r+1)
                
        return answer
    except AttributeError:
        print NO_UPDATE_FOUND
    except:
        print "Error: "+str(sys.exc_info())
    return answer

def check_version(r=0):
    if r == 0:
        try:
            versions = models.Version.objects.all().order_by('-id')
            if versions.count() > 0:
                version = versions[0]
                r = version.revision
        except:
            pass

    if int(r) >= int(utils.REVISION):
        print NO_UPDATE_FOUND
        return
    
    run_syncdb()    
    
    last_udate = 0
    all_update = True
    i = int(r)
    while i<utils.REVISION: # Строго меньше, т.к. для текущей ревизии обновлений и быть не может.
        if not update(i):
            all_update = False
        i = i+1
    
    if all_update:
        run_initbase()
        models.Version.objects.create(version = utils.VERSION_PREFIX, branch = utils.BRANCH, revision = utils.REVISION)
    else:
        print UPDATE_ERROR
        
    try:
        import monitoring
        for event in monitoring_events:
            if event["action"] == "action":
                #monitoring_events.append({"action":"action", "type":'update', "description":'Обновление для ревизии %s'%(r+1)})
                monitoring.action(type=event["type"], description=event["description"], json_description=event["json_description"], error_level=0, message_id=event["message_id"])
            else:
                monitoring.warning(type=event["type"], description=event["description"], json_description=event["json_description"], error_level=0, message_id=event["message_id"])
    except:
        print "Ошибка записи в журнал событий"
    