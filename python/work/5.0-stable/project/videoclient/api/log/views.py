from api.views import json_response, getDictFromListModel
from videoclient import models
from videoclient.videoanalytics import models as vaModels
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



TYPE_VA = "va"
TYPE_IDENT = "ident"
@json_response
def data(request, type):
    answer = dict()
   
    params = request.REQUEST
    if 'limit' not in params:
        answer["error"] = "limit in params not found"
        return answer
    
    limit = params["limit"] if "limit" in params else 15
    last_id = params["last_id"] if "last_id" in params else None
    
    if type==TYPE_VA:
        isVa = True
    else:
        isVa = False
    
    if isVa:
        journals = vaModels.DetectorLog.objects.all()
    else:
        journals = models.Journal.objects.exclude(agregate=None)
        journals = journals.extra(where=['videoclient_journal.id = videoclient_journal.agregate_id'])
    
    if 'get_count' in params:
        if params["get_count"] == "true":
            count = journals.count()
            answer["count"] = count
        elif params["get_count"] != "false":
            answer["error"] = "get_count mast be true or false"
            return answer
    
    if last_id is not None:
        journals = journals.filter(id__lt = last_id)
        
    
    if not isVa and 'filter_only_ident' in params:
        only_ident = params["filter_only_ident"]
        if only_ident == "true":
            journals = journals.exclude(person=None)
        elif only_ident != "false":
            answer["error"] = "filter_only_ident mast be true or false"
            return answer
    
    if 'filter_camera_uuid' in params:
        uuid = params["filter_camera_uuid"]
        journals = journals.filter(camera__uuid = uuid)

    if 'filter_datetime_start' in params:
        filter_datetime_start = params["filter_datetime_start"]
        begin_time = None
        try:
            begin_time = datetime.datetime.strptime(filter_datetime_start, "%Y-%m-%dT%H:%M:%S")
        except:
            answer["error"] = "start datatime is incorrect, it mast be datatime in iso format YYYY-MM-DDTHH:MM:SS"
            answer["exception"] = str(sys.exc_info())
            c
            return answer
        if begin_time is not None:
            if isVa:
                journals = journals.filter(dt_detect__gte = begin_time)
            else:
                journals = journals.filter(dt_first_fixed__gte = begin_time)

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
            if isVa:
                journals = journals.filter(dt_detect__lt = end_time)
            else:
                journals = journals.filter(dt_first_fixed__lt = end_time)
        
    filter_detect_type = params.get('filter_detect_type', None)
    if isVa and filter_detect_type:
        journals = journals.filter(detector_type__dtype=filter_detect_type)        
        
    journals = journals.order_by('-id')
    journals = journals[:limit]
    
    items = getDictFromListModel(journals, recurse_fields=["camera", "detector_type", "person"], rename_fields={"finded": "found"}, json_parse=['info'])
    from videoarchive import utils as archive_utils
    for item in items:
        id = archive_utils.getDetailVideo(item["id"])
        if id: item["video_id"] = id 
    answer["journal"] = items
    
    answer["status"] = True
    return answer

