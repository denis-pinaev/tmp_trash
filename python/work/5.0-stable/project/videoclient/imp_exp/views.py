# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
import logging
import sys
from videoclient.views import tester, initBalancer, JsonResponse, exportPath, learning, getDataPersonJson
from videoclient.balancer import Balancer  
from utils import getAllPhotosByName, updateBalId
import tempfile
import json
from imp_exp import forms
from cStringIO import StringIO
from xml.dom.minidom import parseString
from videoclient import models
from videoclient import settings
from videoclient import forms as VcForms
from django.utils.translation import ugettext as _
import datetime
import math
import os
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required


def get_keys_values(data, group_id=None):
    keys = ''
    values = ''
    
    i = 0
    for d in data:
        if d == "id" or d == "bal_id" or d == "user_id" or data[d] == None:
            continue
        if group_id and d == "group_id":
            data[d] = group_id
        if i>0:
            keys=keys+','
            values=values+','
        i = i+1
        keys = keys+d
        values = values+"'"+str(data[d])+"'"
    
    return '('+keys+')', '('+values+')'

def get_alpha(x1, y1, x2, y2):
    dx = math.fabs(float(x2)-float(x1))
    dy = math.fabs(float(y2)-float(y1))
    cosa = dx*dx / dx / math.sqrt(dx*dx+dy*dy)
    alpha = math.acos(cosa)
    return alpha

def rotate_xy(x1, y1, alpha):
    x1 = float(x1)
    y1 = float(y1)
    x = x1*math.cos(alpha)-y1*math.sin(alpha)
    y = x1*math.sin(alpha)+y1*math.cos(alpha)
    return x, y

def normal(x1, y1, fx, fy, dqx, dqy):
    x = (x1-fx)/dqx
    y = (y1-fy)/dqy
    return x, y

def getStatusId(cursor, group_id):
    sql = "select videoclient_statususer.id as status_id from videoclient_list join videoclient_types on videoclient_list.type_id = videoclient_types.id join videoclient_statususer on videoclient_types.division_id = videoclient_statususer.division_id where group_id = %s limit 1;" %(group_id)
    logging.info("sql: %s" %sql)
    cursor.execute(sql)
    cursor_data =  cursor.fetchall()
    return cursor_data[0][0] if len(cursor_data)>0 and len(cursor_data[0])>0 else None

from videoclient.views import JsonSTRResponse as JavaScriptResponse

from videoclient import status_thread

class ImportThread(status_thread.StatusThread):
   
    user_id = 0
    
    def __init__(self, buffer, group_id, user_id):
        self.buffer = buffer
        self.group_id = group_id
        self.user_id = user_id
        status_thread.StatusThread.__init__(self)
    
    def run(self):  
        try:   
            import hashlib, time, random
            code = hashlib.sha1(str(time.time())).hexdigest() + str(int(1000 * random.random()))
            zip_path='%s%s.zip' % (settings.TEMPORARY_FOLDER, code)
            ff = open(zip_path, 'w+b')
            self.buffer.seek(0)
            ff.write(self.buffer.read())
            ff.close()
            query = 'cd %s; ./manage.py import_person %s %s %s %s' % (settings.PROJECT_ROOT+'project/videoclient/', zip_path, str(self.group_id), str(self.getThreadId()), str(self.user_id))            
            pid = os.spawnvp(os.P_NOWAIT, 'sh', ['sh', '-c', query])
        except:
            return

@tester
@permission_required('user_perms.perm_lists')
def import_person(request):
    data = dict()
    data["status"] = False
    
    try:
        form = forms.ImportPersonForm(request.REQUEST, request.FILES)
        group_id = request.REQUEST["group"] if 'group' in request.REQUEST else 'NULL' 
        if not form.is_valid():
            data["errors"] = form.errors
            data["message"] = _("Ошибка обработки формы")
            return JavaScriptResponse(data)
    except:
        data["exception"] = str(sys.exc_info())
        data["message"] = _("Неизвестная ошибка при обработке формы")
        logging.exception("imp_exp import-person form check: " + str(sys.exc_info()))
        return JavaScriptResponse(data)

    try:
        HOST, PORT, LOGIN, PASSWORD, USER, Error = initBalancer(True)
        if Error:
            data["errors"] = "Balanser is not init"
            data["message"] = _("Ошибка инициализации управляющей системы")
            return JavaScriptResponse(data)
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        b.getPreview(0,0)
        b.open()
        b.close()
    except:
        data["exception"] = str(sys.exc_info())
        data["message"] = _("Неизвестная ошибка при инициализации управляющей системы")
        logging.exception("imp_exp import-person initBalancer(): " + str(sys.exc_info()))
        return JavaScriptResponse(data)
    try:    
        file = form.cleaned_data["file"]
        buffer = StringIO()
        for t in file: buffer.write(t)
    except:
        data["exception"] = str(sys.exc_info())
        data["message"] = _("Неизвестная ошибка при создании временных файлов")
        logging.exception("imp_exp import-person can't create  tmp file ")
        return JavaScriptResponse(data)
    try:
        thread = ImportThread(buffer, group_id, request.user.id)
        data["thread_id"] = thread.getThreadId()
        thread.start()
    except:
        data["exception"] = str(sys.exc_info())
        data["message"] = _("Ошибка создания потока для импорта персон")
        logging.exception("")
        return JavaScriptResponse(data)
  
    data["status"] = True
    return JavaScriptResponse(data)

