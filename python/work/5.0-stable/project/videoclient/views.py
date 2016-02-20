# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from videoclient.balancer import Balancer
from PIL import Image, ImageDraw
from django.db import transaction
import os
import re
import json
import commands
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from videoclient.settings import *
from django.contrib import auth
from django import forms
from videoclient.communicator import Communicator
from videoclient.communicator import models as CommunicatorModels
from videoclient import models
from videoclient import forms as VcForms
import datetime
import time
import logging
from utils import getDefaultParams, dataJournal, dataAccess, gen_filename, get_journal_path, get_value_defaultparams, getDataDivision, renamePerson, REVISION, check_rule, getNamePersonByBalId, getDataAnketaList, getPersonByBalId, getPersonIdByBalId, DeletePerson, getDataVideo, dataGet, VERSION, getAllPhotosByName, updateBalId, getAllPhotosByBalId, smart_truncate, translit, queryset_iterator, getFoundFaceInJournal
from videoclient.settings import last_journal_update, wait_unidentified_person, MEDIA_ROOT, reaction_time, add_not_ident_person, count_time_test, time_span_time_test, script_export_info, TEST_JAR, TEST_CONFIG, TEST_OUTPUT, TEST_TMP_FILE, TEST_OUTPUT_URL, division_visitor, division_person, division_employee, self_learning, show_ident_window, show_ident_window_recogn_only, ICON_EYES, ICON_REC, USE_ZIP_FILE, DEFAULT_COMMUNICATOR_VIDEO_CODEC, PROJECT_ROOT
import settings
from django.db.models import Q
from videoclient.utils import dataNavigation, draw_face_on_image, getCameraByUUID
from django.shortcuts import get_object_or_404
from django.template import Context, loader, RequestContext
from videoclient.profile import models as ProfileModels
from PIL import Image
from PIL.ExifTags import TAGS
from django.utils import simplejson, translation
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from cStringIO import StringIO as StringIO
from math import sqrt
import Queue
import base64
from videoanalytics.models import DetectorLog
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import permission_required, login_required

#
# TODO
# Необходимо реализовать при помощи стандартного CONTEXT_PROCESSORS
#
def render_to_response_ex(request, *args, **kwargs):  
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)

def getTimeInHMS():
    time_now = datetime.datetime.now()
    return str(time_now.strftime("%H:%M:%S"))

def saveError(data, description, save_last_error=True, show=False):
    if save_last_error:
        filename = MEDIA_ROOT + 'errors/lasterror.err'
        path = os.path.dirname(filename)
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(filename, 'w+b')
        f.write(data)
        f.close()
    from videoclient import monitoring
    monitoring.warning(type='exception', description=description, show=show, error_file=data, error_level=0)

def tester(func):
    def wrapper(request, *args, **kw):
        try:
            return func(request, *args, **kw)
        except:
            logging.exception("tester: "+str(sys.exc_info()))
            from django.views import debug
            output =  debug.technical_500_response(request, *sys.exc_info())
            if DEBUG:
                return output
            else:
                saveError(output._get_content(), description = _("Неизвестная ошибка: "))
                data = dict()
                data.update(getDefaultParams(request))
                data.update({"was_error":True})
                return render_to_response_ex(request, "500.html", data)
    return wrapper



def initCommunicators():
    from videoclient import models
    #global SERVERC, PORTC, COMMUNICATORS
    COMMUNICATORS = []
    comms = models.Communicator.objects.filter(active = True)
    SERVERC = ''
    PORTC = ''

    for comm in comms:
        COMMUNICATORS.append({'host': comm.host, 'port': comm.port, 'mjpeg_port': comm.mjpeg_port, 'id': comm.id, 'commun': comm})
        SERVERC = SERVERC + str(comm.host)+'*'
        PORTC = PORTC + str(comm.port)+'*'
        
    if len(SERVERC)>0:
        SERVERC = SERVERC[0:len(SERVERC)-1]
    if len(PORTC)>0:
        PORTC = PORTC[0:len(PORTC)-1]
    return SERVERC, PORTC, COMMUNICATORS

def getAllActiveCameras(url_reverse_name=None, ext_args=[]):
    all_active_cameras = []
    communicator_errors_info = []

    c = Communicator()
    res_cameras = c.getCameras(filter_active=True)
    c.close()
    del c
    
    if res_cameras["success"]:
        all_active_cameras = res_cameras["cameras"]
        if url_reverse_name:
            for camera in all_active_cameras:
                e_args = [camera.uuid]
                for ea in ext_args:
                    e_args.append(ea)
                setattr(camera, "url_reverse_name", str(reverse(url_reverse_name, args=e_args)))
        
        communicator_errors_info = res_cameras["communicator_errors_info"]

    return {'all_active_cameras': all_active_cameras, 'communicator_errors_info': communicator_errors_info}

def getActiveSystemCameras(uuid, url_reverse_name, ext_args=[]):
    res_all_active_cameras = getAllActiveCameras(url_reverse_name, ext_args=[])
    all_active_cameras = res_all_active_cameras["all_active_cameras"]
    communicator_errors_info = res_all_active_cameras["communicator_errors_info"]

    if not uuid:
        #get first active uuid in system
        try:
            uuid = all_active_cameras[0].uuid
        except:
            uuid = None
    
    camera = None
    if uuid:
        try:
            camera = models.Camera.objects.filter(uuid=uuid)[0]
        except:
            camera = None
        if camera is not None:
			try:
                # Получеем режим рамеры
				c = Communicator()
				res_cam_mode = c.getModeScheduler(camera.uuid)
				if res_cam_mode["success"]:
					setattr(camera, "mode", res_cam_mode["answer"])
				else:
					setattr(camera, "mode", 0)
			except:
				logging.exception("")
    
    return {'all_active_cameras': all_active_cameras, 'communicator_errors_info': communicator_errors_info, 'camera': camera}

#TODO
#remove later
def initCameras():
    return True

def initBalancer(check=False):
    try:
        if models.Balancer.objects.filter(active = True).count()>0:
            bal = models.Balancer.objects.filter(active=True)[0]
            HOST = bal.host
            PORT = bal.port
            LOGIN = bal.login
            PASSWD = bal.passwd
            USER = bal.user
            if check: return HOST, PORT, LOGIN, PASSWD, USER, False
            else: return HOST, PORT, LOGIN, PASSWD, USER
    except: 
        logging.exception("initBalancer "+str(sys.exc_info()))
    if check: return DEFAULT_BALANCER_HOST, DEFAULT_BALANCER_PORT, DEFAULT_BALANCER_LOGIN, DEFAULT_BALANCER_PASSWORD, DEFAULT_BALANCER_USER, True
    else: return DEFAULT_BALANCER_HOST, DEFAULT_BALANCER_PORT, DEFAULT_BALANCER_LOGIN, DEFAULT_BALANCER_PASSWORD, DEFAULT_BALANCER_USER

SIZE = (120, 120)

COUNT_FRAME = 3

LIMIT = settings.PAGINATION_DEFAULT_PAGINATION
LIMIT_CAM = 20
MAX_NAME_LEN = 17

import sys
import codecs
import locale, codecs; locale.setlocale(locale.LC_ALL, '')
        
encoding = locale.getlocale()[1]
#if not encoding:
encoding = "utf-8"
import sys;
reload(sys);
sys.setdefaultencoding(encoding)
sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

class Persons:
    
    ids = []
    persons = []
    photos = []
        
    init = False
        
    def start(self, param, filter = ''):
        self.ids = []
        self.persons = []
        self.photos = []
        ids = []
        persons = []
        photos = []
        try:
            ids, persons, photos = param.getPersons()
        except:
            self.init = False
            return 0
        filter = filter.lower()
        if len(filter)>0:
            i = 0
            while i<len(persons):
                pp = persons[i].lower()
                if pp.count(filter)>0:
                    self.ids.append(ids[i])
                    self.persons.append(persons[i])
                    self.photos.append(photos[i])
                i = i+1
        else:
            self.ids = ids
            self.persons = persons
            self.photos = photos
        
        self.init = True;
        
        return len(persons)
    
    def res(self):
        return (self.ids, self.persons, self.photos)
        
import threading
import time        
pers = Persons();
         

def getPreview(filename, size, reload = False):
    import os.path, os
    preview = filename.replace('.jpg', '_%sx%s.jpg' %size)
    
    try:
        if reload or not os.path.exists(preview):
            img = Image.open(filename);
            img.thumbnail(size)

            f = open(preview, 'w+b')
            img.save(f, "JPEG")
            f.close()
    except:
        pass
    
    return preview
    
    
def getPreviewByName(idName, num, reload = False):
    filename = LEARNING_IMAGES + '%s/%04d.jpg'  % (idName, num)
    size = (80, 120)
    size = SIZE
    return getPreview(filename, size, reload)
    
def getAllImages(idName, reload = False):
    #path = settings.MEDIA_ROOT + STAR_PHOTO_PATH + idName
    path = LEARNING_IMAGES + idName
    for f in os.listdir(path):
        filename = "%s/%s" % (path, f)
        if os.path.isdir(filename):
            continue
        size = (60, 80)
        size = (80, 120)
        size = SIZE
        if re.search("_%sx%s.jpg" % size, filename):
            continue
        if re.search(".jpg", filename):
            getPreview( filename, size, reload)
            
def genPages(count, start, limit=LIMIT):
    
    start = int(start-1)/limit*limit #res
    
    out_pages = []
    
    pages = 1 #res
    if count >0:
        pages = (count-1)/limit+1
    
    page = start/limit+1 #res
    
    i = page;
    while i>=1 and i>page-3:
        out_pages.append(i)
        i= i-1
        
    i = page+1;
    while i<=pages and (i<page+3 or len(out_pages)<6):
        out_pages.append(i)
        i= i+1
        
    i = page-3;
    while i>=1 and len(out_pages)<6:
        out_pages.append(i)
        i= i-1
        
    out_pages.sort()
    
    return (page, pages, out_pages)

class LoginForm(forms.Form):
    login = forms.CharField(required=False) #max_length=30, 
    password = forms.CharField(required=False)
    json = forms.CharField(required=False)
    auth_key = forms.CharField(required=False)
    
@tester
def login(request):
    goto = "/ident/"
    from wizard import models as wModels
    all_settings = wModels.Settings.objects.all()
    if all_settings.count() == 0:
        goto = "/wizard/" 
    if request.user.is_authenticated():
        if request.user.groups.filter(name='group_security').count()>0:
            goto = reverse('security', args=[])
        return HttpResponseRedirect(goto)
    
    template_name = "login.html"
    # Для iPad используем отдельный шаблон
    if "HTTP_USER_AGENT" in request.META and "iPad" in request.META["HTTP_USER_AGENT"]:
        template_name = "login_ipad.html"
    
    data = dict()
    data = {'version': VERSION, 'host': HTTP_HOST, 'error': False, 'select_page': 'login'}
    
    form = LoginForm(request.REQUEST, request.FILES);
    if form.is_valid():
        username = form.cleaned_data['login']
        password = form.cleaned_data['password']
        hash = form.cleaned_data['auth_key']
        from videoclient.models import LogingHash
        if hash:
            loging = LogingHash.get_loging_by_hash(hash)
            if not loging:
                data["error"] = True
                return render_to_response_ex(request,  template_name, data);
            username = loging.login
            password = loging.password
            loging.delete()
        else:
            if not username:
                data["error"] = False
                return render_to_response_ex(request,  template_name, data);
            
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            from videoclient.models import LoginJournal, User
            #if isinstance(user, User):
            users = User.objects.filter(id = user.id)
            if len(users)>0:
                if users[0].status.division.id != 1:
                    if 'json' in request.REQUEST: 
                        return JsonResponse({'status': False})
                    data["error"] = True
                    return render_to_response_ex(request,  template_name, data);
                import datetime
                now = datetime.datetime.now()
                LoginJournal.objects.create(user = users[0], login = now)
                users[0].last_access = now
                users[0].save()
            if 'json' in request.REQUEST:
                from videoclient.models import LogingHash 
                return JsonResponse({'status': True, 'auth_key': LogingHash(login=username, password=password).hash})
            else:
                auth.login(request, user)
            if request.user.groups.filter(name='group_security').count()>0:
                goto = reverse('security', args=[])
            return HttpResponseRedirect(goto)
        else:
            if 'json' in request.REQUEST: 
                return JsonResponse({'status': False})
            data["error"] = True
            return render_to_response_ex(request,  template_name, data);
    else:
        if 'json' in request.REQUEST: 
            return JsonResponse({'status': False})
        data["error"] = False
        return render_to_response_ex(request,  template_name, data);
    
@tester    
def logout(request, time = None):
    user = request.user
    from videoclient.models import LoginJournal, User
    users = User.objects.filter(id = user.id)
    if len(users)>0:
        logs = LoginJournal.objects.filter(user = users[0])
        log = logs[len(logs)-1] 
        if time is None:
            import datetime
            log.logout = datetime.datetime.now()
        else:
            log.logout = time
        log.save()
    auth.logout(request)
    response = HttpResponseRedirect("/")
    response.set_cookie("start", '1')
    return response

@tester
@permission_required('user_perms.perm_logs')
@permission_required('user_perms.perm_lists')
def journal_person_autocomplete(request):
    search = request.REQUEST['q']
    persons = models.PersonId.objects.all()
    try:
        srch = search.split()
        i = 0
        while i<len(srch):
            f = srch[i]
            persons = persons.filter(Q(person__first_name__icontains=f) | Q(person__last_name__icontains=f) | Q(person__middle_name__icontains=f))
            i += 1
    except:
        logging.exception("")
    
    fs = u"" + render_to_string("journal_person_search_result.html", {"results": persons,},)
    return HttpResponse(fs.decode("UTF-8"), mimetype='text/plain')   

@tester
@permission_required('user_perms.perm_settings')
def settings(request):
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    
    error = False
    cameras = []
    #ips = dict()
    c = Communicator()
    
    COMMUNICATORS = c.getListOfCommunicators()
    
    only_active = request.REQUEST.get("only_active", None)
    if only_active == None: only_active = True
    else: only_active = str(only_active) == "1"
    
    active_qnt = 0    
    if only_active:
        res_cameras = c.getCameras(filter_active=True)
        if res_cameras["success"]:
            active_qnt = len(res_cameras["cameras"])
    else:
        res_cameras = c.getCameras(filter_active=True)
        if res_cameras["success"]:
            active_qnt = len(res_cameras["cameras"])
        res_cameras = c.getCameras()
    
    
    if res_cameras["success"]:
        cameras = res_cameras["cameras"]
        for camera in cameras:
            try:
                setattr(camera, "commun", camera.commun)
            except:
                setattr(camera, "commun", None)
            try:
                setattr(camera, "com_host", camera.commun.host)
            except:
                setattr(camera, "com_host", None)
            try:
                setattr(camera, "com_port", camera.commun.port)
            except:
                setattr(camera, "com_port", None)
            try:
                setattr(camera, "com_mjpeg_port", camera.commun.mjpeg_port)
            except:
                setattr(camera, "com_mjpeg_port", None)
            setattr(camera, "info", "%s %s" % (camera.ip, camera.type))
            selfLearning = "false"
            
            detects = dict()
            if camera.active:
                
                # Убрано, т.к. автообучение не используется.
#                try:
#                    selfLearning = b.getCameraParameter(camera.ip, camera.type, param = 'selfLearning')[0]
#                except:
#                    logging.exception(str(sys.exc_info()))
#                    selfLearning = "false"
#                setattr(camera, "selfLearning", selfLearning)
                selfLearning = "false"
                setattr(camera, "selfLearning", selfLearning)
                
                #get detectors settings
                try:
                    res_cam_mode = c.getModeScheduler(camera.uuid)
                    if res_cam_mode["success"]:
                        setattr(camera, "mode", res_cam_mode["answer"])
                    else:
                        setattr(camera, "mode", 0)
    
                    from videoclient.utils import get_value_defaultparams
                    if int(get_value_defaultparams("show_videoanalitycs")):
                        detects["isOnCrowd"] = False
                        try:
                            #detects["isOnCrowd"] = b.getParameter("control.detector.crowd.need.alert")#change HERE
                            detects["isOnCrowd"] = b.getCameraParameter(camera.uuid, "crowdNeedAlert")[0]
                            if detects["isOnCrowd"] == "true":
                                detects["isOnCrowd"] = True
                            else:
                                detects["isOnCrowd"] = False
                        except:
                            detects["isOnCrowd"] = False
    
                        '''
                        detects["isOnSeparatingObjects"] = False
                        try:
                            isOnSeparatingObjects = c.executeCommand('getModeDetectScheduler', {'numcamera': camera["numcamera"], 'detect': 'separatingObjects'}, 'IsActive')
                            detects["isOnSeparatingObjects"] = isOnSeparatingObjects["result"]
                        except:
                            detects["isOnSeparatingObjects"] = False
                            logging.info("settings_videoanalytics: getModeDetectScheduler is failed: " + str(sys.exc_info()))
                        '''
                        detects["isOnleftThings"] = False
                        try:
                            isOnleftThings = c.executeCommand('getModeDetectScheduler', {'uuid': camera.uuid, 'detect': 'leftThings'}, 'IsActive')
                            detects["isOnleftThings"] = isOnleftThings["result"]
                        except:
                            detects["isOnleftThings"] = False
                            logging.info("settings_videoanalytics: getModeDetectScheduler is failed: " + str(sys.exc_info()))
                        
                        detects["isOnFire"] = False
                        try:
                            isOnFire = c.executeCommand('getModeDetectScheduler', {'uuid': camera.uuid, 'detect': 'fireDetect'}, 'IsActive')
                            detects["isOnFire"] = isOnFire["result"]
                        except:
                            detects["isOnFire"] = False
                            logging.info("settings_videoanalytics: getModeDetectScheduler is failed: " + str(sys.exc_info()))
                        
                        detects["isOnSmoke"] = False
                        try:
                            isOnSmoke = c.executeCommand('getModeDetectScheduler', {'uuid': camera.uuid, 'detect': 'smokeDetect'}, 'IsActive')
                            detects["isOnSmoke"] = isOnSmoke["result"]
                        except:
                            detects["isOnSmoke"] = False
                            logging.info("settings_videoanalytics: getModeDetectScheduler smokeDetect is failed: " + str(sys.exc_info()))
                        
                        isOnFlash = False
                        try:
                            isOnFlash = c.executeCommand('getModeDetectScheduler', {'uuid': camera.uuid, 'detect': 'flashDetect'}, 'IsActive')
                            detects["isOnFlash"] = isOnFlash["result"]
                        except:
                            detects["isOnFlash"] = False
                            logging.info("settings_videoanalytics: getModeDetectScheduler flashDetect is failed: " + str(sys.exc_info()))
                except:
                    pass
            setattr(camera, "detects", detects)
           
    c.close()
    del c
    
    b.close()
    del b
    
    profiles_list = ProfileModels.CamerasProfile.objects.all()

    from videoclient.utils import get_value_defaultparams
    ident_window_position = get_value_defaultparams("ident_window_position")
    data = dict()
    data.update(getDefaultParams(request, 'settings'))
    data.update({'version': VERSION, 'host': HTTP_HOST, 'select_page': 'settings',
                              'select_subpage': 'cameras', 'user': request.user.username,
                              'cameras': cameras, 'camqnt': len(cameras), 'communicators': COMMUNICATORS,
                              'error': error, 'modes': [0, 1, 2, -1],
                              'ident_window_position': ident_window_position,
                              'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER},
                              "profiles_list": profiles_list, 'only_active': only_active, 'active_qnt':active_qnt
                              })
    
    if request.REQUEST.has_key('data'):
        response = render_to_response_ex(request, "datasettings.html", data)
    else:
        response = render_to_response_ex(request, "settings.html", data)
    return response

#
#
#
#