@json_response
def last_data(request, type):
    answer = dict()
   
    params = request.REQUEST
    if 'limit' not in params:
        answer["error"] = "limit in params not found"
        return answer
    
    limit = params["limit"] if "limit" in params else 10
    first_id = params["first_id"] if "first_id" in params else None
    wait = float(params["wait"]) if "wait" in params else None
    delay = float(params["delay"]) if "delay" in params else 0.05
    
    if type==TYPE_VA:
        isVa = True
    else:
        isVa = False
    
    start = time.time()
    filter_detect_type = params.get('filter_detect_type', None)
    while True:
        query_time = 0
        start_query_time = time.time() 
        if isVa:
            journals = vaModels.DetectorLog.objects.all()
        else:
            journals = models.Journal.objects.exclude(agregate=None)

        if first_id is not None:
            journals = journals.filter(id__gt = first_id)
            
        if 'filter_camera_uuid' in params:
            uuid = params["filter_camera_uuid"]
            journals = journals.filter(camera__uuid = uuid)
    
        if isVa and filter_detect_type:
            journals = journals.filter(detector_type__dtype=filter_detect_type)
    
        journals = journals.order_by('-id')
        journals = journals[:limit]
        journals = list(journals)
        journals.reverse()
        
        stop_query_time = time.time()
        query_time += stop_query_time - start_query_time
        
        break
        if wait:
            if len(journals)>0:
                break
            if time.time()-start+delay>=wait:
                break
            time.sleep(delay)
        else:
            break
    
    start_query_time = time.time()
    if not isVa:
        items = getDictFromListModel(journals, recurse_fields=["camera", "person", "status"], rename_fields={"finded": "found"}, json_parse=['info'])
    else:
        items = getDictFromListModel(journals, recurse_fields=["cameraUuid", "detector_type"], rename_fields={}, json_parse=['json_data'])

    stop_query_time = time.time()
    query_time += stop_query_time - start_query_time

    if not isVa:
        ident_data = []
        for item in items:
            encoded_string_original = ""
            try:
                original = settings.WWW_ROOT[:-1] + item["original"]
                image_file = open(original, "rb")
                encoded_string_original = base64.b64encode(image_file.read())
                image_file.close()
            except:
                encoded_string_original = ""
            
            encoded_string_found = ""
            try:
                found = settings.WWW_ROOT[:-1] + item["found"]
                image_file = open(found , "rb")
                encoded_string_found = base64.b64encode(image_file.read())
                image_file.close()
            except:
                encoded_string_found = ""
            
            try:
                #person_name = "%s %s %s" % (item["person"]["person"]["first_name"], item["person"]["person"]["middle_name"], item["person"]["person"]["last_name"])
                person_name = "%s %s %s" % (item["person"]["person"]["first_name"], item["person"]["person"]["last_name"], item["person"]["person"]["middle_name"],)
            except:
                person_name = ""
            
            person_id = 0
            try:
                person_id = int(item["person"]["person"]["id"])
            except:
                person_id = 0

            eyes_distance = 0
            try:
                face = parseFaceString(item["found_face"])
                eyes_distance = getEyesDistance(face)
            except:
                eyes_distance = 0
            
            focusfactor = ""
            try:
                focusfactor = item["info"]["focusfactor"]
            except:
                focusfactor = ""
            
            noisefactor = ""
            try:
                noisefactor = item["info"]["noisefactor"]
            except:
                noisefactor = ""
            
            noiseStdDev = ""
            try:
                noiseStdDev = item["info"]["noiseStdDev"]
            except:
                noiseStdDev = "" 
            
            if float(item["coeff"]) == 100:
                factor = "1.00"
            else:
                factor = float(item["coeff"]) / 100
            ident_data.append({'db_image': encoded_string_found, 'image': encoded_string_original, 'carousel_image': encoded_string_original, 'carousel_face_margin_top': 0, 'factor': factor, 'person_id':  person_id, 'eyes_distance': eyes_distance, 'focusfactor': focusfactor, 'noisefactor': noisefactor, 'noiseStdDev': noiseStdDev, 'idents_count': '', 'detectTime': getTimeInHMS(), 'last_journal_id': int(item["id"]), 'person_name': person_name, 'person': item["person"]})
            
        answer["ident_data"] = ident_data
    else:
        firedetect_data = []
        smokedetect_data = []
        flashdetect_data = []
        leftthings_data = []
        result_data = []
        for item in items:
            get_image = False
            iWidth = iHeight = 0
            back_img = None
            try:
                frame = settings.WWW_ROOT[:-1] + item["frame"]
                #frame = settings.WWW_ROOT[:-1] + "/files/detects/test.jpg"
                image_file = open(frame , "rb")
                back_img = Image.open(image_file)
                iWidth, iHeight = back_img.size
                get_image = True
            except:
                logging.exception("Logdetect open image file error: %s", str(sys.exc_info()))
                get_image = False

            if back_img and get_image:
                try:
                    json_data = item["json_data"]
                    for currentObj in json_data["objects"]:
                        points = map(lambda x: int(x), currentObj["points"].split(','))
                        coords_list = get_extended_detect_area(iWidth, iHeight, points[0], points[2], points[1], points[3])
                        obj_content, obj_margin_top = get_object_thumbnail(request, back_img, coords_list[0],  coords_list[2], coords_list[1], coords_list[3])
                        
                        append_str = {'image': base64.b64encode(obj_content), 'margin_top': obj_margin_top, 'detectTime': getTimeInHMS(), 'frame_color': '', 'need_to_show': 1, 'data_type': json_data["alertSubType"], 'id': currentObj["id"]}
                        if json_data["alertSubType"] == "fireDetect":
                            firedetect_data.append(append_str)
                        if json_data["alertSubType"] == "smokeDetect":
                            smokedetect_data.append(append_str)
                        if json_data["alertSubType"] == "flashDetect":
                            flashdetect_data.append(append_str)
                        if json_data["alertSubType"] == "leftThings":
                            leftthings_data.append(append_str)
                except:
                    logging.exception("Logdetect get object thumbnail block error: %s", str(sys.exc_info()))


            try:
                image_file.close()
            except:
                pass
        
        if len(firedetect_data) > 0:
            result_data.append(firedetect_data)
        if len(smokedetect_data) > 0:
            result_data.append(smokedetect_data)
        if len(flashdetect_data) > 0:
            result_data.append(flashdetect_data)
        if len(leftthings_data) > 0:
            result_data.append(leftthings_data)

        answer["result_data"] = result_data

    answer["query_time"] = query_time
    answer["journal"] = items
    
    answer["status"] = True
    return answer