class ExportThread(status_thread.StatusThread):
    
    def __init__(self, persons):
        self.persons = persons
        status_thread.StatusThread.__init__(self)
        
    
    def run(self):
        
        self.setRunning()
        self.setMaxValue(len(self.persons))
        
        data = dict()
        data["status"] = False
        
        filename = 'export_persons.zip'
        data["url"] = "/exportfile/?export_persons=%s" %filename
        
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        
        import zipfile
        zf = zipfile.ZipFile(exportPath(person=True)+filename, 
                         mode='w',
                         compression=zipfile.ZIP_DEFLATED, 
                         )
        from cStringIO import StringIO
        
        updateBalId()
        person_num = 0
        for person in self.persons:

            obj = models.PersonId.objects.raw("select * from videoclient_personid join videoclient_person on videoclient_personid.person_id = videoclient_person.id where videoclient_personid.id = %s" %person)
            obj = list(obj)
            obj = obj[0]
            
            try:
                photos_data = getAllPhotosByName(person, bal_id_update=False)
            except:
                data["exception"] = str(sys.exc_info())
                data["message"] = _("Неизвестная ошибка при инициализации управляющей системы")
                self.setFinished()
                self.setAnswer(data)
                return
            
            if "status" in photos_data and not photos_data["status"]:
                data["exception"] = "BalancerException"
                data["message"] = _("Неизвестная ошибка при инициализации управляющей системы")
                logging.exception(str(sys.exc_info()))
                self.setFinished()
                self.setAnswer(data)
                return 

            photos_id = photos_data["id"]
            photos = photos_data["photos"]
            
            photos_json = []
            for photo in photos:
                meta = {}
                name = photo["num"]
                images, params = b.getPersonPhotoWithParams(photos_id, name)
                if len(images) == 0:
                    continue
                image = images[0]
                filename = name+'.png'
                zf.writestr(person+'/'+filename, image)
                filename_base = name + '_base.png'
                base_image = settings.LEARNING_IMAGES + '%s/%04d.jpg'  % (person, int(photo["num"]))
                b_image = ''
                if os.path.isfile(base_image):
                    f = open(base_image, 'r+b')
                    wrapper = f.read()
                    f.close()
                    zf.writestr(person+'/'+filename_base, wrapper)
                    b_image = filename_base
                try:
                    photoexif = get_object_or_404(models.PhotoExifData, photo_id=int(photo["num"]), person_id = int(person))
                    if photoexif and photoexif.exif:
                        #zf.writestr('%s/%s_meta.json' % (person, int(photo["num"])), json.dumps(photoexif.exif))
                        meta = photoexif.exif
                except:
                    pass
                photos_json.append({"name": filename, "base_name": b_image, "params": params, "meta": meta})
                
            zf.writestr(person+'/photos.json', json.dumps(photos_json))
            
            data_person = getDataPersonJson(person)
            zf.writestr(person+'/personid.json', json.dumps(data_person["personid"]))
            zf.writestr(person+'/person.json', json.dumps(data_person["person"]))
            
            person_num+=1
            self.setValue(person_num)
        
        zf.close()
        
        b.close()
        del b
        data["status"] = True 
        self.setAnswer(data)   
        self.setFinished()

@tester
@permission_required('user_perms.perm_lists')
def export_person(request):
    data = dict()
    data["status"] = False
    persons = []

    try:
     
        if request.REQUEST.has_key('group'):
            #persons = []
            personIds = models.PersonId.objects.filter(active=1, person__group__id=int(request.REQUEST["group"]))
            for p in personIds:
                persons.append(str(p.id))
        else:
            form = VcForms.ExportPersonForm(request.REQUEST)
            if not form.is_valid():
                data["error"] = form.errors
                data["message"] = _("Ошибка обработки формы")
                return JsonResponse(data)
        
        try:
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            b.getPreview(0,0)
            b.close()
            del b
        except:
            data["exception"] = str(sys.exc_info())
            data["message"] = _("Неизвестная ошибка при инициализации управляющей системы")
            logging.exception(str(sys.exc_info()))
            return JsonResponse(data)
        
        persons = form.cleaned_data['persons'].split(',')
        
    except:
        data["exception"] = str(sys.exc_info())
        data["message"] = _("Неизвестная ошибка при экспорте персон")
        logging.exception(str(sys.exc_info()))
    
    try:
        thread = ExportThread(persons)
        data["thread_id"] = thread.getThreadId()
        thread.start()
    except:
        data["exception"] = str(sys.exc_info())
        data["message"] = _("Ошибка создания потока для импорта песон")
        logging.exception("")
        return JavaScriptResponse(data)
  
    data["status"] = True
        
    return JsonResponse(data)