def ChooseCamera(request, c_settings = True, person ='' , return_data = False):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    error = False
    all_active_cameras = getAllActiveCameras()
    if len(all_active_cameras) == 0:
        error = True
    
    dis_eye = None
    data = dict()
    data.update(getDefaultParams(request, 'learn'))
    data.update({'version': VERSION, 'host': HTTP_HOST, 'select_page': 'learn',
                              'select_subpage': 'learn', 'user': request.user.username,
                              'cameras': all_active_cameras,
                              'error': error, 'modes': [0, 1, 2, -1],
                              'dis_eye': dis_eye,
                              'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}})
    
    name_template = 'settings.html'
    if not c_settings:
        name_template = 'choose_camera.html'
        data['person'] = person

    if return_data:
        return data
    
    response = render_to_response_ex(request, name_template, data) 
    return response

@tester
def choose_camera(request, person=None):
    return ChooseCamera(request, False, person)

def save_tmp_image(data, parent=None):
    fileno, path = tempfile.mkstemp()
    import PIL
    if isinstance(data, PIL.Image._ImageCrop):
        data.convert("RGB").save(path, "PNG")
    else:
        f = open(path, 'w+b')
        f.write(data)
        f.close()
    
    f = open(path, 'r+b')
    img = models.TmpImage()
    img.parent = parent
    img.save()
    img.image.save('i.png', File(f))
    img.save()
    os.remove(path)
    return img
    
def learning(data_file, name_person, distortion=None, add_original_photo=True, face=None, original_photo=None, command='learning', return_res = False, eyes=None):
    res = {}
    res2 = None
    try:
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        res, res2 = b.learning(data_file, name_person, distortion = distortion, face=face, command=command, res2=True, eyes=eyes)
        b.close()
        del b
    except:
        logging.exception("learning upload1: "+str(sys.exc_info()))
        if return_res:
            return False, res2
        return False
    
    logging.info('res: '+str(res))
    
    if len(res)>1:
        parent = save_tmp_image(data_file)
        file = FileWrapper(data_file)
        image = Image.open(file.File)
        size_x, size_y = image.size
        list = []
        for r in res:
            if 'face' not in r:
                continue
            face = r['face'].split(',')
            i = 0
            while i < len(face): 
                face[i] = float(face[i])
                i = i+1
                
            x_min = int(min((face[0], face[2], face[4], face[6])))
            y_min = int(min((face[1], face[3], face[5], face[7])))
            x_max = int(max((face[0], face[2], face[4], face[6])))
            y_max = int(max((face[1], face[3], face[5], face[7])))
            i = i+1
            
            x_min_new = x_min - (x_max-x_min)/2 #Увеличиваем захват, берем больше фона
            if x_min_new<0:
                x_min_new=0
            x_max = x_max+x_min-x_min_new
            if x_max>size_x:
                x_max=size_x
            x_min=x_min_new                
            x_max = x_min+(x_max-x_min)/3*3
                                   
            if float(x_max-x_min)/3 > float(y_max-y_min)/4:
                add_len = (float(x_max-x_min)/3*4-(y_max-y_min))
                y_min = y_min-add_len/2
                y_max = y_max+add_len/2
               
                if y_min<0:
                    y_max = y_max-y_min
                    y_min=0
               
                if y_max>size_y:
                    y_max=size_y                    
                     
            img1 = image.crop((int(x_min), int(y_min), int(x_max), int(y_max)))
            img = save_tmp_image(img1, parent)
            img1.thumbnail((120,120))
            preview = save_tmp_image(img1, img)
            list.append({'url': preview.image.url, 'code': preview.id})
        logging.info(str(list))
            
        return list
            
    elif len(res) == 0:
        if return_res:
            return False, res2
        return False
        
    res = res[0]
    
    if not res.has_key('name_photo') or res['name_photo'] == 'none':
        if return_res:
            return False, res2
        return False
    
    name_person = name_person.encode("utf-8")
    
    try:
        if res.has_key('id') and res["id"] != "none":
            persons = models.PersonId.objects.filter(id = int(name_person))
            if persons.count() > 0:
                persons[0].bal_id = int(res["id"])
                persons[0].save()
    except:
        logging.exception("learning upload2: "+str(sys.exc_info()))
    
    try:
        if res.has_key('name_photo'):
            if add_original_photo:
                if original_photo is not None:
                    logging.info('original_photo()')
                    data_file=original_photo
                photo_name = int(res['name_photo'])
                filename = LEARNING_IMAGES + '%s/%04d.jpg'  % (name_person, photo_name)
                path = os.path.dirname(filename)
                if not os.path.exists(path):
                    os.makedirs(path)
                f = open(filename, 'w+b')
                f.write(data_file)
                f.close()
            
                try:
                    res = get_exif(filename)
                    if len(res) > 0:
                        exifdata = res
                        person_id = get_object_or_404(models.PersonId, pk=int(name_person))
                        photoexif = models.PhotoExifData(personid=person_id, person_id=name_person, photo_id=photo_name, exif=exifdata)
                        photoexif.save()
                except:
                    logging.exception("learning upload exif: "+str(sys.exc_info()))
    except:
        logging.exception("learning upload3: "+str(sys.exc_info()))

    if return_res:
        return True, res2
    return True


class LearnForm( forms.Form ):
    file0  = forms.FileField(required=False)
    file1  = forms.FileField(required=False)
    file2  = forms.FileField(required=False)
    file3  = forms.FileField(required=False)
    file4  = forms.FileField(required=False)
    file5  = forms.FileField(required=False)
    file6  = forms.FileField(required=False)
    file7  = forms.FileField(required=False)
    file8  = forms.FileField(required=False)
    file9  = forms.FileField(required=False)
    file10  = forms.FileField(required=False)
    file11  = forms.FileField(required=False)
    file12  = forms.FileField(required=False)
    file13  = forms.FileField(required=False)
    file14  = forms.FileField(required=False)
    file15  = forms.FileField(required=False)
    file16  = forms.FileField(required=False)
    file17  = forms.FileField(required=False)
    file18  = forms.FileField(required=False)
    file19  = forms.FileField(required=False)
    
import os
import tempfile
from django.core.files import File
class FileWrapper(object):
    def __init__(self, wrapper):
        self.fileno, self.path = tempfile.mkstemp()
        f = open(self.path, 'w+b')
        f.write(wrapper)
        f.close()
        f = open(self.path, 'rb')
        self.File = File(f)
    def __del__(self):
        os.remove(self.path)

def circle(draw, point):
    radius = 4
    draw.ellipse((point[0]-radius, point[1]-radius, point[0]+radius, point[1]+radius), outline=(255, 153, 0))
    draw.ellipse((point[0]-radius+1, point[1]-radius+1, point[0]+radius-1, point[1]+radius-1), outline=(255, 153, 0))


def lines(draw, point, point2):
    len = float(1)/4
    import math
    dx = float(point2[0] - point[0])
    dy = float(point2[1] - point[1]) 
    draw.line((point[0], point[1], point[0]+dx*len, point[1]+dy*len), fill=(255, 153, 0))
    draw.line((point2[0]-dx*len, point2[1]-dy*len, point2[0], point2[1]), fill=(255, 153, 0))
    
@tester
@login_required
def image(request):

    wrapper = ""
    try:
    
        id = int(request.GET['id'])
        photo = int(request.GET['photo'])
        
        personId = getPersonIdByBalId(id)
        filename = LEARNING_IMAGES + '%s/%04d.jpg'  % (personId.id, photo)
    
        params = dict()
        
        if request.GET.has_key('big') and os.path.isfile(filename):
            f = open(filename, "r+b")
            wrapper =  f.read() 
            f.close()
        else:
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            SERVERC, PORTC, COMMUNICATORS = initCommunicators()
            
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            wrapper = None
            images, params = b.getPersonPhotoWithParams(id, photo)
            wrapper = images[0]
    #        if request.GET.has_key('big'):
    #            images, params = b.getPersonPhotoWithParams(id,photo)
    #            wrapper = images[0]
    #        else:
    #            wrapper = b.getPreview(id, photo)[1][0]
            b.close()
            del b
        
        width = None
        height = None    
        if request.GET.has_key('width') and request.GET.has_key('height'):
            width = int(request.GET['width'])
            height = int(request.GET['height'])
        elif not request.GET.has_key('big'):
            width = 120
            height = 120
        
        koef = float(1)
        #if width and height:
        try:
            file = FileWrapper(wrapper)
            img = Image.open(file.File)
            fWidth, fHeight = img.size
            img.thumbnail((width, height), Image.ANTIALIAS)
            sWidth, sHeight = img.size
            koef = float(sWidth)/float(fWidth) if float(sWidth)/float(fWidth) < float(sHeight)/float(fHeight) else float(sHeight)/float(fHeight) 
            fileno, path = tempfile.mkstemp()
            img.convert("RGB").save(path, "PNG")
            f = open(path, 'r+b')
            wrapper = f.read()
            f.close()    
        except:
            logging.exception("resize: "+str(sys.exc_info()))
        
        if request.GET.has_key('eyes'):
            try:
                logging.info("params: "+str(params))
                
                file = FileWrapper(wrapper)
                logging.info("1")
                img = Image.open(file.File)
                img = img.convert("RGB")
                logging.info("2")
                
                
                draw = ImageDraw.Draw(img) # Create a draw object
                
                try:
                    eyes = params["response"][0]["info"][0]["eyes"].split(',')
                    
                    x1 = float(eyes[0])*koef
                    y1 = float(eyes[1])*koef
                    x2 = float(eyes[2])*koef
                    y2 = float(eyes[3])*koef
                    
                    circle(draw, (x1,y1))
                    circle(draw, (x2,y2))
                except:
                    logging.exception("put eyes:"+str(sys.exc_info()))
                    
                try:
                    eyes = params["response"][0]["info"][0]["chin"].split(',')
                    
                    x1 = float(eyes[0])*koef
                    y1 = float(eyes[1])*koef
                    
                    circle(draw, (x1,y1))
                except:
                    logging.exception("put eyes:"+str(sys.exc_info()))
                    
                try:
                    eyes = params["response"][0]["info"][0]["nose"].split(',')
                    
                    x1 = float(eyes[0])*koef
                    y1 = float(eyes[1])*koef
                    
                    circle(draw, (x1,y1))
                except:
                    logging.exception("put eyes:"+str(sys.exc_info()))
                    
                try:
                    eyes = params["response"][0]["info"][0]["quad"].split(',')
                    icon = Image.open(ICON_REC)
                    size_icon= icon.size
                    x1 = float(eyes[0])*koef
                    y1 = float(eyes[1])*koef
                    x2 = float(eyes[2])*koef
                    y2 = float(eyes[3])*koef
                    x3 = float(eyes[4])*koef
                    y3 = float(eyes[5])*koef
                    x4 = float(eyes[6])*koef
                    y4 = float(eyes[7])*koef
                    
                    lines(draw, (x1, y1), (x2, y2))
                    lines(draw, (x2, y2), (x3, y3))
                    lines(draw, (x3, y3), (x4, y4))
                    lines(draw, (x4, y4), (x1, y1))
                except:
                    logging.exception("put eyes:"+str(sys.exc_info()))
                
                fileno, path = tempfile.mkstemp()
                logging.info("convert")
                img.convert("RGB").save(path, "PNG", quality = 60, optimize=1)
                f = open(path, 'r+b')
                wrapper = f.read()
                f.close()
            except:
                logging.exception(str(sys.exc_info()))
    except:
        logging.exception(str(sys.exc_info()))
        wrapper = ""
    
    if len(wrapper) == 0:
        from videoclient import settings
        f = open(settings.MEDIA_ROOT+"images/exception_photo120x120.gif", "r+b")
        wrapper = f.read()
        f.close()
    response = HttpResponse(wrapper, content_type='image/jpg')
    response['Content-Length'] = len(wrapper)
    response['Content-Disposition'] = 'attachment;filename=photo%s_%s.jpg' %(id, photo)
    return response

SHAREIMAGE_SIZE = (485, 330)

def create_watermarked(path_src, path):
    from wizer import settings

    source_image = Image.open(path_src)
    watermark = Image.open(settings.WATERMARK)
    source_image.thumbnail(SHAREIMAGE_SIZE, Image.BICUBIC)
    source_image.paste(watermark, (0, 0), watermark)
    source_image.save(path, "JPEG", quality = 60, optimize=1)

def json_response(data):
    #from django.utils import simplejson    
    #return HttpResponse(simplejson.dumps(data), mimetype='text')
    import json
    return HttpResponse(json.dumps(data), mimetype="application/json")

@tester
@login_required
def execute_method(request):
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    args = []
    i = 1
    while request.REQUEST.has_key('arg'+str(i)):
        args.append(request.REQUEST['arg'+str(i)])
        i= i+1 
   
    name = request.REQUEST['name']
            
    try:
        if name == 'addCamera' and len(args)>0 and args[0] == 'JVC':
            c = Communicator(time_out = 20)
        else:
            c = Communicator()
        c = Communicator()
        res = c.executeMethodByName(name, args)
        value = ''
        try:
            curr_val = ''
            if name == 'setBrightnessCamera' and len(args)>0: curr_val  = c.getBrightnessCamera(args[0])
            elif name == 'setSharpnessCamera' and len(args)>0: curr_val  = c.getSharpnessCamera(args[0])    
            elif name == 'setSaturationCamera' and len(args)>0: curr_val  = c.getSaturationCamera(args[0])
            elif name == 'setContrastCamera' and len(args)>0: curr_val  = c.getContrastCamera(args[0])
            elif name == 'setQualityCamera' and len(args)>0: curr_val  = c.getQualityCamera(args[0])            
            elif name == 'setShortexposures' and len(args)>0: curr_val  = c.getShortexposures(args[0])
            if curr_val and curr_val['success']:
                value = curr_val['answer']
        except:
            logging.exception("execute_method: get value %s, error: %s" %(str(name), str(sys.exc_info())))
        c.close();
        
        if request.REQUEST.has_key('format'):
            if request.REQUEST['format'] == 'json':
                return json_response({"status": res["success"], "result": value})

        return HttpResponse(res["success"])    
    except:
        logging.exception("execute_method: "+str(sys.exc_info()))
        return HttpResponse(str(sys.exc_info()))

@tester
@login_required
def execute_method_balancer(request):
    import socket
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    
    args = []
    i = 1
    while request.REQUEST.has_key('arg'+str(i)):
        args.append(request.REQUEST['arg'+str(i)])
        i= i+1 
    
    name = request.REQUEST['name']
    res = False
    try:
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        b.open()
        if b.connect: 
            from videoclient import settings
            b.TIME_OUT = settings.SAVE_CAMERA_BALANCER_TIMEOUT
            res = b.executeMethodByName(name, args)
            logging.info(b.TIME_OUT)
        b.close()
        del b
    except socket.error:
        logging.info("BALANCER SOCKET ERROR"+str(sys.exc_info()))
        errno, errstr = sys.exc_info()[:2]        
        if errno == socket.timeout: res = "timeout"
    except:
        logging.info("BALANCER ERROR "+str(sys.exc_info()))

    if request.REQUEST.has_key('format'):
        if request.REQUEST['format'] == 'json':
            return json_response({"status": res, "result": ''})
    return HttpResponse(res)

def get_camera_distortion(uuid):
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    
    dstr1 = "0"
    dstr2 = "0"
    dstr3 = "0.5"
    dstr4 = "0.5"

    try:
        dstr = b.getCameraParameter(uuid)
        if len(dstr) == 4:
            ndstr = 4
            dstr1, dstr2, dstr3, dstr4 = dstr
        else:
            ndstr =  3
            dstr1, dstr3, dstr4 = dstr
    except:
        logging.exception("getDistortion: "+str(sys.exc_info()))
        ndstr = 3
        dstr1 = "0"
        dstr3 = "0.5"
        dstr4 = "0.5"
        
    b.close()
    del b
    
    distorsion = {'p1': dstr1, 'p2': dstr2, 'p3': dstr3, 'p4': dstr4, 'count': ndstr}
    logging.info('distorsion: '+str(distorsion))
    return distorsion
    
@tester
@permission_required('user_perms.perm_settings')
def camera(request, uuid=None, project = None):
    res_get_all_active_cameras = getActiveSystemCameras(uuid, 'camera-settings')
    all_active_cameras = res_get_all_active_cameras["all_active_cameras"]
    camera = res_get_all_active_cameras["camera"]
    communicator_errors_info = res_get_all_active_cameras["communicator_errors_info"]
    
    # if camera exists
    error = False
    if camera:
    
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    
        resolution = None
        capture_rect = None
        brightness  = None
        saturation = None
        sharpness = None
        contrast = None
        quality = None
        gamma = None
        light_hz = None
        night_mode = None
        illumination = None
        low_light = None
        short_exposures = None
        scheduler = None
        cameramode = 0    
        frame_minification = None
    
        c = Communicator()
        try:
            fps_answer = dict()
            try:
                fps = c.executeCommand('getCameraSetting', {'uuid': uuid, 'parameter': 'fps'}, 'GetValues', get_values=["value", "list"])
                if "list" in fps:
                    fps["list"] = fps["list"].split(',')
                fps_answer["fps"] = fps 
            except:
                logging.exception("")
	  
            resolution = c.getResolutionCamera(uuid)
            if resolution["success"]: resolution = resolution["answer"]
            if 'resol' not in resolution or not isinstance(resolution['resol'], list) or len(resolution['resol']) < 2:
                """
                    В случае если список разрешений не получен,
                    или это не список, или получили только одно
                    разрешение, то создаем свой
                """  
                resol=[]
                resol.append({'width': '320',  'height': '240', 'fps': '10'})
                resol.append({'width': '640',  'height': '480', 'fps': '10'})
                resol.append({'width': '800',  'height': '600', 'fps': '10'})
                resol.append({'width': '1280',  'height': '1024', 'fps': '10'})
                resol.append({'width': '1600',  'height': '1200', 'fps': '10'})
                resol.append({'width': '2048',  'height': '1536', 'fps': '10'})
                resol.append({'width': '2272',  'height': '1704', 'fps': '10'})
                resol.append({'width': '2560',  'height': '1600', 'fps': '10'})
                resol.append({'width': '2592',  'height': '1944', 'fps': '10'})
                resolution["resol"]=resol
                try:
                    """
                        Проверяем есть ли текущее разрешение
                        камеры в списке разрешений, если нет,
                        то добавляем его туда
                    """                    
                    if 'width' in resolution and 'height' in resolution:
                        add = True
                        width = resolution['width']
                        height = resolution['height']
                        for r in resol:
                            if width == r['width'] and height == r['height']:
                                add = False
                        if add:
                            resol.append({'width': width,  'height': height, 'fps': '10'})
                    if ('max_width' in resolution and 'max_height' in resolution and
                        ('max_width' in resolution != 'width' in resolution or 
                         'max_height' in resolution != 'height' in resolution)):
                        width = resolution['max_width']
                        height = resolution['max_height']
                        p = filter(lambda x: r["width"] == width and height == r['height'], r)
                        if len(filter(lambda x: r["width"] == width and height == r['height'], r)) == 0:
                            resol.append({'width': width,  'height': height, 'fps': '10'})                             
                    resolution["resol"]=resol
                except:
                    logging.exception(str(sys.exc_info()))
            resolution["resol"] = sorted(resolution["resol"], key=lambda x: (int(x["width"]), int(x["height"])))
        except:
            logging.exception("/camera/ getResolutionCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
       
        try:
            res_capture_rect = c.getCaptureRectCamera(uuid)
            if res_capture_rect['success']:
                capture_rect = res_capture_rect['answer']
        except:
            logging.exception("/camera/ getCaptureRectCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))            
        try:
            res_brightness = c.getBrightnessCamera(uuid)
            if res_brightness['success']:
                brightness = res_brightness['answer']
        except:
            logging.exception("/camera/ getBrightnessCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        try:
            res_saturation = c.getSaturationCamera(uuid)
            if res_saturation['success']:
                saturation = res_saturation['answer']
        except:
            logging.exception("/camera/ getSaturationCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        try:
            res_sharpness = c.getSharpnessCamera(uuid)
            if res_sharpness['success']:
                sharpness = res_sharpness['answer']
        except:
            logging.exception("/camera/ getSharpnessCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        try:
            res_contrast = c.getContrastCamera(uuid)
            if res_contrast['success']:
                contrast = res_contrast['answer']
        except:
            logging.exception("/camera/ getContrastCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        try:
            res_quality = c.getQualityCamera(uuid)
            if res_quality['success']:
                quality = res_quality['answer']
        except:
            logging.exception("/camera/ getQualityCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        try:
            res_gamma = c.getGammaCamera(uuid)
            if res_gamma['success']:
                gamma = res_gamma['answer']
        except:
            logging.exception("/camera/ getGammaCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        try:
            res_light_hz = c.getLightHZCamera(uuid)
            if res_light_hz['success']:
                light_hz = res_light_hz['answer']
        except:
            logging.exception("/camera/ getLightHZCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        try:
            res_night_mode = c.getNightModeCamera(uuid)
            if res_night_mode['success']:
                night_mode = res_night_mode['answer']
        except:
            logging.exception("/camera/ getNightModeCamera uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))

        try:
            res_illumination = c.getIlluminationMode(uuid)
            if res_illumination['success']:
                illumination = res_illumination['answer']
        except:
            logging.exception("/camera/ getIlluminationMode uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        
        try:
            res_low_light = c.getLowLight(uuid)
            if res_low_light['success']:
                low_light = res_low_light['answer']
        except:
            logging.exception("/camera/ getLowLight uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        
        try:
            res_low_light = c.getShortexposures(uuid)
            if res_low_light['success']:
                low_light = res_low_light['answer']
        except:
            logging.exception("/camera/ getShortexposures uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
                     
        try:
            res_scheduler = c.getParamsScheduler(uuid)
            if res_scheduler['success']:
                scheduler = res_scheduler['answer']
        except:
            logging.exception("/camera/ getParamsScheduler uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        
        try:
            res_cameramode = c.getModeScheduler(uuid)
            if res_cameramode['success']:
                cameramode = res_cameramode['answer']
        except:
            logging.exception("/camera/ getModeScheduler uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))
        
        producer_set = False
    
        curprofile = None
        camera_id = 0
        try:
            if camera:
                b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
                b.open()
                if b.connect: 
                    res = b.getCameraParameter(camera.uuid, "frame-minification")
                    if len(res) > 0 and res[0] != 'None': frame_minification = res[0]
                    else: 
                        res = b.getParameter("control.daemon.VA.frame-minification")
                        frame_minification = res
                b.close()
                del b
        except:
            logging.exception("/camera/ getFrameMinification uuid = %s, error: %s" %(str(uuid), str(sys.exc_info())))          

        if error == '': 
            source  = camera.ip
            type = camera.type
            ct = str(camera.type).lower()
            producer_set = ct.find("goal")==0 or ct.find("av")==0
            cam_obj = models.Camera.objects.get_or_create(ip = camera.ip, type = camera.type)
            camera_id = cam_obj[0].id   
        
        distorsion = get_camera_distortion(camera.uuid)
           
        profiles_list = ProfileModels.CamerasProfile.objects.all()
    
        data = dict()
        data.update(getDefaultParams(request, 'settings', project))

        data["kpp_list"] = models.Kpp.objects.all().order_by("id")
        data["all_active_cameras"] = all_active_cameras
        data["selected_camera"] = camera
        
        c.close()
        del c        
        
    else:
        error = 'camera'
        
    data.update({'version': VERSION, 'host': HTTP_HOST, 'select_page': 'settings',
                            'select_subpage': 'camera', 'communicator_errors_info': communicator_errors_info, 'camqnt': len(all_active_cameras), "producer_set":producer_set,
                            'resolution': resolution, 'capture_rect': capture_rect, 'brightness': brightness,
                            'saturation': saturation, 'sharpness': sharpness, 'contrast': contrast,
                            'quality': quality, 'gamma': gamma, 'light_hz': light_hz,
                            'night_mode': night_mode, 'illumination': illumination,
                            'low_light': low_light, 'short_exposures': short_exposures,
                            'distorsion': distorsion,'cameramode': cameramode, 'camera': camera,
                            'user' :  request.user.username, 'scheduler': scheduler,
                            'uuid' : uuid,
                            'error': error,
                            'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER},
                            'profiles_list':profiles_list, 'frame_minification': frame_minification})
    data.update(fps_answer)
    if request.GET.has_key('data'):
        response = render_to_response_ex(request, "datacamera.html", data)
    else:
        response = render_to_response_ex(request, "camera.html", data)
    
    return response
    
@tester
@permission_required('user_perms.perm_settings')
def distortion_settings(request, communicator, numcamera, cameramode):
    
    COMMUNICATORS = []
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
    
    error = ''
    camera = ''
    c = None
    server = ''
    port = ''
    cam_num = 0
    cam_id = 0
    try:
        server = COMMUNICATORS[int(communicator)]['host']
        port = COMMUNICATORS[int(communicator)]['port']
        c = Communicator(COMMUNICATORS[int(communicator)]['host'], COMMUNICATORS[int(communicator)]['port'])
        c.open()
        cameras = c.getCameras()
        for camera_ in cameras:
            if camera_["numcamera"] == numcamera:
                cam_id = cam_num
                camera = camera_
            try:
                cam = models.Camera.objects.get_or_create(ip = camera_['ip'], type = camera_['type'])
                camera["name"] = cam[0].name
            except:
                pass
            cam_num += 1
    except:
        error = 'communicator'
        del c

    #models.Camera.objects.get_or_create(ip = camera['ip'], type = camera['type'])
        
    if error == '':
        c.close()
        del c
    data = dict()    
    data.update(getDefaultParams(request, 'settings'))
    data.update({'version': VERSION, 'host': HTTP_HOST,  'select_page': 'settings',
                                'select_subpage': 'distortion', 'user': request.user.username, 
                                'server': server, 'port': port, 'error': error, 'communicator': communicator,
                                'numcamera': numcamera, 'cameramode': cameramode, 'camera': camera,
                                'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}})
    return render_to_response_ex(request, "distortion.html", data)

@tester
@permission_required('user_perms.perm_settings')
def settings_recognition(request):
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
    
    
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    dis_eye = None
    journalBoundCoeff = None
    try:
        dis_eye = b.getParameter('control.fd.preprocessing.min.face.side.pixels')
    except:
        dis_eye = 0
    try:
        journalBoundCoeff = b.getParameter('journalBoundCoeff')
    except:
        journalBoundCoeff = 0
    try:
        minBoundCoeffForLearn = b.getParameter('control.min.bound.coeff.for.learn','oxion')
    except:
        minBoundCoeffForLearn = 0
    try:
        maxBoundCoeffForLearn = b.getParameter('control.max.bound.coeff.for.learn','oxion')
    except:
        maxBoundCoeffForLearn = 0
    try:
        noiseLevel = b.getParameter("control.noise.level")
    except:
        noiseLevel = 0
    try:
        control_noise_deviation = b.getParameter("control.noise.deviation")
    except:
        control_noise_deviation = 0
    try:
        control_focus_factor = b.getParameter("control.focus.factor")
    except:
        control_focus_factor = 0
    
    try:
        control_check_face_for_identification = b.getParameter("control.check.face.for.identification")
    except:
        control_check_face_for_identification = None
    try:
        control_check_eyes_for_identification = b.getParameter("control.check.eyes.for.identification")
    except:
        control_check_eyes_for_identification = None
        
    try:
        control_check_face_for_learning = b.getParameter("control.check.face.for.learning", "oxion")
    except:
        control_check_face_for_learning = None
    try:
        control_check_eyes_for_learning = b.getParameter("control.check.eyes.for.learning", "oxion")
    except:
        control_check_eyes_for_learning = None
        
    try:
        control_fd_deep_level = b.getParameter("control.fd.deep.level")
    except:
        control_fd_deep_level = None
    try:
        control_fd_deep_level_heavy = b.getParameter("control.fd.deep.level.heavy")
    except:
        if control_fd_deep_level is not None:
            control_fd_deep_level_heavy = control_fd_deep_level
        else:
            control_fd_deep_level_heavy = None
    try:
        control_fd_deep_level_light = b.getParameter("control.fd.deep.level.light")
    except:
        if control_fd_deep_level is not None:
            control_fd_deep_level_light = control_fd_deep_level
        else:
            control_fd_deep_level_light = None
    
    try:
        control_fd_detect_type = b.getParameter("control.fd.detect.type")
    except:
        if control_fd_deep_level is not None:
            if control_fd_deep_level == '20110520':
                control_fd_detect_type = 'light'
            else:
                control_fd_detect_type = 'heavy'
        else:
            control_fd_detect_type = None
    
    try:
        control_mirror_eyes_identification = b.getParameter("control.fr.with.mirroring")
    except:
        control_mirror_eyes_identification = None   
    
    try:
        clusterTypeValue = b.getParameter("control.fr.answer.type")
    except:
        clusterTypeValue = None
        
    try:
        preprocessing_min_image_to_face_side_ratio = b.getParameter("control.fd.preprocessing.min.image.to.face.side.ratio")
    except:
        preprocessing_min_image_to_face_side_ratio = 1  
        
    try:
        preprocessing_max_image_to_face_side_ratio = b.getParameter("control.fd.preprocessing.max.image.to.face.side.ratio")
    except:
        preprocessing_max_image_to_face_side_ratio = "14.4"
        
          
        
    try:
        minEyesDistance = b.getParameter("minEyesDistance")
    except:
        minEyesDistance = 0    
    b.close()
    del b
    
    data = dict()    
    data.update(getDefaultParams(request, 'settings'))
    data.update({'version': VERSION, 'host': HTTP_HOST,  'select_page': 'settings',
                                'select_subpage': 'recognition', 'user': request.user.username,
                                'dis_eye': dis_eye, 'journalBoundCoeff': journalBoundCoeff, 'noiseLevel': noiseLevel, 'minEyesDistance': minEyesDistance,
                                'minBoundCoeffForLearn': minBoundCoeffForLearn, 'maxBoundCoeffForLearn': maxBoundCoeffForLearn,
                                'control_focus_factor': control_focus_factor, 'control_noise_deviation': control_noise_deviation,
                                'control_check_face_for_identification': control_check_face_for_identification,
                                'control_mirror_eyes_identification': control_mirror_eyes_identification,
                                'control_check_eyes_for_identification': control_check_eyes_for_identification,
                                'control_check_face_for_learning': control_check_face_for_learning,
                                'control_check_eyes_for_learning': control_check_eyes_for_learning,
                                'control_fd_deep_level': control_fd_deep_level,
                                'control_fd_detect_type': control_fd_detect_type,
                                'control_fd_deep_level_heavy': control_fd_deep_level_heavy,
                                'clusterTypeValue': clusterTypeValue,
                                'control_fd_deep_level_light': control_fd_deep_level_light,
                                'preprocessing_min_image_to_face_side_ratio': preprocessing_min_image_to_face_side_ratio,
                                'preprocessing_max_image_to_face_side_ratio': preprocessing_max_image_to_face_side_ratio })
    
    return render_to_response_ex(request, "settings_recognition.html", data)

@tester
def getIdentData(request):
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
    
    data = {'version': VERSION, 'host': HTTP_HOST,  'select_page': 'ident', 'user': request.user.username, 'server': SERVERC, 'port': PORTC,
            'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}}
    
    res = get_value_defaultparams("res_interface")
    
    if res == "0":
        if COMMUNICATORS and len(COMMUNICATORS)>1:
            data['limit_cameras'] = 5
        else:
            data['limit_cameras'] = 7
    elif res == "1":
        if COMMUNICATORS and len(COMMUNICATORS)>1:
            data['limit_cameras'] = 8
        else:
            data['limit_cameras'] = 10
    else:
        if COMMUNICATORS and len(COMMUNICATORS)>1:
            data['limit_cameras'] = 3
        else:
            data['limit_cameras'] = 5
    return data


def get_svg_draw_params(uuid):
    #получаем размеры изображения, чтобы создать svg холст нужного размера
    width = MAX_JS_VIDEO_SCREEN
    height = 480
    try:
        cameras = CommunicatorModels.Camera.objects.filter(uuid=uuid, active=True)
        if cameras:
            data_file = get_camera_last_frame(cameras[0])
            if data_file:
                im = StringIO(data_file)
                back_img = Image.open(im)
                fWidth, fHeight = back_img.size
                im.close()
                sWidth, sHeight = fWidth, fHeight
                
                # маштабирование с сохранением пропрорций 
                width = MAX_JS_VIDEO_SCREEN
                if sWidth > width: sHeight = max(sHeight * width / sWidth, 1); sWidth = width
            
                width, height = sWidth, sHeight 
    except:
        logging.exception(sys.exc_info())
    
    margin = int((MAX_JS_VIDEO_SCREEN - width) / 2)
    return width, height, margin
    
@tester
@permission_required('user_perms.perm_view')
def ident(request, uuid=None):
    
    data = dict()
    
    data.update(getDefaultParams(request, 'ident_js'))
        
    res_get_all_active_cameras = getAllActiveCameras(url_reverse_name='js_ident')

    all_active_cameras = res_get_all_active_cameras["all_active_cameras"]
    data["communicator_errors_info"] = res_get_all_active_cameras["communicator_errors_info"]

    if not uuid:
        if 'uuid' in request.COOKIES:
            uuid = request.COOKIES['uuid']
        else:
            #get first active uuid in system
            try:
                uuid = all_active_cameras[0].uuid
            except:
                uuid = None

    camera = None
    if uuid:
        try:
            camera = models.Camera.objects.filter(uuid=uuid)[0]
        except:
            camera = None
        if camera is not None:
            c = Communicator()
            res_cam_mode = c.getModeScheduler(camera.uuid)
            if res_cam_mode["success"]:
                setattr(camera, "mode", res_cam_mode["answer"])
            else:
                setattr(camera, "mode", 0)
    videoclips = []
    try:
        videoclips = models.Roller.objects.exclude(tm_stop=None)
    except:
        logging.info("ident: get videoclips failed: " + str(sys.exc_info()))

    data["videoclips"] = videoclips.count()
    
    urls_arr = {}
    try:
        for l in models.List.objects.exclude(group=SELF_LEARNING):
            if get_object_or_404(models.Types, pk=l.type_id).division.id == division_person:
                urls_arr[l.group_id] = '/anketaperson/'
            if get_object_or_404(models.Types, pk=l.type_id).division.id == division_employee:
                urls_arr[l.group_id] = '/anketastaff/'
            if get_object_or_404(models.Types, pk=l.type_id).division.id == division_visitor:
                urls_arr[l.group_id] = '/anketavisitor/'
    except:
        pass
    data['urls_arr'] = urls_arr

    data.update(getDefaultParams(request, 'ident_js'))
    data["all_active_cameras"] = all_active_cameras
    data["selected_camera"] = camera

    data["js_video_refresh_limit"] = 50
    data["boundFactor"] = get_value_defaultparams(journalBoundCoeff)
    data["page_refresh_time"] = 1000 * 60 * 20
    data["clearCarouselAfter"] = 70
    data["ident_page"] = True
    data["show_detect_alerts"] = int(get_value_defaultparams('show_detect_alerts'))
    data["add_to_carousel_fire_delay"] = int(get_value_defaultparams('add_to_carousel_fire_delay'))
    data["add_to_carousel_flash_delay"] = int(get_value_defaultparams('add_to_carousel_flash_delay'))
    data["add_to_carousel_smoke_delay"] = int(get_value_defaultparams('add_to_carousel_smoke_delay'))
    data["add_to_carousel_leftthings_delay"] = int(get_value_defaultparams('add_to_carousel_leftthings_delay'))
    data["draw_frame_fire_delay"] = int(get_value_defaultparams('draw_frame_fire_delay'))
    data["draw_frame_smoke_delay"] = int(get_value_defaultparams('draw_frame_smoke_delay'))
    data["draw_frame_flash_delay"] = int(get_value_defaultparams('draw_frame_flash_delay'))
    data["draw_frame_face_delay"] = int(get_value_defaultparams('draw_frame_face_delay'))
    data["draw_frame_leftthings_delay"] = int(get_value_defaultparams('draw_frame_leftthings_delay'))
    
    last_idents = []
    if camera:
        try:
            from django.db.models import Max
            last_ids = models.Journal.objects.filter(coeff__gte=float(data["boundFactor"]), camera=camera.pk).exclude(person=None).values('person_id').annotate(id_max=Max('id'))
            ids = []
            for l in last_ids:
                ids.append(l["id_max"])

            last_idents = models.Journal.objects.filter(id__in=ids).order_by('-id')[:5]
        except:
            last_idents = []
        
        for i in last_idents:
            try:
                name = "%s %s %s" % (i.person.person.first_name, i.person.person.last_name, i.person.person.middle_name)
                setattr(i, "person_name", name)
                setattr(i, "found_url", i.finded.url)
            except:
                setattr(i, "person_name", _("Отсутствует..."))
            
            try:
                if datetime.datetime.now().year != i.dt_last_fixed.year or datetime.datetime.now().month != i.dt_last_fixed.month or datetime.datetime.now().day != i.dt_last_fixed.day:
                    setattr(i, "detect_date", i.dt_last_fixed.strftime('%d.%m.%Y'))
                else:
                    setattr(i, "detect_date", "")
            except:
                setattr(i, "detect_date", "")
            setattr(i, "is_free", False)

    new_last_idents = []
    for i in last_idents:
        new_last_idents.append(i)
    while len(new_last_idents)<5:
        new_last_idents.append({"is_free": True})
    data["last_idents"] = new_last_idents

    last_journal_id = 0
    try:
        last_journal_id = models.Journal.objects.filter(camera=camera.pk).order_by('-id')[:1]
        if len(last_journal_id) > 0:
            last_journal_id = last_journal_id[0].pk
        else:
            last_journal_id = models.Journal.objects.all().order_by('-id')[:1]
            if len(last_journal_id) > 0:
                last_journal_id = last_journal_id[0].pk
            else:
                last_journal_id = 0
    except:
        logging.exception(str(sys.exc_info()))
        last_journal_id = 0

    data["last_journal_id"] = int(last_journal_id)
        
    if len(data["last_idents"]) < 1:
        data["last_idents"] = None
    
    try:
        if DetectorLog.objects.count() > 0:
            last_row = DetectorLog.objects.all().order_by('-id')[:1]
            data["last_detect_message_id"] = int(last_row[0].id)
        else:
            data["last_detect_message_id"] = 0
    except:
        data["last_detect_message_id"] = None
    
    last_ident_message_id = last_journal_id
    try:
        last_ident_message_journal = models.Journal.objects.all().order_by('-id')[:1]
        if last_ident_message_journal:
            last_ident_message_id = last_ident_message_journal[0].agregate.id
    except:
        last_ident_message_id = last_journal_id
    data["last_ident_message_id"] = int(last_ident_message_id)
    
    #get svg draw size and margin
    try:
        data["width"], data["height"], data["svg_margin"] = get_svg_draw_params(uuid)
    except:
        data["width"] = MAX_JS_VIDEO_SCREEN
        data["height"] = 480
        data["svg_margin"] = 0
    
    response = render_to_response_ex(request, "ident_js.html", data)
    if uuid:
        response.set_cookie("uuid", uuid)
    return response

@tester
@login_required
def big_video_frame_info(request):
    import ast
    data = dict()
    data["info_big_camera"] = True
    
    c = Communicator()
    #get resolution
    resolution = None
    try:
        res_t_data = c.getResolutionCamera(request.REQUEST["uuid"])
        if res_t_data["success"]:
            if res_t_data.has_key('fps'):
                resolution = '%sx%sx%s' % (res_t_data["width"], res_t_data["height"], res_t_data["fps"])
            else:
                resolution = '%sx%s' % (res_t_data["width"], res_t_data["height"])
    except:
        logging.info("big_video_frame_info: c.getResolutionCamera failed: " + str(sys.exc_info()))
    
    captureRect = None
    try:
        res_t_data = c.getCaptureRectCamera(request.REQUEST["uuid"])
        if res_t_data["success"]:
            captureRect = '%sx%s, x=%s, y=%s' % (res_t_data["answer"]["width"], res_t_data["answer"]["height"], res_t_data["answer"]["x"], res_t_data["answer"]["y"])
    except:
        logging.info("big_video_frame_info: c.getCaptureRectCamera failed: " + str(sys.exc_info()))
    
    c.close()
    del c

    data["resolution"] = resolution
    data["captureRect"] = captureRect
    html = mark_safe(render_to_string("ident_js_forms.html", data))

    result = {'res': 'success', 'html': html}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@login_required
def get_ident_person_info(request):
    try:
        balIds = request.REQUEST["balIds"].split(',')
        persons = []
        for balId in balIds:
            p = getPersonByBalId(int(balId))
            group = ''
            id = ''
            if p:
                group = int(p.group.pk)
                id = int(p.pk)
            persons.append({'balId': int(balId), 'name': getNamePersonByBalId(int(balId)), 'group': group, 'person_id': id})
        
        result = { 'res': 'success', 'persons': persons }
    except:
        result = { 'res': 'error' }

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def circleWithColor(draw, point, color, radius=4):
    draw.ellipse((point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius), outline = color)
    draw.ellipse((point[0] - radius+1, point[1] - radius + 1, point[0] + radius - 1, point[1] + radius - 1), outline = color)

def get_object_thumbnail(request, back_img, x1, y1, x2, y2, max_obj_width = 72, max_obj_height = 72):  
    objWidth = 0
    objHeight = 0
    
    back_img = back_img.convert("RGB")
    try:
        object_frame = back_img.copy()
        object_frame = object_frame.crop((x1, y1, x2, y2))
        objWidth, objHeight = object_frame.size
        
        if objWidth > objHeight:
            newHeight = (((max_obj_width * 100) / objWidth) * objHeight) / 100
            object_frame.thumbnail((max_obj_width, newHeight), Image.ANTIALIAS)
        else:
            newWidth = (((max_obj_height * 100) / objHeight) * objWidth) / 100
            object_frame.thumbnail((newWidth, max_obj_height), Image.ANTIALIAS)
        
        objWidth, objHeight = object_frame.size
        
        if objHeight < max_obj_height:
            margin_top = int((max_obj_height - objHeight) / 2)
        else:
            margin_top = 0
        
        output = StringIO()
        object_frame.save(output, format="JPEG", quality=100)
        obj_content = output.getvalue()
        output.close()
    except:
        obj_content = ''

    return obj_content, margin_top
            
def analyzing_data(request, frame, data_type, chain_mode, back_img, factor):
    #get objects data
    objects_data = []
    if frame[data_type]:
        
        bitmap = frame[data_type]["bitmap_list"]
        b_w = frame[data_type]["b_width"]
        b_h = frame[data_type]["b_height"]

        checkmap = []
        
        for line in bitmap:
            checkline = []
            for x in line:
                checkline.append(0)
            checkmap.append(checkline)
        
        y_val = 0
        fill_q = Queue.Queue()
        
        for line in checkmap:
            for x_val in range(0, len(line)-1):
                if checkmap[y_val][x_val] == 0 and bitmap[y_val][x_val] == 1:
                    checkmap[y_val][x_val] = 1
                    fill_q.put([y_val, x_val])
                    
                    #смотрим соседей
                    cur_object = []
                    
                    l_x = None
                    l_y = None
                    r_x = None
                    r_y = None
                    
                    while not fill_q.empty():
                        t_val = fill_q.get()
                        t_x = t_val[1]
                        t_y = t_val[0]
                        
                        #считаем координаты рамки объекта
                        #инициализация
                        if not l_x:
                            l_x = t_x
                            
                        if not l_y:
                            l_y = t_y
                            
                        if not r_x:
                            r_x = t_x
                            
                        if not r_y:
                            r_y = t_y
                            
                        #проверка
                        if t_x < l_x:
                            l_x = t_x
                            
                        if t_y < l_y:
                            l_y = t_y
                        
                        if t_x > r_x:
                            r_x = t_x
                        
                        if t_y > r_y:
                            r_y = t_y
                        
                        
                        cur_object.append([t_y, t_x])
                        
                        #4 chain mode
                        if not t_y == 0:
                            if checkmap[t_y-1][t_x] == 0 and bitmap[t_y-1][t_x] == 1:
                                fill_q.put([t_y-1, t_x])
                                checkmap[t_y-1][t_x] = 1
                        
                        if not t_y == len(checkmap) - 1:
                            if checkmap[t_y+1][t_x] == 0 and bitmap[t_y+1][t_x] == 1:
                                fill_q.put([t_y+1, t_x])
                                checkmap[t_y+1][t_x] = 1
                        
                        if not t_x == 0:
                            if checkmap[t_y][t_x-1] == 0 and bitmap[t_y][t_x-1] == 1:
                                fill_q.put([t_y, t_x-1])
                                checkmap[t_y][t_x-1] = 1
                        
                        if not t_x == len(line) - 1:
                            if checkmap[t_y][t_x+1] == 0 and bitmap[t_y][t_x+1] == 1:
                                fill_q.put([t_y, t_x+1])
                                checkmap[t_y][t_x+1] = 1
                                
                        if chain_mode:
                            if not t_y == 0 and not t_x == 0:
                                if checkmap[t_y-1][t_x-1] == 0 and bitmap[t_y-1][t_x-1] == 1:
                                    fill_q.put([t_y-1, t_x-1])
                                    checkmap[t_y-1][t_x-1] = 1
                                
                                if not t_y == 0 and not t_x == len(line) - 1:
                                    if checkmap[t_y-1][t_x+1] == 0 and bitmap[t_y-1][t_x+1] == 1:
                                        fill_q.put([t_y-1, t_x+1])
                                        checkmap[t_y-1][t_x+1] = 1
                                
                                if not t_y == len(checkmap) - 1 and not t_x == len(line) - 1:
                                    if checkmap[t_y+1][t_x+1] == 0 and bitmap[t_y+1][t_x+1] == 1:
                                        fill_q.put([t_y+1, t_x+1])
                                        checkmap[t_y+1][t_x+1] = 1
                                
                                if not t_y == len(checkmap) - 1 and not t_x == 0:
                                    if checkmap[t_y+1][t_x-1] == 0 and bitmap[t_y+1][t_x-1] == 1:
                                        fill_q.put([t_y+1, t_x-1])
                                        checkmap[t_y+1][t_x-1] = 1
                    
                    #if data_type == 'fire_obj_data':
                    #    raise Exception("ke")
                    
                    #TODO: make a thumbnail    
                    #objWidth = 0
                    #objHeight = 0
                    #try:
                    #    object_frame = back_img.copy()
                    #    object_frame = object_frame.crop((int(l_x * b_w), int(l_y * b_h), int((r_x * b_w) + b_w), int((r_y * b_h) + b_h)))
                    #    objWidth, objHeight = object_frame.size
                        
                    #    max_obj_width = 72
                    #    max_obj_height = 72
                        
                    #    if objWidth > objHeight:
                    #        newHeight = (((max_obj_width * 100) / objWidth) * objHeight) / 100
                    #        object_frame.thumbnail((max_obj_width, newHeight), Image.ANTIALIAS)
                    #    else:
                    #        newWidth = (((max_obj_height * 100) / objHeight) * objWidth) / 100
                    #        object_frame.thumbnail((newWidth, max_obj_height), Image.ANTIALIAS)
                        
                    #    objWidth, objHeight = object_frame.size
                        
                    #    if objHeight < max_obj_height:
                    #        margin_top = int((max_obj_height - objHeight) / 2)
                    #    else:
                    #        margin_top = 0
                        
                    #    output = StringIO()
                    #    object_frame.save(output, format="JPEG")
                    #    obj_content = output.getvalue()
                    #    output.close()
                    #except:
                    #    obj_content = ''
                    
                    # убрать т.к сейчас используется отображение детектов из журнала
                    #obj_content, margin_top = get_object_thumbnail(request, back_img, int(l_x * b_w),  int(l_y * b_h), int((r_x * b_w) + b_w), int((r_y * b_h) + b_h))  
                    

                    objects_data.append({"crds": cur_object, "l_x": l_x * b_w * factor, "l_y": l_y * b_h * factor, "r_x": ((r_x * b_w) + b_w) * factor, "r_y": ((r_y * b_h) + b_h) * factor, "b_w": b_w, "b_h": b_h, "factor": factor, 'image': '', 'margin_top': '', 'detectTime': getTimeInHMS(), 'frame_color': '', 'need_to_show': 1, 'data_type': data_type})

            y_val += 1
            
        #raise Exception(sep_obj_data)
    return objects_data

def get_extended_detect_area(fWidth, fHeight, left, right, top, bottom, factor=20):
    attach_length = int((factor * fWidth) / 100)          
    left_side = left - attach_length
    if left_side < 0:
        left_side = 0
    
    right_side = right + attach_length
    if right_side > fWidth:
        right_side = fWidth
    
    top_side = top - attach_length
    if top_side < 0:
        top_side = 0
    
    bot_side = bottom + attach_length
    if bot_side > fHeight:
        bot_side = fHeight

    return [left_side, right_side, top_side, bot_side]
    
@tester
@login_required    
def get_ident_video_frame(request):
    frame_content = ''
    error_remark = ""
    try:
        uuid = request.REQUEST.get("uuid", None)
        camera = is_active_camera(uuid)
        if camera:        
            data_file = get_camera_last_frame(camera)
            if data_file:
                im = StringIO(data_file)
                frame = Image.open(im)
                fWidth, fHeight = frame.size
                width = MAX_JS_VIDEO_SCREEN
                im.close()
          
                height = (((width * 100) / fWidth) * fHeight) /100
                frame.thumbnail((width, 1000), Image.ANTIALIAS)
                          
                output = StringIO()
                frame.save(output, format="JPEG", quality=100)
                frame_content = output.getvalue()
                output.close()
            else:
                error_remark = "can't get video frame"                
        else:
            error_remark = "camera isn't active"

        result = { 'res': 'success', 'image': base64.b64encode(frame_content), 'error_remark': error_remark}
    except:
        logging.exception("get video frame communicator error:" + str(sys.exc_info()))
        result = { 'res': 'error' }

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def is_active_camera(uuid=None):
    try:
       if not uuid: return False
       c = Communicator()
       cameras = c.getCameras(filter_active=True)
       camera = CommunicatorModels.Camera.objects.filter(uuid=uuid, active=True)
       if camera: return camera[0]
    except:
        logging.exception()
    return False    

@tester
@login_required
def get_ident_video_frame_detects_free(request):
    try:
        error_remark = ""
        uuid = request.REQUEST.get("uuid", None)
        if not is_active_camera(uuid):
            error_remark = "camera isn't active"
        
        result = { 'res': 'success', 'error_remark': error_remark}
    except:
        logging.exception("get video frame communicator error:" + str(sys.exc_info()))
        result = { 'res': 'error' }

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def get_camera_last_frame(camera):
    import urllib
    import StringIO
    
    face_content = None
    url = "http://%(com_host)s:%(com_port)s/image?uuid=%(uuid)s" % ({"com_host": camera.commun.host, "com_port": camera.commun.mjpeg_port, "uuid": camera.uuid})
    f = urllib.urlopen(url)
    data_file = f.read()
    f.close()
    if data_file in ("correct frame is not received", "incorrect [ipcamera]-parameter value"):
        return face_content
    return data_file

def get_camera_image(camera, width=72, height=54):

    data_file = get_camera_last_frame(camera)
    if not data_file: return data_file
    
    face_content = ""
    k1 = width/height
    try:
        buff = StringIO(data_file)
        img = Image.open(buff)
        widthf, heightf = img.size
        k2 = widthf/heightf
        if k1 >= k2:
            height = height/k2
        else:
            width = width*k2
        img.thumbnail((width, height), Image.ANTIALIAS)
        buff.close()
        buff = StringIO()
        img.save(buff, format="JPEG")
        face_content = buff.getvalue()
        buff.close()
    except:
        logging.exception("get_camera_image: "+str(sys.exc_info()))                   
    return face_content

@tester
@login_required
def get_all_video_frames(request):
    import ast
    sys_cameras = ast.literal_eval(request.REQUEST["sys_cameras"])
    width = request.REQUEST.get("width", None)
    if width and not str(width).isdigit():
        width = None
    else: 
        width = int(width)
    height = request.REQUEST.get("height", None)
    if height and not str(height).isdigit():
        height = None
    else: 
        height = int(height)  
    
    import base64
    
    frames_result = []
    
    for x in range(0, len(sys_cameras)):
        uuid = sys_cameras[x].get("uuid", '')
        result = {'res': 'error'}
        error_remark = ''
        try:
            if uuid:
                camera = CommunicatorModels.Camera.objects.filter(uuid=uuid, active=True)
                if camera:
                    frame_content = get_camera_image(camera[0], width, height)
                    if frame_content:
                        result = {'res': 'success', 'image': base64.b64encode(frame_content), 'error_remark': error_remark}
        except:
            logging.exception("get video frame communicator error:" + str(sys.exc_info()))
        
        frames_result.append({'uuid': uuid, 'result': result})

    return HttpResponse(simplejson.dumps(frames_result), mimetype='application/json')

def unescape(s):
    try:
        import htmllib
        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(s)
        return p.save_end()
    except: return s

def escape_char(val):
    try:
        import cgi
        return cgi.escape(val)
    except: return val  

@tester
@login_required
def executeCommunicatorMethod(request):
    import ast
    params = ast.literal_eval(request.REQUEST["params"])
    
    host = None
    port = None
    mjpeg_port = None
    if len(request.REQUEST["host"]) > 1:
        host = request.REQUEST["host"]
    if len(request.REQUEST["port"]) > 1:
        port = request.REQUEST["port"]
    if len(request.REQUEST["mjpeg_port"]) > 1:
        mjpeg_port = request.REQUEST["mjpeg_port"]

    if params.get("url", None):
        params["url"] = unescape(params["url"])
        params["url"] = escape_char(params["url"])
    
    c = Communicator()
    try:
        answer = c.executeCommand(request.REQUEST["methodName"], params, request.REQUEST["answer_type"], host=host, port=port, mjpeg_port=mjpeg_port)
        if not answer["error_remark"]:
            result = {'result': 'success', 'answer': answer["result"]}
        else:
            logging.info("c.executeCommand failed remark: %s" % answer["error_remark"])
            result = {'result': 'error', 'error': answer["error_remark"]}
    except:
        logging.info("executeCommunicatorMethod failed "+str(sys.exc_info()))
        result = {'result': 'error'}

    c.close()
    del c

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@login_required
def get_extended_video_info(request):
    balancers = None
    data = dict()
    videocards = []
    
    try:
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        balancers = b.getSystemInfo()
        b.close()
        del b
    except:
        logging.info("get_extended_video_info: b.getSystemInfo failed: " + str(sys.exc_info()))
    
    if balancers and balancers.has_key("balancer"):
        for balancer in balancers["balancer"]:
            if balancer.has_key("daemons"):
                for daemons in balancer["daemons"]:
                    if not isinstance(daemons, dict):
                        continue
                    for daemon in daemons["daemon"]:
                        if daemon.has_key("address") and daemon.has_key("name") and daemon.has_key("temperature") and daemon.has_key("port"):
                            if not "CPU" in daemon["name"]:
                                videocards.append({'address': daemon["address"], 'name': daemon["name"], 'temperature': int(daemon["temperature"]), 'port': int(daemon["port"]) })
    
        data["videocard_info"] = True
        data["videocards"] = videocards
    
        html = mark_safe(render_to_string("ident_js_forms.html", data))
        result = { 'res': 'success', 'html': html }
    else:
        result = {'res': 'error'}
    
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')
 
#@tester
def change_language(request):
    from django.utils import translation
    from videoclient.models import *
    

    language = translation.get_language()
    
    if request.POST.has_key('lang'):
        pLang = request.POST['lang']
        pLang = pLang.lower()
        if Language.objects.all().filter(name = pLang).count>0:
            language = pLang
    else:    
        langs = Language.objects.all()
        i = 0
        while i<len(langs) and langs[i].name != language: 
            i=i+1
        while i<len(langs) and langs[i].name == language: 
            i=i+1
        if i<len(langs):
            language = langs[i].name
        else:
            language = langs[0].name
#    if Language.objects.all().filter(name != language).count>0:
#        lang = Language.objects.get(name != language)
#        language = lang.name
    response = HttpResponse(language.swapcase())
    LANGUAGE_CODE = language
    response.set_cookie("django_language", language)
    return response
    
@tester
@login_required    
def help(request):
    
    distr_version = None
    try:
        from videoclient import settings
        f = open(settings.VERSION_FILE, 'r+b')
        distr_version = f.read()
        f.close()
    except:
        logging.exception(str(sys.exc_info())) 
    data = {'version': VERSION, 'host': HTTP_HOST,  'select_page': 'help', 'user': request.user.username, 'distr_version': distr_version,}
    data.update(getDefaultParams(request, 'help', ""))
    data["admin"] = check_rule(request)
    response = render_to_response_ex(request, "help.html", data)    
    return  response

def getShortFileName(session_key):
    return MEDIA_ROOT + 'tmp/%s/pre/' %session_key

def getFileName(session_key, fname, uni = False):
    filename = ''
    
    if not uni:
        filename = getShortFileName(session_key) + '%s/%s' %( fname, fname )
    else:
        filename = getShortFileName(session_key) + '%s/%s' %(fname, fname)
        path = os.path.dirname(filename)
        count = 1
        while os.path.exists(path):
            filename = getShortFileName(session_key) + '%s%s/%s' %(count, fname, fname)
            path = os.path.dirname(filename)
            count = count+1
        os.makedirs(path)
    return filename
    
def delete_images(parent_images):
    for image in parent_images:
        if image is None:
            continue    
        delete_images(models.TmpImage.objects.filter(parent=image))
        image.delete()
        
class TestFromLogPerson(forms.Form):
    person = forms.CharField(required=False)
    #personname = forms.IntegerField(required=True)
    coeff = forms.FloatField(required=True)
    cameraIp = forms.CharField(required=True, max_length=16)
    cameraType = forms.CharField(required=True)
    time = forms.IntegerField(required=True) 
    #dt_fixed = forms.DateTimeField(required=True)
    original = forms.ImageField(required=False)
    finded = forms.ImageField(required=False)
    originalFace = forms.CharField(required=False)
    foundFace = forms.CharField(required=False)
    
def thumbnail(filename, size):#<-????? wtf
    return True 
    logging.info("logperson thumbnail filename: %s" %filename)
    #fimg = open(filename, "r+b")
    iimg = Image.open(filename)
    width, height = iimg.size
    if width > size[0] or height > size[1]:
        iimg.thumbnail(size)
    iimg.save(filename)

OSIZE = (240, 240)
FSIZE = (120, 120)
timecalculate_starttime = time.time()
timecalculate_dataTime = []
timecalculate_index = 0

def timecalculate(myindex = timecalculate_index):
    import time
    global timecalculate_starttime, timecalculate_dataTime, timecalculate_index
    dTime = time.time() - timecalculate_starttime
    if len(timecalculate_dataTime) > myindex:
        timecalculate_dataTime[myindex]['time']+=dTime
    else:
        timecalculate_dataTime.append({'index': myindex, 'time': dTime})
    logging.info("%s: %s" %(myindex, dTime))
    timecalculate_index+=1
    timecalculate_starttime = time.time()
    

def getDataSavedPhoto(type, filename, detect, url_prefix):
    answer = dict()
    other_data = dict()
    import settings
    if ('%sFaceImage' %type) in detect and detect["%sFaceImage"%type] and detect["%sFaceImage"%type] != 'null':
        url = ''
        
        db_path =  models.getModelFileNameByFileName(os.path.join('/%s' %type, filename))
        url = os.path.join(settings.MEDIA_URL, db_path)
        
        
        full_path = os.path.join(settings.MEDIA_ROOT, db_path)
        dir_name = os.path.dirname(full_path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        while os.path.isfile(full_path):
            full_path = "%s_%s" %(full_path[:-4], full_path[-4:])
            db_path = "%s_%s" %(db_path[:-4], db_path[-4:])
            #logging.info("change_path_name" + str(full_path))
        f = open(full_path, 'w+b')
        import base64
        f.write(base64.b64decode(detect["%sFaceImage"%type]))
        f.close()
        
        answer["%sUrl" %(type)] = url_prefix+url
        other_data[type] = db_path
    else:
        other_data[type] = ''
    return {'answer': answer, 'other_data': other_data}


def check_field(name, detect):
    if name in detect and detect[name] is not None and str(detect[name]) != '' and str(detect[name]) != 'null':
        return True
    else:
        return False

def logperson_package(request):
    """Функция для пакетного добавления записей в журнал"""
    answer = dict()
    answer["status"] = False
    
    try:
# Получение запроса из файла необходимо в целях отладки
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
            #logging.info(query_str)
    except:
        logging.exception(str(sys.exc_info()))
        from videoclient import monitoring
        monitoring.warning(type='exception', description=_("Ошибка получения запроса на добавление идентификаций от управляющей системы"), show=False)
        answer["exception"] = str(sys.exc_info())
        return JsonResponse(answer)
    
    try:
# обработка запроса

        import json
        import time
        import datetime
        query = json.loads(query_str)

# проверки полей
         
        if not check_field('detects', query):
            answer["error"] = "detects not found"
            return JsonResponse(answer)
        detects = query['detects']
        
        if check_field('size', query) and query['size'] != len(detects):
            answer["error"] = "size not equal len of detects"
            return JsonResponse(answer)
        
        if len(detects) == 0:
            answer["error"] = "size of detects is zero"
            return JsonResponse(answer)

# загрузка настроек
        
        from videoclient import utils
        default_coeff = float(utils.get_value_defaultparams(journalBoundCoeff))
        default_add_not_ident_person = int(utils.get_value_defaultparams(add_not_ident_person))
        default_delay_for_create_new_group = int(utils.get_value_defaultparams(delay_for_create_new_group))
        default_show_ident_window = int(utils.get_value_defaultparams(show_ident_window))
        default_show_ident_window_recogn_only = int(utils.get_value_defaultparams(show_ident_window_recogn_only))
                   
# инициализация переменных
        
        answer["detects"] = []
        # список полей используемых при insert
        names = ["person_id",
                 "person_not_found_id",
                 "camera_id",
                 "coeff",
                 "bound_coeff",
                 "original",
                 "found",
                 "agregate_id",
                 "dt_first_fixed",
                 "dt_last_fixed",
                 "t_first_fixed",
                 "t_last_fixed",
                 "photos_count",
                 "original_face",
                 "found_face",
                 "dt_open",
                 "info",
                 "show_info"]
        # список вставляемых записей
        items = []

# получение списка идентификаторов персон
        
        # Список идентификаторов персон
        all_person_id = []
        # Множество идентификаторов персон
        all_person_id_set = dict()
        
        # Минимальное и максимальное время.
        minAlertTime = None
        maxAlertTime = None
        
        
        for detect in detects:
            if check_field('personName', detect) and str(detect["personName"]).isdigit() and str(detect["personName"]) not in all_person_id_set:
                try:
                    person_id = str(detect["personName"])
                    all_person_id.append(person_id)
                    all_person_id_set[person_id] = True
                except:
                    logging.exception(str(sys.exc_info()))
            if check_field('alertTime', detect):
                alertTimeTmp = float(detect["alertTime"])/1000
                if maxAlertTime is None or alertTimeTmp>maxAlertTime:
                    maxAlertTime = alertTimeTmp 
                if minAlertTime is None or alertTimeTmp<minAlertTime:
                    minAlertTime = alertTimeTmp
        
        if minAlertTime is None:
            minAlertTime = time.time()
        if maxAlertTime is None:
            maxAlertTime = minAlertTime
            
        minAlertTime = datetime.datetime.fromtimestamp(minAlertTime)
        minAlertDayToday = datetime.datetime(year = minAlertTime.year, month = minAlertTime.month, day = minAlertTime.day)
        
        minAlertTimeSubDelay = minAlertTime - datetime.timedelta(seconds=default_delay_for_create_new_group)
        
        if minAlertTimeSubDelay < minAlertDayToday:
            minAlertTimeSubDelay = minAlertDayToday
        
        minAlertTimeSubDelay_str = minAlertTimeSubDelay.strftime('%Y-%m-%d %H:%M:%S')

        
        maxAlertTime = datetime.datetime.fromtimestamp(maxAlertTime)
        maxAlertTime_str = maxAlertTime.strftime('%Y-%m-%d %H:%M:%S')
                
        
# инициализация базы данных    

        from django.db import connection
        cursor = connection.cursor()
        
# получение данных о детектах
        lastident_fields_full = ['id']
        lastident_fields = ['person_id', 'camera_id', 'time', 'agregate_id']
        lastident_fields_full.extend(lastident_fields)
                
        # Список соответствий: идентификатор персоны - время последней идентификации
        all_ident_persons = dict()
        
        if len(all_person_id)>0:
            sql = "delete from videoclient_lastident where time < '%s';" % minAlertTimeSubDelay_str
            cursor.execute(sql)
            sql = "select %s from videoclient_lastident where person_id in (%s);" % (', '.join(lastident_fields_full), ', '.join(all_person_id))
            cursor.execute(sql)
            resault_lastident = cursor.fetchall()
            for row in resault_lastident:
                i = 0
                item=dict()
                while i < len(lastident_fields_full):
                    item[lastident_fields_full[i]] = row[i] 
                    i+=1
                if int(item['person_id']) not in all_ident_persons:
                    all_ident_persons[int(item['person_id'])] = dict()
                all_ident_persons[int(item['person_id'])][int(item['camera_id'])] = item
        
# Инициализация списков учавствующий ... TODO дописать комментарий
        update_last_ident = []
        update_last_ident_set = dict() # множество 
        create_last_ident = [] # список создаваемых записей last_ident
        
        all_cameras = dict()
        all_persons = dict()
        
# получение последнего идентификатора журнала
        try:
            sql = "select last_value, is_called from videoclient_journal_id_seq;";
            cursor.execute(sql)
            rows = cursor.fetchall()
            agregate_id = rows[0][0] if rows[0][1] else 0
        except:
            agregate_id = 0
            
        lastident_id = 0            
            
# обработка детектов
        
        for detect in detects:
            answer_detect = dict()
            answer_detect["status"] = False
            other_data = dict()
            try:
                # обработка времени.
                if check_field('index', detect):
                    answer_detect['index'] = detect['index']
                if check_field('alertTime', detect):
                    alertTime = float(detect["alertTime"])/1000
                else:
                    alertTime = time.time()
                
                alertTime = datetime.datetime.fromtimestamp(alertTime)
                alertDateTime_str = alertTime.strftime('%Y-%m-%d %H:%M:%S')
                alertTime_str = alertTime.strftime('%H:%M:%S')
                
                other_data['dt_open'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                other_data['dt_first_fixed'] = alertDateTime_str
                other_data['dt_last_fixed'] = alertDateTime_str
                
                other_data['t_first_fixed'] = alertTime_str
                other_data['t_last_fixed'] = alertTime_str
                
                if check_field('info', detect):
                    import json
                    other_data['info'] = json.dumps(detect['info'])
                else:
                    other_data['info'] = '{}'
                
                # TODO  надо перевести на UUID
                # По аналогии проверка на наличие UUID
                # И изменить множество созданных камер
                # И изменить создание камеры с UUID
                
                if not check_field('cameraIp', detect):
                    answer_detect["error"] = "cameraIp is not found"
                    answer["detects"].append(answer_detect)
                    continue
                
                if not check_field('cameraType', detect):
                    answer_detect["error"] = "cameraType is not found"
                    answer["detects"].append(answer_detect)
                    continue
                
                if not check_field('cameraUuid', detect):
                    answer_detect["error"] = "cameraUuid is not found"
                    answer["detects"].append(answer_detect)
                    continue
                
                cameraIp = detect["cameraIp"]
                cameraType = detect["cameraType"]
                cameraUUID = detect["cameraUuid"]
                
                if cameraUUID in all_cameras:
                    camera = all_cameras[cameraUUID]
                else:
                    camera, create = models.Camera.objects.get_or_create(uuid=cameraUUID)
                    if create:
                        cam = camera
                        cam.ip = cameraIp
                        cam.type = cameraType
                        cam.save()

                    if cameraUUID not in all_cameras:
                        all_cameras[cameraUUID] = dict()
                    all_cameras[cameraUUID] = camera
                    
                other_data['camera_id'] = camera.id
                
                
                # Конец переделки по UUID
                
                personId = None
                person_not_found_id = None
                personCoeff = 0
                
                if check_field("personCoeff", detect):
                    personCoeff = float(detect["personCoeff"])
                    
                if check_field("personName", detect) and str(detect["personName"]).isdigit():
                    if personCoeff >= default_coeff:
                        """Выполняем поиск персоны для идентифицированной записи"""
                        try:
                            if int(detect["personName"]) in all_persons:
                                person = all_persons[int(detect["personName"])]
                            else:
                                persons = models.PersonId.objects.filter(id=int(detect["personName"]))
                                if persons.count()>0:
                                    person = persons[0]
                                else:
                                    person = None
                            if person:
                                personId = int(detect["personName"])
                                answer_detect["fio"] = person.get_fio()
                                all_persons[int(detect["personName"])] = person
                        except:
                            logging.exception(str(sys.exc_info()))
                            personId = None
                    else:
                        """Выполняем поиск персоны для не идентифицированной записи"""
                        try:
                            if int(detect["personName"]) in all_persons:
                                person = all_persons[int(detect["personName"])]
                            else:
                                persons = models.PersonId.objects.filter(id=int(detect["personName"]))
                                if persons.count()>0:
                                    person = persons[0]
                                else:
                                    person = None
                            if person:
                                person_not_found_id = int(detect["personName"])
                                all_persons[int(detect["personName"])] = person
                        except:
                            logging.exception(str(sys.exc_info()))
                            person_not_found_id = None
                            
                                                    
                if not default_add_not_ident_person and not personId:
                    answer_detect["status"] = True
                    answer_detect["addNew"] = False
                    answer["detects"].append(answer_detect)
                    continue
                
                if not default_show_ident_window or (default_show_ident_window_recogn_only and not personId):
                    other_data['show_info'] = 1
                    
                other_data["photos_count"] = 1
                other_data["coeff"] = personCoeff * 100
                other_data["bound_coeff"] = default_coeff * 100
                other_data["person_id"] = personId if personId is not None else "NULL";
                if person_not_found_id is not None:
                    other_data["person_not_found_id"] = person_not_found_id
                else:
                    other_data["person_not_found_id"] = "NULL";
                
                url_prefix = "http://%s" % request.get_host()
                filename = get_journal_path(gen_filename())
                
                temp_data = getDataSavedPhoto('original', filename, detect, url_prefix)
                answer_detect.update(temp_data["answer"])
                other_data.update(temp_data["other_data"])
                
                #Определяем есть ли смысл сохранять найденную картинку или нет
                if personId is not None or person_not_found_id is not None:
                    temp_data = getDataSavedPhoto('found', filename, detect, url_prefix)
                    answer_detect.update(temp_data["answer"])
                    other_data.update(temp_data["other_data"])
                else:
                    other_data['found'] = other_data['original']
                
                
                answer_detect["personId"] = personId
                
                agregate_id+=1
                
                if personId and personId in all_ident_persons and camera.id in all_ident_persons[personId] and all_ident_persons[personId][camera.id]["agregate_id"]:
                    current_ident = all_ident_persons[personId][camera.id]
                    
                    ident_person_date_time = current_ident['time'].replace(tzinfo=None)
                    ident_person_date = datetime.date(year = ident_person_date_time.year, month = ident_person_date_time.month, day = ident_person_date_time.day)
                    alertDate = datetime.date(year = alertTime.year, month = alertTime.month, day = alertTime.day)
                    
                    a_id = str(current_ident["agregate_id"])
                
                    if personId not in all_ident_persons:
                        all_ident_persons[personId] = dict() 
                    all_ident_persons[personId][camera.id]["agregate_id"] = a_id
                    all_ident_persons[personId][camera.id]['time'] = alertTime
                        

                    other_data['agregate_id'] = a_id
                    #last_ident_item['agregate_id'] = a_id
                    if current_ident['id'] not in update_last_ident_set:
                        update_last_ident.append(str(current_ident['id']))
                        update_last_ident_set[current_ident['id']] = True                        
                elif personId:
                    lastident_id-=1
                    other_data['agregate_id'] = agregate_id
                    if personId not in all_ident_persons: all_ident_persons[personId] = dict()
                    if camera.id not in all_ident_persons[personId]: all_ident_persons[personId][camera.id] = dict()
                    
                    all_ident_persons[personId][camera.id]['id'] = lastident_id
                    all_ident_persons[personId][camera.id]['person_id'] = personId
                    all_ident_persons[personId][camera.id]['camera_id'] = camera.id
                    all_ident_persons[personId][camera.id]['agregate_id'] = agregate_id
                    all_ident_persons[personId][camera.id]['time'] = maxAlertTime
                    
                    update_last_ident_set[lastident_id] = True
                    
                    create_last_ident.append("(%s, %s, '%s', %s)" %(personId, camera.id, alertDateTime_str, agregate_id))
                else:
                    other_data['agregate_id'] = agregate_id
                    
                    
                
                if check_field('originalFace', detect):
                    other_data['original_face'] = detect["originalFace"]
                else:
                    other_data['original_face'] = 'NULL'
                    
                if check_field('foundFace', detect):
                    other_data['found_face'] = detect["foundFace"]
                else:
                    other_data['found_face'] = 'NULL' 
                
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
            sql = 'insert into videoclient_journal (%s) values %s' %(', '.join(names), ', '.join(items))
            cursor.execute(sql)
            
        # создание записи о времени последних идентификаций
        if len(create_last_ident)>0: 
            sql = 'insert into videoclient_lastident (%s) values %s' %(', '.join(lastident_fields), ', '.join(create_last_ident))
            cursor.execute(sql)
            
        # обновление времени последних идентификаций без созданием новой группы
        if len(update_last_ident)>0:
            sql = "update videoclient_lastident set time = '%s' where id in (%s)" %(maxAlertTime_str, ', '.join(update_last_ident))
            cursor.execute(sql)
         
        transaction.commit_unless_managed()
        
        answer["status"] = True
    except:
        logging.exception(str(sys.exc_info()))
        saveError(query_str, description=_("Запрос от управляющей системы на добавление идентификаций в журнал не был обработан. "), save_last_error=False, show=True)
        answer["exception"] = str(sys.exc_info())
        if 'detects' in answer:
            for detect in answer["detects"]:
                detect["addNew"] = False
    return JsonResponse(answer)
               
@tester
@login_required               
def checkjournal(request):
    data = dict()
    data["status"] = False
    try:
        journals = models.Journal.objects.filter(show_info=None).order_by("id")
        journals = journals.extra(where=['videoclient_journal.id = videoclient_journal.agregate_id'])
        journals = journals[:1]
        if journals.count()>0:
            j = journals[0]
            if j.person != None and j.coeff>=int(float(get_value_defaultparams(journalBoundCoeff))*100):                       
                models.Journal.objects.filter(id=j.id).update(show_info=1)                      
                data = employee(request, j.id)
            else:                        
                tr = get_value_defaultparams(reaction_time)
                wup = get_value_defaultparams(wait_unidentified_person)
                #if (j.dt_continue and j.dt_continue<=j.dt_last_fixed) or (j.dt_continue ==None and j.dt_last_fixed+datetime.timedelta(seconds=int(tr))>=datetime.datetime.now() and j.dt_first_fixed + datetime.timedelta(seconds=int(wup)) <= j.dt_last_fixed):
                if j.dt_first_fixed + datetime.timedelta(seconds=int(wup)) <= datetime.datetime.now():                            
                    models.Journal.objects.filter(id=j.id).update(show_info=1) 
                    data = employee(request, j.id)
        else:
            request.session[wait_unidentified_person] = False                                         
    except:
        logging.exception("checkjournal: "+str(sys.exc_info()))
        data["status"] = False
    return JsonResponse(data)
    
    
def sizes(journal):
    data = dict()
    #fimg = open(filename, "r+b")
    OSIZE = (240, 240)
    FSIZE = (240, 240)
    try:
        width, heigth = FSIZE
        if journal.finded:
            logging.info('sizes: %s' % (MEDIA_ROOT+str(journal.finded)))
            fimg = Image.open(MEDIA_ROOT+str(journal.finded))
            wh = fimg.size
            if wh:
                width, height = wh
                if width > FSIZE[0]:
                    height = (height*FSIZE[0])/width
                    width = FSIZE[0]
                if height > FSIZE[1]:
                    width = (width*FSIZE[1])/height
                    height = FSIZE[1]          
        logging.info('sizes: %s' % (MEDIA_ROOT+str(journal.original)))
        
        data['finded']= dict()
        data['finded']['width'] = width
        data['finded']['height'] = height
    except:
        data['finded']= dict()
        data['finded']['width'] = FSIZE[0]
        data['finded']['height'] = FSIZE[1]
        logging.exception("sizes finded"+str(sys.exc_info()))
        
    try:
        width, heigth = OSIZE
        oimg = Image.open(MEDIA_ROOT+str(journal.original))
        width, height = oimg.size
        if width > OSIZE[0]:
            height = (height*OSIZE[0])/width
            width = OSIZE[0]
        if height > OSIZE[1]:
            width = (width*OSIZE[1])/height
            height = OSIZE[1]
        data['original']= dict()
        data['original']['width'] = width
        data['original']['height'] = height
    except:
        data['original']= dict()
        data['original']['width'] = OSIZE[0]
        data['original']['height'] = OSIZE[1]
        logging.exception("sizes original"+str(sys.exc_info()))
    logging.info(data)
    return data     

@tester
@login_required
def employee(request, journalid=0):    
    
    data = getDefaultParams(request, 'journal')
    data.update(dataJournal(request, journalid))
    data.update(dataAccess(request, journalid))
    data.update(getDataDivision(request))
    data["csm"] = int(float(get_value_defaultparams(journalBoundCoeff))*100)
    from videoclient import settings
    from videoclient.models import Event
    
    data['sizes'] = sizes(data['journal'])
        
    event = None
    if data["journal"].person is not None:
        event = Event.objects.get(name_id="on_ident", profile=None)
    else:
        event = Event.objects.get(name_id="on_no_ident", profile=None)
        
    if (event) and (event.active) and (event.sound is not None):
        data['event'] = event.sound.sound.url
    
    if str(get_value_defaultparams(name=show_ident_window_recogn_only)) == "1" and not data["journal"].person:
        return {"status" : False}
    if str(get_value_defaultparams(name="show_ident_window")) == "0":
        return {"status" : False}

    template = loader.get_template('employee.html')  
    c = Context(data)
    content = template.render(c)
    return {"status" : True, "content": str(content)}

@tester
@permission_required('user_perms.perm_logs')
def showjournalphoto(request, journalid=None):    
    
    try:
        if journalid is not None:
            journals = models.Journal.objects.filter(id=int(journalid))
#            subquery = "videoclient_journal_agregate_view"
#            condition = "videoclient_journal.agregate_id = videoclient_journal_agregate_view.agregate_id"
#            journals = journals.extra(tables=[subquery], where=[condition])
#            journals = journals.extra(select={'dt_first_fixed_min': "videoclient_journal_agregate_view.dt_first_fixed_min", 
#                                              'dt_last_fixed_max': "videoclient_journal_agregate_view.dt_last_fixed_max",
#                                              'count_records': "count_records"})
            journal = journals[0] # Не безопастное обращение, желательна предварительная проверка.
            data = dict()
            data['sizes'] = sizes(journal)
            data['journal'] = journal
            journals = models.Journal.objects.filter(agregate = journal.agregate).order_by('id') # Сортировка, ранние детекты впереди
            
            param_aggregator = models.ParamAggregator.getRecord()
            
            journals = journals.filter(id__gt=param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_FIRST_ID))
            journals = journals.filter(id__lte=param_aggregator.getParam(models.ParamAggregator.PARAM_JOURNAL_LAST_ID))
            data['journals'] = journals 
            
            data.update(getDataDivision(request))
            
            if 'small' in request.REQUEST:
                return render_to_response_ex(request, "showjournalphoto_photo.html", data)
            else:
                return render_to_response_ex(request, "showjournalphoto.html", data)
    except:
        logging.exception(str(sys.exc_info()))
        
    sinfo = '<div style="text-align: center;"><img src="/files/%s" width="%s" height="%s" alt="" /></div>';        
    return HttpResponse(sinfo % ("images/no_photo120x120.gif", 120, 120))

@tester
@permission_required('user_perms.perm_lists')
def delete_person(request):
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    
    persons = request.POST['persons'].split(',')
    photos = None
    if request.POST.has_key('photos'):
        photos = request.POST['photos'].split(',')
    
    try:
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        for person in persons:
            personId = getPersonIdByBalId(person)
            person_dir = os.path.join(LEARNING_IMAGES, '%s/' %personId.id)
            if photos is None or len(photos) == 0:
                import shutil 
                shutil.rmtree(person_dir)
                b.deleting(person)
            else:
                for photo in photos:
                    if photo.isdigit():
                        photo_path = os.path.join(person_dir, '%04d.jpg' %int(photo))
                        if os.path.isfile(photo_path): os.unlink(photo_path)  #Удаление фотографии
                    b.deleting(person, photo)
        b.close()
        del b
    except:
        logging.exception(str(sys.exc_info()))
        return HttpResponse('False')
    
    return HttpResponse('True')

@tester
@permission_required('user_perms.perm_lists')
def rename_person(request):
    if request.POST.has_key('oldName') and request.POST.has_key('newName'):
        oldName = request.POST['oldName']
        newName = request.POST['newName']
        answer = renamePerson(oldName, newName)
        return HttpResponse(answer)
    return HttpResponse('False')

@tester
@permission_required('user_perms.perm_logs')
def journal(request, project=None):
    from videoclient.utils import check_rule, dataNavigation, dataGet
    from videoclient.utils import get_value_defaultparams
    import commands
    
    if not check_rule(request, True, is_moderator=True):
        if request.GET.has_key('data'):
            return HttpResponse("reload")
        else:
            return HttpResponseRedirect("/")
    data = getDefaultParams(request, 'journal', project)
    data.update( {"csm": float(get_value_defaultparams(journalBoundCoeff))*100})
    
    if request.GET.has_key('makezip'):
        data.update(dataJournal(request, makezip=True))
        data = export_journalphotos(request, data['users'])
        return JsonResponse(data)
    
    data.update(dataJournal(request))

    data.update(getDataDivision(request))
    #data.update(dataNavigation(request, data['all_users']))
    #data["users"] = data["users"][data['start']-1:data['finish']-1]
    data.update(dataGet(request, ignore_list=["data", "amp", "page", "all_pages", "sorto", "up"]))
    if space:
        s = commands.getoutput(space)
        s = s.replace("\n", "")
        m = re.match(r".*G *([0-9]+)%.*", s)
        if m and m.group(1):
            data["space"] = 100-int(m.group(1))
    
    urls_arr = {}
    try:
        for l in models.List.objects.exclude(group=SELF_LEARNING):
            if get_object_or_404(models.Types, pk=l.type_id).division.id == division_person:
                urls_arr[l.group_id] = '/anketaperson/'
            if get_object_or_404(models.Types, pk=l.type_id).division.id == division_employee:
                urls_arr[l.group_id] = '/anketastaff/'
            if get_object_or_404(models.Types, pk=l.type_id).division.id == division_visitor:
                urls_arr[l.group_id] = '/anketavisitor/'
    except:
        pass
    data['urls_arr'] = urls_arr
    
    data['version_journal'] = ''
    if request.COOKIES.has_key("version_journal") and request.COOKIES["version_journal"] == "simple": 
        data['version_journal'] = 'simple'
    
    if request.GET.has_key('data') and not request.GET.has_key('countrows'):
        if data['version_journal'] == 'simple':
            return render_to_response_ex(request, "data_simple_journal.html", data)
        else:
            return render_to_response_ex(request, "data_journal.html", data)
    elif request.GET.has_key('countrows'):
        return JsonResponse({'countrows': data['all_users'],'all_countrows': data['all_countrows']})
    else:
        return render_to_response_ex(request, "journal_simple.html", data)

@tester
@permission_required('user_perms.perm_logs')
def get_journal_photo(request, journal_id=None, ptype='original'):
    journal = get_object_or_404(models.Journal, id=journal_id)
    if ptype in ['original', 'original_draw_face'] :    
        filename = WWW_ROOT + 'files/%s' % journal.original
    else:
        filename = WWW_ROOT + 'files/%s' % journal.finded
    f = open(filename, 'r+b')
    wrapper = f.read()
    f.close()
    
    if ptype == 'original_draw_face':
        koef = float(1)
        '''
        try:
            file = FileWrapper(wrapper)
            img = Image.open(file.File)
            fWidth, fHeight = img.size
            img.thumbnail((width, height), Image.ANTIALIAS)
            sWidth, sHeight = img.size
            koef = float(sWidth)/float(fWidth) if float(sWidth)/float(fWidth) < float(sHeight)/float(fHeight) else float(sHeight)/float(fHeight) 
            fileno, path = tempfile.mkstemp()
            img.convert("RGB").save(path, "PNG")
            f = open(path, 'r+b')
            wrapper = f.read()
            f.close()    
        except:
            logging.exception("resize: "+str(sys.exc_info()))
        '''
        try:
            file = FileWrapper(wrapper)
            img = Image.open(file.File)
            img = img.convert("RGB")
            
            draw = ImageDraw.Draw(img) # Create a draw object
            face = journal.found_face.split(',')
            try:

                x1 = float(face[9])*koef
                y1 = float(face[10])*koef
                x2 = float(face[12])*koef
                y2 = float(face[13])*koef
                
                circle(draw, (x1,y1))
                circle(draw, (x2,y2))
            except:
                logging.exception("put eyes:"+str(sys.exc_info()))
                
            try:                
                x1 = float(face[18])*koef
                y1 = float(face[19])*koef
                
                circle(draw, (x1,y1))
            except:
                logging.exception("put eyes:"+str(sys.exc_info()))
                
            try:                
                x1 = float(face[15])*koef
                y1 = float(face[16])*koef
                
                circle(draw, (x1,y1))
            except:
                logging.exception("put eyes:"+str(sys.exc_info()))
                
            try:
                icon = Image.open(ICON_REC)
                size_icon= icon.size
                x1 = float(face[0])*koef
                y1 = float(face[1])*koef
                x2 = float(face[2])*koef
                y2 = float(face[3])*koef
                x3 = float(face[4])*koef
                y3 = float(face[5])*koef
                x4 = float(face[6])*koef
                y4 = float(face[7])*koef
                
                lines(draw, (x1, y1), (x2, y2))
                lines(draw, (x2, y2), (x3, y3))
                lines(draw, (x3, y3), (x4, y4))
                lines(draw, (x4, y4), (x1, y1))
            except:
                logging.exception("put eyes:"+str(sys.exc_info()))
            
            fileno, path = tempfile.mkstemp()
            logging.info("convert")
            img.convert("RGB").save(path, "PNG", quality = 60, optimize=1)
            f = open(path, 'r+b')
            wrapper = f.read()
            f.close()
        except:
            logging.exception(str(sys.exc_info()))

    
    response = HttpResponse(wrapper, content_type='image/jpeg')
    response['Content-Length'] = len(wrapper)
    response['Content-Disposition'] = 'attachment;filename=%s.jpg' % journal_id
    return response
    
def month_ago(date=None, c=1):
    if date:
        d = False
        day = date.day
        logging.info(day)
        while not d:
            try: 
                d = datetime.date(date.year-(0 if date.month-c>0 else 1), date.month-c if date.month-c>0 else 12+date.month-c, day)
            except:
                logging.info(sys.exc_info()) 
                d = False
            day -= 1
            logging.info(day)
        #_d = date - datetime.timedelta(weeks=4*c)
        #return datetime.date(_d.year, _d.month, date.day)
        return d 
    return None

def UnlinkFileDir(d):
    try:
        if os.path.exists(d): os.unlink(d)
        for i in range(4):
            d = os.path.dirname(d)
            os.rmdir(d)
        return True
    except:
        return False  
    

from videoclient import status_thread

class ClearThread(status_thread.StatusThread):
   
    def __init__(self, dt):
        self.dt = dt
        status_thread.StatusThread.__init__(self)
    
    def run(self):
        try:
            import time
            time.sleep(1)
            if self.dt == 'all':
                query = 'cd %s;python ./manage.py clear_journal --all --id=%s' % (PROJECT_ROOT+'project/videoclient/', str(self.getThreadId()))
            else:
                query = 'cd %s;python ./manage.py clear_journal --date=%s --id=%s' % (PROJECT_ROOT+'project/videoclient/', str(self.dt), str(self.getThreadId()))
            pid = os.spawnvp(os.P_NOWAIT, 'sh', ['sh',  '-c', query])
            logging.info("query ClearThread: "+ query) 
        except:
            logging.error("ClearThread.run: " + str(sys.exc_info()))
            return        
        
@tester
@permission_required('user_perms.perm_logs')
@permission_required('user_perms.perm_logs_clear')
def clearjournal(request):
    data = dict()
    data["status"] = False
    try:  
        from forms import TestClearDataJournal
        form = TestClearDataJournal(request.REQUEST, request.FILES)
        if form.is_valid():          
            if "period" in form.cleaned_data and form.cleaned_data["period"] in (0,1,2,3,4):
                dt = None
                if form.cleaned_data["period"]==0: dt = datetime.datetime.now()-datetime.timedelta(days=7)
                elif form.cleaned_data["period"]==1: dt = month_ago(datetime.datetime.now(), 1)
                elif form.cleaned_data["period"]==2: dt = month_ago(datetime.datetime.now(), 3)
                elif form.cleaned_data["period"]==3 and "dataClear" in form.cleaned_data: dt = form.cleaned_data["dataClear"]
                elif form.cleaned_data["period"]==4: dt = 'all' 
                if dt:
                    try:
                        thread = ClearThread(dt)
                        data["thread_id"] = thread.getThreadId()
                        thread.start()
                    except:
                        data["exception"] = str(sys.exc_info())
                        data["message"] = _("Ошибка создания потока для импорта песон")
                        logging.exception("")
                    data["status"] = True
        else:
            data["message"] = _("Ошибка обработки входных данных")    
    except:
        data["exception"] = str(sys.exc_info())
        data["message"] = _("Ошибка обработки входных данных")
        logging.exception("")
    return JsonResponse(data)

def exportPath(person = None, photo = None):
    from videoclient.settings import EXPORT_PATH
    base = EXPORT_PATH
    if person:
        if photo:
            return "%s%s.png" %(base, photo)
        else: 
            return "%s" %(base)
    else:
        return base

@tester
@permission_required('user_perms.perm_lists')
def export(request):
        
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    
    persons = request.REQUEST['persons'].split(',')
    photos = None
    if request.POST.has_key('photos'):
        photos = request.REQUEST['photos'].split(',')
    urltarname = 'True'
    try:
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        for person in persons:
            if photos == None:
                pass
                #b.deleting(person)
            else:
                
                path = os.path.dirname(exportPath(person))
                if not os.path.exists(path):
                    os.makedirs(path)

                urltarname = "/exportfile/?person="+person
                
                if USE_ZIP_FILE:
                    import zipfile
                    zf = zipfile.ZipFile(exportPath(person)+person+".zip", 
                         mode='w',
                         compression=zipfile.ZIP_DEFLATED, 
                         )
                else:
                    import tarfile
                    tarname = exportPath(person)+person+".tar.bz2"; 
                    tar = tarfile.open(tarname, "w:bz2")
                    
                for photo in photos:
                    image = b.getPersonPhoto(person, photo)[0]
                    filename_base = photo + '_base.png'
                    base_image = LEARNING_IMAGES + '%s/%04d.jpg'  % (getPersonIdByBalId(person).id, int(photo))
                    if os.path.isfile(base_image):
                        f = open(base_image, 'r+b')
                        wrapper = f.read()
                        f.close()

                    if USE_ZIP_FILE:
                        zf.writestr(photo+'.png', image)
                        if os.path.isfile(base_image):
                            zf.writestr(filename_base, wrapper)
                    else:
                        filename = exportPath(person, photo)
                        img = open(filename, "w+b")
                        img.write(image)
                        img.close()
                        tar.add(filename, photo+'.png')
                        if os.path.isfile(base_image):
                            img = open(filename, "w+b")
                            img.write(wrapper)
                            img.close()
                            tar.add(filename, filename_base)
                if USE_ZIP_FILE:
                    zf.close()
                else:
                    tar.close()
                    try:
                        for photo in photos:
                            filename = exportPath(person, photo)
                            os.unlink(filename)
                    except:
                        logging.exception("export:"+str(sys.exc_info()))
        b.close()
        del b
    except:
        logging.exception("export:"+str(sys.exc_info()))
        return HttpResponse('False')
    
    return HttpResponse(urltarname)

def FetchOneAssoc(cursor) :
    data = cursor.fetchone()
    if data == None :
        return None
    desc = cursor.description

    dict = {}

    for (name, value) in zip(desc, data) :
        if isinstance(value, datetime.datetime) or isinstance(value, datetime.date) or isinstance(value, datetime.time):
            value = str(value)
        dict[name[0]] = value

    return dict

def save_journal_data(zf, id_nodes, filters=None):
    """
    Запись данных журнала в zip-архив
    """
    NODES_ON_PAGE = 15#количество записей на страницах во внутренних отчётах
    AGR_NODES_ON_PAGE = 30#количество записей на страницах в корне архива
    MAX_FILE_IN_DIR = 32000#максимальное количество файлов в каталоге
    try:
        cur_col_file_in_dir = 0
        add_report = get_value_defaultparams("add_report_export_journal")#необходимость добавления отчёта
        nodes = models.Journal.objects.filter(id__in = id_nodes)
        
        #данные для страниц в корне архива
        if add_report == '1':
            no_photo_path = MEDIA_ROOT+'images/no_photo120x120.gif'
            f = open(no_photo_path, 'r+b')
            no_photo = f.read()        
            f.close()
            if id_nodes:
                zf.writestr("HTML/no_photo120x120.gif", str(no_photo))
            agr_length_j = len(nodes)
            agr_length_photo_j = len(models.Journal.objects.filter(agregate__in = id_nodes))
            agr_length_ident_j = len(nodes.exclude(person=None))
            agr_pages = int(agr_length_j / AGR_NODES_ON_PAGE)
            if (agr_length_j % AGR_NODES_ON_PAGE) > 0:
                agr_pages += 1
            agr_data = []
            if nodes:
                content = '<script type="text/javascript">function init() {window.location.href = "HTML/pages/0/0.html"}window.onload = init;</script>'
                zf.writestr("index.html", str(content))
        id_dir = 0
        nodes_count = 0
        for node in nodes:
            nodes_count += 1
            cur_col_file_in_dir +=1
            if cur_col_file_in_dir > MAX_FILE_IN_DIR:
                id_dir += 1
                cur_col_file_in_dir = 1
            data_j = []
            
            agr_min_coeff = 100
            agr_max_coeff = 0
            agr_time_first_fixed = datetime.time(23,59,59,999)
            agr_time_last_fixed = datetime.time(0,0,0,0)
            agr_curr_page = int(nodes_count/AGR_NODES_ON_PAGE)     
            if (nodes_count % AGR_NODES_ON_PAGE) == 0:
                agr_curr_page -= 1

            journals = models.Journal.objects.filter(agregate = node.agregate)
            generator = queryset_iterator(journals)
            for j in generator:
                id_person = ''
                if j.person:
                    id_person = str(j.person.id)

                #сохраняем фото
                ext = "jpeg"
                
                if j.original and not j.original == '':
                    ext = str(j.original).split('.')[-1]
                    filepath_o = MEDIA_ROOT + str(j.original)
                    if os.path.isfile(filepath_o):
                        f = open(filepath_o, 'r+b')
                        wrapper = f.read()
                        f.close() 
                        zf.writestr('photo/original/%s/agregate%s/id%s_%s_%s_%s_original.%s' % (id_dir, j.agregate.id, j.pk, j.dt_first_fixed.strftime('%d%m%Y'), j.dt_first_fixed.strftime('%H%M%S'), id_person, ext), wrapper)
                if j.person is not None or j.person_not_found is not None:
                    if j.finded and not j.finded == '':
                        ext = str(j.finded).split('.')[-1]
                        filepath_f = MEDIA_ROOT + str(j.finded)
                        if os.path.isfile(filepath_f):
                            f = open(filepath_f, 'r+b')
                            wrapper = f.read()
                            f.close()
                            zf.writestr('photo/found/%s/agregate%s/id%s_%s_%s_%s_found.%s' % (id_dir,j.agregate.id,  j.pk, j.dt_first_fixed.strftime('%d%m%Y'), j.dt_first_fixed.strftime('%H%M%S'), id_person, ext), wrapper)
 
                #сохраняем json-данные
                if j.found_face and not j.found_face == '':
                    res = dict()
                    res['correlation_coefficient'] = j.coeff
                    res['boundary_coefficient'] = j.bound_coeff
                    res['face'] = getFoundFaceInJournal(j.found_face)
                    if j.person:
                        res['person_id'] = j.person.id
                    elif j.person_not_found:
                        res['person_id'] = j.person_not_found.id
                    zf.writestr('JSON/%s/agregate%s/id%s_%s_%s_%s_data.json' % (id_dir,j.agregate.id, j.pk, j.dt_first_fixed.strftime('%d%m%Y'), j.dt_first_fixed.strftime('%H%M%S'), id_person), json.dumps(res, sort_keys=False, indent=4))
                
                #собираем данные для html-отчёта    
                if add_report == '1':                
                    d = dict()
                    d["id"] = j.id
                    d["dt_first_fixed"] = j.dt_first_fixed
                    d["dt_last_fixed"] = j.dt_last_fixed
                    d["corr_coeff"] = j.coeff
                                        
                    if agr_time_last_fixed < j.t_last_fixed:
                        agr_time_last_fixed = j.t_last_fixed
                    if agr_time_first_fixed > j.t_first_fixed:
                        agr_time_first_fixed = j.t_first_fixed
                        
                    if agr_max_coeff < j.coeff:
                        agr_max_coeff = j.coeff
                    if agr_min_coeff > j.coeff:
                        agr_min_coeff = j.coeff
                    #d["percent"] = get_percent_corr_coeff(j.coeff)
                    if j.original and not j.original == '':
                        ext = str(j.original).split('.')[-1]
                        d["original"] = '../../../../photo/original/%s/agregate%s/id%s_%s_%s_%s_original.%s' % (id_dir, j.agregate.id, j.pk, j.dt_first_fixed.strftime('%d%m%Y'), j.dt_first_fixed.strftime('%H%M%S'), id_person, ext)
                    if j.person and j.finded and not j.finded == '':
                        ext = str(j.finded).split('.')[-1]
                        d["found"] = '../../../../photo/found/%s/agregate%s/id%s_%s_%s_%s_found.%s' % (id_dir, j.agregate.id, j.pk, j.dt_first_fixed.strftime('%d%m%Y'), j.dt_first_fixed.strftime('%H%M%S'), id_person, ext)
                    data_j.append(d) 
            
            #создаём html-отчёт 
            if add_report == '1':  
                #создаём отчёты для отдельных записей в журнале              
                try:    
                    pages = int(len(data_j) / NODES_ON_PAGE)
                    if (len(data_j) % NODES_ON_PAGE) > 0:
                        pages += 1
                    data=dict()
                    data["url_to_agr_list"] = '../../../pages/%s/%s.html' % (int(agr_curr_page/MAX_FILE_IN_DIR), str(agr_curr_page))
                    
                    if node.person:
                        data["person"] = node.person.person
                    data["id"] = node.id
                    data["col_photo"] = len(data_j)
                    
                    for p in range(pages):
                        f_begin = (p * NODES_ON_PAGE)
                        f_end = (NODES_ON_PAGE * p) + NODES_ON_PAGE
                        if p == pages:
                            data["journals"] = data_j[f_begin:len(data_j)]
                        else:
                            data["journals"] = data_j[f_begin:f_end]
                        #pagination
                        data["content"] = False
                        data["pages"] = True
                        data["pagination"] = ''
                        if pages > 1:
                            for i in range(pages):
                                data["page"] = i
                                data["sel_page"] = p
                                data["p_name"] = i + 1
                                data["pagination"] += u'%s' % render_to_string("journal_export.html", data)
                        data["pages"] = False
                        data["pagination"] = mark_safe(data["pagination"])
                        #html
                        data["content"] = True
                        data['version']=VERSION
                        try:
                            zf.writestr('HTML/agregates/%s/agregate%s/%s.html' % (id_dir,j.agregate.id, p), render_to_string("journal_export.html", data).encode('UTF-8'))
                        except:
                            error = True
                            logging.exception('add file to archive error: ' + str(sys.exc_info()))
                except:
                    logging.exception('export error: ' + str(sys.exc_info()))
                #создаём отчёт для основных записей
                agr_journal = {'data': node,
                               'url_page': '../../agregates/%s/agregate%s/%s.html' % (id_dir,node.agregate.id, '0'),
                               'min_coeff': agr_min_coeff,
                               'max_coeff': agr_max_coeff,
                               #коэффициент для казанского вокзала
                               #'min_percent': get_percent_corr_coeff(agr_min_coeff),
                               #'max_percent': get_percent_corr_coeff(agr_max_coeff),
                               'time_first_fixed': agr_time_first_fixed,
                               'time_last_fixed': agr_time_last_fixed,
                               'col_photo': len(data_j)
                               }
                if node.original and not node.original == '':
                    ext = str(node.original).split('.')[-1]
                    agr_journal["original"] = '../../../photo/original/%s/agregate%s/id%s_%s_%s_%s_original.%s' % (id_dir, node.agregate.id, node.pk, node.dt_first_fixed.strftime('%d%m%Y'), node.dt_first_fixed.strftime('%H%M%S'), id_person, ext)
                if j.finded and not j.finded == '':
                    ext = str(j.finded).split('.')[-1]
                    agr_journal["found"] = '../../../photo/found/%s/agregate%s/id%s_%s_%s_%s_found.%s' % (id_dir, node.agregate.id, node.pk, node.dt_first_fixed.strftime('%d%m%Y'), node.dt_first_fixed.strftime('%H%M%S'), id_person, ext)
            
                agr_data.append(agr_journal)
                if (nodes_count % AGR_NODES_ON_PAGE) == 0 or (nodes_count == agr_length_j):
                    data = dict()
                    data["journals"] = agr_data
                    data["all_journals"] = agr_length_j
                    data["all_ident_journals"] = agr_length_ident_j
                    data["all_photo_journals"] = agr_length_photo_j
                    data["filters"] = filters
                    data["content"] = False
                    data["pages"] = True
                    data["pagination"] = ''       
                    if agr_pages > 1:
                        for i in range(agr_pages):
                            data["page"] = i
                            data["dir_page"] = int(i / MAX_FILE_IN_DIR)
                            data["sel_page"] = agr_curr_page 
                            data["p_name"] = i + 1
                            data["pagination"] += u'%s' % render_to_string("journal_export_main.html", data)
                    data["pagination"] = mark_safe(data["pagination"])
                    data["pages"] = False
                    data["content"] = True
                    data['version'] = VERSION
                    try:
                        zf.writestr('HTML/pages/%s/%s.html' % (int(agr_curr_page / MAX_FILE_IN_DIR), str(agr_curr_page)), render_to_string("journal_export_main.html", data).encode('UTF-8'))
                    except:
                        error = True
                        logging.exception('add file to archive error: ' + str(sys.exc_info()))
                    agr_data = []
    except:
        logging.exception("")

@tester
@permission_required('user_perms.perm_logs')
@permission_required('user_perms.perm_logs_export')
def export_journalphotos(request, journals=None):
    filename = 'exported_journalphotos.zip'
    zip_file = exportPath(person=True) + filename
    
    #downloading export_photos
    if os.path.isfile(zip_file) and request.REQUEST.has_key('download'):
        f = open(zip_file, 'r+b')
        wrapper = f.read()
        f.close()
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Length'] = len(wrapper)
        response['Content-Disposition'] = 'attachment;filename=%s' % filename
        return response
    
    dir_name = os.path.dirname(zip_file)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    
    #creation zip archive
    data = dict()
    data["status"] = False
    data["url"] = "/export_journalphotos/?download=1"
    
    import zipfile
    zf = zipfile.ZipFile(zip_file, mode='w', allowZip64=True,compression=zipfile.ZIP_DEFLATED,)
    if journals:
        #получаем список применённых фильтров
        '''
        from videoclient.filters.views import JournalsFilters
        jfilters = JournalsFilters()
        jfilters.setFilters(HAVE_TIMES=True, HAVE_DATES=True, HAVE_CAMERAS=True, HAVE_IDENT=True, HAVE_FIO=True, HAVE_ID_PERSON=True, HAVE_ID_RECORD=True, HAVE_BIG_FILTER=True)
        filters = jfilters.getFilters(request)   
        if "cameras" in filters:                         
            filters["cameras"] = models.Camera.objects.filter(id__in = filters["cameras"])
        
        id_nodes = map(lambda x: x.agregate.id , journals)        
        save_journal_data(zf, id_nodes, filters=filters)   
        '''
        id_nodes = map(lambda x: x.agregate.id , journals)        
        save_journal_data(zf, id_nodes, filters=filter)   
         
    else:    
        jlist = request.REQUEST['jlist'].split(',')
        try:
            id_nodes = map(lambda x: int(x) , jlist)
        except:
            id_nodes = []
        save_journal_data(zf, id_nodes)            
    data["status"] = True
    try:
        zf.close()
    except:
        error = True
        logging.exception('close archive error: ' + str(sys.exc_info()))
    if journals:
        return data
    else:
        return JsonResponse(data)

@tester
@permission_required('user_perms.perm_settings')
def save_distortion(request):
    data = dict()
    data["status"] = False
    
    try:
     
        form = VcForms.SaveDistortionForm(request.REQUEST)
        if not form.is_valid():
            data["error"] = form.errors
            return JsonResponse(data)
        distr = form.save()
        data["id"] = distr.id
        data["status"] = True    
    except:
        data["error"] = str(sys.exc_info())
        logging.exception("save_distortion: "+str(sys.exc_info()))
    return JsonResponse(data)    

@tester
@permission_required('user_perms.perm_settings')
def delete_distortion(request):
    data = dict()
    data["status"] = False
    
    try:
     
        form = VcForms.DeleteDistortionForm(request.REQUEST)
        if not form.is_valid():
            data["error"] = form.errors
            return JsonResponse(data)
        id = form.cleaned_data["id"]
        models.Distortion.objects.filter(id = id).delete()
        data["status"] = True    
    except:
        data["error"] = str(sys.exc_info())
        logging.exception("save_distortion: "+str(sys.exc_info()))
    return JsonResponse(data)


@tester
@permission_required('user_perms.perm_lists')
def exportfile(request):
    try:
        import os
        #if not (request.REQUEST.has_key('person') or request.REQUEST.has_key('export_persons')):
        #    raise Http404
        
        if request.REQUEST.has_key('person'):
            person = request.REQUEST['person']
            if USE_ZIP_FILE:
                tarname = exportPath(person)+person+".zip";
                filename = '%s.zip' %(person)
            else:
                tarname = exportPath(person)+person+".tar.bz2";
                filename = '%s.tar.bz2' %(person)
            
        else:
            filename = request.REQUEST['export_persons']
            tarname = exportPath(person=True)+filename
            
        #if not os.path.isfile(tarname):
        #    raise Http404
        
        ftar = open(tarname, 'r+b')
        datatar = ftar.read()
        ftar.close()
        if USE_ZIP_FILE:
            response = HttpResponse(datatar, content_type='application/zip') # 
            response['Content-Length'] = len(datatar)
            response['Content-Disposition'] = 'attachment;filename=%s' %(filename)
            #response['Content-Encoding'] = 'gzip'
        else:
            response = HttpResponse(datatar, content_type='application/x-tar') # 
            response['Content-Length'] = len(datatar)
            response['Content-Disposition'] = 'attachment;filename=%s' %(filename)
            response['Content-Encoding'] = 'x-bzip2'
        
        os.unlink(tarname)
        
        return response
    except:
        #raise Http404
        logging.exception("exportfile: "+str(sys.exc_info()))
        return HttpResponse('Error: '+str(sys.exc_info()))
    return HttpResponse('Error')

@tester
def alertsettings(request, project=None):
    if not check_rule(request):
        return HttpResponseRedirect("/")
    data = dict()
    data.update(getDefaultParams(request, 'alert', project))
    
    from forms import TestAddAlerts
    form = TestAddAlerts(request.REQUEST, request.FILES)
    if form.is_valid():
        models.Alerts.objects.create(name=form.cleaned_data["new_address"])
        return HttpResponseRedirect("")
    """
    if form.is_valid():
    form = TestDelAlerts(request.GET, request.FILES)
        if form.cleaned_data["delo"]:
            for rp in range(1,form.cleaned_data["delo"]+1):
                try:
                    if "pi"+str(rp) in request.GET: models.Alerts.objects.get(id=int(request.GET["pi"+str(rp)])).delete()
                except: logging.exception(sys.exc_info())
            return HttpResponseRedirect("")
    """
    from videoclient.balancer import Balancer
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    try:
        data['alerterServer'] = b.getParameter("alerterServer")
    except: data['alerterServer'] = None
    data["alerts"] = models.Alerts.objects.all()
    b.close()
    del b
    return render_to_response_ex(request, "po4settings_alert.html", data)
   
@tester
@permission_required('user_perms.perm_monitoring')    
def rebootdaemon(request):
    try:
        form = VcForms.TestRebootDaemon(request.REQUEST, request.FILES)
        info = "True"      
        if form.is_valid():    
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            info = b.rebootDaemon(form.cleaned_data["balancerIp"], form.cleaned_data["balancerPort"], form.cleaned_data["daemonType"], form.cleaned_data["daemonIp"], form.cleaned_data["daemonPort"])
            b.close()
            return HttpResponse(info)      
    except:
        logging.exception("rebootdaemon "+str(sys.exc_info()))
    return HttpResponse("False")

@tester
@permission_required('user_perms.perm_monitoring')
def set_balancer_state(request):
    try:
        form = VcForms.TestSetBalancerState(request.REQUEST, request.FILES)
        info = "True"      
        if form.is_valid():    
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            info = b.setBalancerState(form.cleaned_data["balancerIp"], form.cleaned_data["balancerPort"], form.cleaned_data["stateUsed"], form.cleaned_data["daemonip"], form.cleaned_data["daemonport"], form.cleaned_data["type"])
            b.close()
            return HttpResponse(info)
        else:
            return HttpResponse(str(form.errors))
    except:
        logging.exception("set_balancer_state: "+str(sys.exc_info()))
    return HttpResponse("False")

def getCountPersonPhotosOfObject(request, obj=None, mainlist=False, bal_id_update=True):
    from utils import getBalIdByName, updateBalId

    HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
    b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
    
    if bal_id_update:
        updateBalId()
    
    person_ids = []
    for person in obj:
        if mainlist:
            person_id = getBalIdByName(person.id, bal_id_update=False)
        else:
            person_id = getBalIdByName(person["id"], bal_id_update=False)
        if person_id is not None:
            person_ids.append('%s' % person_id)

    p_sum = 0
    try:
        if len(person_ids) > 0:
            res = b.getPersonsPhotos(person_ids = person_ids)
            for n in res:
                if n["p_num"] is not None:
                    p_sum += int(n["p_num"])
    except:
        logging.exception("balancer method getPersonsPhotos "+str(sys.exc_info()))
    b.close()
    del b
    
    return p_sum

def getLeftPhotosCount():
    
    data = dict()
    left_photos = 0
    left_pictures_space = None
    
    try:
        HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        
        left_photos = None
        try:
            left_photos = b.getLeftPhotosCount()
            left_pictures_space = b.getLeftPicturesSpace()
        except:
            logging.exception("balancer method getPersonsPhotos "+str(sys.exc_info()))
        b.close()
        del b
        
    except:
        logging.exception(str(sys.exc_info()))
    
    if left_photos<0: left_photos = 0
    if left_pictures_space is not None and left_pictures_space >= 0: left_photos = min(left_photos, left_pictures_space)
        
    return {'left_photos': left_photos}

@tester
@permission_required('user_perms.perm_lists')
def lists(request):
    
    data = dict()
    data.update(getDefaultParams(request, 'lists', None))
    
    import settings
    from videoclient.models import List
    lists = List.objects.filter(active = True).exclude(id__in=[settings.self_learning]).order_by('-id')
   
    data["lists"] = lists

    return render_to_response_ex(request, "lists.html", data)

def getDataNameAndUrl(id):
    name = getNamePersonByBalId(id)
    person = getPersonByBalId(id)
    url = ""
    if person:
        if person.status.division.id == division_visitor:
            url = '/anketavisitor/%s/' %person.id
        elif person.status.division.id == division_person:
            url = '/anketaperson/%s/' %person.id
        elif person.status.division.id == division_employee:
            url = '/anketastaff/%s/' %person.id
        elif person.status.division.id == division_auto:
            url = '/anketaauto/%s/' %person.id
                        
        if person.group: 
            url = url+'?group=%s' %person.group.id
    data = dict();
    data["name"] = name
    data["url"] = url
    return data

@tester
@permission_required('user_perms.perm_view')
def url_name_person(request):
    if request.GET.has_key('id'):
        try:
            id = request.GET['id']
            data = getDataNameAndUrl(id)
            name = data["name"]
            url = data["url"]
            return HttpResponse("%s,%s" %(name,url))
        except:
            logging.exception("url_name_person"+str(sys.exc_info()))            
    return HttpResponse(",")

@tester
@permission_required('user_perms.perm_view')
def person_info_url(request):
    if request.GET.has_key('id'):
        try:
            id = request.GET['id']
            data = getDataNameAndUrl(id)
            if data.get("url"): return HttpResponseRedirect(data["url"])
        except:
            logging.exception("person_info_url "+str(sys.exc_info()))            
    return render_to_response('page_not_person.html', getDefaultParams(request, 'lists', None), context_instance=RequestContext(request)) 
    #return HttpResponseRedirect(reverse("lists"))

def getDataPersonJson(id):
    data = dict()
    
    from django.db import connection
    cursor = connection.cursor()
    
    cursor.execute("select * from videoclient_personid where id = %s" %id)
    personid_json = FetchOneAssoc(cursor)
    
    cursor.execute("select * from videoclient_person where id = %s" %personid_json["person_id"])
    person_json = FetchOneAssoc(cursor)
    
    transaction.commit_unless_managed()
    
    data["personid"] = personid_json
    data["person"] = person_json
    return data

from django.db import models as django_models

def getDictDataCommunicators():
    import settings
    m_lists = models.Communicator.objects.filter(active=True)
    d_lists = getDictFromListModel(m_lists) 
    return d_lists    

def getDictDataLists():
    import settings
    m_lists = models.List.objects.filter(active=True).exclude(group__id__in=[settings.noise_learning, settings.self_learning])
    d_lists = getDictFromListModel(m_lists) 
    return d_lists

from django.db.models.fields.files import ImageFieldFile
def getDictFromItemModel(item, recurse_fields=[]):
    a_item = dict()
    fields = item._meta.fields

    for field in fields:
        name = field.name
        value = getattr(item, name)
        if isinstance(value, django_models.Model):
            if name in recurse_fields:
                value = getDictFromItemModel(item=value, recurse_fields=recurse_fields)
            else:
                value = value.pk
        elif isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
            value = value.isoformat()
        elif isinstance(value, ImageFieldFile):
            value = value.url
        a_item[name] = value
    return a_item

def getDictFromListModel(list, recurse_fields=[]):
    return [getDictFromItemModel(item=item, recurse_fields=recurse_fields) for item in list]

def getDictDataPersons(params=None, bal_id_update=True):
    m_persons = models.PersonId.objects.filter(active=True)
    if params is not None:
        if "group" in params and params["group"] is not None: m_persons = m_persons.filter(person__group__id = params["group"])
        if "id" in params and params["id"] is not None: m_persons = m_persons.filter(id = params["id"])
    d_persons = getDictFromListModel(m_persons, recurse_fields=['person'])
    from utils import getBalIdByName, updateBalId
    if bal_id_update:
        updateBalId()
    for person in d_persons:
        try:
            if 'bal_id' not in person or 'bal_id' in person and person['bal_id'] is None:
                if 'id' in person:
                    person['bal_id'] = int(getBalIdByName(person['id'], bal_id_updaate=False))
        except:
            logging.exception(str(sys.exc_info()))
    return d_persons

def managePerson(params):
    id = params['id'] if 'id' in params else None
    
    if id is not None:
        idPersons = models.PersonId.objects.filter(id = id)
        if idPersons.count() == 0:
            return id
        
    status = models.StatusUser.objects.raw("select videoclient_statususer.id as id from videoclient_list join videoclient_types on videoclient_list.type_id = videoclient_types.id join videoclient_statususer on videoclient_types.division_id = videoclient_statususer.division_id where group_id = %s limit 1;" %params["group"])
    
    person =  models.Person.objects.create(first_name=params["first_name"], last_name=params["last_name"], middle_name=params["middle_name"], group_id=params["group"], action=0, status_id = status[0].id)
    
    if id is not None:        
        idPerson = models.PersonId.objects.get(id = id)
        idPerson.person = person
        idPerson.save()
        person.action = 1
    else:
        idPerson = models.PersonId.objects.create(active=True, person=person)
            
    person.id_person=idPerson.id
    person.save()
    return idPerson.id

def getPhotos(params):
    id = params['id'] if 'id' in params else None
    bal_id = params['bal_id'] if 'bal_id' in params else None
    if bal_id is not None:
        return getAllPhotosByBalId(bal_id)
    else:
        return getAllPhotosByName(id)
    
def getCameras(params):
    id = params['id'] if 'id' in params else None
    if id is not None:
        communicator = models.Communicator.objects.get(id=id)
        host = communicator.host
        port = communicator.port
    else:
        host = params['host']
        port = params['port']
    c = Communicator(host, port)
    cameras = c.getCameras()
    c.close()
    del c
    for camera in cameras:
        if 'ip' in camera and 'type' in camera:
            m_camera, create = models.Camera.objects.get_or_create(ip=camera["ip"], type=camera["type"])
            camera["id"] = m_camera.pk
        else:
            camera["error"] = "ip or type not found"
    return cameras

def addCamera(params):
    
    answer = dict()
    status = False
    result = {'answer': answer, 'status': status}
    
    if 'camera_type' not in params:
        answer["error"] = "type in params not found"
        result = {'answer': answer, 'status': status}
        return result
    
    if 'camera_url' not in params:
        if 'camera_ip' not in params:
            answer["error"] = "ip in params not found"
            result = {'answer': answer, 'status': status}
            return result
    
    id = params['id'] if 'id' in params else None
    camera_type = params["camera_type"] if "camera_type" in params else None
    camera_ip = params["camera_ip"] if "camera_ip" in params else None
    camera_mac = params["camera_mac"] if "camera_mac" in params else '000000000000'
    camera_port = params["camera_port"] if "camera_port" in params else None
    camera_num = params["camera_num"] if "camera_num" in params else None
    camera_user = params["camera_user"] if "camera_user" in params else None
    camera_psw = params["camera_psw"] if "camera_psw" in params else None
    camera_url = params["camera_url"] if "camera_url" in params else None
    
    if id is not None:
        communicator = models.Communicator.objects.get(id=id)
        host = communicator.host
        port = communicator.port
    else:
        host = params['host']
        port = params['port']
    
    c = Communicator(host, port)
    isAddedCamera = c.addCamera(type=camera_type, ip=camera_ip, mac=camera_mac, port=camera_port, num=camera_num, user=camera_user, psw=camera_psw, url=camera_url, json=True)
    c.close()
    del c
    
    status = isAddedCamera["status"]
    if "remark" in isAddedCamera:
        answer["error"] = isAddedCamera["remark"]
    result = {'answer': answer, 'status': status}

    return result

def deleteCamera(params):
    answer = dict()
    status = False
    result = {'answer': answer, 'status': status}
    
    if 'id' not in params and ('host' not in params or 'port' not in params):
        answer["error"] = "id or host:port in params not found"
        result = {'answer': answer, 'status': status}
        return result
    
    if 'numcamera' not in params:
        answer["error"] = "numcamera not found"
        result = {'answer': answer, 'status': status}
        return result
    
    id = params['id'] if 'id' in params else None
    if id is not None:
        communicator = models.Communicator.objects.get(id=id)
        host = communicator.host
        port = communicator.port
    else:
        host = params['host']
        port = params['port']
    
    numcamera = params['numcamera']
        
    c = Communicator(host, port)
    c.deleteCamera(numcamera)
    c.close()
    del c
    
    status = True
    result = {'answer': answer, 'status': status}
    return result
    
def getJournal(params):    
    answer = dict()
    status = False
    result = {'answer': answer, 'status': status}
    
    if 'limit' not in params:
        answer["error"] = "limit in params not found"
        result = {'answer': answer, 'status': status}
        return result
    
    limit = params["limit"] if "limit" in params else 15
    last_id = params["last_id"] if "last_id" in params else None
    
    if 'type' in params and params["type"]=="va":
        isVa = True
    else:
        isVa = False
    
    if isVa:
        from videoclient.videoanalytics import models as vanaliticsModels
        journals = vanaliticsModels.DetectorLog.objects.all()
    else:
        journals = models.Journal.objects.exclude(agregate=None)
        journals = journals.extra(where=['videoclient_journal.id = videoclient_journal.agregate_id'])
    
    if 'get_count' in params:
        if params["get_count"] == "true":
            count = journals.count()
            answer["count"] = count
        elif params["get_count"] != "false":
            answer["error"] = "get_count mast be true or false"
            result = {'answer': answer, 'status': status}
            return result
    
    if last_id is not None:
        journals = journals.filter(id__lt = last_id)
        
    if 'filter' in params:
        filter = params["filter"]
        if not isVa and 'only_ident' in filter:
            only_ident = filter["only_ident"]
            if only_ident == "true":
                journals = journals.exclude(person=None)
            elif only_ident != "false":
                answer["error"] = "only_ident mast be true or false"
                result = {'answer': answer, 'status': status}
                return result
        if 'camera' in filter:
            camera = filter["camera"]
            if 'id' in camera:
                id = camera["id"]
                journals = journals.filter(camera__id = id)
            elif 'ip' in camera and 'type' in camera:
                ip = camera["ip"]
                type = camera["type"]
                journals = journals.filter(camera__ip = ip, camera__type=type)
            else:
                answer["error"] = "id or ip:port in params not found"
                result = {'answer': answer, 'status': status}
                return result
        if 'datetime' in filter:
            datetime_f = filter["datetime"]
            if 'begin' in datetime_f:
                begin_time = None
                try:
                    begin_time = datetime.datetime.strptime(datetime_f["begin"], "%Y-%m-%dT%H:%M:%S")
                except:
                    answer["error"] = "begin datatime is incorrect, it mast be datatime in iso format YYYY-MM-DDTHH:MM:SS"
                    answer["exception"] = str(sys.exc_info())
                    logging.exception(str(sys.exc_info()))
                    result = {'answer': answer, 'status': status}
                    return result
                if begin_time is not None:
                    if isVa:
                        journals = journals.filter(dt_detect__gte = begin_time)
                    else:
                        journals = journals.filter(dt_first_fixed__gte = begin_time)
            if 'end' in datetime_f:
                end_time = None
                try:
                    end_time = datetime.datetime.strptime(datetime_f["end"], "%Y-%m-%dT%H:%M:%S")
                except:
                    answer["error"] = "end datatime is incorrect, it mast be datatime in iso format YYYY-MM-DDTHH:MM:SS"
                    answer["exception"] = str(sys.exc_info())
                    logging.exception(str(sys.exc_info()))
                    result = {'answer': answer, 'status': status}
                    return result
                if end_time is not None:
                    if isVa:
                        journals = journals.filter(dt_detect__gte = end_time)
                    else:
                        journals = journals.filter(dt_first_fixed__gte = end_time)
                
        
    journals = journals.order_by('-id')
    journals = journals[:limit]
    
    items = getDictFromListModel(journals, recurse_fields=["camera", "detector_type", "person"])
    answer["journal"] = items
    
    status = True
    result = {'answer': answer, 'status': status}

    return result
    
# example  /json_sdk/?query={"command": "get_person_name", "params": {"id": 1254}}
GET_LISTS = 'get_lists'
GET_COMMUNICATORS = 'get_communicators'
GET_CAMERAS = 'get_cameras'
GET_PERSONS = 'get_persons'
GET_PERSON_NAME = 'get_person_name'
GET_PHOTOS = 'get_photos'
GET_JOURNAL = 'get_journal'
ADD_CAMERA = 'add_camera'
ADD_LIST = 'add_list'
MANAGE_PERSON = 'manage_person'
DELETE_CAMERA = 'delete_camera'
DELETE_PERSON = 'delete_person'
DELETE_LIST = 'delete_list'

def json_sdk(request):
    answer = dict()
    answer["status"] = False
    try:
        if not check_rule(request):
            answer["error"] = "user is not authenticated"
            return JsonResponse(answer)
        if 'query' not in request.REQUEST: 
            answer["error"] = "query not found"
            return JsonResponse(answer)
        query = json.loads(str(request.REQUEST["query"]))
        
        if 'command' not in query:
            answer["error"] = "command not found"
            return JsonResponse(answer)
        command = query["command"]
        
        if command in [GET_PERSON_NAME, MANAGE_PERSON, DELETE_PERSON, GET_PHOTOS, GET_CAMERAS, ADD_CAMERA, GET_JOURNAL, DELETE_CAMERA, DELETE_LIST, ADD_LIST]:
            if 'params' not in query:
                answer["error"] = "params not found"
                return JsonResponse(answer)
            params = query["params"]
            if command == GET_PERSON_NAME:
                if 'id' not in params:
                    answer["error"] = "id in params not found"
                    return JsonResponse(answer)
                id = params["id"]
                
                person = getPersonByBalId(id)
                if not person:
                    answer["error"] = "person not found"
                    return JsonResponse(answer)
                
                answer.update(getDataNameAndUrl(id))
                answer.update(getDataPersonJson(person.id_person))
            elif command == MANAGE_PERSON:
                if 'group' not in params:
                    answer["error"] = "group in params not found"
                    return JsonResponse(answer)
                if 'first_name' not in params:
                    answer["error"] = "first_name in params not found"
                    return JsonResponse(answer)
                if 'last_name' not in params:
                    answer["error"] = "last_name in params not found"
                    return JsonResponse(answer)
                if 'middle_name' not in params:
                    answer["error"] = "middle_name in params not found"
                    return JsonResponse(answer)
                id = managePerson(params)
                if id is None:
                    answer["error"] = "person not found"
                    return JsonResponse(answer)
                answer["persons"] = getDictDataPersons({"id": id})
            elif command == DELETE_PERSON:
                if 'id' not in params:
                    answer["error"] = "id in params not found"
                    return JsonResponse(answer)
                try:
                    DeletePerson(request, params['id'])
                except:
                    logging.exception(str(sys.exc_info()))
                    answer["exception"] = str(sys.exc_info())
                    answer["status"] = False
                    return JsonResponse(answer)
            elif command == DELETE_LIST:
                if 'id' not in params:
                    answer["error"] = "id_was_not_found"
                    return JsonResponse(answer)
                try:
                    delete, error = DeleteList(users=[params['id']])
                    if not delete: 
                        answer["error"] = error 
                        answer["status"] = False
                except:
                    logging.exception(str(sys.exc_info()))
                    answer["error"] = "exception"
                    answer["exception"] = str(sys.exc_info())
                    answer["status"] = False
                    return JsonResponse(answer)
            elif command == ADD_LIST:
                if 'name' not in params:
                    answer["error"] = "name_was_not_found"
                    return JsonResponse(answer)
                if "type" not in params:
                    answer["error"] = "type_was_not_found"
                    return JsonResponse(answer)
                if "group" in params: del(params["group"])
                result = addList(params)
                answer.update(result["answer"])
                if not result["status"]: return JsonResponse(answer)
            elif command == GET_PHOTOS:
                if 'id' not in params and 'bal_id' not in params:
                    answer["error"] = "id or bal_id in params not found"
                    return JsonResponse(answer)
                answer['photos_num'] = getPhotos(params)
            elif command == GET_CAMERAS:
                if 'id' not in params and ('host' not in params or 'port' not in params):
                    answer["error"] = "id or host:port in params not found"
                    return JsonResponse(answer)
                answer['cameras'] = getCameras(params)
            elif command == ADD_CAMERA:
                if 'id' not in params and ('host' not in params or 'port' not in params):
                    answer["error"] = "id or host:port in params not found"
                    return JsonResponse(answer)
                result = addCamera(params)
                answer.update(result["answer"])
                if not result["status"]:
                    return JsonResponse(answer)
            elif command == DELETE_CAMERA:
                result = deleteCamera(params)
                answer.update(result["answer"])
                if not result["status"]:
                    return JsonResponse(answer)
            elif command == GET_JOURNAL:
                result = getJournal(params)
                answer.update(result["answer"])
                if not result["status"]:
                    return JsonResponse(answer)
            else:
                answer["error"] = "command is undefined"
                return JsonResponse(answer)
                
        elif command == GET_LISTS:
            answer["lists"] = getDictDataLists()
        elif command == GET_COMMUNICATORS:
            answer["communicators"] = getDictDataCommunicators()
        elif command == GET_PERSONS:
            params = None
            if "params" in query: params = query["params"]
            answer["persons"] = getDictDataPersons(params)
        else:
            answer["error"] = "command is undefined"
            return JsonResponse(answer)                
                
        answer["status"] = True
    except:
        logging.exception(str(sys.exc_info()))
        answer["exception"] = str(sys.exc_info())
    return JsonResponse(answer) 

from xml.dom.minidom import parseString


def recursXml(xml_node):
    value = None
    nodes = xml_node.childNodes
    if len(nodes)>0:
        value = dict();
        for node in nodes:
            name = node.localName                
            if (len(node.childNodes) == 1) and (node.childNodes[0].localName == None):
                value[name] = node.childNodes[0].toxml()
            else:
                arr = []

                if value.has_key(name):
                    #if value[name] 
                    arr = value[name]
                arr.append(recursXml(node))
                value[name] = arr
    else:
        value = xml_node.toxml()
        
    return value
    
    
#    def getSystemInfo(self, id_command = 'SDKBalancer'):
#        
#        self.__connect()
#                
#        xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>getSystemInfo</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>getSystemInfo%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)                
#        
#        self.__sendXml(xml_file)
#        self.__sendSize(0)
#
#        xml_node = self.__readXml()
#                       
#        if xml_node.getElementsByTagName('status')[0].firstChild.toxml() != '200 OK':
#            return None;
#       
#        res = []
#        res = self.recursXml(xml_node.getElementsByTagName('balancers')[0])
#        return res

def addList(params):
    answer = dict()
    status = False
    
    form = VcForms.ListForm(params)
    if form.is_valid():
        list = form.save(commit=False)
        g1, create = models.GroupPerson.objects.get_or_create(id=list.id)
        g1.name = list.name
        g1.save()
        list.group = g1
        list.active = True
        list.save()
        answer["id"] = list.id
        status = True
    else:
        answer['exception'] = form.errors
    answer['status'] = status
    return answer

@tester
def maps(request):
    return HttpResponseRedirect("/")
    if not check_rule(request):
        return HttpResponseRedirect("/")
    data = dict()
    data.update(getDefaultParams(request, 'map', None))
    f = open(MEDIA_ROOT+'map/map.xml', 'r+b')
    xml = parseString(f.read()) 
    f.close()
    xml_terminals = xml.getElementsByTagName('terminal')
    terminals = []
    for xml_terminal in xml_terminals:
        terminal = dict()
        xml_cameras = xml_terminal.getElementsByTagName('camera')
        cameras = []
        for xml_camera in xml_cameras:
            camera = dict()
            attrs = xml_camera.attributes
            i=0
            while i< attrs.length:
                item = attrs.item(i)
                camera[item.name] = item.value
                i=i+1
            cameras.append(camera)
        terminal['cameras'] = cameras
        
        attrs = xml_terminal.attributes
        i=0
        while i< attrs.length:
            item = attrs.item(i)
            terminal[item.name] = item.value
            i=i+1
        terminals.append(terminal)
    data['terminals'] = terminals; 
    #from videoclient.models import List
    #data['lists'] = List.objects.all()
    
    return render_to_response_ex(request, "map.html", data)

@tester
@permission_required('user_perms.perm_lists')
@permission_required('user_perms.perm_lists_edit')
def anketalist(request, id = None):
    if not check_rule(request, False,is_moderator=False):
        return HttpResponseRedirect("/")
    data = dict()
    data.update(getDefaultParams(request, 'anketalist', None))
    data.update(getDataAnketaList(request, id))
    if data.has_key("redirect"):
        return HttpResponseRedirect(data["redirect"])
    return render_to_response_ex(request, "addlist.html", data)   

def DeleteList(users=[]):
    delete_list = False    
    lists = models.List.objects.filter(id__in = users)
    if lists.count() == 0: return delete_list, "list_was_not_found"
    error = "list_was_not_empty"
    for l in lists:
        p = models.PersonId.objects.filter(person__status__division__id=l.type.division_id, active=1, person__group__id=l.group_id).count()
        if p == 0:
            l.active = False
            l.save()
            delete_list = True
            error = ""
    return delete_list, error

@tester
@permission_required('user_perms.perm_lists')
@permission_required('user_perms.perm_lists_edit')
def delete_list(request):
    #try:    
    if True:
        users = request.REQUEST['lists'].split(',')
        i = 0
        logging.info(str(users))
        while i<len(users):
            users[i] = int(users[i])
            i+=1
        delete, error = DeleteList(users)
        return HttpResponse(delete)
    #except:
    #    logging.exception("delete_list: "+str(sys.exc_info()))
    return HttpResponse(False)

def JsonResponse(data):
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def JavaScriptResponse(data):
    return HttpResponse(simplejson.dumps(data), mimetype="application/javascript")

def JsonSTRResponse(data):
    return HttpResponse(str(simplejson.dumps(data)))

@tester
@permission_required('user_perms.perm_monitoring')
def get_balancer_statistics(request):
    COLORS = ['0xFF0000', '0x006600', '0x000088']
    try:
        form = VcForms.TestGetStatistics(request.REQUEST, request.FILES)
        if form.is_valid():    
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            balancerIp = form.cleaned_data["ip"].split("*")
            balancerPort = form.cleaned_data["port"].split("*")
            i = 0
            sum = None
            while i<1 or (i<len(balancerIp)-1) and (len(balancerIp)>1):
                try:
                    data = b.getBalancerStatistics(balancerIp[i], balancerPort[i])
                except:
                    logging.exception("getBalancerStatistics: "+str(sys.exc_info()))
                    data = None
                if sum:
                    if not data:
                        i = i+1 
                        continue
                    k = 0
                    while k<len(data):
                        l = 0
                        while l<len(data[k]):
                            sum[k][l] = int(sum[k][l]) + int(data[k][l])
                            l = l+1
                        k = k+1
                else:
                    sum = data
                i = i+1
                
            #data = b.getBalancerStatistics(form.cleaned_data["balancerIp"], form.cleaned_data["balancerPort"])
            data = sum
            b.close()
            if data:
                index = 0
                res = []
                colors = COLORS
                if form.cleaned_data["colors"]:
                    colors = form.cleaned_data["colors"].split(',')
                if form.cleaned_data["index"]:
                    indexes = form.cleaned_data["index"].split(',')
                    for i in indexes:
                        res.append({'color': colors[int(i)%len(colors)], 'data': data[int(i)]})
                else:
                    i = 0
                    for d in data:
                        res.append({'color': colors[int(i)%len(colors)], 'data': d})
                        i=i+1
                return JsonResponse(res)
            else:
                return HttpResponse(False)
        else:
            return JsonResponse(form.errors)
    except:
        logging.exception("set_balancer_state: "+str(sys.exc_info()))
    return HttpResponse("False")

@tester
@permission_required('user_perms.perm_monitoring')
def get_balancers_statistics(request):
    colors = ['#FF6600', '#0099FF', '#00FF00', '#FF0000', '#FF00FF', '#0000FF']
    import copy
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    
    #balancerIp = form.cleaned_data["ip"].split("*")
    #balancerPort = form.cleaned_data["port"].split("*")
    
    i = 0
    bal_data = []
    
    sum = None
    p = 0
    balancers = b.getSystemInfo()
    for balancer in balancers["balancer"]:
        try:
            data = b.getBalancerStatistics(balancer["address"], balancer["port"])
            tmp_data = []
            tmp_data1 = copy.deepcopy(data)
            tmp_data = copy.deepcopy(data)
            k = 0
            while k<len(tmp_data):
                l = 0
                while l<len(tmp_data[k]):
                    tmp_data1[k][l] = int(data[k][l])
                    l = l+1
                k = k+1
            bal_data.append(tmp_data1)
        except:
            logging.error("getBalancerStatistics: " + str(sys.exc_info()))
            data = None
            bal_data.append(data)

        if sum:
            if not data:
                continue
            k = 0
            while k<len(data):
                l = 0
                while l<len(data[k]):
                    sum[k][l] = int(sum[k][l]) + int(data[k][l])
                    l = l+1
                k = k+1
        else:
            sum = copy.deepcopy(data)
    #data = b.getBalancerStatistics(form.cleaned_data["balancerIp"], form.cleaned_data["balancerPort"])
    
    #raise Exception('%s * %s * %s' % ( str(sum[0][0]), str(bal_data[0][0][0]), str(bal_data[1][0][0]) ) )
    #raise Exception('%s * %s * %s' % ( str(sum), bal_data[0],bal_data[1] ) )
    data = sum

    b.close()
    if data:
        res = []
        for d in data:
            res.append({'data': d})

        res1 = []
        for d in bal_data:
            res1.append({'b_data': d})

        result = {'main_graph': res, 'bal_graph': res1}
        return JsonResponse(result)
    else:
        return HttpResponse(False)
    
@tester
@permission_required('user_perms.perm_monitoring')    
def get_balancer_daemons_statistics(request):
    COLORS = ['0xFF0000', '0x006600', '0x000088', '0xFF6600', '0xFF0088', '0x006688']
    if True:
        form = VcForms.TestGetDaemonsStatistics(request.REQUEST)
        if form.is_valid():    
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            balancerIp = form.cleaned_data["ip"].split("*")
            balancerPort = form.cleaned_data["port"].split("*")
            i = 0
            sum = None
            while i<1 or (i<len(balancerIp)-1) and (len(balancerIp)>1):
                #try:
                balancers = b.getSystemInfo()
                #except:
                #    logging.exception("getBalancerStatistics: "+str(sys.exc_info()))
                #    data = None
                
                data = []
                for balancer in balancers["balancer"]:
                    if balancer["address"] == balancerIp[i] and balancer["port"] == balancerPort[i]:
                        if int(balancer["fdQueue"]) >= 0: data.append([int(balancer["fdQueue"])])
                        if int(balancer["frQueue"]) >= 0: data.append([int(balancer["frQueue"])])
                        if int(balancer["fsQueue"]) >= 0: data.append([int(balancer["fsQueue"])])
                        if int(balancer["sdQueue"]) >= 0: data.append([int(balancer["sdQueue"])])
                        if int(balancer["ddQueue"]) >= 0: data.append([int(balancer["ddQueue"])])
                
                if sum:
                    if not data:
                        i = i+1 
                        continue
                    k = 0
                    while k<len(data):
                        l = 0
                        while l<len(data[k]):
                            sum[k][l] = int(sum[k][l]) + int(data[k][l])
                            l = l+1
                        k = k+1
                else:
                    sum = data
                i = i+1
                
            #data = b.getBalancerStatistics(form.cleaned_data["balancerIp"], form.cleaned_data["balancerPort"])
            data = sum
            b.close()
            if data:
                index = 0
                res = []
                colors = COLORS
                if form.cleaned_data["colors"]:
                    colors = form.cleaned_data["colors"].split(',')
                #if form.cleaned_data["index"]:
                #    indexes = form.cleaned_data["index"].split(',')
                #    for i in indexes:
                #        res.append({'color': colors[int(i)%len(colors)], 'data': data[int(i)]})
                #else:
                i = 0
                for d in data:
                    res.append({'color': colors[int(i)%len(colors)], 'data': d})
                    i=i+1
                return JsonResponse(res)
            else:
                return HttpResponse(False)
        else:
            return JsonResponse(form.errors)
    #except:
    #    logging.exception("set_balancer_state: "+str(sys.exc_info()))
    #return HttpResponse("False")

@tester
@permission_required('user_perms.perm_monitoring')
def get_balancer_daemons_statistics_js(request):
    COLORS = ['FF6600', '0099FF', '00FF00', 'FF0000', 'FF00FF', '0000FF']

    graph_data = []
    fdQueue = frQueue = fsQueue = sdQueue = ddQueue = None
    #try:
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    balancers = b.getSystemInfo()
    
    for balancer in balancers["balancer"]:
        result = []
        if balancer["active"] == "true":
            if int(balancer["fdQueue"]) >= 0:
                fdQueue = int(balancer["fdQueue"])
            else:
                fdQueue = 0
            if int(balancer["frQueue"]) >= 0:
                frQueue = int(balancer["frQueue"])
            else:
                frQueue = 0
            if int(balancer["fsQueue"]) >= 0:
                fsQueue = int(balancer["fsQueue"])
            else:
                fsQueue = 0
            if int(balancer["sdQueue"]) >= 0:
                sdQueue = int(balancer["sdQueue"])
            else:
                sdQueue = 0
            if int(balancer["ddQueue"]) >= 0:
                ddQueue = int(balancer["ddQueue"])
            else:
                ddQueue = 0
        else:
            fdQueue = 0
            frQueue = 0
            fsQueue = 0
            sdQueue = 0
            ddQueue = 0
            
        result = [{'v': fdQueue, 'name': 'FD', 'color': COLORS[0]}, {'v': frQueue, 'name': 'FR', 'color': COLORS[1]}, {'v': fsQueue, 'name': 'FS', 'color': COLORS[2]}, {'v': sdQueue, 'name': 'SD', 'color': COLORS[3]}, {'v': ddQueue, 'name': 'DD', 'color': COLORS[4]}]
        graph_data.append(result)
        
    b.close()

    return JsonResponse(graph_data)
    #except:
    #    logging.exception("get_balancer_daemons_statistics_js: " + str(sys.exc_info()))
    #    return HttpResponse("False")

@tester
@permission_required('user_perms.perm_monitoring')
def get_camera_statistics_js(request):
    try:
        c = Communicator()
        res_frame_answer = c.getCameraFrameStat(request.REQUEST["uuid"], 1, 1, 1)
        c.close()
        del c

        if res_frame_answer["success"]:
            frame_answer = res_frame_answer["answer"]
        
            result = {'v': frame_answer["detectDaemonTime"], 'color': 'CC3300', 'name': 'detectDaemonTime'}, {'v': frame_answer["detectTotalTime"], 'color': '0066CC', 'name': 'detectTotalTime'}, {'v': frame_answer["recognitionDaemonTime"], 'color': '00CC00', 'name': 'recognitionDaemonTime'}, {'v': frame_answer["recognitionTotalTime"], 'color': 'FF9900', 'name': 'recognitionTotalTime'}
            return JsonResponse({'status': 'success', 'data': result})
        else:
            return JsonResponse({'status': 'error'})
    except:
        logging.exception("get_camera_statistics_js: "+str(sys.exc_info()))
        return JsonResponse({'status': 'error'})
    
@tester
@permission_required('user_perms.perm_monitoring')
def get_communicator_statistics(request):
    #try:
    COLORS = ['0xFF0000', '0x006600', '0x000088']
    if True:
        form = VcForms.TestGetStatistics(request.REQUEST, request.FILES)
        if form.is_valid():    
            balancerIp = form.cleaned_data["ip"].split("*")
            balancerPort = form.cleaned_data["port"].split("*")
            i = 0
            sum = None
            while i<1 or (i<len(balancerIp)-1) and (len(balancerIp)>1):
                #try:
                if True:
                    c = Communicator(balancerIp[i], int(balancerPort[i]))
                    data = c.getStatistics()
                    c.close()
                    del c
                #except:
                #    logging.exception("getCommunicatorStatistics: "+str(sys.exc_info()))
                #    data = None
                if sum:
                    if not data:
                        i = i+1 
                        continue
                    
                    for e in data:
                        l = 0
                        while l<len(data[e]):
                            sum[e][l] = int(sum[e][l]) + int(data[e][l])
                            l = l+1
#                    k = 0
#                    while k<len(data):
#                        l = 0
#                        while l<len(data[k]):
#                            sum[k][l] = int(sum[k][l]) + int(data[k][l])
#                            l = l+1
#                        k = k+1
                else:
                    sum = data
                    for ss in sum:
                        s = sum[ss]
                        s.reverse()
                        while len(s)<600:
                            s.append([0])
                        s.reverse()
                i = i+1
                
            #data = b.getBalancerStatistics(form.cleaned_data["balancerIp"], form.cleaned_data["balancerPort"])
            data = sum
            
            if data:
                index = 0
                res = []
                colors = COLORS
                if form.cleaned_data["colors"]:
                    colors = form.cleaned_data["colors"].split(',')
                if form.cleaned_data["index"]:
                    indexes = form.cleaned_data["index"].split(',')
                    i = 0
                    while i < len(indexes):
#                        if indexes[int(i)] == 'missed':
#                            j = 0
#                            while j<len(data['missed']):
#                                data['missed'][j] = int(data['missed'][j])*10;
#                                #data['missed'][j] = data['missed'][j]+100
#                                j=j+1
                        res.append({'color': colors[int(i)%len(colors)], 'data': data[indexes[int(i)]]})
                        i = i+1
#                    for i in indexes:
#                        res.append({'color': colors[int(i)%len(colors)], 'data': data[i]})
                else:
                    i = 0
                    for d in data:
                        res.append({'color': colors[int(i)%len(colors)], 'data': data[d]})
                        i=i+1
                return JsonResponse(res)
            else:
                return HttpResponse(False)
        else:
            return JsonResponse(form.errors)
    #except:
    #    logging.exception("set_balancer_state: "+str(sys.exc_info()))
    #return HttpResponse("False")

@tester
@permission_required('user_perms.perm_monitoring')
def get_communicator_statistics_js(request):
    data = []
    answer = dict()
    c = Communicator()
    try:
        communicators = c.getListOfCommunicators()
        for com in communicators:
            answer = None
            try:
                res_getStatistics = c.getStatistics(str(com["host"]), str(com["port"]), str(com["mjpeg_port"]))
                answer = res_getStatistics["answer"]
            except:
                answer = None
            data.append(answer)
        
        try:
            c.close()
            del c
        except:
            pass

        return JsonResponse(data)
    except:
        logging.exception("get_communicator_statistics_js: "+str(sys.exc_info()))
        
    try:
        c.close()
        del c
    except:
        pass
    
    return JsonResponse({'status': 'error'})
        

@tester
def get_detect_coefficients(request):
    """ Получение коэффициентов для вкладки просмотр. """
    data = dict()
    data["status"] = False
    form = VcForms.CheckStartRollerForm(request.GET)
    logging.info(form.errors)
    if not form.is_valid():
        return JsonResponse(data)
    
    id = form.cleaned_data["uuid"]
    cameras = CommunicatorModels.Camera.objects.filter(uuid=id)
    if cameras.count() == 0:
        return JsonResponse(data)
    camera = cameras[0]

    detect_avg = 0
    time_detect = 0
    
    c = Communicator()
    # Среднее время обработки кадра
    try:
        answer = c.getStatistics(camera.commun.host, camera.commun.port, camera.commun.mjpeg_port)["answer"]
        if "avg" in answer and answer["avg"]:
            avg = answer["avg"]
            detect_avg = float(sum(avg)) / len(avg) / 1000
    except:
        logging.exception(sys.exc_info())
        detect_avg = 0    
    # Время детектирования лиц с учетом накладных расходов и очередей:
    try:
        cameras = c.getCameras()
        camera = filter(lambda x: x.uuid == id and x.active, cameras["cameras"])
        if camera:
            cameramode = c.getModeScheduler(id)
            if int(cameramode.get("answer", 0)) > 0:
                frame_answer = c.getCameraFrameStat(id, 1, 1, 1)
                if frame_answer["success"]:
                    frame_answer = frame_answer.get("answer", None)
                    if (frame_answer and "detectTotalTime" in frame_answer and 
                        frame_answer["detectTotalTime"] and frame_answer["detectTotalTime"] != 'Null'):
                        time_detect = frame_answer["detectTotalTime"]
    except:
        logging.exception(sys.exc_info())
        time_detect = 0

    c.close()
    del c
    
    data["k1"] = round(time_detect, 3)
    data["k2"] = round(detect_avg, 3)
    data["status"] = True
    return JsonResponse(data)
    
@tester
@permission_required('user_perms.perm_settings')
def set_self_learning(request):
    try:
        form = VcForms.TestSetSelfLearning(request.REQUEST, request.FILES)
        if form.is_valid():    
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            if form.cleaned_data["param"]:
                p1 = "true"
            else:
                p1 = "false"
            data = b.setCameraParameter(source = form.cleaned_data["source"], type = form.cleaned_data["type"], p1=p1, param='selfLearning')
            b.close()
            return HttpResponse(data)
        else:
            return JsonResponse(form.errors)
    except:
        logging.exception("set_self_learning: "+str(sys.exc_info()))
    return HttpResponse("False")    

CONST_DIVISION = 'Автообученные'
CONST_STATUS = 'Автообученный'

@tester
def createPerson(id):
    import settings
    idPerson = models.PersonId.objects.create(bal_id = id)
    
    try:
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        param = [{'name':'person_name', 'param':str(idPerson.id)}, {'name':'person_id', 'param':str(id)}]
        b.renamePerson(param)
        b.close()
    except:
        logging.exception("createPerson rename: "+str(sys.exc_info()))
        models.PersonId.objects.filter(id = idPerson.id).delete()
        return 0
    
    user = models.Person.objects.create()
    try:
        user.first_name = str(id)
        user.division = models.DivisionUser.objects.get(name = CONST_DIVISION)
        user.status = models.StatusUser.objects.get(name = CONST_STATUS, division=user.division)
        user.group = models.GroupPerson.objects.get(id = settings.self_learning)
        user.action = 0
        user.id_person = idPerson.id
        user.save()    
        
        idPerson.person = user
        idPerson.save()
    except:
        logging.exception("createPerson create user: "+str(sys.exc_info()))
        models.PersonId.objects.filter(id = idPerson.id).delete()
        models.Person.objects.filter(id = user.id).delete()
        return 0
    
    try:
        if models.List.objects.filter(id = settings.self_learning).count() == 1 :
            list = models.List.objects.get(id = settings.self_learning)
            list.active = True
            list.save()
    except:
        logging.exception("createPerson set vctive List")
    
    return idPerson.id

@tester
@permission_required('user_perms.perm_settings')
def self_learning(request):
    try:
        form = VcForms.TestSelfLearning(request.REQUEST, request.FILES)
        if form.is_valid():    
            res = createPerson(form.cleaned_data["id"])
            if res != 0:
                return HttpResponse(True)
        else:
            return JsonResponse(form.errors)
    except:
        logging.exception("self_learning: "+str(sys.exc_info()))
    return HttpResponse("False")

@tester
@permission_required('user_perms.perm_logs')
def delete_self_person(request):
    try:
        form = VcForms.TestSelfLearning(request.REQUEST, request.FILES)
        if form.is_valid():
            personid =  getPersonIdByBalId(form.cleaned_data["id"])
            res = DeletePerson(request, personid.id)
            if res != 0:
                return HttpResponse(True)
        else:
            return JsonResponse(form.errors)
    except:
        logging.exception("self_learning: "+str(sys.exc_info()))
    return HttpResponse("False")


@tester
@permission_required('user_perms.perm_settings')
def delete_camera(request):
    
    try:
        form = VcForms.TestCameraDelete(request.REQUEST, request.FILES)
        if form.is_valid():
            uuid = form.cleaned_data["uuid"]
            if uuid is not None:
                c = Communicator()
                res_delCam = c.deleteCamera(uuid)
                num_answer = False
                if res_delCam["success"]:
                    num_answer = res_delCam["answer"]
            
                c.close()
                del c
            else:
                num_answer = True
            
                
            #id = form.cleaned_data["id"]
            #if id:
            #    try:
            #        models.Camera.objects.filter(id = id).update(active = False)
            #        id_answer = True
            #    except:
            #        logging.exception(str(sys.exc_info()))
            #        id_answer = False
            #else:
            #    id_answer = True
            answer = num_answer
            
            if 'uuid' in request.COOKIES:
                c_uuid = request.COOKIES['uuid']
                if c_uuid == uuid:
                    response = HttpResponse(str(answer)) 
                    response.delete_cookie('uuid') 
                    return response
            return HttpResponse(str(answer))
                
             
            #return HttpResponse(str(answer))#answer
        else:
            return HttpResponse(str(form.errors))
    except:
        logging.exception(str(sys.exc_info()))
        return HttpResponse(str(sys.exc_info()))
    
    return HttpResponse("False")

@tester
@permission_required('user_perms.perm_settings')
def set_alias_camera(request):
    try:
        form = VcForms.TestCameraAlias(request.GET, request.FILES)
        if form.is_valid():
            cam = models.Camera.objects.filter(id=form.cleaned_data["cid"])
            if cam.count()>0:
                cam.update(name=form.cleaned_data["name"] if "name" in form.cleaned_data else "")
                return HttpResponse("True")
        else:return HttpResponse(str(form.errors))
        return HttpResponse("False1")
    except:
        logging.exception("set_alias_camera "+str(sys.exc_info()))
        return HttpResponse("False2")

@tester
@permission_required('user_perms.perm_view')
def video(request):
    data = dict()
    data.update(getDefaultParams(request, 'video', None))
    data.update(getDataVideo(request))
    data.update(dataNavigation(request, data['found_rollers']))
    data["rollers"] = data["rollers"][data['start']-1:data['finish']-1]
    data.update(dataGet(request))
    
    return render_to_response_ex(request, "video.html", data)

@tester
@permission_required('user_perms.perm_view')
def videoclip_download(request):

    id = int(request.GET['id'])
    roller = get_object_or_404(models.Roller, pk=id)
    if os.path.isfile(VIDEO_CLIP_PATH + roller.filename):
        f = open(VIDEO_CLIP_PATH + roller.filename, 'r+b')
        wrapper = f.read()
        f.close()
        #хром в windows при скачивании сам добавляет раширение, которое указано в content_type
        response = HttpResponse(wrapper, content_type='application/octet-stream')
        response['Content-Length'] = len(wrapper)
        response['Content-Disposition'] = 'attachment;filename=%s' % (roller.filename)
        return response
    else:
        return Http404

def divDatetime(now = datetime.datetime.now()):
    today = datetime.date(year = now.year, month = now.month, day = now.day)
    time = datetime.time(hour = now.hour, minute = now.minute, second = now.second)
    return today, time

@tester
@permission_required('user_perms.perm_view')
def startRecord(request):
    data = dict()
    data["status"] = False
    rollers = models.Roller.objects.exclude(tm_stop=None)
    data["all_rollers"] = rollers.count()
    
    try:
        form = VcForms.CheckStartRollerForm(request.REQUEST) 
        if not form.is_valid():
            data["errors"] = form.errors
            return JsonResponse(data)
        
        uuid = form.cleaned_data["uuid"]
        camera = getCameraByUUID(uuid)
        if camera:
            rollers = models.Roller.objects.filter(camera__uuid = uuid, dt_stop = None, tm_stop=None)
            
            c = Communicator()
            res_status_record = c.statusRecord(uuid)
    
            if res_status_record["success"]:
                status = res_status_record["answer"]
    
                if status != '0':
                    data["rollers"] = rollers.count()
                    try:   
                        res_stopRecord = c.stopRecord(uuid)
                        if res_stopRecord["success"]:
                            filename = res_stopRecord["answer"]
                            today, time = divDatetime(datetime.datetime.now())
                            rollers.update(dt_stop=today, tm_stop=time)
                            data["status"] = True
                        else:
                            data["status"] = False
                    except:
                        data["status"] = False
                        logging.exception("stopRecord: "+str(sys.exc_info()))
                else:
                    res_start_record = c.startRecord(uuid=uuid)
                    if res_start_record["success"]:
                        filename = res_start_record["answer"]
                        if filename:
                            today, time = divDatetime(datetime.datetime.now())
                            roller = models.Roller.objects.create(camera=camera, com=camera.commun, dt_start = today, tm_start = time, filename=filename)
                            data["id"] = roller.id
                            data["status"] = True
                        else:
                            data["error"] = "Filename is None"
                    else:
                        data["status"] = False
        
                c.close()
                del c
                rollers = models.Roller.objects.exclude(tm_stop=None)
                data["all_rollers"] = rollers.count()
            else:
                data["status"] = False
        else:
            data["status"] = False

    except:
        data["status"] = False
        data["error"] = str(sys.exc_info())
        logging.exception("startRecord: "+str(sys.exc_info()))
    return JsonResponse(data)

@tester
@permission_required('user_perms.perm_view')
def statusRecord(request):
    data = dict()
    data["status"] = False

    try:
        form = VcForms.CheckStartRollerForm(request.REQUEST) 
        if not form.is_valid():
            data["errors"] = form.errors
            return JsonResponse(data)
        
        uuid = form.cleaned_data["uuid"]
        rollers = models.Roller.objects.filter(camera__uuid = uuid, dt_stop = None, tm_stop=None)
        
        c = Communicator()
        res_status_record = c.statusRecord(uuid)
        c.close()
        del c
        
        if res_status_record["success"]:
            status = res_status_record["answer"]

            if rollers.count()>0 and status=="0":
                data["rollers"] = rollers.count()
                today, time = divDatetime(datetime.datetime.now())
                rollers.update(dt_stop=today, tm_stop=time)
                data["status"] = True
            data["status"] = True
            data["value"] = status
        else:
            data["status"] = False
    except:
        data["status"] = False
        data["error"] = str(sys.exc_info())
        logging.exception("startRecord: "+str(sys.exc_info()))
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
 
def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    if i._getexif():
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    return ret

@tester
@login_required
def get_photo_meta(request):
    import ast
    person_id = request.REQUEST['person_id']
    photo_id = request.REQUEST['photo_id']
    data = {}
    html = ''
    try:
        photoexif = get_object_or_404(models.PhotoExifData, photo_id=int(photo_id), person_id = int(person_id))
        if photoexif and photoexif.exif:
            exif = ast.literal_eval(photoexif.exif)
            for key in exif.iterkeys():
                html += u'%s - %s<br />' % (key, exif[key])
            data['meta'] = u'<div class="photometa_info">%s</div>' %  html
    except:
        pass
    return JsonResponse(data)

@tester
@permission_required('user_perms.perm_lists')
@permission_required('user_perms.perm_logs')
def get_journal_training_form(request):
    data = dict()
    if request.REQUEST.has_key('search'):
        search = request.REQUEST['search']
        results = {}
        try:
            personIds = models.PersonId.objects.filter(active=1)
            srch = search.split()
            i = 0
            while i<len(srch):
                f = srch[i]
                results = personIds.filter(Q(person__first_name__icontains=f) | Q(person__last_name__icontains=f) | Q(person__middle_name__icontains=f))
                i += 1
        except:
            pass
        data["results"] = results
        if len(results) > 0:
            data["search_status"] = True
        data["search"] = search
        return render_to_response_ex(request, "journal_training_search_result.html", data)

    data["di_name"]= request.REQUEST['di_name']
    if request.REQUEST['di_name'] == 'group':
        form = VcForms.TrainingPersonGroup(auto_id='%s')

    data["form"] = form

    return render_to_response_ex(request, "journal_training_wizard.html", data)

@tester
@login_required
def template_new(request):
    return render_to_response_ex(request, "template_new.html", {'version': VERSION, 'host': HTTP_HOST,  'select_page': 'template_new', 'user': request.user.username,})

def create_noise_person():
    import settings
    idPerson = models.PersonId.objects.create()
    user = models.Person.objects.create()
    try:
        user.first_name = str(idPerson.id)
        user.division = models.DivisionUser.objects.get(name = CONST_DIVISION)
        user.status = models.StatusUser.objects.get(name = CONST_STATUS, division=user.division)
        user.group = models.GroupPerson.objects.get(id = int(settings.noise_learning))
        user.action = 0
        user.id_person = idPerson.id
        user.save()    
        
        idPerson.person = user
        idPerson.save()
    except:
        logging.exception(str(sys.exc_info()))
        models.PersonId.objects.filter(id = idPerson.id).delete()
        models.Person.objects.filter(id = user.id).delete()
        return 0
    
    try:
        if models.List.objects.filter(id = settings.noise_learning).count() == 1 :
            list = models.List.objects.get(id = settings.noise_learning)
            list.active = True
            list.save()
    except:
        logging.exception("createPerson set vctive List")
    
    return idPerson 

@tester
@permission_required('user_perms.perm_lists')
#@transaction.commit_manually
def noiselist_result(request):
    data = dict()
    data.update(getDefaultParams(request, 'noiselist_result', None))
    #tid = transaction.savepoint()
    photos = []
    data['status_true'] = 0
    data['status_false'] = 0
    if 'journal_ids' in request.REQUEST:
        journal_ids = request.REQUEST['journal_ids'].split(',')
        res = create_noise_person()
        
        
        if res:
            data['person'] = res
            res = res.id
            data['res'] = res
            was_learn = False
            for id in journal_ids:
                photo = dict()
                try:
                    journals = models.Journal.objects.filter(id = int(id))
                    if journals.count() == 0:
                        continue
                    journal = journals[0]
                    file = open(journal.original.path, 'r+b')
                    data_file = file.read()
                    file.close()
                    
                    l, res2 = learning(data_file, str(res), face=journal.found_face, command='learnNoisePerson', return_res = True)
                    photo['res2'] = res2
                    if l and l is not None and not isinstance(l, list):
                        data['status_true']+=1
                        photo['status'] = True
                        was_learn = True
                    else:
                        data['status_false']+=1
                        photo['status'] = False     
                    photo['journal'] = journal
                except:
                    logging.exception("self_learning: "+str(sys.exc_info()))
                    photo['exception'] = str(sys.exc_info())
                photos.append(photo)
            if not was_learn:
                try:
                    models.PersonId.objects.filter(id = res).delete()
                    models.Person.objects.filter(id_person = res).delete()
                except:
                    logging.exception(str(sys.exc_info()))
    data['photos'] = photos
    data['all_learn_errors'] = ['Max Photos Restriction Achieved', 'Service Temporary Unavailable', 'Low Quality Picture', 'Internal Server Error', 'Face is not found', 'Bad face', 'Bad eyes', 'Bad Parameters', 'Small eyes distance', 'Picture must contain one face', 'Max Photos Restriction Achieved', 'Max Persons Restriction Achieved', 'Max Daemon Photos Restriction Achieved', 'Bad Value', 'Incorrect Parameter Name', 'Incorrect Xml Format', 'Permission Denied', 'Access Denied', 'Unsupported Method']
    #if len(photos)>0:
    #    transaction.savepoint_commit(tid)
    #else:
    #    transaction.savepoint_rollback(tid)
    
    return render_to_response_ex(request, "noiselist_result.html", data)

TMP_DIR_FOR_UPLOAD = "/tmp/upload_image2/"
@tester
@login_required
def get_upload_image(request, path):
    absolute_path = os.path.join(TMP_DIR_FOR_UPLOAD, path)
    if not os.path.isfile(absolute_path):
        raise Http404
    
    f = open(absolute_path, 'r+b')
    wrapper = f.read()
    f.close()
    response = HttpResponse(wrapper, content_type='image/jpg')
    response['Content-Length'] = len(wrapper)
    response['Content-Disposition'] = 'attachment;filename=photo%s.jpg' %(path)
    return response

def save_upload_file(data, name=""):
    if not os.path.isdir(TMP_DIR_FOR_UPLOAD):
        os.makedirs(TMP_DIR_FOR_UPLOAD)
        
    res = []
    images = []
    
    try:
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        res, images = b.faceDetect(data, api_version="2.0")
        b.close()
        del b
    except:
        logging.exception(str(sys.exc_info()))
        return res
    
    if len(res) >= 1 and len(images) >= 1:
        fileno, path = tempfile.mkstemp(dir=TMP_DIR_FOR_UPLOAD)
        f = open(path, 'w+b')
        f.write(data)
        f.close()
        
        filename = os.path.basename(path)
        
        import StringIO
        list = []
        i = 0
        
        for image in images:
            if "cutting_face" not in res[i]:
                continue
            res[i] = res[i]["cutting_face"]
            r = res[i]
            if 'face_string' not in r:
                continue
            data_image = StringIO.StringIO(image)
            try:
                img = Image.open(data_image)
            except:
                logging.exception(str(sys.exc_info()))
                return res
            face_width, face_height = img.size
            
            fileno, path_face = tempfile.mkstemp(dir=TMP_DIR_FOR_UPLOAD)
            img.save(path_face, 'PNG')
            
            filename_face = os.path.basename(path_face)
            r["filename"] = filename
            r["url_photo"] = reverse('get_upload_image', args=[filename])
            r["filename_face"] = filename_face
            r["url_photo_face"] = reverse('get_upload_image', args=[filename_face])
            r["face_width"] = face_width
            r["face_height"] = face_height
            r["face_dist"] = models.distCalculation(r["face_string"])
            if face_width>face_height :
                r["size_width"] = "120px"
                r["size_height"] = ""
            else:
                r["size_width"] = ""
                r["size_height"] = "120px"
            i += 1
    return res

@tester
@permission_required('user_perms.perm_lists')
def upload_multiple(request, select_page, id):
    
    data = {}
    data.update(getDefaultParams(request, 'lists', ""))
    
    faces = []
    errors = 0
    for files_name in request.FILES:
        for file in request.FILES.getlist(files_name):
            faces.extend(save_upload_file(file.read(), str(file)))
    data["faces"] = faces
    data["errors"] = errors
    data["select_sub_page"] = select_page
    data["id"] = id
    from videoclient import utils
    data['addperson'] = utils.idToName(id)
    from videoclient import models
    person = models.PersonId.objects.get(id = int(id)).person
    data['user'] = person.getDict()
    data['learn'] = True
    data['faces_json'] = json.dumps(faces)
    return render_to_response_ex(request, "upload_multiple.html", data)

@tester
@permission_required('user_perms.perm_lists')
def upload_multiple_resault(request, select_page, id):
    
    data = {}
    data.update(getDefaultParams(request, 'lists', ""))
    
    faces = json.loads(request.REQUEST["faces_json"])
    distortion = request.REQUEST["distortion"]
    from videoclient import utils
    addperson = utils.idToName(id)
     
    index = 0
    photos = []
    data['status_all'] = 0
    data['status_true'] = 0
    data['status_false'] = 0
    for face in faces:
        if ('face%s' %index) not in request.REQUEST:
            index = index+1
            continue
        
        index = index+1
        
        photo = dict()
        try:
            
            file = open(os.path.join(TMP_DIR_FOR_UPLOAD, face["filename_face"]), 'r+b')
            data_file = file.read()
            file.close()
            
            l, res2 = learning(data_file, str(addperson), face=face["full_face"], distortion=distortion, return_res = True)
            face['res2'] = res2
            data['status_all']+=1
            if l and l is not None and not isinstance(l, list):
                data['status_true']+=1
                face['status'] = True
            else:
                data['status_false']+=1
                face['status'] = False     
        except:
            logging.exception("self_learning: "+str(sys.exc_info()))
            face['exception'] = str(sys.exc_info())
            
    data["select_sub_page"] = select_page
    data["id"] = id
    data['addperson'] = addperson
    from videoclient import models
    person = models.PersonId.objects.get(id = int(id)).person
    data['user'] = person.getDict()
    data['learn'] = True
    data['all_learn_errors'] = ['Max Photos Restriction Achieved', 'Service Temporary Unavailable', 'Low Quality Picture', 'Internal Server Error', 'Face is not found', 'Bad face', 'Bad eyes', 'Bad Parameters', 'Small eyes distance', 'Picture must contain one face', 'Max Photos Restriction Achieved', 'Max Persons Restriction Achieved', 'Max Daemon Photos Restriction Achieved', 'Bad Value', 'Incorrect Parameter Name', 'Incorrect Xml Format', 'Permission Denied', 'Access Denied', 'Unsupported Method']
    data["faces"] = faces
    
    return render_to_response_ex(request, "upload_multiple_resault.html", data)        

@tester
@permission_required('user_perms.perm_settings')
def set_default_params(request):
    import settings
    status = True
    from videoclient import utils
    if "param" in request.REQUEST and "value" in request.REQUEST:
        status = utils.update_value_defaultparams(request.REQUEST["param"], request.REQUEST["value"], create_new = True);
    else:
        status = False
    return JsonResponse({"status": status})

#
# TODO
# Убрать если не нужно
# 
def translation_convert(request):
    all_strings = models.Translation.objects.filter(group__id=1)
    f = open("translations_en.txt", "w+")
    i = 0
    for s in all_strings:
        f.write('msgid "%s"\n' % s.phrase)
        f.write('msgstr "%s"\n' % s.translate)
        f.write('\n')
        i+=1
        #if s.translate:
        #    raise Exception(s.translate)
    f.close()
    
    f = open("translations_ru.txt", "w+")
    i = 0
    for s in all_strings:
        f.write('msgid "%s"\n' % s.phrase)
        f.write('msgstr ""\n')
        f.write('\n')
        i+=1
        #if s.translate:
        #    raise Exception(s.translate)
    f.close()
    
    raise Exception("Done! %s - objects" % i)

@tester
@permission_required('user_perms.perm_settings')
def check_similar_camera(request):
    try:
        form = VcForms.CheckSimilarCameraForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data.get("ip", None)
            url = form.cleaned_data.get("url", None)
            if ip:
                port = form.cleaned_data.get("port", None)
                if port and CommunicatorModels.Camera.objects.filter(ip=ip, port=port, active=True).count()>0:
                    return JsonResponse({"status": True})
                elif CommunicatorModels.Camera.objects.filter(ip=ip, active=True).count()>0: 
                    return JsonResponse({"status": True})
            elif url: 
                if CommunicatorModels.Camera.objects.filter(type="URL", url__startswith=url, active=True).count()>0:
                    return JsonResponse({"status": True})
    except:
        logging.exception("check_similar_camera: "+str(sys.exc_info()))
    return JsonResponse({"status": False})

@tester
@permission_required('user_perms.perm_security')
def security_main(request, uuid=None):
    data = dict()

    try:
        #
        # TODO
        # проверки переделать на новый разграничения прав
        #
        if check_rule(request, ident, is_sec=True):
            data.update(getDefaultParams(request, 'ident_js'))
            if data["access"] == 'Охранник' or data["access"] == 'Security':
                return HttpResponseRedirect(reverse('security', args=[]))
    except:
        pass

    
    res_get_all_active_cameras = getAllActiveCameras(url_reverse_name='js_ident')

    all_active_cameras = res_get_all_active_cameras["all_active_cameras"]
    data["communicator_errors_info"] = res_get_all_active_cameras["communicator_errors_info"]

    import datetime
    ctime = datetime.datetime.today()
    data["full_date"] = ctime.strftime("%d.%m.%Y")
    
    if not uuid:
        if 'uuid' in request.COOKIES:
            uuid = request.COOKIES['uuid']
            all_active_cameras_n = []
            for cam in all_active_cameras:
                if cam.uuid == uuid:
                    all_active_cameras_n.insert(0, cam)
                else:
                    all_active_cameras_n.append(cam)
            all_active_cameras = all_active_cameras_n
        else:
            #get first active uuid in system
            try:
                uuid = all_active_cameras[0].uuid
            except:
                uuid = None

    if uuid:
        camera = None
        try:
            camera = models.Camera.objects.filter(uuid=uuid)[0]
        except:
            camera = None
        
        videoclips = []
        try:
            videoclips = models.Roller.objects.exclude(tm_stop=None)
        except:
            logging.info("ident: get videoclips failed: " + str(sys.exc_info()))

        data["videoclips"] = videoclips.count()
        
        urls_arr = {}
        try:
            for l in models.List.objects.exclude(group=SELF_LEARNING):
                if get_object_or_404(models.Types, pk=l.type_id).division.id == division_person:
                    urls_arr[l.group_id] = '/anketaperson/'
                if get_object_or_404(models.Types, pk=l.type_id).division.id == division_employee:
                    urls_arr[l.group_id] = '/anketastaff/'
                if get_object_or_404(models.Types, pk=l.type_id).division.id == division_visitor:
                    urls_arr[l.group_id] = '/anketavisitor/'
        except:
            pass
        data['urls_arr'] = urls_arr
    
        data.update(getDefaultParams(request, 'ident_js'))
        data["all_active_cameras"] = all_active_cameras
        data["selected_camera"] = camera

        data["js_video_refresh_limit"] = 50
        data["boundFactor"] = get_value_defaultparams(journalBoundCoeff)
        data["page_refresh_time"] = 1000 * 60 * 20
        data["clearCarouselAfter"] = 70
        data["ident_page"] = True
        data["show_detect_alerts"] = int(get_value_defaultparams('show_detect_alerts'))
        data["add_to_carousel_fire_delay"] = int(get_value_defaultparams('add_to_carousel_fire_delay'))
        data["add_to_carousel_flash_delay"] = int(get_value_defaultparams('add_to_carousel_flash_delay'))
        data["add_to_carousel_smoke_delay"] = int(get_value_defaultparams('add_to_carousel_smoke_delay'))
        data["add_to_carousel_leftthings_delay"] = int(get_value_defaultparams('add_to_carousel_leftthings_delay'))
        data["draw_frame_fire_delay"] = int(get_value_defaultparams('draw_frame_fire_delay'))
        data["draw_frame_smoke_delay"] = int(get_value_defaultparams('draw_frame_smoke_delay'))
        data["draw_frame_flash_delay"] = int(get_value_defaultparams('draw_frame_flash_delay'))
        data["draw_frame_face_delay"] = int(get_value_defaultparams('draw_frame_face_delay'))
        data["draw_frame_leftthings_delay"] = int(get_value_defaultparams('draw_frame_leftthings_delay'))
        
        last_idents = []
        if camera:
            try:
                from django.db.models import Max
                last_ids = models.Journal.objects.filter(coeff__gte=float(data["boundFactor"]), camera=camera.pk).exclude(person=None).values('person_id').annotate(id_max=Max('id'))
                ids = []
                for l in last_ids:
                    ids.append(l["id_max"])

                last_idents = models.Journal.objects.filter(id__in=ids).order_by('-id')[:5]
            except:
                last_idents = []
            
            for i in last_idents:
                try:
                    name = "%s %s %s" % (i.person.person.first_name, i.person.person.last_name, i.person.person.middle_name)
                    setattr(i, "person_name", name)
                    setattr(i, "found_url", i.finded.url)
                except:
                    setattr(i, "person_name", _("Отсутствует..."))
                
                try:
                    if datetime.datetime.now().year != i.dt_last_fixed.year or datetime.datetime.now().month != i.dt_last_fixed.month or datetime.datetime.now().day != i.dt_last_fixed.day:
                        setattr(i, "detect_date", i.dt_last_fixed.strftime('%d.%m.%Y'))
                    else:
                        setattr(i, "detect_date", "")
                except:
                    setattr(i, "detect_date", "")
                setattr(i, "is_free", False)

        new_last_idents = []
        for i in last_idents:
            new_last_idents.append(i)
        while len(new_last_idents)<5:
            new_last_idents.append({"is_free": True})
        data["last_idents"] = new_last_idents

        last_journal_id = 0
        try:
            last_journal_id = models.Journal.objects.filter(camera=camera.pk).order_by('-id')[:1]
            if len(last_journal_id) > 0:
                last_journal_id = last_journal_id[0].pk
            else:
                last_journal_id = models.Journal.objects.all().order_by('-id')[:1]
                if len(last_journal_id) > 0:
                    last_journal_id = last_journal_id[0].pk
                else:
                    last_journal_id = 0
        except:
            logging.exception(str(sys.exc_info()))

        data["last_journal_id"] = int(last_journal_id)
            
        if len(data["last_idents"]) < 1:
            data["last_idents"] = None
        
        try:
            if DetectorLog.objects.count() > 0:
                last_row = DetectorLog.objects.all().order_by('-id')[:1]
                data["last_detect_message_id"] = int(last_row[0].id)
            else:
                data["last_detect_message_id"] = 0
        except:
            data["last_detect_message_id"] = None
        
        #get svg draw size and margin
        try:
            data["width"], data["height"], data["svg_margin"] = get_svg_draw_params(uuid)
        except:
            data["width"] = MAX_JS_VIDEO_SCREEN
            data["height"] = 480
            data["svg_margin"] = 0
        
    response = render_to_response_ex(request, "security_main.html", data)
    if uuid:
        response.set_cookie("uuid", uuid)
    return response
