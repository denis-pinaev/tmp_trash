#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from videoclient.balancer import Balancer
from PIL import Image, ImageDraw
import os
import re
import json
import time
import commands
from django.shortcuts import render_to_response
from videoclient.settings import *
from django.contrib import auth
from django import forms
from videoclient.communicator import Communicator
from videoclient import models
import datetime
import logging
from utils import getDefaultParams, dataVAJournal, dataAccess, gen_filename, get_journal_path, get_value_defaultparams, getDataDivision, renamePerson, REVISION, getNamePersonByBalId, getDataAnketaList, getPersonByBalId, getPersonIdByBalId, DeletePerson, getDataVideo, dataGet, VERSION, getAllPhotosByName
from videoclient.settings import last_journal_update, wait_unidentified_person, MEDIA_ROOT, reaction_time, add_not_ident_person, count_time_test, time_span_time_test, script_export_info, TEST_JAR, TEST_CONFIG, TEST_OUTPUT, TEST_TMP_FILE, TEST_OUTPUT_URL, division_visitor, division_person, division_employee, self_learning, show_ident_window_recogn_only, ICON_EYES, ICON_REC, USE_ZIP_FILE, DEFAULT_COMMUNICATOR_VIDEO_CODEC
import settings
from django.db.models import Q
from videoclient.utils import dataNavigation
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from videoclient.profile import models as ProfileModels
from PIL import Image
from PIL.ExifTags import TAGS
from django.utils import simplejson
from videoclient.views import  tester, getIdentData, getDefaultParams, initBalancer, initCommunicators, JsonResponse, circleWithColor, getTimeInHMS, get_object_thumbnail, render_to_response_ex, getActiveSystemCameras
from videoclient.videoanalytics.forms import LeftThingsDetectorForm, BackgroundDetectorForm, TestFromLogDetect, TestClearDataJournal
from models import DetectorLog, Detector
from time import time
import random
from django.core.urlresolvers import reverse
import ast
from cStringIO import StringIO as StringIO
from django.utils.translation import ugettext as _
import base64
from django.contrib.auth.decorators import permission_required, login_required

import sys

IDENT_TYPE = "ident"
IDENT_NAME = _('Идентификации')

@tester
@permission_required('user_perms.perm_logs')
def journal_videoanalytics(request):

    data = dict()
    data = getIdentData(request)
    if space:
        s = commands.getoutput(space)
        s = s.replace("\n", "")
        m = re.match(r".*G *([0-9]+)%.*", s)
        if m and m.group(1):
            data["space"] = 100-int(m.group(1))

    data.update(getDefaultParams(request, 'journal_videoanalytics'))
    #data.update( {"csm": float(get_value_defaultparams(journalBoundCoeff))*100})
    data.update(dataVAJournal(request))
    #raise Exception(data["all_users"])
    data.update(getDataDivision(request))
    data.update(dataNavigation(request, data['all_users']))
    data["users"] = data["users"][data['start']-1:data['finish']-1]
    data.update(dataGet(request))
    
    #if request.GET.has_key('data') and not request.GET.has_key('countrows'):
    #    return render_to_response("datajournal.html", data)
    #elif request.GET.has_key('countrows'):
    #    return JsonResponse({'countrows': data['all_users']})
    #else:
    if request.GET.has_key('data') and not request.GET.has_key('countrows'):
        return render_to_response_ex(request, "data_journal_videoanalitics.html", data)
    return render_to_response_ex(request, "journal_videoanalytics.html", data)

@tester
@permission_required('user_perms.perm_logs')
def get_preview_image(request, id=None):
    try:
        journal_log = get_object_or_404(DetectorLog, id=int(id))
        #filename = settings.LOGDETECT_IMAGES + str(journal_log.preview)
        wrapper = get_picture_with_detector_areas(request, journal_log)
#        filename = journal_log.preview.path 
#        f = open(filename, "r+b")
#        wrapper =  f.read() 
#        f.close()
        
        response = HttpResponse(wrapper, content_type='image/jpg')
        response['Content-Length'] = len(wrapper)
        response['Content-Disposition'] = 'attachment;filename=%s.jpg' % journal_log.preview
        return response
    except:
        return True
    
@tester
@permission_required('user_perms.perm_logs')
def get_original_image(request, id=None):
    from PIL import Image, ImageDraw
    import tempfile
    import ast

    try:
        journal_log = get_object_or_404(DetectorLog, id=int(id))
        wrapper = get_picture_with_detector_areas(request, journal_log)
        response = HttpResponse(wrapper, content_type='image/jpeg')
        response['Content-Length'] = len(wrapper)
        response['mimetype'] = 'image/jpeg'
        response['Content-Disposition'] = 'attachment;filename=%s' % journal_log.frame
        return response
    except:
        return True

def GetInHMS(seconds):
    hours = seconds / 3600
    seconds -= 3600 * hours
    minutes = seconds / 60
    seconds -= 60 * minutes
    
    return {'hours': hours, 'minutes': minutes, 'seconds': seconds}

def round_params(param, digits):
    param = round(float(param), digits)
    return str(param).replace(",", ".")
    
