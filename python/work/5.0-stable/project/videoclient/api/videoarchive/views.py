from api.views import json_response, getDictFromListModel
from videoclient import models, utils
from videoarchive.va import models as vaModels
from videoclient.communicator import Communicator
import datetime
import time
import logging
import sys
from videoclient.views import getTimeInHMS, get_extended_detect_area, get_object_thumbnail
import base64
from videoclient import settings
from videoclient.utils import getBalIdByName, parseFaceString, getEyesDistance
import json
from cStringIO import StringIO as StringIO
from PIL import Image


@json_response
def video(request):
    answer = dict()
   
    params = request.REQUEST
    if 'limit' not in params:
        answer["error"] = "limit in params not found"
        return answer
    
    limit = params["limit"] if "limit" in params else 15
    last_id = params["last_id"] if "last_id" in params else None
    
    rollers = vaModels.VaRoller.objects.all().exclude(tm_stop=None)
    
    if 'get_count' in params:
        if params["get_count"] == "true":
            count = rollers.count()
            answer["count"] = count
        elif params["get_count"] != "false":
            answer["error"] = "get_count mast be true or false"
            return answer
    
    if last_id is not None:
        rollers = rollers.filter(id__lt = last_id)
       
    if 'filter_camera_id' in params:
        id = params["filter_camera_id"]
        rollers = rollers.filter(id_command__id_camera__id = id)

    if 'filter_signal_type' in params:
        signal_type = params["filter_signal_type"]
        rollers = rollers.filter(id_command__id_signal__str_id = signal_type)

    if 'filter_camera_ip' in params and 'filter_camera_type' in params:
        ip = params["filter_camera_ip"]
        type = params["filter_camera_type"]
        rollers = rollers.filter(id_command__id_camera__ip = ip, id_command__id_camera__type=type)

    if 'filter_datetime_start' in params:
        filter_datetime_start = params["filter_datetime_start"]
        begin_time = None
        try:
            begin_time = datetime.datetime.strptime(filter_datetime_start, "%Y-%m-%dT%H:%M:%S")
        except:
            answer["error"] = "start datatime is incorrect, it mast be datatime in iso format YYYY-MM-DDTHH:MM:SS"
            answer["exception"] = str(sys.exc_info())
            logging.exception(str(sys.exc_info()))
            return answer
        if begin_time is not None:
            rollers = rollers.filter(tm_start__gte = begin_time)

    if 'filter_datetime_finish' in params:
        filter_datetime_finish = params["filter_datetime_finish"]
        end_time = None
        try:
            end_time = datetime.datetime.strptime(filter_datetime_finish, "%Y-%m-%dT%H:%M:%S")
        except:
            answer["error"] = "finish datatime is incorrect, it mast be datatime in iso format YYYY-MM-DDTHH:MM:SS"
            answer["exception"] = str(sys.exc_info())
            logging.exception(str(sys.exc_info()))
            return answer
        if end_time is not None:
            rollers = rollers.filter(tm_stop__lt = end_time)

    rollers = rollers.order_by('-tm_start')
    rollers = rollers[:limit]

    #items = getDictFromListModel(rollers, recurse_fields=["camera", "detector_type", "person"], rename_fields={"finded": "found"}, json_parse=['info'])
    items = getDictFromListModel(rollers, recurse_fields=["id_command", "id_camera", "id_signal"], rename_fields={"id_camera": "camera", "id_signal": "signal"}, json_parse=[])

    from videoclient.settings import journalBoundCoeff
    k_cs = utils.get_value_defaultparams(journalBoundCoeff)
    for r in items:
        face_count = vaModels.VaPersonsFrame.objects.filter(id_archive=r["id_command"]["id_archive"], id_camera=r["id_command"]["camera"]["id"], tm_dt__gte=r["tm_start"].replace("T", " "), tm_dt__lte=r["tm_stop"].replace("T", " "))
        r["face_count"] = face_count.count()
        r["person_count"] = face_count.filter(k_cs__gte=k_cs).count()
    
    answer["rollers"] = items    
    answer["status"] = True
    return answer

