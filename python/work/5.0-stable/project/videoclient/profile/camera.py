# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from videoclient import views
from videoclient.views import tester
from videoclient.profile import models
from videoclient.communicator import models as VModels
from videoclient.communicator import Communicator
from videoclient.balancer import Balancer
from django.utils.translation import ugettext, ugettext_lazy as _
import json
import logging
import sys
from django.contrib.auth.decorators import permission_required

params = [{"param": ['brightness'], "name": 'setBrightnessCamera', "communicator": True},
          {"param": ['sharpness'], "name": 'setSharpnessCamera', "communicator": True},
          {"param": ['saturation'], "name": 'setSaturationCamera', "communicator": True},
          {"param": ['contrast'], "name": 'setContrastCamera', "communicator": True},
          {"param": ['quality'], "name": 'setQualityCamera', "communicator": True},
          {"param": ['light'], "name": 'setIlluminationMode', "communicator": True},
          {"param": ['qualitylow'], "name": 'setLowLight', "communicator": True},
          {"param": ['shortexposures'], "name": 'setShortexposures', "communicator": True},
          {"param": ['frequency'], "name": 'setLightHZCamera', "communicator": True},
          {"param": ['daynight'], "name": 'setNightModeCamera', "communicator": True},
          {"param": ['x', 'y', 'width', 'height'], "name": 'setCaptureRectCamera', "communicator": True},
          {"param": ['distr1', 'distr2', 'distr3', 'distr4'], "alias": "distortion", "name": 'setCameraParameter', "communicator": False},
          {"param": ['frame_minification'], "alias": "frame-minification", "name": 'setCameraParameter', "communicator": False},
          {"param": ['interval', 'delay', '-1', '-1', '-1'], "name": 'setParamsScheduler', "communicator": True},
          {"param": ['-1', '-1', 'limit_fd', '-1', '-1'], "name": 'setParamsScheduler', "communicator": True},
          {"param": ['-1', '-1', '-1', 'limit_fr', '-1'], "name": 'setParamsScheduler', "communicator": True},
          {"param": ['-1', '-1', '-1', '-1', 'limit_fl'], "name": 'setParamsScheduler', "communicator": True},
         ]

class CheckCameraParamsForm(forms.Form):    
    brightness = forms.IntegerField(required=False)    
    sharpness = forms.IntegerField(required=False)
    saturation = forms.IntegerField(required=False)    
    contrast = forms.IntegerField(required=False)
    quality = forms.IntegerField(required=False)  
    light = forms.ChoiceField(choices = ((0,0),(1,1),(2,2),(3,3)), required=False)  
    qualitylow = forms.ChoiceField(choices = (("highspeed", "highspeed"), ('speed', 'speed'), ('balance', 'balance'), ('quality', 'quality'), ('moonlight', 'moonlight')), required=False)
    shortexposures = forms.IntegerField(required=False)
    frequency = forms.ChoiceField(choices = ((50,50), (60,60)), required=False)
    daynight = forms.ChoiceField(choices = ((0,0),(1,1),(2,2)), required=False)
    resolution = forms.IntegerField(required=False)
    area = forms.IntegerField(required=False)         
    height = forms.IntegerField(required=False)
    width = forms.IntegerField(required=False)
    x = forms.IntegerField(required=False)
    y = forms.IntegerField(required=False)
    distr = forms.ChoiceField(choices = ((3,3), (4,4)), required=False)
    distr1 = forms.FloatField(required=False)
    distr2 = forms.FloatField(required=False)
    distr3 = forms.FloatField(required=False)
    distr4 = forms.FloatField(required=False)
    interval = forms.IntegerField(required=False)
    delay = forms.IntegerField(required=False)
    limit_fd = forms.IntegerField(required=False)
    limit_fr = forms.IntegerField(required=False)
    limit_fl = forms.IntegerField(required=False)
    idprofile = forms.IntegerField(required=True)
#    idcamera = forms.IntegerField(required=True)
    idcamera =  forms.RegexField(label=_("idcamera"), max_length=36, regex=r'^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$',
        help_text = _("Required. 36 characters or fewer. Letters, digits and '-' only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and '-' characters.")})
    kpp = forms.IntegerField(required=False)
    frame_minification = forms.IntegerField(required=False)

def get_camera_id(uuid):
    try:
        if uuid:
            cam_obj = VModels.Camera.objects.get(uuid=uuid)
            if cam_obj:
                if cam_obj.type == "URL":
                    return cam_obj.id, cam_obj.url, cam_obj.type
                else: return cam_obj.id, cam_obj.ip, cam_obj.type
    except: logging.exception(sys.exc_info())
    return None, '', ''