@tester    
@permission_required('user_perms.perm_settings')    
def settings_videoanalytics(request, uuid=None):
    
    data = dict()
    data = getIdentData(request)
    
    res_get_all_active_cameras = getActiveSystemCameras(uuid, 'settings_videoanalytics2')
    data["all_active_cameras"] = res_get_all_active_cameras["all_active_cameras"]
    camera = res_get_all_active_cameras["camera"]
    data["communicator_errors_info"] = res_get_all_active_cameras["communicator_errors_info"]
    
    error = ''
    
    c = Communicator()
    if camera:
        #crowdDetect
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        
        data["isOnCrowd"] = False
        try:
            #data["isOnCrowd"] = b.getParameter("control.detector.crowd.need.alert")
            data["isOnCrowd"] = b.getCameraParameter(camera.uuid, "crowdNeedAlert")[0]
            if data["isOnCrowd"] == "true":
                data["isOnCrowd"] = True
            else:
                data["isOnCrowd"] = False
        except:
            data["isOnCrowd"] = False
    
        '''    
        data["isOnSeparatingObjects"] = False
        try:
            isOnSeparatingObjects = c.executeCommand('getModeDetectScheduler', {'uuid': camera.uuid, 'detect': 'separatingObjects'}, 'IsActive')
            data["isOnSeparatingObjects"] = isOnSeparatingObjects["result"]
        except:
            data["isOnSeparatingObjects"] = False
            logging.info("settings_videoanalytics: getModeDetectScheduler is failed: " + str(sys.exc_info()))
        '''
        
        data["isOnleftThings"] = False
        try:
            isOnleftThings = c.executeCommand('getModeDetectScheduler', {'uuid': camera.uuid, 'detect': 'leftThings'}, 'IsActive')
            data["isOnleftThings"] = isOnleftThings["result"]
        except:
            data["isOnleftThings"] = False
            logging.info("settings_videoanalytics: getModeDetectScheduler is failed: " + str(sys.exc_info()))
        
        data["isOnFire"] = False
        try:
            isOnFire = c.executeCommand('getModeDetectScheduler', {'uuid': camera.uuid, 'detect': 'fireDetect'}, 'IsActive')
            data["isOnFire"] = isOnFire["result"]
        except:
            data["isOnFire"] = False
            logging.info("settings_videoanalytics: getModeDetectScheduler is failed: " + str(sys.exc_info()))
        
        data["isOnSmoke"] = False
        try:
            isOnSmoke = c.executeCommand('getModeDetectScheduler', {'uuid': camera.uuid, 'detect': 'smokeDetect'}, 'IsActive')
            data["isOnSmoke"] = isOnSmoke["result"]
        except:
            data["isOnSmoke"] = False
            logging.info("settings_videoanalytics: getModeDetectScheduler smokeDetect is failed: " + str(sys.exc_info()))
        
        isOnFlash = False
        try:
            isOnFlash = c.executeCommand('getModeDetectScheduler', {'uuid': camera.uuid, 'detect': 'flashDetect'}, 'IsActive')
            data["isOnFlash"] = isOnFlash["result"]
        except:
            data["isOnFlash"] = False
            logging.info("settings_videoanalytics: getModeDetectScheduler flashDetect is failed: " + str(sys.exc_info()))
        
        '''
        s_obj_data = None
        try:
            get_values = ['maxMod0', 'minMod1', 'counterApproxLevel', 'connectedComp', 'maxMod1', 'minMod2', 'maxMod2', 'mode', 'bound', 'minPixelInObject', 'autoLearning', 'a', 'closeItr', 'morphology', 'minMod0', 'e']
            s_obj_data = c.executeCommand('getSettingsDetectScheduler', {'uuid': camera.uuid, 'detect': 'separatingObjects'}, 'GetValues', get_values)
        except:
            logging.info("settings_videoanalytics: getSettingsDetectScheduler separatingObjects is failed: " + str(sys.exc_info()))
        if s_obj_data:
            if s_obj_data.has_key('returned_values'):
                data["s_obj_data"] = s_obj_data["returned_values"]
        
        try:
            data["autoLearning"] = int(s_obj_data["returned_values"]["autoLearning"])
            data["morphology"] = int(s_obj_data["returned_values"]["morphology"])
            data["connectedComp"] = int(s_obj_data["returned_values"]["connectedComp"])
        except:
            pass
        '''
        
        lthings_data = None
        try:
            get_values = ['alertTime', 'autoLearning', 'bound', 'cleaningIntervalSeconds', 'interval', 'maxMergingGapPercent', 'maxMod0', 'maxMod1', 'maxMod2', 'maxObjectArea', 'minMod0', 'minMod1', 'minMod2', 'minNumPixelInObject', 'minObjectArea', 'mode', 'startingLearningPercent', 'startingLearningTime', 'waitingTime', 'morphology', 'connectedComp']
            lthings_data = c.executeCommand('getSettingsDetectScheduler', {'uuid': camera.uuid, 'detect': 'leftThings'}, 'GetValues', get_values)
        except:
            error = 'communicator'
            logging.info("settings_videoanalytics: getSettingsDetectScheduler leftThings is failed: " + str(sys.exc_info()))
        
        if lthings_data:
            if lthings_data.has_key('returned_values'):
                data["lthings_data"] = lthings_data["returned_values"]
        
        fireDetect_data = None
        try:
            get_values = ['alertTime', 'firedPixelsThreshold', 'minFireArea', 'maxMergingGapPercent', 'watchOverFrameCount', 'reliabilityThresholdPercent', 'numBlockWidth', 'numBlockHeight', 'foregroundToFireMaxRatio', 'slidingAvgAlpha', 'minForegroundPixelsPercent', 'minFireDelta']
            fireDetect_data = c.executeCommand('getSettingsDetectScheduler', {'uuid': camera.uuid, 'detect': 'fireDetect'}, 'GetValues', get_values)
        except:
            error = 'communicator'
            logging.info("settings_videoanalytics: getSettingsDetectScheduler fireDetect is failed: " + str(sys.exc_info()))
        
        if fireDetect_data:
            if fireDetect_data.has_key('returned_values'):
                data["fireDetect_data"] = fireDetect_data["returned_values"]
                data["fireDetect_data"]["minFireArea"] = round_params(data["fireDetect_data"]["minFireArea"], 2)
                data["fireDetect_data"]["slidingAvgAlpha"] = round_params(data["fireDetect_data"]["slidingAvgAlpha"], 2)
                data["fireDetect_data"]["minForegroundPixelsPercent"] = round_params(data["fireDetect_data"]["minForegroundPixelsPercent"], 2)
                data["fireDetect_data"]["minFireDelta"] = round_params(data["fireDetect_data"]["minFireDelta"], 2)
        
        smokeDetect_data = None
        try:
            get_values = ['alertTime', 'threshold', 'emaDelay', 'emaAlpha', 'minSmokeArea', 'numWidthBlocks', 'numHeightBlocks']
            smokeDetect_data = c.executeCommand('getSettingsDetectScheduler', {'uuid': camera.uuid, 'detect': 'smokeDetect'}, 'GetValues', get_values)
        except:
            error = 'communicator'
            logging.info("settings_videoanalytics: getSettingsDetectScheduler smokeDetect is failed: " + str(sys.exc_info()))
        
        if smokeDetect_data:
            if smokeDetect_data.has_key('returned_values'):
                data["smokeDetect_data"] = smokeDetect_data["returned_values"]
                data["smokeDetect_data"]["emaAlpha"] = round_params(data["smokeDetect_data"]["emaAlpha"], 3)
                data["smokeDetect_data"]["threshold"] = round_params(data["smokeDetect_data"]["threshold"], 3)
                data["smokeDetect_data"]["minSmokeArea"] = round_params(data["smokeDetect_data"]["minSmokeArea"], 2)
        
        flashDetect_data = None
        try:
            get_values = ['alertTime', 'emaAlpha', 'emaDelay', 'bounceUpContrast', 'bounceDownContrast', 'bounceUpBrightness', 'bounceDownBrightness', 'numWidthBlocks', 'numHeightBlocks']
            flashDetect_data = c.executeCommand('getSettingsDetectScheduler', {'uuid': camera.uuid, 'detect': 'flashDetect'}, 'GetValues', get_values)
        except:
            error = 'communicator'
            logging.info("settings_videoanalytics: getSettingsDetectScheduler flashDetect is failed: " + str(sys.exc_info()))
        
        if flashDetect_data:
            if flashDetect_data.has_key('returned_values'):
                data["flashDetect_data"] = flashDetect_data["returned_values"]
                data["flashDetect_data"]["emaAlpha"] = round_params(data["flashDetect_data"]["emaAlpha"], 3)
                data["flashDetect_data"]["bounceUpContrast"] = round_params(data["flashDetect_data"]["bounceUpContrast"], 3)
                data["flashDetect_data"]["bounceDownContrast"] = round_params(data["flashDetect_data"]["bounceDownContrast"], 3)
                data["flashDetect_data"]["bounceUpBrightness"] = round_params(data["flashDetect_data"]["bounceUpBrightness"], 3)
                data["flashDetect_data"]["bounceDownBrightness"] = round_params(data["flashDetect_data"]["bounceDownBrightness"], 3)
        
        #crowdDetect
        data["crowdDetectSize"] = ""
        try:
            data["crowdDetectSize"] = crowdDetectSize = b.getCameraParameter(camera.uuid, "crowdSize")[0]#b.getParameter("control.detector.crowd.size")#todo
        except:
            data["crowdDetectSize"] = ""
        
        data["crowdDetectTimeout"] = ""
        try:
            crowdDetectTimeout = b.getCameraParameter(camera.uuid, "crowdAlertTimeout")[0]#b.getParameter("control.detector.crowd.timeout")
            data["crowdDetectTimeout"] = int(int(crowdDetectTimeout) / 1000)
        except:
            data["crowdDetectTimeout"] = ""
        
        del b
    
    c.close()
    del c
    
    data["error"] = error
    data["selected_camera"] = camera
    data.update(getDefaultParams(request, 'settings_vanalytics'))
    return render_to_response_ex(request, "settings_videoanalytics.html", data)

