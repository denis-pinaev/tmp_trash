#codding=utf-8

import models
import logging
import datetime
import sys

def warning(**kwargs):
    kwargs["status"] = 'warning'
    create_message(**kwargs)
    
def info(**kwargs):
    kwargs["status"] = 'info'
    create_message(**kwargs)
    
def action(**kwargs):
    kwargs["status"] = 'action'
    create_message(**kwargs)
 

def create_message(**kwargs):
    ERROR_LEVEL_TIME_DELTA = 30
    try:
        error_file = None
        if "error_file" in kwargs:
            import copy
            error_file = copy.deepcopy(kwargs["error_file"])
            del kwargs["error_file"] 
        kwargs["status"] = kwargs["status"] if 'status' in kwargs else 'unknown'
        kwargs["type"] = kwargs["type"] if 'type' in kwargs else 'unknown'
        kwargs["description"] = kwargs["description"] if 'description' in kwargs else None
        kwargs["show"] = not kwargs["show"] if 'show' in kwargs else True
        error_level = kwargs["error_level"] = kwargs["error_level"] if 'error_level' in kwargs else 3
        message_id = kwargs["message_id"] = kwargs["message_id"] if 'message_id' in kwargs else None
        now = datetime.datetime.now()
        date = datetime.date(year = now.year, month=now.month, day=now.day)
        if message_id is None or not message_id:
            kwargs["date"] = date
            req = models.Events.objects.filter(**kwargs)
            now = now-datetime.timedelta(seconds=5)
            time = datetime.time(hour = now.hour, minute = now.minute, second = now.second)
            req = req.filter(time__gt=time)
            if req.count()==0:
                event = models.Events.objects.create(**kwargs)
                if error_file is not None:
                    event.save_error(error_file)
        else:
            now_delta = now - datetime.timedelta(seconds=ERROR_LEVEL_TIME_DELTA)
            time = datetime.time(hour=now_delta.hour, minute=now_delta.minute, second=now_delta.second)
            
            req = models.Events.objects.filter(message_id=message_id, date=date, time__gt=time, description=kwargs["description"], error_level__gt=0)
            if req.count()>0:
                last_req = req[0]
                last_error_level = last_req.error_level
                error_level = last_error_level - 1 if last_error_level <= error_level else error_level
                last_req.delete()
                
            if error_level <= 0:
                error_level = 0
                kwargs["show"] = False
            else:
                kwargs["show"] = True
            kwargs["error_level"] = error_level
            event = models.Events.objects.create(**kwargs)
            if error_file is not None:
                event.save_error(error_file)
    except:
        logging.exception('create_message: '+str(sys.exc_info()))