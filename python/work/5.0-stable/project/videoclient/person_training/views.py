#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from videoclient.balancer import Balancer
from PIL import Image, ImageDraw
import os
import re
import json
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
from videoclient.utils import dataNavigation, draw_face_on_image, circleWithColor
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from videoclient.profile import models as ProfileModels
from PIL import Image
from PIL.ExifTags import TAGS
from django.utils import simplejson
from videoclient.views import  tester, getIdentData, getDefaultParams, initBalancer, JsonResponse, getAllActiveCameras, circleWithColor, getTimeInHMS, get_object_thumbnail, render_to_response_ex, circleWithColor, get_svg_draw_params, learning
from videoclient.videoanalytics.forms import LeftThingsDetectorForm, BackgroundDetectorForm, TestFromLogDetect, TestClearDataJournal
from time import time
import random
from django.core.urlresolvers import reverse
import ast
from cStringIO import StringIO as StringIO
import base64
from utils import getBalIdByName, getAllPhotosByName
from math import sqrt
from videoclient import forms as VcForms
from django.contrib.auth.decorators import permission_required

import sys

@tester
@permission_required('user_perms.perm_lists')    
def get_object_thumbnail(request, back_img, x1, y1, x2, y2, max_obj_width=120, max_obj_height=120, eye1=None, eye2=None, nose=None, chin=None, quad=None):
    objWidth = 0
    objHeight = 0
    COLOR = (255, 153, 0)
    
    try:
        object_frame = back_img.copy()
        fWidth, fHeight = object_frame.size
        
        object_frame = object_frame.crop((x1, y1, x2, y2))
        objWidth, objHeight = object_frame.size
        
        if objWidth > objHeight:
            newHeight = (((max_obj_width * 100) / objWidth) * objHeight) / 100
            object_frame.thumbnail((max_obj_width, newHeight), Image.ANTIALIAS)
        else:
            newWidth = (((max_obj_height * 100) / objHeight) * objWidth) / 100
            object_frame.thumbnail((newWidth, max_obj_height), Image.ANTIALIAS)
        
        objWidth, objHeight = object_frame.size
        factor = float(objWidth)/float(fWidth) if float(objWidth)/float(fWidth) < float(objHeight)/float(fHeight) else float(objHeight)/float(fHeight)
        draw = ImageDraw.Draw(object_frame)
        draw_face_on_image(draw, eye1=eye1, eye2=eye2, nose=nose, chin=chin, quad=quad, factor=factor, color=COLOR)  
        del draw
        
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
        margin_top = 0

    return obj_content, margin_top

def get_person_list(id):
    person_list = None
    try:
        person_list = get_object_or_404(models.List, pk=id)
    except:
        person_list = None
    return person_list

def get_person_url():
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
    
    return urls_arr

def get_person_url2():
    urls_arr = {}
    try:
        for l in models.List.objects.exclude(group=SELF_LEARNING):
            if get_object_or_404(models.Types, pk=l.type_id).division.id == division_person:
                urls_arr[l.group_id] = '/persons/'
            if get_object_or_404(models.Types, pk=l.type_id).division.id == division_employee:
                urls_arr[l.group_id] = '/staff/'
            if get_object_or_404(models.Types, pk=l.type_id).division.id == division_visitor:
                urls_arr[l.group_id] = '/visitors/'
    except:
        pass
    
    return urls_arr

@tester
@permission_required('user_perms.perm_lists')
def training(request, uuid=None, local_person_id=0):
    
    bal_id = None
    try:
        bal_id = getBalIdByName(local_person_id)
    except:
        bal_id = None

    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        
    photos = None
    if bal_id:
        #photos = getAllPhotosByName(local_person_id)
        try:
            photos = b.getPersonPhotos(bal_id)[0]
        except:
            photos = []
    
    person = None
    try:
        person = models.PersonId.objects.get(id = int(local_person_id)).person
    except:
        person = None

    data = dict()

    res_get_all_active_cameras = getAllActiveCameras(url_reverse_name='person_training2', ext_args=[local_person_id])
    all_active_cameras = res_get_all_active_cameras["all_active_cameras"]
    
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
    
    data = getIdentData(request)
    data.update(getDefaultParams(request, 'person_training'))
    data["person"] = person
    data['urls_arr'] = get_person_url()
    data["person_list"] = get_person_list(person.group.pk)
                    
    if camera:
        data["maxPhotos"] = 0
        try:
            data["maxPhotos"] = b.getParameter("control.max.photos.per.person")
        except:
            data["maxPhotos"] = 0
        
        if photos:
            photos = map(lambda x: int(x), photos)
            data["photos"] = photos
            data["photos_count"] = len(photos)
        else:
            data["photos"] = None
            data["photos_count"] = 0
        data["person_id"] = local_person_id
        data["bal_id"] = bal_id
        data["person_training_page"] = True
    
        data["all_active_cameras"] = all_active_cameras
        data["draw_frame_face_delay"] = int(get_value_defaultparams('draw_frame_face_delay'))
        
        #get svg draw size and margin
        try:
            data["width"], data["height"], data["svg_margin"] = get_svg_draw_params(camera.uuid)
        except:
            data["width"] = MAX_JS_VIDEO_SCREEN
            data["height"] = 480
            data["svg_margin"] = 0
    
    data["selected_camera"] = camera
    data["communicator_errors_info"] = res_get_all_active_cameras["communicator_errors_info"]
    
    b.close()
    del b

    return render_to_response_ex(request, "person_training.html", data)