@tester
@permission_required('user_perms.perm_settings')
def set_settings_videoanalytics(request):  
    data = dict()
    data["status"] = False
    data["bg_gen_error"] = False
    err = False
    
    form = LeftThingsDetectorForm(request.REQUEST)
    if form.is_valid():
        try:
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            SERVERC, PORTC, COMMUNICATORS = initCommunicators()
            c = Communicator(COMMUNICATORS[form.cleaned_data['com_id']]['host'], COMMUNICATORS[form.cleaned_data['com_id']]['port'])
            c.open()
        except:
            err = True
            logging.exception("set_settings_videoanalytics communicator connect problem: " + str(sys.exc_info()))
        
        #trying to save detectors settings
        try:
            set_status = c.setSettingsDetectScheduler(form)
            
            if not set_status["error_remark"]:
                data["status"] = set_status["result"]
            else:
                logging.exception("setSettingsDetectScheduler leftthings: Error remark: %s, Communicator id: %s, Camera num: %s " % (str(set_status["error_remark"]), str(form.cleaned_data['com_id']), str(form.cleaned_data['cam_id'])))
        except:
            err = True
        #trying to turn on/off detector
        isLeftThingsOn = c.getModeDetectScheduler(form.cleaned_data['cam_id'])
        if not isLeftThingsOn["error_remark"]:
            if request.REQUEST["check_thingsDetector"] == '1':
                if not isLeftThingsOn["result"]:
                    turn_status = c.turnOnOffModeDetectScheduler(form, mode='on', detect='leftThings')
                    if turn_status["error_remark"]:
                        logging.exception("turnOnModeDetectScheduler leftthings: Error remark:%s, Communicator id %s: Camera num: %s" % ( str(turn_status["error_remark"]), str(form.cleaned_data['com_id']), str(form.cleaned_data['cam_id'])))
                        if "background isn't found" in turn_status["error_remark"]:
                            data["bg_gen_error"] = True
                            err = True
            else:
                if isLeftThingsOn["result"]:
                    turn_status = c.turnOnOffModeDetectScheduler(form, mode='off', detect='leftThings')
                    if turn_status["error_remark"]:
                        logging.exception("turnOffModeDetectScheduler leftthings: Error remark: %s, Communicator id: %s: Camera num: %s " % (str(turn_status["error_remark"]), str(form.cleaned_data['com_id']), str(form.cleaned_data['cam_id'])))
                        err = True
        else:
            logging.exception("getModeDetectScheduler leftthings: Error remark: %s, Communicator id: %s, Camera num: %s " % (str(isLeftThingsOn["error_remark"]), str(form.cleaned_data['com_id']), str(form.cleaned_data['cam_id'])))
            err = True

        try:
            c.close()
            del c
        except:
            pass

    if set_status["result"]:
        data["status"] = True

    if err:
        data["status"] = False

    return JsonResponse(data)

