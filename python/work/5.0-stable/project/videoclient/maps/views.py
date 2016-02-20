#coding=utf-8
from django.shortcuts import render_to_response
from videoclient import utils as vUtils
from monitoring import utils
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from videoclient.views import  tester, getIdentData, get_camera_last_frame, is_active_camera
from videoclient.utils import getDefaultParams
import settings
import commands
import logging
import json
import sys
import re
from django.utils import simplejson
from videoclient.maps.forms import MapForm, MapImageForm, MapTerminalForm, MapCameraForm
from django.forms.util import ErrorList
from models import *
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.safestring import mark_safe
import tempfile
import os
import Image
from shutil import copyfile
from videoclient.models import Camera, Lens
from videoclient.communicator import Communicator
from videoclient.views import initCommunicators, render_to_response_ex
from django.contrib.auth.decorators import permission_required
from StringIO import StringIO

MAP_IMAGE_SIZE = (1200, 768)

def mapthumbnail(filename, size):
    from time import time
    imgName = u'%s.jpg' % int(time())
    newfile = settings.MAP_IMAGES + imgName
    try:
        path = os.path.dirname(newfile)
        if not os.path.exists(path):
            os.makedirs(path)
        iimg = Image.open(filename)
        rgbimg = iimg.convert('RGB')
        width, height = rgbimg.size
        if width > size[0] or height > size[1]:
            rgbimg.thumbnail(size)
        rgbimg.save(newfile)
        return imgName
    except:
        logging.exception("map image upload thumbnail: "+str(sys.exc_info()))
        return ''

def get_image_size(map):
    try:
        image_file = settings.MAP_IMAGES + str(map.image)
        img = Image.open(image_file)
        # get the image's width and height in pixels
        w, h = img.size
        return {'width': w, 'height': h}
    except:
        return {'width': '', 'height': ''}

@tester
@permission_required('user_perms.perm_maps')
def get_image(request, id=None):
    try:
        map = get_object_or_404(Map, id=int(id))
        filename = settings.MAP_IMAGES + str(map.image)
        f = open(filename, "r+b")
        wrapper =  f.read() 
        f.close()
        
        response = HttpResponse(wrapper, content_type='image/jpg')
        response['Content-Length'] = len(wrapper)
        response['Content-Disposition'] = 'attachment;filename=%s.jpg' % map.image
        return response
    except:
        return True

def get_map_object_type_choices(form_mode='object_type_choices', id=None):
    data = dict()
    data["selected_id"] = id
    data[form_mode] = True
    objTypeChoices = ''
    data["objTypes"] = dict()
    try:
        data["objTypes"] = MapObjectType.objects.all().order_by('name')
    except:
        pass
    objTypeChoices = mark_safe(render_to_string("forms.html", data))
    data[form_mode] = False
    return objTypeChoices

def get_map_city_choices(id=None):
    data = dict()
    data["selected_id"] = id
    data["city_choices"] = True
    citiesChoices = ''
    data["mapcities"] = dict()
    try:
        data["mapcities"] = MapCity.objects.all().order_by('name')
    except:
        pass
    citiesChoices = mark_safe(render_to_string("forms.html", data))
    data["city_choices"] = False
    return citiesChoices

def get_map_objnames_choices(objtype_id=None, city_id=None, objname_id=None):
    data = dict()
    data["selected_id"] = objname_id
    data["objname_choices"] = True
    objnameChoices = ''
    data["obj_names"] = dict()
    try:
        data["obj_names"] = MapObject.objects.filter(map_object_type__id=objtype_id, city__id=city_id).order_by('name')
    except:
        pass
    objnameChoices = mark_safe(render_to_string("forms.html", data))
    data["objname_choices"] = False
    return objnameChoices