@tester
@permission_required('user_perms.perm_lists')
def get_training_photos(request):
    person_id = request.POST["person_id"]
    
    bal_id = None
    try:
        bal_id = getBalIdByName(person_id)
    except:
        bal_id = None
    
    total_photos = 0
    all_photos = []
    
    try:
        if bal_id:
            photos = getAllPhotosByName(person_id)
            total_photos = len(photos["photos"])

            photo_ids = []
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            
            for p in photos["photos"]:
                photo_ids.append(int(p["num"]))
            
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            if len(photo_ids) > 0:
                for p_id in photo_ids:
                    try:
                        wrapper = None
                        images, params = b.getPersonPhotoWithParams(bal_id, p_id)
                        wrapper = images[0]
                        
                        im = StringIO(wrapper)
                        back_img = Image.open(im)
                        back_img = back_img.convert("RGB")
                        width, height = back_img.size
                        obj_content, margin_top = get_object_thumbnail(request, back_img, 0, 0, width, height)
                        all_photos.append({'image': base64.b64encode(obj_content), 'margin_top': margin_top, 'photo_id': p_id})
                    except:
                        all_photos.append({'image': '', 'margin_top': '', 'photo_id': p_id})
        
            b.close()
            del b
    except:
        all_photos = []
    
    result = {'all_photos': all_photos, 'total_photos': total_photos}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_lists')
def edit_photos(request, uuid=None, local_person_id=0):
    
    person = None
    try:
        person = models.PersonId.objects.get(id = int(local_person_id)).person
    except:
        person = None
        
    exclude_photos = []
    try:
        exclude_photos = request.GET["ex"]
        exclude_photos = map(lambda x: int(x), exclude_photos.split(','))
    except:
        exclude_photos = []
    
    bal_id = None
    try:
        bal_id = getBalIdByName(local_person_id)
    except:
        bal_id = None
    
    camera = None
    try:
        camera = models.Camera.objects.filter(uuid=uuid)[0]
    except:
        camera = None
    
    all_active_cameras = getAllActiveCameras(url_reverse_name='person_training2', ext_args=[local_person_id])
    
    if not uuid:
        #get first active uuid in system
        try:
            uuid = all_active_cameras[0].uuid
        except:
            uuid = None
    
    if camera:
        total_photos = 0
        all_photos = []
        
        if bal_id:
            photos = getAllPhotosByName(local_person_id)
            photo_ids = []
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            
            for p in photos["photos"]:
                if int(p["num"]) in exclude_photos:
                    photo_ids.append(int(p["num"]))
                    total_photos+=1
            
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            if len(photo_ids) > 0:
                for p_id in photo_ids:
                    try:
                        wrapper = None
                        images, params = b.getPersonPhotoWithParams(bal_id, p_id)
    
                        #checking for eyes
                        eyes = None
                        try:
                            eyes = map(lambda x: float(x), params["response"][0]["info"][0]["eyes"].split(","))
                        except:
                            eyes = None
                        
                        if eyes:
                            eye1 = None
                            try:
                                eye1 = [eyes[0], eyes[1]]
                            except:
                                eye1 = None
                            
                            eye2 = None
                            try:
                                eye2 = [eyes[2], eyes[3]]
                            except:
                                eye2 = None
                        
                        #checking for nouse
                        nose = None
                        try:
                            nose = map(lambda x: float(x), params["response"][0]["info"][0]["nose"].split(","))
                        except:
                            nose = None
                        
                        #checking for nouse
                        chin = None
                        try:
                            chin = map(lambda x: float(x), params["response"][0]["info"][0]["chin"].split(","))
                        except:
                            chin = None
                        
                        #checking for quad
                        quad = None
                        try:
                            quad = map(lambda x: float(x), params["response"][0]["info"][0]["quad"].split(","))
                        except:
                            quad = None
                            
                        eyes_distance = 0
                        if eye1 and eye2:
                            try:
                                eyes_distance = round(float(sqrt(((eye1[0] - eye2[0])**2) + ((eye1[1] - eye2[1])**2))), 1)
                            except:
                                eyes_distance = 0
                        
                        
                        wrapper = images[0]
                        
                        im = StringIO(wrapper)
                        back_img = Image.open(im)
                        back_img = back_img.convert("RGB")
                        width, height = back_img.size
                        obj_content, margin_top = get_object_thumbnail(request, back_img, 0, 0, width, height, eye1=eye1, eye2=eye2, nose=nose, chin=chin, quad=quad)
                        all_photos.append({'image': base64.b64encode(obj_content), 'margin_top': margin_top, 'photo_id': p_id, 'w': width, 'h': height, 'eyes_distance': eyes_distance})
                    except:
                        all_photos.append({'error': True, 'photo_id': p_id})
                        logging.info("Edit training photos from camera: " + str(sys.exc_info()))
        
            b.close()
            del b
    
        data = dict()
        data = getIdentData(request)
        data.update(getDefaultParams(request, 'person_training'))
        data["bal_id"] = bal_id
        data["person"] = person
        data['urls_arr'] = get_person_url()
        data["person_list"] = get_person_list(person.group.pk)
        data["all_active_cameras"] = all_active_cameras
        data["total_photos"] = total_photos
        data["all_photos"] = all_photos
        data["page_show"] = True
        if len(exclude_photos) == 0:
            data["page_show"] = False
        data["back_camera_url"] = reverse('person_training2', args=[camera.uuid, local_person_id])
    
    data["selected_camera"] = camera
    
    return render_to_response_ex(request, "training_photos.html", data)