@tester
@permission_required('user_perms.perm_settings')
def bg_generation(request):
    data = dict()
    data["status"] = False
    form = BackgroundDetectorForm(request.REQUEST)
    if form.is_valid():
        #trying to save background detectors settings
        try:
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            SERVERC, PORTC, COMMUNICATORS = initCommunicators()
            c = Communicator(COMMUNICATORS[form.cleaned_data['com_id']]['host'], COMMUNICATORS[form.cleaned_data['com_id']]['port'])
            c.open()
            
            set_status = c.setSettingsDetectScheduler(form, detect='background')
            turn_status = c.turnOnOffModeDetectScheduler(form, mode='on', detect='background')
            
            c.close()
            del c
            
            if not set_status["error_remark"]:
                data["status"] = set_status["result"]
            else:
                logging.exception("setSettingsDetectScheduler background: Error remark: %s, Communicator id: %s Camera num: %s " % (str(set_status["remark"]), str(form.cleaned_data['com_id']), str(form.cleaned_data['cam_id'])))
            
            if not turn_status["error_remark"]:
                data["status"] = turn_status["result"]
            else:
                logging.exception("turnOnOModeDetectScheduler background: Error remark: %s, Communicator id: %s Camera num: %s " % (str(turn_status["remark"]), str(form.cleaned_data['com_id']), str(form.cleaned_data['cam_id'])))
            
            
            if set_status["result"] and turn_status["result"]:
                data["status"]  = True
        except:
            data["status"] = False
    return JsonResponse(data)

@tester
@permission_required('user_perms.perm_logs')
@permission_required('user_perms.perm_logs_clear')
def clearjournal(request):
    """
    Очистка журнала видеоаналитики
    """
    from videoclient.views import month_ago, UnlinkFileDir
    try:
        logging.info("videoanalytics clearjournal")
        form = TestClearDataJournal(request.REQUEST, request.FILES)
        if form.is_valid():    
            if "period" in form.cleaned_data and form.cleaned_data["period"] in (0,1,2,3, 4):
                dt = None
                if form.cleaned_data["period"]==0: dt = datetime.datetime.now()-datetime.timedelta(days=7)
                elif form.cleaned_data["period"]==1: dt = month_ago(datetime.datetime.now(), 1)
                elif form.cleaned_data["period"]==2: dt = month_ago(datetime.datetime.now(), 3)
                elif form.cleaned_data["period"]==3 and "dataClear" in form.cleaned_data: dt = form.cleaned_data["dataClear"]
                elif form.cleaned_data["period"]==4: dt = 'all' 
                if dt:
                    c = 100
                    if dt == 'all':
                        journal = DetectorLog.objects.all()
                    else:
                        journal = DetectorLog.objects.filter(dt_detect__lte=dt)
                    for j in journal:
                        #return HttpResponse(dt)
                        if j.frame:
                            #frame_path = settings.LOGDETECT_IMAGES + str(j.frame)
                            frame_path = j.frame.path
                            if os.path.exists(frame_path): UnlinkFileDir(frame_path)
                        if j.preview:
                            #preview_path = settings.LOGDETECT_IMAGES + str(j.preview)
                            preview_path = j.preview.path
                            if os.path.exists(preview_path): UnlinkFileDir(preview_path)
                            
                    from django.db import connection, transaction
                    cursor = connection.cursor()   
                    if dt == 'all':                      
                        query = "delete from videoanalytics_detectorlog"
                    else:
                        query = "delete from videoanalytics_detectorlog where dt_detect<='%s'" % (dt)
                    cursor.execute(query)
                    transaction.commit_unless_managed()
                    return HttpResponse('True')
        return HttpResponse('False')       
    except:
        logging.exception("videoanalytics clearjournal " + str(sys.exc_info()))
        return HttpResponse('False')