@tester
@permission_required('user_perms.perm_settings')
def save(request):
    try:
        form = CheckCameraParamsForm(request.POST, request.FILES)
        logging.info(form.errors)
        if form.is_valid():
            logging.info(form.cleaned_data)
            if form.cleaned_data["idprofile"]<=0 or form.cleaned_data["idcamera"]<0: return HttpResponse("False")
            numcamera = form.cleaned_data["idcamera"]
            camera_id, source, type = get_camera_id(numcamera)
            logging.info(camera_id)
            if not camera_id: return HttpResponse("False")
            
            p = {}
            for cd in form.cleaned_data:
                if not cd in ("idprofile", "idcamera"): p[cd] = form.cleaned_data[cd]
            prof = models.CamerasProfile.objects.filter(id=form.cleaned_data["idprofile"])
            if prof.count()>0:
                update = False 
                p = json.dumps(p)
                if prof[0].text != p:
                    prof.update(text=p)
                    update = True
                    return HttpResponse(update_camera(profileid=prof[0].id, numcamera=numcamera, source=source, type=type))
        else: return HttpResponse(json.dumps(form.errors))
        return HttpResponse("True")
    except:
        logging.exception("profile save "+str(sys.exc_info()))
        return HttpResponse("False")
        

def set(request):
    pass

class CheckNewProfileForm(forms.Form):
    name = forms.CharField(max_length=64, required=False)
    idprofile = forms.IntegerField(required=False) 
    
@tester
@permission_required('user_perms.perm_settings')    
def add_profile(request):
    try:
        form = CheckNewProfileForm(request.REQUEST, request.FILES)
        if form.is_valid():
            if "idprofile" in form.cleaned_data:
                p = models.CamerasProfile.objects.filter(id=form.cleaned_data["idprofile"])
                if p.count() > 0: return HttpResponse(p[0].id)
            if form.cleaned_data.get("name", None):
                p = models.CamerasProfile.objects.filter(name=form.cleaned_data["name"])
                if p.count() > 0: return HttpResponse("error:dublicate")
                return HttpResponse(models.CamerasProfile.objects.create(name=form.cleaned_data["name"]).id)
            return  HttpResponse("error:wrongname")
        else: HttpResponse("error:%s" % (str(form.errors)))
    except:
        logging.exception("profile add_profile %s" % (str(sys.exc_info())))
        return HttpResponse("error:adderror")      

def applyResolution(x, y, w, h, maxResolution):
        from math import ceil
        dx = 32
        dy = 16
        minResolutionWidth = 320
        minResolutionHeight = 240

        #area = setAreaObjects()

        x = max(0, x);
        x = min(maxResolution["w"] - minResolutionWidth, x);

        y = max(0, y);
        y = min(maxResolution["h"] - minResolutionHeight, y);

        x = ceil(x / dx) * dx;
        y = ceil(y / dy) * dy;
        
        w = max(minResolutionWidth, w);
        w = min(maxResolution["w"] - x, w);

        h = max(minResolutionHeight, h);
        h = min(maxResolution["h"] - y, h);

        w = ceil(w / dx) * dx;
        if (h != 600 and h != 240):
            h = ceil(h / dy) * dy;

        return {"x": x, "y": y, "w": w, "h": h, "maxW": maxResolution["w"], "maxH": maxResolution["h"]};

def getMaxResolution(resolution, i):
    w = 320
    h = 240    
    try:
        resol = resolution["resol"][i]
        w = resol["width"]
        h = resol["height"]
    except:
        logging.exception("getMaxResolution "+str(sys.exc_info()))
    logging.info(w)
    logging.info(h)
    return {"w": int(w), "h": int(h)}    

def update_camera_field(camera_id, ptext):
    cam = VModels.Camera.objects.filter(id = camera_id)
    if "kpp" in ptext:
        kpp = VModels.Kpp.objects.filter(id = ptext["kpp"])
        if kpp:
            cam.update(kpp=kpp[0])
            return True
    return False