@tester
@permission_required('user_perms.perm_lists')
def edit_persons(request):
    data = dict()
    data = getDefaultParams(request, 'journal', project=None)

    if request.REQUEST.has_key('pids'):
        pids = request.REQUEST["pids"]
        data["t_pids"] = pids
        try:
            pids = map(lambda x: int(x), pids.split(','))
        except:
            pids = []

        journal_persons = models.Journal.objects.filter(id__in=pids)
        
        data["journal_persons"] = journal_persons
        data["total_persons"] = len(journal_persons)
    
    return render_to_response_ex(request, "training_persons.html", data)

@tester
@permission_required('user_perms.perm_lists')
def person_form(request):
    data = dict()
    data = getDefaultParams(request, 'journal', project=None)

    if request.REQUEST.has_key('pids'):
        pids = request.REQUEST["pids"]
        data["pids"] = pids
    if request.REQUEST.has_key('tpids'):
        tpids = request.REQUEST["tpids"]
        data["t_pids"] = tpids
    
    exclude_dict = [settings.SELF_LEARNING, settings.noise_learning]
    data["lists"] = models.List.objects.exclude(group__id__in=exclude_dict).filter(active=True)
    data["category"] = models.Category.objects.filter()
    data["all_statuses"] = models.StatusUser.objects.filter()
    data['urls_arr'] = get_person_url()
    #raise Exception(data["all_divisions"])

    return render_to_response_ex(request, "get_create_anketa.html", data)

@tester
@permission_required('user_perms.perm_lists')
def get_or_create_person(request):
    form = VcForms.PersonChangeForm(request.GET, request.FILES)
    if form.is_valid():
        person = models.Person(first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"], middle_name=form.cleaned_data["middle_name"], action=0, group_id=form.cleaned_data["group"], status_id=form.cleaned_data["status"], category_id=form.cleaned_data["category"])
        person.save()
        person_id = models.PersonId(person_id=person.id, active=True)
        person_id.save()
        person.id_person = person_id.id
        person.save()
        result = {'res': 'success', 'person_id': person.id}
    else:
        result = {'res': 'error'}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_lists')
def training_result(request):
    from videoclient import models
    
    data = dict()
    data = getDefaultParams(request, 'journal', project=None)
    
    pids = None
    if request.REQUEST.has_key('pids'):
        pids = request.REQUEST["pids"]

    person_id = None
    if request.REQUEST.has_key('person_id'):
        person_id = request.REQUEST["person_id"]
    
    if pids and person_id:
        from videoclient import utils
        pids = map(lambda x: int(x), pids.split(","))
        j_persons = models.Journal.objects.filter(id__in=pids)
        person = models.Person.objects.get(id = int(person_id))
        data['urls_arr'] = get_person_url()

        data['status_all'] = 0
        data['status_true'] = 0
        data['status_false'] = 0

        for face in j_persons:
            try:
                file = open(settings.MEDIA_ROOT + str(face.original), 'r+b')
                data_file = file.read()
                file.close()
                
                l, res2 = learning(data_file, str(person.id_person), face=face.found_face, return_res = True)
                setattr(face, "res2",  res2)
                data['status_all']+=1
                if l and l is not None and not isinstance(l, list):
                    data['status_true']+=1
                    setattr(face, "status",  True)
                else:
                    data['status_false']+=1
                    setattr(face, "status",  False)
            except:
               logging.exception("self_learning: " + str(sys.exc_info()))
               setattr(face, "exception",  str(sys.exc_info()))

        data["person"] = person
        data["faces"] = j_persons
        
    return render_to_response_ex(request, "result_training.html", data)