PREVIEW_IMAGE_SIZE = (200, 300)

def image_thumbnail(filename, size, fname):
    imgName = u'pre_%s.jpg' % fname
    newfile = settings.LOGDETECT_IMAGES + imgName
    try:
        path = os.path.dirname(newfile)
        if not os.path.exists(path):
            os.makedirs(path)
        iimg = Image.open(filename)
        width, height = iimg.size
        if width > size[0] or height > size[1]:
            iimg.thumbnail(size)
        iimg.save(newfile)
        os.unlink(filename)
        return imgName
    except:
        logging.exception("map image upload thumbnail: "+str(sys.exc_info()))
        return ''

ORIGINAL_IMAGE_SIZE = (600, 400)

def original_image_thumbnail(filename, size, fname):
    imgName = u'%s.jpg' % fname
    newfile = settings.LOGDETECT_IMAGES + imgName
    try:
        path = os.path.dirname(newfile)
        if not os.path.exists(path):
            os.makedirs(path)
        iimg = Image.open(filename)
        width, height = iimg.size
        if width > size[0] or height > size[1]:
            iimg.thumbnail(size)
        iimg.save(newfile)
        os.unlink(filename)
        return width, height, imgName
    except:
        logging.exception("map image upload thumbnail: "+str(sys.exc_info()))
        return ''
    