@tester
@permission_required('user_perms.perm_maps')
def map(request, map_id=None):

    data = dict()
    data = getIdentData(request)
    data.update(getDefaultParams(request, 'maps'))
    
    all_cameras = None
    try:
        all_cameras = Camera.objects.filter().order_by('pk')
    except:
        all_cameras = None
    
    data["all_cameras"] = all_cameras    
    
    map = dict()
    if map_id:
        try:
            map = get_object_or_404(Map, id=int(map_id))
        except:
            pass
    else:
        try:
            map = Map.objects.filter()[0]
        except:
            pass
    data["map"] = map
    data["map_is_exist"] = True
    
    data["image_size"] = get_image_size(map)
    
    try:
        map_obj_type_id = map.obj_type.pk
        map_obj_name_id = map.obj_name.pk
        map_city_id = map.city.pk
    except:
        map_obj_type_id = None
        map_obj_name_id = None
        map_city_id = None
        data["map_is_exist"] = False
        return render_to_response_ex(request, "maps.html", data)

    data["objTypeChoices"] = get_map_object_type_choices(form_mode='object_type_choices2', id=map_obj_type_id)
    data["cityChoices"] = get_map_city_choices(map.city.pk)
    data["objNames"] = get_map_objnames_choices(objtype_id=map_obj_type_id, city_id=map_city_id, objname_id=map_obj_name_id)
    
    data["map_terminals"] = MapTerminal.objects.filter(map=map.pk)
    data["map_terminal_cameras"] = MapCamera.objects.filter(map=map.pk)
    
    return render_to_response_ex(request, "maps.html", data)

@tester
@permission_required('user_perms.perm_maps')
@permission_required('user_perms.perm_maps_edit')
def view_add_map(request):
    data = dict()
    result = dict()

    data["objTypeChoices"] = get_map_object_type_choices()

    data["add_map_form"] = True
    if request.method == 'POST':
        if request.POST.has_key('upload_image'):
            form = MapImageForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    file = form.cleaned_data["image"]
                    input_file = ''
                    for t in file: input_file += t
                    fileno, path = tempfile.mkstemp()
                    f = open(path, 'w+b')
                    f.write(input_file)
                    f.close()
                    
                    result = {'res': 'success'}
                except:
                    result = {'res': 'not valid'}
                
                try:
                    mapImage = mapthumbnail(path, MAP_IMAGE_SIZE)
                    if not mapImage == '':
                        map = get_object_or_404(Map, id=int(request.POST['map_id']))
                        map.image=mapImage
                        map.save()
                except:
                    pass
            else:
                result = {'res': 'not valid'}
            return HttpResponse(simplejson.dumps(result), mimetype='json')
        else:
            try:
                form = MapForm(request.POST, request.FILES)
                if form.is_valid():
                    #смотрим на наличие города в базе, если есть берем его id, если нет, создаем новый
                    try:
                        city = form.cleaned_data["city"]
                        cities = MapCity.objects.filter(name=city)
                        if len(cities)>0:
                            try:
                                mapCity = cities[0]
                            except:
                                pass
                        else:
                            mapCity = MapCity(name=city)
                            mapCity.save()
                    except:
                        pass
                    
                    #смотрим тип объекта в базе, если есть берем его id, если нет, создаем новый
                    try:
                        obj_type = form.cleaned_data["obj_type"]
                        if not request.POST['new_obj_type'] == '':
                            objType = MapObjectType(name=obj_type)
                            objType.save()
                        else:
                            obj_types = MapObjectType.objects.filter(id=int(obj_type))
                            objType = obj_types[0]
                    except:
                        pass
                    
                    #смотрим на наличие названия объекта в базе, если есть берем его id, если нет, создаем новый
                    try:
                        obj_name = form.cleaned_data["obj_name"]
                        obj_names = MapObject.objects.filter(name=obj_name, map_object_type=objType, city=mapCity)
                        if len(obj_names)>0:
                            try:
                                mapObjName = obj_names[0]
                            except:
                                pass
                        else:
                            mapObjName = MapObject(map_object_type=objType, name=obj_name, city=mapCity)
                            mapObjName.save()
                    except:
                        pass
    
                    try:
                        map = Map(city_id=mapCity.id, obj_type_id=objType.id, obj_name_id=mapObjName.id)
                        map.save()
                    except:
                        pass
                    result = {'res': 'success', 'map_id': map.id}
                    return HttpResponse(simplejson.dumps(result), mimetype='application/json')
                else:
                    data["form"] = form
                    data["city"] = request.REQUEST['city']
                    data["obj_name"] = request.REQUEST['obj_name']
                    result = {'res': 'not valid', 'html': render_to_string("forms.html", data), 'add_map_form': True}
            except:
                logging.exception("map add form: "+str(sys.exc_info()))
            return HttpResponse(simplejson.dumps(result), mimetype='application/json')
    else:
        result = {'res': 'success', 'html': render_to_string("forms.html", data), 'add_map_form': True}

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
@permission_required('user_perms.perm_maps_edit')
def add_terminal(request):
    data = dict()
    result = dict()

    if request.method == 'POST':
        data["terminal_name"] = request.POST["name"]
        data["terminal_model_id"] = int(request.POST["model"])
        data["terminal_number"] = request.POST["number"]
        data["terminal_direction"] = request.POST["direction"]
        data["terminal_description"] = request.POST["description"]

    data["terminal_model_choices"] = True
    data["terminal_model_types"] = MapTerminalType.objects.all()
    data["terminal_select_choices"] = render_to_string("forms.html", data)
    data["terminal_model_choices"] = False
    
    data["terminal_direction_choices"] = True
    data["terminal_direction_types"] = Direction.objects.all().order_by('pk')
    data["terminal_select_direction_choices"] = render_to_string("forms.html", data)
    data["terminal_direction_choices"] = False
    
    data["add_terminal_form"] = True
    if request.method == 'POST':
        form = MapTerminalForm(request.POST)
        if form.is_valid():
            try:
                map_terminal = MapTerminal(name=request.POST["name"], model_id=int(request.POST["model"]), number=int(request.POST["number"]), direction_id=int(request.POST["direction"]), description=request.POST["description"], map_id=int(request.POST["map"]), x=0, y=0)
                map_terminal.save()
            except:
                pass
            result = {'res': 'success', 'id': map_terminal.id, 'x': map_terminal.x, 'y': map_terminal.y}
        else:
            data["form"] = MapTerminalForm(request.POST)
            result = {'res': 'not valid', 'html': render_to_string("forms.html", data)}
    else:
        data["form"] = MapTerminalForm()
        result = {'res': 'success', 'html': render_to_string("forms.html", data)}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
