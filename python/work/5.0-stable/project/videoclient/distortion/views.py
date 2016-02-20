# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
import logging
import sys
import os
from videoclient.balancer import Balancer
from videoclient.models import Balancer as modBalancer
from videoclient.models import PersonId
from videoclient.communicator import models
from videoclient.views import initBalancer, render_to_response_ex, tester, get_svg_draw_params, get_camera_distortion, getAllActiveCameras
from videoclient.distortion.forms import ImageFileForm
from videoclient.person_training.views import get_person_url, get_person_url2, get_person_list
from utils import getDefaultParams
from django import forms
from django.utils import simplejson
from videoclient import settings
import re
import datetime
import json
import base64
from cStringIO import StringIO as StringIO
from PIL import Image
from django.contrib.auth.decorators import permission_required

class SetDistortionForm(forms.Form):    
    distortion = forms.RegexField(label=u"Параметры дисторсии", max_length=40, regex=u'^[-0-9.]+,[-0-9.]+,[-0-9.]+(,[-0-9.]+)*$', required=True)
    image = forms.ImageField(label=u'Изображение', required=True)
    code = forms.CharField(required=True, max_length=16)

def gen_filename(ext = ".jpg"):
    datenow = datetime.datetime.today()
    year = str(datenow.year)
    month = str(datenow.month)
    day = str(datenow.day)
    hour = str(datenow.hour)
    minute = str(datenow.minute)
    if (len(month)<2):
        month = "0%s" % month
    if (len(day)<2):
        day = "0%s" % day
    if (len(hour)<2):
        hour = "0%s" % hour
    return "%s%s%s%s" % (year, month, day, hour)

def get_journal_path(filename):
    return "%s/%s/%s/%s" % (filename[:4], filename[4:6], filename[6:8], filename[8:10])

@tester
@permission_required('user_perms.perm_distortion')
def set_distortion(request):
    try:
        input_file = ""
        form = SetDistortionForm(request.POST, request.FILES)
        filename = ""
        if form.is_valid():
            filename = "%s%s/%s.jpg" % (settings.TMP_DISTORSION_DIR, get_journal_path(gen_filename()), form.cleaned_data["code"])
            dr = os.path.dirname("%s%s" % (settings.MEDIA_ROOT, filename))
            if not os.path.exists(dr): os.makedirs(dr)
            m = re.match(r'[-0-9.]+,[-0-9.]+,[-0-9.]+,[-0-9.]+', form.cleaned_data["distortion"])
            distortion = "distortion35" if m else "distortion3"
            HOST, PORT, LOGIN, PASSWORD, USER, Error = initBalancer(True)
            if not Error:
                 file = form.cleaned_data["image"]
                 for t in file: input_file += t
                 b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
                 params = [{'name':distortion, 'param':form.cleaned_data["distortion"]}]
                 info = b.fanStudio(input_file, params)[0]
                 b.close()
                 f = open("%s%s" % (settings.MEDIA_ROOT, filename), "w+b")
                 f.write(info)
                 f.close()
                 return HttpResponse("%s%s" % (settings.MEDIA_URL, filename))
                 """
                 return HttpResponse(info, mimetype="text/html")
                 response = HttpResponse(info, content_type='image/jpg')
                 response['Content-Length'] = len(info)
                 response['Content-Disposition'] = 'attachment;filename=distortion_result.jpg'
                 return response
                 """
        else: logging.info(form.errors())
    except:
        logging.exception("set_distortion "+str(sys.exc_info()))
    if input_file and filename:
        f = open("%s%s" % (settings.MEDIA_ROOT, filename), "w")
        f.write(input_file)
        f.close()
        return HttpResponse("%s%s" % (settings.MEDIA_URL, filename))
        """        
        return HttpResponse(input_file, mimetype="text/html")
        response = HttpResponse(input_file, content_type='image/jpg')
        response['Content-Length'] = len(input_file)
        response['Content-Disposition'] = 'attachment;filename=distortion_result.jpg'
        return response
        """
    return HttpResponse("")