from videoclient.videoanalytics import models as vanModels    
def getDataSavedPhoto(type, filename, detect, url_prefix):
    answer = dict()
    other_data = dict()
    import settings
    if 'originalPicture' in detect and detect['originalPicture'] and detect['originalPicture'] != 'null':
        url = ''
        db_path = vanModels.getDetectsFileNameByFileName(os.path.join('/',filename))
        url = os.path.join(settings.MEDIA_URL, db_path)
        
        full_path = os.path.join(settings.MEDIA_ROOT, db_path)
        dir_name = os.path.dirname(full_path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        while os.path.isfile(full_path):
            full_path = "%s_%s" %(full_path[:-4], full_path[-4:])
            db_path = "%s_%s" %(db_path[:-4], db_path[-4:])
            
        f = open(full_path, 'w+b')
        import base64
        f.write(base64.b64decode(detect['originalPicture']))
        f.close()
        
        answer["%sUrl" %(type)] = url_prefix+url
        other_data[type] = db_path
    else:
        other_data[type] = ''
    return {'answer': answer, 'other_data': other_data}    

from videoclient.views import check_field
@tester
def log_detect_package(request):
    """Пакетная обработка детекторов видеоаналитики"""
    answer = dict()
    answer["status"] = False
    try:
# Получение запроса из файла
        import settings
        if os.path.exists(os.path.join(settings.PROJECT_ROOT, 'query.txt')):
            import settings
            f = open(os.path.join(settings.PROJECT_ROOT, 'query.txt'), 'r+b')
            query_str = f.read()
            f.close()   # TODO убрать и сделать проверку из request
        else:
# получение запроса из request
            if 'data' not in request.REQUEST:
                answer["error"] = "data not found"
                return JsonResponse(answer)
            
            query_str = request.REQUEST["data"]

# обработка запроса
        
        query = json.loads(query_str)

# проверки полей
        if not check_field('detects', query):
            answer["error"] = "detects not found"
            return JsonResponse(answer)
        detects = query['detects']
        
        if check_field('size', query) and query['size'] != len(detects):
            answer["error"] = "size not equal len of detects"
            return JsonResponse(answer)

# загрузка настроек
        
        from videoclient import utils
        #default_coeff = float(utils.get_value_defaultparams(journalBoundCoeff))
                   
# инициализация переменных
        
        answer["detects"] = []
        names = ['dt_detect', 'frame', 'preview', 'camera_id', 'detector_type_id', 'json_data']
        items = []
        
# инициализация базы данных        
        
        from django.db import connection, transaction
        cursor = connection.cursor()
        
        all_cameras = dict()
        all_sub_types = dict()
            
# обработка детектов
        
        for detect in detects:
            answer_detect = dict()
            answer_detect["status"] = False
            other_data = dict()
            try:
                # Индекс детекта в пакете, 
                # необходимо в ответе вернуть такой же
                if check_field("index", detect):
                    answer_detect["index"] = detect["index"]
                
                # Проверка и обработка времени детекта
                if check_field("alertTime", detect):
                    alertTime = float(detect["alertTime"])/1000
                else:
                    alertTime = time.time()
                
                alertTime = datetime.datetime.fromtimestamp(alertTime)
                alertTime_str = alertTime.strftime("%Y-%m-%d %H:%M:%S")
                time_update = alertTime_str
                other_data["dt_detect"] = alertTime_str
                
                
                # Проверки на наличие cameraIp и cameraType
                # обработка этих параметров идет ниже
                if not check_field("cameraIp", detect):
                    answer_detect["error"] = "cameraIp not found"
                    answer["detects"].append(answer_detect)
                    continue
                
                if not check_field("cameraType", detect):
                    answer_detect["error"] = "cameraType not found"
                    answer["detects"].append(answer_detect)
                    continue
                
                if not check_field("cameraUuid", detect):
                    answer_detect["error"] = "cameraUuid is not found"
                    answer["detects"].append(answer_detect)
                    continue
                
                # Обработка параметров камеры
                cameraIp = detect["cameraIp"]
                cameraType = detect["cameraType"]
                cameraUUID = detect["cameraUuid"]
                
                if cameraUUID in all_cameras:
                    camera = all_cameras[cameraUUID]
                else:
                    camera, create = models.Camera.objects.get_or_create(uuid=cameraUUID)
                    cam = camera
                    cam.ip = cameraIp
                    cam.type = cameraType
                    cam.save()

                    if cameraUUID not in all_cameras:
                        all_cameras[cameraUUID] = dict()
                    all_cameras[cameraUUID] = camera

                other_data["camera_id"] = camera.id                
                
                
                # Проверка типа детектора
                if not check_field("alertSubType", detect):
                    answer_detect["error"] = "alertSubType not found"
                    answer["detects"].append(answer_detect)
                    continue
                
                alertSubType = detect["alertSubType"]
                
                # Получаем ID ветектора в случае
                # если нет такого детектора то создаем
                if alertSubType in all_sub_types:
                    subType = all_sub_types[alertSubType]
                else:
                    subType, create = vanModels.Detector.objects.get_or_create(dtype = alertSubType)
                    if create:
                        subType.name = alertSubType
                        subType.save()
                    all_sub_types[alertSubType] = subType
                other_data["detector_type_id"] = subType.id
                                
                
                # Проверка и сохранение кадра
                host_ip = request.get_host()
                detect["host_ip"] = host_ip
                url_prefix = "http://%s" % host_ip
                filename = get_journal_path(gen_filename())
                
                temp_data = getDataSavedPhoto('frame', filename, detect, url_prefix)
                answer_detect.update(temp_data["answer"])
                other_data.update(temp_data["other_data"])
                other_data['preview'] = other_data['frame'] 
                
                
                if check_field('originalPicture', detect):
                    del detect['originalPicture']
                    
                other_data['json_data'] = json.dumps(detect)
                
                answer_detect["addNew"] = True
                
                item = []
                for name in names:
                    if name in other_data and other_data[name] is not None and other_data[name] != 'NULL':
                        item.append("'%s'" %other_data[name])
                    else:
                        item.append("NULL")
                items.append("(%s)" %(', '.join(item)) )
                
                answer_detect["status"] = True
            except:
                logging.exception(str(sys.exc_info()))
                answer_detect["exception"] =  str(sys.exc_info())
            answer["detects"].append(answer_detect)
        
        if len(items) > 0:
            sql = 'insert into videoanalytics_detectorlog (%s) values %s' %(', '.join(names), ', '.join(items))
            cursor.execute(sql)
            
        transaction.commit_unless_managed()
        
        answer["status"] = True
    except:
        logging.exception(str(sys.exc_info()))
        answer["exception"] = str(sys.exc_info())
        if 'detects' in answer:
            for detect in answer["detects"]:
                detect["addNew"] = False
    logging.info(str(answer))
    return JsonResponse(answer)    

@tester
def log_detect(request):
    import ast
    import tempfile
    import sys
    
    data = {'status': False, 'addNew': False}
    w = h = None
    try:
        logging.info("logdetect init...")
        form = TestFromLogDetect(request.POST, request.FILES)
        data = form.cleaned_data["data"]
        logging.info("log_detect incoming data: " + str(data))
    except:
        pass

    try:
        #form = TestFromLogDetect(request.POST, request.FILES)
        if form.is_valid():
            fname = u'%s%s' %(int(time()), random.randint(0,99999))
            data = form.cleaned_data["data"]
            json_data = ast.literal_eval(data)
            logging.info("log_detect incoming data: " + str(json_data))
            try:
                if json_data["detector"] == 'leftThings':
                    preview = form.cleaned_data["preview"]
                    if preview:
                        try:
                            input_file = ''
                            for t in preview: input_file += t
                            fileno, path = tempfile.mkstemp()
                            f = open(path, 'w+b')
                            f.write(input_file)
                            f.close()
                            preview_image = image_thumbnail(path, PREVIEW_IMAGE_SIZE, fname)
                        except:
                            logging.exception("logdetect thumbnail preview generation" + str(sys.exc_info()))
                if json_data["detector"] == 'background':
                    preview_image = None
                frame = form.cleaned_data["frame"]
                if frame:
                    try:
                        input_file = ''
                        for t in frame: input_file += t
                        fileno, path = tempfile.mkstemp()
                        f = open(path, 'w+b')
                        f.write(input_file)
                        f.close()
                        w, h, frame_image = original_image_thumbnail(path, ORIGINAL_IMAGE_SIZE, fname)
                    except:
                        logging.exception("logdetect thumbnail frame generation" + str(sys.exc_info()))
                try:
                    detector = get_object_or_404(Detector, dtype=json_data["detector"])
                    detectLog = DetectorLog(json_data=data, camera_name=json_data["camera"]["ip"], camera_type=json_data["camera"]["type"], preview=preview_image, frame=frame_image, orig_width=w, orig_height=h, detector_type=detector)
                    detectLog.save()
                    
                    frame_url = ''
                    preview_url = ''
                    try:
                        url_prefix = "http://%s" % request.get_host()
                        frame_url = url_prefix + reverse('get_original_image', args=[detectLog.pk])
                        preview_url = url_prefix + reverse('get_preview_image', args=[detectLog.pk])
                    except:
                        logging.exception("logdetect answer url failed" + str(sys.exc_info()))
                    
                    data = { 'status': True, 'addNew': True, 'frame_url': frame_url, 'preview_url': preview_url }
                except:
                    log.exception("logdetect can't add record to tabale DetectoLog" + str(sys.exc_info()))
            except:
                c
                data = {'status': False, 'addNew': False}
    except:
        logging.exception(str(sys.exc_info()))
    #raise Exception("OK")
    return JsonResponse(data)


def parse_json_face(j_string):
    """ Выделить из координат элементы лица """
    res = dict()
    params = map(lambda x: float(x), j_string.split(','))
    
    res['face'] = (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
    res['is_face'] = int(params[8])
            
    res['eye1'] = (params[9], params[10])
    res['is_eye1'] = int(params[11])
    
    res['eye2'] = (params[12], params[13])
    res['is_eye2'] = int(params[14])
    
    res['nouse'] = (params[15], params[16])
    res['is_nouse'] = int(params[17])
    
    res['chin'] = (params[18], params[19])
    res['is_chin'] = int(params[20])

    return res

def get_picture_draw(img_path, rgb=False, width=360):
    """ Ресайз картинки """
    frame = Image.open(img_path)
    if rgb:
        frame = frame.convert("RGB")
    fWidth, fHeight = frame.size
    height = (((width * 100) / fWidth) * fHeight) /100
        
    frame.thumbnail((width, height), Image.ANTIALIAS)
    sWidth, sHeight = frame.size
    factor = float(sWidth)/float(fWidth) if float(sWidth)/float(fWidth) < float(sHeight)/float(fHeight) else float(sHeight)/float(fHeight)
    return frame, factor, ImageDraw.Draw(frame)

@tester
@permission_required('user_perms.perm_settings')
def get_picture_with_detector_areas(request, alert):
    """ Получение сработавших детекторов """
    color = [(204, 0, 204), (255, 0, 0), (0, 0, 255), (255, 102, 0)]
    col = (0, 0, 0)

    img_path = alert.frame.path
    #img_path = settings.WWW_ROOT[:-1] + "/files/detects/test.jpg"
    frame_content = ''
    row_info = ast.literal_eval(alert.json_data)
    
    if alert.detector_type.dtype == "leftThings":
        col = color[0]
    elif alert.detector_type.dtype == "fireDetect":
        col = color[1]
    elif alert.detector_type.dtype == "smokeDetect":
        col = color[2]
    elif alert.detector_type.dtype == "flashDetect":
        col = color[3]
    
    try:
        frame, factor, draw = get_picture_draw(img_path)
        
        if not alert.detector_type.dtype == 'crowdDetect':
            for object in row_info["objects"]:
                points = object["points"].split(",")
                draw.line((int(points[0])*factor, int(points[1])*factor, int(points[2])*factor, int(points[1])*factor), fill=col, width=1)
                draw.line((int(points[2])*factor, int(points[1])*factor, int(points[2])*factor, int(points[3])*factor), fill=col, width=1)
                draw.line((int(points[2])*factor, int(points[3])*factor, int(points[0])*factor, int(points[3])*factor), fill=col, width=1)
                draw.line((int(points[0])*factor, int(points[1])*factor, int(points[0])*factor, int(points[3])*factor), fill=col, width=1)
        
        if alert.detector_type.dtype == 'crowdDetect':
            if "faces" in row_info:
                for face in row_info["faces"]:
                    try:
                        face_data = parse_json_face(face)
                        drawFaceBorder(draw, color[0], face_data, factor)
                    except:
                        logging.exception(str(sys.exc_info()))
                
        output = StringIO()
        frame.save(output, format="JPEG")
        frame_content = output.getvalue()
        output.close()
        
        del draw
    except:
        logging.exception("get_picture_with_detector_areas: " + str(sys.exc_info()))
    
    return frame_content

def drawFaceBorder(draw, color, face_data, factor):
    """ Рисование границ и элементов лица """
    x1 = float(face_data["eye1"][0]) * factor
    y1 = float(face_data["eye1"][1]) * factor 
    circleWithColor(draw, (x1,y1), color, radius=2)
                    
    x2 = float(face_data["eye2"][0]) * factor
    y2 = float(face_data["eye2"][1]) * factor
    circleWithColor(draw, (x2,y2), color, radius=2)
                        
    x1 = float(face_data["chin"][0]) * factor
    y1 = float(face_data["chin"][1]) * factor
    circleWithColor(draw, (x1,y1), color, radius=2)
        
    x1 = float(face_data["nouse"][0]) * factor
    y1 = float(face_data["nouse"][1]) * factor
    circleWithColor(draw, (x1,y1), color, radius=2)

    #рисуем рамку лица
    corner_size = 7
    line_width = 1
    face = face_data["face"]
    draw.line((int(face[0])*factor, int(face[1])*factor, int(face[0])*factor + corner_size, int(face[1])*factor), fill=color, width=line_width)
    draw.line((int(face[0])*factor, int(face[1])*factor, int(face[0])*factor, int(face[1])*factor + corner_size), fill=color, width=line_width)
                        
    draw.line((int(face[2])*factor, int(face[3])*factor, int(face[2])*factor - corner_size, int(face[3])*factor), fill=color, width=line_width)
    draw.line((int(face[2])*factor, int(face[3])*factor, int(face[2])*factor, int(face[3])*factor + corner_size), fill=color, width=line_width)
                        
    draw.line((int(face[4])*factor, int(face[5])*factor, int(face[4])*factor - corner_size, int(face[5])*factor), fill=color, width=line_width)
    draw.line((int(face[4])*factor, int(face[5])*factor, int(face[4])*factor, int(face[5])*factor - corner_size), fill=color, width=line_width)
                        
    draw.line((int(face[6])*factor, int(face[7])*factor, int(face[6])*factor + corner_size, int(face[7])*factor), fill=color, width=line_width)
    draw.line((int(face[6])*factor, int(face[7])*factor, int(face[6])*factor, int(face[7])*factor - corner_size), fill=color, width=line_width)
    
def getIdentAlerts(request, result):
    """ Получение уникальных по agregate_id идентификаций """
    alerts = result["alerts"]
    aggregate_id = request.GET.get("identid", 0)
    if aggregate_id and str(aggregate_id).isdigit():
        aggregate_id = int(aggregate_id)
        new_alerts = models.Journal.objects.filter(id__gt=aggregate_id).exclude(person=None).exclude(training=True).order_by("id")
        if new_alerts:
            ids = []
            for alert in new_alerts:
                if alert.agregate.id not in ids:
                    ids.append(alert.agregate.id)
                    aggregate_id = max(aggregate_id, alert.id)
                    
                    frame_content = ''
                    path = alert.original.path
                    try:
                        if os.path.exists(path):
                            frame, factor, draw = get_picture_draw(path, rgb=True, width=200)
                    
                            color = (102, 255, 102)
                            face_data = parse_json_face(alert.found_face) 
                            drawFaceBorder(draw, color, face_data, factor)                    
                    
                            output = StringIO()
                            frame.save(output, format="JPEG")
                            frame_content = output.getvalue()
                            output.close()
                            del draw
                    except:
                        logging.exception(sys.exc_info())
                        
                    base_content = ""
                    try:
                        path = alert.finded.path                     
                        if path and os.path.exists(path):
                            frame, factor, draw = get_picture_draw(path, rgb=True, width=200)
                            output = StringIO()
                            frame.save(output, format="JPEG")
                            base_content = output.getvalue()
                            output.close()
                            del draw
                    except:
                        logging.exception(sys.exc_info())
                    
                    alerts.append({'d_id': alert.agregate_id,
                                   'd_type': IDENT_TYPE, 
                                   'd_name': IDENT_NAME, 
                                   'd_time': alert.dt_first_fixed.strftime('%H:%M:%S'), 
                                   'image': base64.b64encode(frame_content), 
                                   'd_camera_ip': alert.camera.ip, 
                                   'd_camera_type': alert.camera.type, 
                                   'd_camera_full_name': alert.camera.full_name(),
                                   'ident': {'fio': alert.person.get_fio(),
                                             'coeff': alert.coeff,
                                             'base_image': base64.b64encode(base_content),
                                             'id': alert.person.person.id,
                                             'group_pk': alert.person.person.group.pk
                                             }
                                   }
                                  )
                    
    result["identid"] = aggregate_id
    return result

@tester    
@login_required    
def check_detector_warnings(request):
    """ Проверка наличия детектов для отображения в интерфейсе """
    alerts = []
    new_alerts = DetectorLog.objects.filter(id__gt=request.GET["checkid"])
    
    for alert in new_alerts:
        row_info = ast.literal_eval(alert.json_data)

        try:
            frame_content = get_picture_with_detector_areas(request, alert)

            if alert.detector_type.dtype == "crowdDetect":
                frame = Image.open(StringIO(frame_content))
                fWidth, fHeight = frame.size
                obj_content, margin_top = get_object_thumbnail(request, frame, 0,  0, int(fWidth), int(fHeight))

                alerts.append({'d_type': alert.detector_type.dtype, 
                               'd_name': alert.detector_type.name, 
                               'd_time': alert.dt_detect.strftime('%H:%M:%S'), 
                               'image': base64.b64encode(frame_content), 
                               'd_camera_ip': row_info["cameraIp"], 
                               'd_camera_type': row_info["cameraType"], 
                               'd_camera_full_name': alert.camera.full_name(), 
                               'crowd_detect_data': {'image': base64.b64encode(obj_content), 
                                                     'margin_top': margin_top, 
                                                     'detectTime': getTimeInHMS(), 
                                                     'frame_color': '#33CC99', 
                                                     'need_to_show': 1, 
                                                     'data_type': 'crowd_detect', 
                                                     'id': 0
                                                     }
                               }
                              )
            else:
                alerts.append({'d_type': alert.detector_type.dtype, 
                               'd_name': alert.detector_type.name, 
                               'd_time': alert.dt_detect.strftime('%H:%M:%S'), 
                               'image': base64.b64encode(frame_content), 
                               'd_camera_ip': row_info["cameraIp"], 
                               'd_camera_type': row_info["cameraType"], 
                               'd_camera_full_name': alert.camera.full_name()
                               }
                              )
        except:
            logging.exception("check_detector_warnings: " + str(sys.exc_info()))
            
    if new_alerts.count() > 0:
        last_row = new_alerts.order_by('-id')[:1]
        checkid = int(last_row[0].id)
    else:
        checkid = request.GET["checkid"]
    
    result = {'checkid': checkid, 'alerts': alerts}
    result = getIdentAlerts(request, result)

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')