@permission_required('user_perms.perm_maps_edit')
def edit_terminal(request):
    data = dict()
    result = dict()
    
    id = int(request.REQUEST["id"])
    terminal = get_object_or_404(MapTerminal, id=id)
        
    if request.method == 'GET':
        data["terminal_name"] = terminal.name
        data["terminal_model_id"] = terminal.model.id
        data["terminal_number"] = terminal.number
        data["terminal_direction"] = terminal.direction.id
        data["terminal_description"] = terminal.description

    data["terminal_model_choices"] = True
    data["terminal_model_types"] = MapTerminalType.objects.all()
    data["terminal_select_choices"] = render_to_string("forms.html", data)
    data["terminal_model_choices"] = False
    
    data["terminal_direction_choices"] = True
    data["terminal_direction_types"] = Direction.objects.all().order_by('pk')
    data["terminal_select_direction_choices"] = render_to_string("forms.html", data)
    data["terminal_direction_choices"] = False
    
    data["cameras"] = MapCamera.objects.filter(terminal=terminal.pk)
    
    data["add_terminal_form"] = True
    if request.method == 'GET':
        result = {'res': 'success', 'html': render_to_string("forms.html", data)}
    if request.method == 'POST':
        form = MapTerminalForm(request.POST)
        if form.is_valid():
            try:
                terminal = get_object_or_404(MapTerminal, id=int(request.REQUEST["id"]))
                terminal.name = request.POST["name"]
                terminal.model_id = int(request.POST["model"])
                terminal.number = request.POST["number"]
                terminal.direction_id = int(request.POST["direction"])
                terminal.description = request.POST["description"]
                terminal.map_id = int(request.POST["map"])
                terminal.save()
                result = {'res': 'success'}
            except:
                result = {'res': 'not valid'}
        else:
            data["form"] = MapTerminalForm(request.POST)
            result = {'res': 'not valid', 'html': render_to_string("forms.html", data)}

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
def get_terminal_info(request):
    data = dict()
    data["terminal_title_info_form"] = True
    id = int(request.REQUEST["id"])
    terminal = get_object_or_404(MapTerminal, id=id)
    data["terminal_cameras"] = MapCamera.objects.filter(terminal=terminal.pk)
    data["terminal_name"] = terminal.name
    data["terminal_model"] = terminal.model.name
    data["terminal_number"] = terminal.number
    data["terminal_direction"] = terminal.direction.name
    data["terminal_description"] = terminal.description
        
    result = {'res': 'success', 'html': render_to_string("forms.html", data)}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
