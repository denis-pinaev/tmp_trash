from django.http import HttpResponse
from django.db.models.fields.files import ImageFieldFile
from django.db import models as django_models
import datetime
from django.utils import simplejson
import logging
import json
import time
import sys

def JsonResponse(data):
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def json_response(func):
    def wrapper(request, *args, **kw):
        answer = dict()
        answer["status"] = False
        start_work_time = time.time()
        if not request.user.is_authenticated():
            answer["error"] = "user isn't authenticated"
        else:
            try:
                answer.update(func(request, *args, **kw))
            except:
                answer["status"] = False
                answer["exception"] = str(sys.exc_info())
                logging.exception(str(sys.exc_info()))
            
        stop_work_time = time.time()
        answer["work_time"] = stop_work_time - start_work_time
        return JsonResponse(answer)
    return wrapper

def getDictFromItemModel(item, recurse_fields=[], rename_fields=[], json_parse=[]):
    a_item = dict()
    fields = item._meta.fields

    for field in fields:
        name = field.name
        value = getattr(item, name)
        if isinstance(value, django_models.Model):
            if name in recurse_fields:
                value = getDictFromItemModel(item=value, recurse_fields=recurse_fields, rename_fields=rename_fields)
            else:
                value = value.pk
        elif isinstance(value, datetime.date) or isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
            value = value.isoformat()
        elif isinstance(value, datetime.time) or isinstance(value, datetime.time):
            value = value.isoformat()
        elif isinstance(value, ImageFieldFile):
            try:
                value = value.url
            except:
                value=''
        if name in rename_fields:
            name = rename_fields[name]
        if name in json_parse:
            value = json.loads(value)
        a_item[name] = value
    return a_item

def getDictFromListModel(list, recurse_fields=[], rename_fields=[], json_parse=[]):
    return [getDictFromItemModel(item=item, recurse_fields=recurse_fields, rename_fields=rename_fields, json_parse=json_parse) for item in list]