def update_camera(profileid=0, numcamera=None, source='', type="", cameraid=0):
    def to_balancer(name, args):
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)            
        res = b.executeMethodByName(name, args)
        b.close()
        del b
        
    def to_communicator(name, args):
        c = Communicator()
        error = c.executeMethodByName(name, args)
        c.close()
        del c       
    
    def get_capture(numcamera):
        c = Communicator()
        capture_rect = c.getCaptureRectCamera(numcamera)
        resolution = c.getResolutionCamera(numcamera)
        c.close()
        del c                  
        return capture_rect, resolution
          
    try:
        HOST, PORT, LOGIN, PASSWD, USER = views.initBalancer()
        SERVERC, PORTC, COMMUNICATORS = views.initCommunicators()
        camera_id = 0
        if numcamera!=None or (source=='' or type==""):
            camera_id, source, type = get_camera_id(numcamera)        
        
        prof = models.CamerasProfile.objects.filter(id=profileid)           
        
        ptext = {}
        if prof.count() > 0:
            ptext = json.loads(prof[0].text)
            update_camera_field(camera_id, ptext)
        index = 0
        for param in params:
            logging.info(param)
            p = [numcamera]
            if param["name"] == "setCameraParameter":
                if "distr" in ptext:
                    #p = [source, type]
                    err = False
                    for pp in param["param"]:                
                        if pp in ptext:
                            if pp == "distr2" and str(ptext["distr"])=="3": p.append("None")
                            else: p.append(ptext[pp])
                        else: 
                            err = True
                            break
                    if err: continue
                else: continue
            elif param["name"] == "setResolutionCamera":
                if "x" in ptext and "y" in ptext and "width" in ptext and "height" in ptext and "resolution" in ptext:
                    capture_rect, resolution = get_capture(numcamera)
                    res = applyResolution(ptext["x"], ptext["y"], ptext["width"], ptext["height"], getMaxResolution(resolution, int(ptext["resolution"])))
                    if capture_rect:
                        p = [numcamera, res["x"], res["y"], res["w"], res["h"]]
                        to_communicator('setCaptureRectCamera', p)
                    p1 = [numcamera, res["maxW"], res["maxH"]]
                    to_communicator('setResolutionCamera', p1)
                    if capture_rect:                    
                        to_communicator('setCaptureRectCamera', p)
                    p = p1
                else: continue
            else:
                err = False
                if len(param["param"]) == 1 and ptext[param["param"][0]] == None: continue 
                for pp in param["param"]:
                    if pp == "-1": p.append(pp)
                    elif pp in ptext: p.append(ptext[pp])
                    else:
                        err = True
                        break
                if err: continue
            if len(p)>1:
                if param["communicator"]: to_communicator(param["name"], p)                
                else:
                    if param.get("alias", None) == "frame-minification":
                        p.append(None)
                        p.append(None)
                        p.append(None)
                        p.append(param["alias"])
                    to_balancer(param["name"], p)
        return True
    except:
        logging.exception("profile update_camera "+str(sys.exc_info()))
        return False

class CheckUpdateCameraParamsForm(forms.Form):
    idprofile = forms.IntegerField(required=True)
    #idcamera = forms.IntegerField(required=True)
    #idcamera = forms.RegexField(regex=u'^[0-9]+(,[0-9]+)*$', required=True)
    idcamera =  forms.RegexField(label=_("idcamera"), max_length=36, regex=r'^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$',
        help_text = _("Required. 36 characters or fewer. Letters, digits and '-' only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and '-' characters.")})

@tester
@permission_required('user_perms.perm_settings')
def apply_profile(request):      
    try:
        form = CheckUpdateCameraParamsForm(request.POST, request.FILES)
        result = True
        if form.is_valid():
            idprofile = form.cleaned_data["idprofile"]
            cam = form.cleaned_data["idcamera"].split(",")
            logging.info(cam)
                        
            prof = models.CamerasProfile.objects.filter(id=idprofile)
            if prof.count()==0: return HttpResponse("False")
            
            for numcamera in cam:              
                #HOST, PORT, LOGIN, PASSWD, USER = views.initBalancer()
                #SERVERC, PORTC, COMMUNICATORS = views.initCommunicators()
                source = ''
                type = ''
#                if numcamera!=None:
                camera_id, source, type = get_camera_id(numcamera)
                
                res = update_camera(profileid=prof[0].id, numcamera=numcamera, source=source, type=type, cameraid=camera_id)
                result = res and result
            return HttpResponse(result)
        else: logging.info(form.errors)        
    except:
        logging.exception("profile apply_profile "+str(sys.exc_info()))
    return HttpResponse("False")

def delete(request):      
    try:
        form = CheckNewProfileForm(request.POST, request.FILES)
        result = False
        if form.is_valid():
            idprofile = form.cleaned_data.get("idprofile", None)
            if not idprofile: return HttpResponse(result) 
                        
            prof = models.CamerasProfile.objects.filter(id=idprofile)
            if prof.count() == 0: return HttpResponse(result)
            
            prof.delete()
            result = True
    except:
        logging.exception("profile delete "+str(sys.exc_info()))
    return HttpResponse(result)