def get_camera_info(request):
    data = dict()
    data["camera_title_info_form"] = True
    id = int(request.REQUEST["id"])
    data["camera"] = get_object_or_404(MapCamera, id=id)
        
    result = {'res': 'success', 'html': render_to_string("forms.html", data)}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
def get_camera_video(request):
    data = dict()
    data["camera_video_form"] = True
    id = int(request.REQUEST["id"])
    data["camera"] = get_object_or_404(MapCamera, id=id)
        
    result = {'res': 'success', 'html': render_to_string("forms.html", data)}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
def get_terminal_full_info(request):
    data = dict()
    
    terminal = get_object_or_404(MapTerminal, id=int(request.REQUEST["id"]))
    data["terminal"] = terminal
    data["map"] = get_object_or_404(Map, id=int(request.REQUEST["map_id"]))
    
    data["terminal_cameras_choices"] = True
    cameras = MapCamera.objects.filter(terminal=terminal.pk).order_by('pk')
    data["terminal_cameras"] = cameras
    data["terminal_select_camera_choices"] = render_to_string("forms.html", data)
    data["terminal_cameras_choices"] = False
    
    data["terminal_full_info"] = True
        
    result = {'res': 'success', 'html': render_to_string("forms.html", data), 'camera_id': cameras[0].pk}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
@permission_required('user_perms.perm_maps_edit')
def save_terminal_position(request):
    termIds = request.REQUEST["termIds"]
    termIds = termIds.split(',')
    termX = request.REQUEST["termX"]
    termX = termX.split(',')
    termY = request.REQUEST["termY"]
    termY = termY.split(',')
    
    i = 0
    success = True
    result = {'res': 'success'}
    for id in termIds:
        try:
            map_terminal = get_object_or_404(MapTerminal, id=id)
            map_terminal.x = int(str(termX[i]).replace('px', ''))
            map_terminal.y = int(str(termY[i]).replace('px', ''))
            map_terminal.save()
        except:
            success = False
        i+=1
    
    if not success:
        result = {'res': 'error'}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
def update_objname_select(request):
    if request.method == 'POST':
        html = get_map_objnames_choices(objtype_id=request.POST["obj_type_id"], city_id=request.POST["city_id"])
        result = {'res': 'success', 'html': html}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
@permission_required('user_perms.perm_maps_edit')
def clear_map_terminals(request):
    result = {'res': 'success'}
    try:
        MapTerminal.objects.filter(map=int(request.REQUEST["map_id"])).delete()
    except:
        result = {'res': 'error'}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
def delete_map_terminal(request):
    result = {'res': 'success'}
    try:
        get_object_or_404(MapTerminal, id=int(request.REQUEST["id"])).delete()
        MapCamera.objects.filter(terminal=int(request.REQUEST["id"])).delete()
    except:
        result = {'res': 'error'}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