@tester
@permission_required('user_perms.perm_distortion')
def camera(request, uuid=None, local_person_id=None):
    
    data = dict()
    
    p_id = 0
    if local_person_id:
        p_id = local_person_id
    
    res_get_all_active_cameras = getAllActiveCameras(url_reverse_name='distortion-camera2', ext_args=[local_person_id])
    all_active_cameras = res_get_all_active_cameras["all_active_cameras"]
    
    if not uuid:
        #get first active uuid in system
        try:
            uuid = all_active_cameras[0].uuid
        except:
            uuid = None
    
    camera = None
    try:
        camera = models.Camera.objects.filter(uuid=uuid)[0]
    except:
        camera = None
    
    data["selected_camera"] = camera
    data["all_active_cameras"] = all_active_cameras
    
    #get camera distortion params
    distortion = None
    if camera:
        try:
            distortion = get_camera_distortion(camera.uuid)
        except:
            logging.exception("getDistortion: "+str(sys.exc_info()))

    if not distortion:
        distortion = {'p1': '0', 'p2': '0', 'p3': '0.5', 'p4': '0.5', 'count': '3'}

    data["distortion"] = distortion
    
    #get svg draw size and margin
    try:
        if local_person_id:
            data["width"], data["height"], data["svg_margin"] = get_svg_draw_params(camera.uuid)
        else:
            data["width"] = settings.MAX_JS_VIDEO_SCREEN
            data["height"] = 480
            data["svg_margin"] = 0
    except:
        data["width"] = settings.MAX_JS_VIDEO_SCREEN
        data["height"] = 480
        data["svg_margin"] = 0
    
    if local_person_id:
        data["person_id"] = int(local_person_id)
        if local_person_id == "0":
            data.update(getDefaultParams(request, 'settings'))
            data.update({'select_subpage': 'cameras'})
        else:
            data.update(getDefaultParams(request, 'lists'))
            
        person = None
        try:
            person = PersonId.objects.get(id = int(local_person_id)).person
        except:
            person = None
        
        if person:
            data["person"] = person
            data['urls_arr'] = get_person_url()
            data['urls_arr2'] = get_person_url2()
            data["person_list"] = get_person_list(person.group.pk)
    
    data["communicator_errors_info"] = res_get_all_active_cameras["communicator_errors_info"]
    
    return render_to_response_ex(request, "camera_distortion.html", data)

@tester
@permission_required('user_perms.perm_distortion')
def set_distortion_by_points(request):
    
    try:
        width = request.REQUEST['width']
        height = request.REQUEST['height']
        lines = json.loads(request.REQUEST['lines'])
        #logging.info("TEST STRING:" + str(lines))
     
        lines_xml = ''
        for line in lines:
            p_count = len(line)
            xml_points = ''
            line_coords = []
            for i in range(0, p_count):
                index = str(i)
                line_coords.append(line[index]['x'])
                line_coords.append(line[index]['y'])
                coords = ",".join(["%s" % (c) for c in line_coords])
                xml_points = '<line>' + str(coords) + '</line>'
            
            lines_xml = lines_xml + xml_points
        
        lines_xml = '<lines>%s</lines>' % lines_xml
        
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        try:
            distortion_answer = b.calculateDistortion(lines_xml, width, height)
            if distortion_answer["status"] == "success":
                result = {'status': 'success', 'distortion': distortion_answer["distortion"]}
        except:
            result = { 'status': 'error' }
    
        b.close()
        del b
    except:
        logging.exception(str(sys.exc_info()))
        result = { 'status': 'error' }
    #logging.info("TEST:" + str(lines_xml))

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_distortion')
def get_image_with_distortion(request):
    try:
        p1 = request.REQUEST['p1']
        p2 = request.REQUEST['p2']
        p3 = request.REQUEST['p3']
        p4 = request.REQUEST['p4']
     
        base64_image = request.REQUEST['base64_image']
        
        distortion_params = '%s,%s,%s,%s' % (p1, p2, p3, p4)
    
        d = [{'name': 'distortion35', 'param': distortion_params}]
        
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        image = b.fanStudio(base64.b64decode(base64_image), d)
        b.close()
        del b
        
        #f = open('base64_test.jpg', 'w+b')
        #f.write(image[0])
        #f.close()
        
        result = { 'status': 'success', 'image': base64.b64encode(image[0])}
    except:
        result = { 'status': 'error'}
        logging.exception(str(sys.exc_info()))

    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

@tester
@permission_required('user_perms.perm_distortion')
def upload_image_for_distortion(request):
    result = dict()
    
    form = ImageFileForm(request.POST, request.FILES)
    if form.is_valid():
        file = form.cleaned_data["image_file"]
        input_file = ''
        for t in file: input_file += t
        im = StringIO(input_file)
        
        back_img = Image.open(im)
        frame_content = ''                 
        fWidth, fHeight = back_img.size
        width = settings.MAX_JS_VIDEO_SCREEN
        height = (((width * 100) / fWidth) * fHeight) /100

        back_img.thumbnail((width, 1000), Image.ANTIALIAS)
        sWidth, sHeight = back_img.size
        
        output = StringIO()
        back_img.save(output, format="JPEG", quality=100)
        frame_content = output.getvalue()
        output.close()
        
        margin = int((settings.MAX_JS_VIDEO_SCREEN - sWidth) / 2)

        result = {'res': 'success', 'image': base64.b64encode(frame_content), 'width': sWidth, 'height': sHeight, "margin": margin}
    else:
        result = {'res': 'error'}
    return HttpResponse(simplejson.dumps(result), mimetype='json')