@permission_required('user_perms.perm_maps_edit')
def delete_terminal_camera(request):
    result = {'res': 'success'}
    cam_id = int(str(request.REQUEST["id"]).replace('camera_', ''))
    try:
        get_object_or_404(MapCamera, id=cam_id).delete()
    except:
        result = {'res': 'error'}
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
@permission_required('user_perms.perm_maps_edit')
def add_camera(request):
    data = dict()
    map_id = int(request.REQUEST["map_id"])

    if request.method == 'POST':
        data["terminal_id"] = int(request.POST["terminal"])
        data["terminal_camera_id"] = int(request.POST["camera"])
        data["terminal_lens_id"] = int(request.POST["lens"])
        data["visible_objects"] = request.POST["visible_objects"]
        data["terminal_direction"] = int(request.POST["direction"])
        data["visibility"] = request.POST["visibility"]
        data["range"] = request.POST["range"]
        data["recognition"] = request.POST["recognition"]
        data["focal"] = request.POST["focal"]
        data["angle"] = request.POST["angle"]

    data["camera_terminals_form"] = True
    data["terminals"] = MapTerminal.objects.filter(map=map_id)
    data["map_terminal_choices"] = render_to_string("forms.html", data)
    data["camera_terminals_form"] = False
    
    data["terminal_direction_choices"] = True
    data["terminal_direction_types"] = Direction.objects.all().order_by('pk')
    data["terminal_select_direction_choices"] = render_to_string("forms.html", data)
    data["terminal_direction_choices"] = False
    
    data["terminal_camera_choices"] = True
    data["terminal_cameras"] = Camera.objects.filter(active=True).order_by('pk')
    data["terminal_select_camera_choices"] = render_to_string("forms.html", data)
    data["terminal_camera_choices"] = False
    
    data["terminal_lens_choices"] = True
    data["terminal_lens"] = Lens.objects.all().order_by('pk')
    data["terminal_select_lens_choices"] = render_to_string("forms.html", data)
    data["terminal_lens_choices"] = False
    
    data["add_camera_form"] = True
    if request.method == 'GET':
        data["visibility"] = '10.0'
        data["range"] = '5.0'
        data["recognition"] = '3.5'
        data["focal"] = '2.0'
        data["angle"] = '45.0'
        result = {'res': 'success', 'html': render_to_string("forms.html", data)}
        return HttpResponse(simplejson.dumps(result), mimetype='application/json')

    if request.method == 'POST':
        form = MapCameraForm(request.POST)
        if form.is_valid():
            try:
                map_camera = MapCamera(map_id=int(request.POST["map_id"]), terminal_id=int(request.POST["terminal"]), camera_id=int(request.POST["camera"]), lens_id=int(request.POST["lens"]), direction_id=int(request.POST["direction"]), visible_objects=request.POST["visible_objects"], visibility=float(request.POST["visibility"]), range=float(request.POST["range"]), recognition=float(request.POST["recognition"]), focal=float(request.POST["focal"]), angle=float(request.POST["angle"]))
                map_camera.save()
            except:
                pass
            result = {'res': 'success', 'html': render_to_string("forms.html", data), 'camera_id': map_camera.id}
        else:
            result = {'res': 'not valid', 'html': render_to_string("forms.html", data)}

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_maps')
@permission_required('user_perms.perm_maps_edit')
def edit_camera(request):
    data = dict()
    result = dict()
    
    map_id = int(request.REQUEST["map_id"])
    id = int(str(request.REQUEST["id"]).replace('camera_', ''))
    if request.method == 'GET':
        map_camera = get_object_or_404(MapCamera, id=id)
        data["terminal_id"] = map_camera.terminal.id
        data["terminal_camera_id"] = map_camera.camera.id
        data["terminal_lens_id"] = map_camera.lens.id
        data["terminal_direction"] = map_camera.direction.id
        data["visible_objects"] = map_camera.visible_objects
        data["visibility"] = str(map_camera.visibility).replace(',','.')
        data["range"] = str(map_camera.range).replace(',','.')
        data["recognition"] = str(map_camera.recognition).replace(',','.')
        data["focal"] = str(map_camera.focal).replace(',','.')
        data["angle"] = str(map_camera.angle).replace(',','.')

    data["camera_terminals_form"] = True
    data["terminals"] = MapTerminal.objects.filter(map=map_id)
    data["map_terminal_choices"] = render_to_string("forms.html", data)
    data["camera_terminals_form"] = False
    
    data["terminal_direction_choices"] = True
    data["terminal_direction_types"] = Direction.objects.all().order_by('pk')
    data["terminal_select_direction_choices"] = render_to_string("forms.html", data)
    data["terminal_direction_choices"] = False
    
    data["terminal_camera_choices"] = True
    data["terminal_cameras"] = Camera.objects.filter(active=True).order_by('pk')
    data["terminal_select_camera_choices"] = render_to_string("forms.html", data)
    data["terminal_camera_choices"] = False
    
    data["terminal_lens_choices"] = True
    data["terminal_lens"] = Lens.objects.all().order_by('pk')
    data["terminal_select_lens_choices"] = render_to_string("forms.html", data)
    data["terminal_lens_choices"] = False
    
    data["add_camera_form"] = True
    if request.method == 'GET':
        result = {'res': 'success', 'html': render_to_string("forms.html", data)}
    if request.method == 'POST':
        form = MapCameraForm(request.POST)
        if form.is_valid():
            try:
                map_camera = get_object_or_404(MapCamera, id=id)
                map_camera.terminal_id = int(request.POST["terminal"])
                map_camera.camera_id = int(request.POST["camera"])
                map_camera.lens_id = int(request.POST["lens"])
                map_camera.visible_objects = request.POST["visible_objects"]
                map_camera.direction_id = int(request.POST["direction"])
                map_camera.focal = float(request.POST["focal"])
                map_camera.angle = float(request.POST["angle"])
                map_camera.visibility=float(request.POST["visibility"])
                map_camera.range=float(request.POST["range"])
                map_camera.recognition=float(request.POST["recognition"])
                map_camera.save()
                result = {'res': 'success', 'terminal_id': map_camera.terminal.id, 'camera_id': map_camera.id, 'direction': str(map_camera.direction.id) }
            except:
                result = {'res': 'not valid'}
        else:
            data["form"] = MapCameraForm(request.POST)
            result = {'res': 'not valid', 'html': render_to_string("forms.html", data)}

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def get_communicator_camera_num(camera):
    num = None

    try:
        c = Communicator(camera.commun.host, int(camera.commun.port))
        cameras = c.getCameras()
        for cam in cameras:
            if str(cam["ip"]) == str(camera.ip):
                num = int(cam["numcamera"])
                break
        c.close()
        del c
    except:
        logging.exception("get_communicator_camera_num get numcamera error:" + str(sys.exc_info()))

    return num

@tester
@permission_required('user_perms.perm_maps')
def get_video_frame(request):
    import base64
    image = None
    jpg = None
    
    try:
        if request.REQUEST.has_key('add_edit'):
            camera = get_object_or_404(Camera, id=int(request.REQUEST["camera_id"]), active=True)
            host = camera.commun.host
            port = int(camera.commun.port)
            cam_id = get_communicator_camera_num(camera)
            if cam_id == None:
                result = {'res': 'error'}
                return HttpResponse(simplejson.dumps(result), mimetype='application/json')

        elif request.REQUEST.has_key('full_info'):
            camera = get_object_or_404(MapCamera, id=int(request.REQUEST["camera_id"]), camera__active=True)
            host = camera.camera.commun.host
            port = int(camera.camera.commun.port)
            cam_id = get_communicator_camera_num(camera.camera)
            if cam_id == None:
                result = {'res': 'error'}
                return HttpResponse(simplejson.dumps(result), mimetype='application/json')

        else:
            camera = get_object_or_404(Camera, id=int(request.REQUEST["camera_id"]), active=True)
            host = camera.commun.host
            port = int(camera.commun.port)
            cam_id = get_communicator_camera_num(camera)
            if cam_id == None:
                result = {'res': 'error'}
                return HttpResponse(simplejson.dumps(result), mimetype='application/json')
    except:
        result = {'res': 'error'}
        logging.exception("get video frame no such camera in system or camera is not active")
        return HttpResponse(simplejson.dumps(result), mimetype='application/json')

    try:
        error_remark = ""
        frame_content = ""
        camera = get_object_or_404(Camera, id=int(request.REQUEST["camera_id"]), active=True)
        if camera:        
            frame_content = get_camera_last_frame(camera)
            if not frame_content:
                error_remark = "can't get video frame"                
        else:
           error_remark = "camera isn't active"
        result = {'res': 'success', 'image': base64.b64encode(frame_content), 'error_remark': error_remark}
    except:
        logging.exception("get video frame communicator error:" + str(sys.exc_info()))
        result = {'res': 'error'}

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')
    #response = HttpResponse(image, content_type='application/jpeg')
    #response['Content-Length'] = len(image)
    #response['Content-Disposition'] = 'attachment;filename=123.jpg'
    #return response