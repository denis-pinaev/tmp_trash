# coding=utf-8

from videoclient.models import *
from videoclient.forms import *
import hashlib
import datetime
import time
#from videoclient.models import DefaultParams, Journal, Person
import logging
import base64
import sys
from videoclient.settings import division_visitor, division_person, division_employee, last_journal_update, status_notdefined, status_enter, status_exit, camera_enter, camera_exit, camera_all, action_delete, WWW_ROOT
from videoclient import settings
from videoclient.models import Person, Journal
from videoclient.communicator import models as comModels
from videoclient.videoanalytics.models import DetectorLog,Detector
#from videoclient.models import DefaultParams, Journal, Person, VisitingCard, PersonId
import re
from django.db.models import Q
from django import forms
from django.shortcuts import get_object_or_404
from videoclient.updates import models as uModels
from django.contrib.auth.models import User as AuthUser
from django.forms.util import ErrorList
from django.db import connection, transaction, DatabaseError
from videoclient.communicator import Communicator

SVN_REVISION = '$Revision: 5539 $'  ######

REVISION = 0
m = re.match(r'[^0-9]*([0-9]+)[^0-9]*', SVN_REVISION)
if m and m.group(1): REVISION = int(m.group(1))

VERSION_PREFIX = settings.VERSION_PREFIX
BRANCH = settings.BRANCH
#REVISION = settings.REVISION

VERSION = "%s.%s.%s" % (VERSION_PREFIX, BRANCH, REVISION)
def check_version():
    try:
        versions = uModels.Version.objects.all().order_by('-id')
        if versions.count() == 0:
            uModels.Version.objects.create(version=VERSION_PREFIX, branch=BRANCH, revision=REVISION)
    except:
        pass
    
check_version() 
    
def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix

def get_value_defaultparams(name="", default_value = 0):
    try:
        if name:
            if DefaultParams.objects.filter(name=name).count() == 1:
                params = DefaultParams.objects.filter(name=name)#DefaultParams.objects.get_or_create(name=name)
                return params[0].value if params[0].value else default_value
    except DatabaseError:
        pass
    except:
        logging.exception("get_value_defaultparams: " + str(sys.exc_info()) + " name: " + str(name)) 
    return default_value

def getDataAllDefaultParams():
    data = dict()
    params = DefaultParams.objects.all()
    for param in params:
        data[param.name] = param.value
    return data
    
def update_value_defaultparams(name="", value=None, create_new = False):
    try:
        if name:
            if DefaultParams.objects.filter(name=name).count() == 1 or create_new:
                params, create = DefaultParams.objects.get_or_create(name=name)#DefaultParams.objects.get_or_create(name=name)
                if value is not None:
                    params.value = value
                    params.save()
                return True
    except:
        logging.exception(str(sys.exc_info()) + " name: " + str(name))
    return False
    
def delete_value_defaultparams(name=""):
    if name:
        DefaultParams.objects.filter(name=name).delete()
        return True
    return False    

def queryset_iterator(queryset, chunksize=1000):
    '''
    Iterate over a Django Queryset ordered by the id

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.
    Note that the implementation of the iterator does not support ordered query sets.
    '''
    import gc
    id = 0
    last_id = queryset[0].id
    queryset = queryset.order_by('id')
    while id < last_id:
        rows = queryset.filter(id__gt=id)[:chunksize]
        for row in rows:
            id = row.id
            yield row
        gc.collect()

def dataNavigation(request, count, select_page=None,limits=[10, 20, 30, 40 ,50]):

    from videoclient.views import genPages, LIMIT
    data = dict()
    
    if request.GET.has_key('per_page'):
        per_page = int(request.GET['per_page'])
    else:
        per_page = limits[0]
    if per_page<1:
        per_page = 1
    limit = per_page
    if select_page and select_page == "photosperson":
        res = get_value_defaultparams("res_interface")
        if res and res == "0":
            limit = 21
        elif res and res == "1":
            limit = 30 
    start = 1
    if request.GET.has_key('start'):
        start = int(request.GET['start'])
    if request.GET.has_key('page'):
        if request.GET['page'].isdigit():
            start = (int(request.GET['page'])-1) *limit +1    
    if start > count:
        if count % limit == 0:
            start = (count / limit-1) * limit + 1
        else:
            start = count / limit * limit + 1
    if start <= 0:
        start = 1

    if per_page != limits[0]:
        data['per_page'] = per_page
    data['limit'] = limit
    data['page'], data['allpages'], data['pages'] = genPages(count, start, limit)
    data['start_page'] = data['pages'][0]
    data['finish_page'] = data['pages'][len(data['pages'])-1]
    data['start'] = start
    data['finish'] = start + limit
    data['limits'] = limits
    return data

"""
def dataGet(request):
    data = dict()
    result = '';
    for g in request.GET:
        if result != '':
            result = result + '&'
        result = result + g + '=' + request.GET[g]
    data['dataGet'] = result
    data['getvars'] = result
    return data
"""
def dataGet(request, ignore_list={}):
    data = dict()
    result = [];
    for g, val in request.GET.items():
        if not g in ignore_list:
            result.append("%s=%s" % (g, val))
    get_result = "&".join(result)
    data['dataGet'] = get_result
    data['getvars'] = get_result
    return data

#
# TODO
# Избавиться от check_rule, перейти на новое разграничение прав
#
def check_rule(request, is_op=False, is_moderator=False, is_sec=False):
    if not request.user.is_authenticated():
        return False
   
    from videoclient.views import logout
   
    user = request.user
    users = User.objects.filter(id=user.id)
    if len(users) == 0:
        return True
    
    user = users[0]
    
    timeout = int(get_value_defaultparams("login_timeout"))
    import datetime
    now = datetime.datetime.now()
    logout_time = user.last_access + datetime.timedelta(seconds=timeout) 
    if now > logout_time:
        logout(request, logout_time)
        return False
    else:
        user.last_access = now
        user.save() 
    
    if user.status.name == "Администратор" or user.status.name == "Administrator":
        return True
    elif user.status.name == "Оператор" or user.status.name == "Operator":
        return is_op
    elif user.status.name == settings.moderator or user.status.name == "Moderator":
        return is_moderator
    
    if is_sec:
        if user.status.name == "Охранник" or user.status.name == "Security":
            return True
        else:
            return False
    
    logout(request)
    return False
    #return HttpResponseRedirect("/")

def get_journal_path(filename):
    return "%s/%s/%s/%s/%s" % (filename[:4], filename[4:6], filename[6:8], filename[8:10], filename[10:])

def gen_filename(ext=".jpg"):
    filename = hashlib.sha1(str(time.time())).hexdigest()
    datenow = datetime.datetime.today()
    year = str(datenow.year)
    month = str(datenow.month)
    day = str(datenow.day)
    hour = str(datenow.hour)
    minute = str(datenow.minute)
    if (len(month) < 2):
        month = "0%s" % month
    if (len(day) < 2):
        day = "0%s" % day
    if (len(hour) < 2):
        hour = "0%s" % hour
    if (len(minute) < 2):
        minute = "0%s" % minute
    return "%s%s%s%s%s%s%s" % (year, month, day, hour, minute, filename, ext)

def getUserRole(uid=0):
    try:
        return [1]
    except:
        logging.info("getUserRole " + str(sys.exc_info()))
        return []
    
def getCurrentTime():
    data = dict()
    now = datetime.datetime.now()
    data['now_hour'] = now.strftime('%H')
    data['now_minute'] = now.strftime('%M')
    data['now_second'] = now.strftime('%S')
    data['now_datetime'] = now
    return data

def getVersion():
    from videoclient import views
    data = dict()
    data['version'] = views.VERSION
    return data

def getDefaultParams(request, page='', project="po4"):
    data = dict()
    if request.GET.has_key('group'):
        data["group"] = request.GET['group']
        data["name_group"] = GroupPerson.objects.get(id=int(data["group"])).name if GroupPerson.objects.filter(id=int(data["group"])).count() == 1 else data["group"]
    elif request.POST.has_key('group'):
        data["group"] = request.POST['group']
        data["name_group"] = GroupPerson.objects.get(id=int(data["group"])).name if GroupPerson.objects.filter(id=int(data["group"])).count() == 1 else data["group"]
    
    if request.REQUEST.has_key("distortion"):
        data["distortion"] = request.REQUEST["distortion"]
            
    data['select_page'] = page
    if request.GET.has_key('select_page'):
        data['select_page'] = request.GET['select_page']
        
    if "training_camera" in request.REQUEST:
        data["training_camera"] = True
        
    import videoclient.settings
    data['host'] = videoclient.settings.HTTP_HOST
        
    data['src_root'] = videoclient.settings.SRC_ROOT
    data['noise_learning'] = videoclient.settings.noise_learning
    if project == "":
        project = None
    
    data['role'] = getUserRole(request.user.id)
        
    data['project'] = project
    if project is None:
        if not request.GET.has_key('select_page'):
            if data['select_page'] != 'setup' and data['select_page'] != 'journal' and data['select_page'] != 'kpp' and data['select_page'] != 'historychange' and data['select_page'] != 'users' and data['select_page'] != 'noiselist_result':
                if data['select_page'] != 'testfr' and data['select_page'] != 'export' and data['select_page'] != 'monitoring_system' and data['select_page'] != 'monitoring_communicator' and data['select_page'] != 'special' and data['select_page'] != 'anketauser' and data['select_page'] != 'map':
                    #if data['select_page'] != 'staff' and data['select_page'] != 'stafflist' and data['select_page'] != 'anketastaff' and data['select_page'] != 'help':
                    if data['select_page'] != 'setup' and data['select_page'] != 'help' and data['select_page'] != 'settings_interface' and data['select_page'] != 'control_settings_settings' and data['select_page'] != 'control_settings_default' and data['select_page'] != 'control_settings_users' and data["select_page"] != 'video' and 'monitoring' not in data["select_page"]:
                        data['select_sub_page'] = data['select_page']
                        data['select_page'] = 'lists'
        data['project_url'] = ""
    else:
        data['project_url'] = "/" + project

    # убрана загрузка из настроек по задаче 8293
    # ревизия 3830
    data['use_js'] = '1'
    
    data['journalBoundCoeff2'] = get_value_defaultparams("journalBoundCoeff")
    
    reboot_host = request.get_host().split(":")
    data['reboot_host'] = reboot_host[0] + ":90"
    
    data['is_active_self_learning'] = settings.is_active_self_learning
    data['self_learning'] = settings.self_learning
    data['show_cameras_count'] = 6
    
    res_interface = get_value_defaultparams("res_interface")
    if res_interface == '1':
        data['show_cameras_count'] = 9
    data['show_cameras_count_ex'] = data['show_cameras_count'] + 1

    from videoclient.views import initBalancer
    HOST, PORT, LOGIN, PASSWORD, USER, Error = initBalancer(True)
    if Error: data["balancer_need_configure"] = True
    
    return data

def dataGuards(model=User, users=None, is_person=False):
    data = dict()
    data['users'] = getDictUsers(users, model)
    i = 0
    while i < len(data['users']):
        user = data['users'][i]
        if model == Person or is_person:
            try:
                persons = Person.objects.all().filter(id_person=user['id_person'], date__lt=user['date'])
                if len(persons) > 0:
                    data['users'][i]['userold'] = persons[len(persons) - 1].getDict()
            except:
                logging.info("dataGuards " + str(sys.exc_info()))
        else:
            try:
                data['users'][i]['fio'] = "%s %s %s" % (data['users'][i]['first_name'], data['users'][i]['last_name'], data['users'][i]['middle_name'])
            except:
                logging.info("dataGuards users " + str(sys.exc_info()))
        if user.has_key('staff'):            
            staff = user['staff']       
            #pid = PersonId.objects.filter(id = int(staff))
            #if pid: data['users'][i]['staff'] = pid[0].getDict()
        
        i = i + 1
    data['all_users'] = len(data['users'])
    return data

def dictConcat(data, add):
    for a in add:
        data[a] = add[a]
    return data

def getDictByArrayModel(all):
    data = []
    for a in all:
        data.append({'id': a.id, 'name': a.name})
    return data

def getDictByModel(model, str=""):
    all = model.objects.all()
    if str != '':
        div = DivisionUser.objects.get_or_create(name=str)
        all2 = model.objects.all().filter(division=int(div[0].id))
        if len(all2) > 0:
            all = all2
    return getDictByArrayModel(all)

def getDictDivision(str):
    data = dict()
    divUser = DivisionUser.objects.get_or_create(name=str)
    data['division'] = divUser[0].id
    return data

def getUserID(username):
    user = 1
    try:
        user = User.objects.get(username=username).id
    except:
        user = 1
    return user

CHANGE = '_change'
CREATE = '_create'
ADDPHOTO = '_addphoto'
def dataUser(request, id=None, one=False):
    data = dict()
    data["save"] = False
    form = UserChangeForm(request.POST, request.FILES)
    data['user'] = dict()
    admin = AuthUser.objects.get(pk=1)

    if request.POST.has_key(CHANGE):
        root_check = True if str(admin.username).lower() == str(request.POST.get('username')).lower() else False
        if not form.is_valid() or root_check:
            data['errors'] = form.errors
            if root_check:
                form._errors['username'] = ErrorList([u'Пользователь с таким именем уже существует'])
        else:
            form.saveUser()
            data["save"] = True
    
    if request.POST.has_key(CREATE):
        root_check = True if str(admin.username).lower() == str(request.POST.get('username')).lower() else False
        if not form.is_valid() or root_check:
            data['errors'] = form.errors
            if root_check:
                form._errors['username'] = ErrorList([u'Пользователь с таким именем уже существует'])
        else:
            id = form.addUser()
            data["save"] = True
    
    if not id:
        if request.POST.has_key("id"):
            id = request.POST["id"]
    
    if id:
        user = User.objects.get(id=int(id))
        data['user'] = user.getDict()
        data['selected_user'] = user
        data['pk_django_groups'] = [group.pk for group in user.groups.all()]
        data['action'] = CHANGE
    else:
        data['action'] = CREATE
        data['user'] = dict()
        for p in request.POST:
            data['user'][p] = request.POST[p]
    data['id'] = id
    
    from django.contrib.auth.models import Group
    data['django_groups'] = Group.objects.exclude(name='group_superuser')

    data['allstatus'] = getDictByModel(StatusUser, 'Операторы')
    data['alldivision'] = getDictByModel(DivisionUser)
    data['allposition'] = getDictByModel(PositionUser, 'Операторы')
    data['allkpp'] = getDictByModel(Kpp)
    
    data['user'].update(getDictDivision('Операторы'))
    data['addphoto'] = ADDPHOTO
    
    if data['user'].has_key('staff'):
        staff = data['user']['staff']
        #data['user']['staff'] = PersonId.objects.get(id = int(staff)).getDict()
    else:
        staff = -1
    data['photoid'], data['photoname'], data['photocount'] = getPersonPhotosByName(staff, one)
    
#    if (not data['user'].has_key('staff')) or (data['user']['staff']['active']):
#        personId = PersonId.objects.filter(person__status__division__name="Сотрудники", active=True)
#    else:
    personId = PersonId.objects.filter(person__status__division__name="Сотрудники")
    
    data['allstaff'] = personId
    
            
    return data

def idToNameForPerson(id):
    person = Person.objects.get(id=id)
    return int(person.id_person)

def idToName(id):
    return int(id)

def renamePerson(oldName, newName):
    if oldName == newName: return False
    from videoclient.balancer import Balancer
    from videoclient.views import initBalancer
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    try:
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        CMD_RENAME = [{'name':'person_name', 'param':oldName}, {'name':'value', 'param':newName}]
        b.renamePerson(CMD_RENAME)        
        b.close()
        del b
        return True
    except:
        return False
    return False

def renameFR(id, id2):
    oldName = idToNameForPerson(id)
    newName = idToNameForPerson(id2)
    return renamePerson(oldName, newName)

def updateBalId(final=False):
    try:
        from videoclient.views import initBalancer
        from videoclient.balancer import Balancer
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        try:
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            ids, names, photos = b.getPersons()
            b.close()
            del b
        except:
            logging.exception(str(sys.exc_info()))
            return False
        
        persons = PersonId.objects.filter(bal_id=None)
        person_names = dict()
        for person in persons:
            person_names[str(idToName(person.id))] = person
        
        from django.db import IntegrityError
        try:
            i = 0;    
            while i < len(names):
                if names[i] in person_names:
                    person_id = person_names[names[i]]
                    person_id.bal_id = ids[i]
                    person_id.save()
                i = i + 1
        except IntegrityError:
            if not final:
                persons = PersonId.objects.all()
                persons.update(bal_id=None)
                return updateBalId(True)
    except:
        logging.exception(str(sys.exc_info()))
    return True    

def getBalIdByName(person_name, bal_id_update=True):
    if person_name <= 0:
        return -1
    if len(str(person_name)) == 0 :
        return -2
    
    
    person_id = PersonId.objects.get(id=int(person_name))
    if person_id.bal_id:
        return person_id.bal_id
    
    if bal_id_update:
        updateBalId()
        person_id = PersonId.objects.get(id=int(person_name))
        if person_id.bal_id:
            return person_id.bal_id
    
    return None

def getBalNameById(id):
    try:
        id = int(id)
        
        from videoclient.views import initBalancer
        from videoclient.balancer import Balancer
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        
        try:
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            ids, names, photos = b.getPersons()
            b.close()
            del b
        except:
            logging.exception("getBalNameById, getPerson: " + str(sys.exc_info()))
            return ""
       
        i = 0;
        while i < len(ids):
            if int(ids[i]) == id:
                return names[i]
            i = i + 1
    except:
        logging.exception("getBalNameById: " + str(sys.exc_info()))
    return ""

def getPersonIdByBalId(id):
    try:
        if PersonId.objects.filter(bal_id=int(id)).count() == 1:
            person = PersonId.objects.get(bal_id=int(id))
        else:
            bal_name = getBalNameById(id)
            person_id = int(bal_name)
            if PersonId.objects.filter(id=int(person_id)).count() == 1:
                personId = PersonId.objects.get(id=person_id)
                personId.bal_id = int(id)
                personId.save()
                person = personId
            else:
                person = None
                
        return person
    except:
        logging.exception("getPersonIdByBalId: " + str(sys.exc_info()))
    return None

def getPersonByBalId(id):
    try:
        person = getPersonIdByBalId(id)
        if person: 
            return person.person
        return None
    except:
        logging.exception("getPersonByBalId: " + str(sys.exc_info()))
    return None

def getNamePersonByBalId(id):
    try:
        p = PersonId.objects.filter(bal_id=int(id))
        if p.count() == 1:
            person = p[0].person
        else:
            bal_name = getBalNameById(id)
            person_id = int(bal_name)
            p = PersonId.objects.filter(id=int(person_id))
            if p.count() == 1:
                personId = p[0]
                personId.bal_id = int(id)
                personId.save()
                person = personId.person
            else:
                person = None
            
        if person is not None:
            person_name = person.first_name if person.first_name else ""
            person_name = person_name + (" " if len(person_name) > 0 and person.last_name else "") + (person.last_name if person.last_name else "")
            person_name = person_name + (" " if len(person_name) > 0 and person.middle_name else "") + (person.middle_name if person.middle_name else "")
            return person_name
    except:
        logging.exception("getNamePersonByBalId: " + str(sys.exc_info()))
    return ""

def DeletePersonFromFr(person):
    try:
        if person:
            logging.info("DelPersonFromFr id" + str(person.id))
            frid = getBalIdByName(person.id, bal_id_update=False)
            logging.info("DelPersonFromFr frid" + str(frid))
            if frid is None: return True
            if frid < 0: return False  
            from videoclient.views import initBalancer
            from videoclient.balancer import Balancer
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            answer = b.deleting(frid)
            b.close()
            del b
            return answer
        return False    
    except:
        logging.exception("DelPersonFromFr " + str(sys.exc_info()))
        return False
    
def getAllPhotosByBalId(id, one=0, get_base64=False, photo_number=None):
    try:
        if id > 0:
            from videoclient.views import initBalancer
            from videoclient.balancer import Balancer
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            num_photos = b.getPersonPhotos(id)[0]
            
            num_photos.sort()
            i = 0 
            photos = []
            
            i = 0
            for photo in num_photos:
                if photo_number is not None and photo_number != photo:
                    continue; 
                images = b.getPersonPhoto(id, photo)
                if len(images) > 0:
                    image = images[0]
                    import Image
                    import StringIO
                    img = Image.open(StringIO.StringIO(image))
                    width, height = img.size
                else:
                    image = ''
                    width = ''
                    height = ''
                
                append_photo = {'num': photo, 'size': {'width': width, 'height': height}}
                if get_base64 and image:
                    append_photo["image_base64"] = base64.b64encode(image)
                photos.append(append_photo)
                
                i = i + 1
                if one > 0 and i >= one:
                    break
                 
            b.close()
            del b
            
            return {'status': True, 'id':id, 'photos': photos, 'count': len(num_photos), 'size': {'width': 120, 'height': 120}}
        return {'status': True, 'id':id, 'photos': [], 'count': 0}
    except:
        logging.exception("getAllPhotosByName: " + str(sys.exc_info()))
    return {'status': False, 'id':id, 'photos': [], 'count': 0}

def getAllPhotosByName(person_name, one=0, bal_id_update=True, get_base64=False, photo_number=None):
    id = getBalIdByName(person_name, bal_id_update=bal_id_update)
    return getAllPhotosByBalId(id, one, get_base64=get_base64, photo_number=photo_number)

def getPersonPhotosByName(person_name, one=0):
    data = getAllPhotosByName(person_name, one)
    if(data['id'] > 0 and data['count'] > 0):
        return data['id'], data['photos'][0]['num'], data['count']
    return -1, -1, -1

def journal_training(pId, journal_ids):
    import os
    journal_ids = str(journal_ids).split(',');
    try:
        person = get_object_or_404(Person, pk=pId)
        person_id = person.id_person
    except:
        logging.exception(str(sys.exc_info()))
    
    count = 0
    
    journals = Journal.objects.filter(pk__in = journal_ids)
    
    for journal in journals:
        try:
            if journal.original and os.path.isfile(journal.original.path):
                f = open(journal.original.path, 'r+b')
                wrapper = f.read()
                f.close()
                if learning(wrapper, str(person_id), face=journal.found_face):
                    found_path = journal.finded
                    if found_path and found_path.path and journal.original != found_path and os.path.isfile(found_path.path): 
                        os.remove(found_path.path)
                        journal.finded = journal.original
                    count += 1
                    journal.person_id = person_id
                    journal.coeff = 100
                    journal.training = True
                    journal.save()
        except:
            logging.exception(str(sys.exc_info()))
    
    if count>0:
        param_aggregator = ParamAggregator.getRecord()
        param_aggregator.setParam(ParamAggregator.PARAM_JOURNAL_IDENT_COUNT, param_aggregator.getParam(ParamAggregator.PARAM_JOURNAL_IDENT_COUNT) + count)
           
    
    #if count == 0:
    #    try:
    #        personId.delete()
    #        person.delete()
    #    except:
    #        pass
    return count

def dataPerson(request, id, param, id2=None, one=0):
    data = dict()
    data["save"] = False
    form = PersonChangeForm(request.POST, request.FILES);
    data['user'] = dict()
    
    if request.REQUEST.has_key('journal_ids'):
        data['journal_ids'] = request.REQUEST['journal_ids']
    res = {}    
    if request.POST.has_key(CHANGE):    
        if not form.is_valid():
            data['errors'] = form.errors
        else:
            id = form.saveUser()
            if request.REQUEST.has_key('journal_ids'):
                res = journal_training(id, request.REQUEST["journal_ids"])
                data["istraining"] = True
                if res > 0:
                    data["learned"] = True
                if data.has_key('journal_ids'):
                    del data['journal_ids']
            data["save"] = True

    if request.POST.has_key(CREATE):
        if not form.is_valid():
            data['errors'] = form.errors
        else:
            id = form.addUser()
            if request.REQUEST.has_key('journal_ids'):
                res = journal_training(id, request.REQUEST["journal_ids"])
                data["istraining"] = True
                if res > 0:
                    data["learned"] = True
                if data.has_key('journal_ids'):
                    del data['journal_ids']
            data["save"] = True
    
    if not id:
        if request.POST.has_key("id"):
            id = request.POST["id"]
    
    if id:
        user = Person.objects.get(id=int(id))
        data['user'] = user.getDict()
        data['action'] = CHANGE
    else:
        data['action'] = CREATE
        data['user'] = dict()
        for p in request.POST:
            data['user'][p] = request.POST[p]
    data['id'] = id
        
    data['allstatus'] = getDictByModel(StatusUser, param)
    data['alldivision'] = getDictByModel(DivisionUser)
    data['allposition'] = getDictByModel(PositionUser, param)
    data['allkpp'] = getDictByModel(Kpp)
    data['allcategory'] = getDictByModel(Category)
    data['alldocuments'] = getDictByModel(Document)
    
    data['user'].update(getDictDivision(param))
    data['user']['user'] = getUserID(request.user.username)
    data['addphoto'] = ADDPHOTO
    data['articleList'] = Article.objects.order_by("id")
    data['articleItem'] = ArticleItem.objects.order_by("id")
    data['articlePart'] = ArticlePart.objects.order_by("id")
    
    if data['user'].has_key('id_person'):
        id_person = data['user']['id_person']
    else:
        id_person = -1
    data['photoid'], data['photoname'], data['photocount'] = getPersonPhotosByName(id_person, one)
    
    if id2:
        user = Person.objects.get(id=int(id2))
        data['user2'] = user.getDict()
    else:
        data['user2'] = data['user']
    
    if id and (not request.POST.has_key(CREATE)):    
        vc = VisitingCard.objects.filter(visitor__person__id=int(id))
        if vc.count() > 0:
            vcid = vc[0].id
        else:
            vcid = None
    else:
        vcid = None
    from videoclient.po4.views import getDataVisitorCard
    errors = None
    if data.has_key('errors'):
        errors = data['errors'] 
    data.update(getDataVisitorCard(request, vcid, id, id_person))
    if data.has_key('errors'):
        if errors is not None:
            data['errors'].update(errors)
    return data

def dataPhotoById(id):
    data = dict()
    personId = PersonId.objects.get(id=id)
    data['allphotos'] = getAllPhotosByName(personId.id)
    data['user'] = personId.getDict()
    return data

def getGround(request):
    data = dict()    
    data['ground'] = Ground.objects.all()
    return data

class TestDataJournal(forms.Form):
    dateBegin = forms.DateField(required=False, input_formats=('%d.%m.%Y',),)
    dateEnd = forms.DateField(required=False, input_formats=('%d.%m.%Y',),)

    hour_beg = forms.IntegerField(required=False)
    min_beg = forms.IntegerField(required=False)
    sec_beg = forms.IntegerField(required=False)
    hour_end = forms.IntegerField(required=False)
    min_end = forms.IntegerField(required=False)
    sec_end = forms.IntegerField(required=False)
    
    no_date = forms.CharField(required=False)
    id_person = forms.CharField(required=False)
    defined = forms.CharField(required=False)
    cameras = forms.CharField(required=False)
    fio = forms.CharField(required=False)
    id_record = forms.CharField(required=False)
    filter = forms.CharField(required=False)
    
    all_pages = forms.CharField(required=False)
    
    delo = forms.IntegerField(required=False)
    concato = forms.IntegerField(required=False)
    sorto = forms.IntegerField(required=False)    
    start = forms.IntegerField(required=False)
    up = forms.IntegerField(required=False)
    communicator = forms.IntegerField(required=False)
    camera = forms.IntegerField(required=False)

def SortList(x, ind=[]):
    for i in ind:
        x = x[i] 
    return x

def GlobalSortUser(users, sort=[], s=0, up=0):
    i = 1
    logging.info(users)
    for srts in sort:
        if s == i:
                users = sorted(users, key=lambda x: (SortList(x, srts) is not None, SortList(x, srts)), reverse=up)                
                return users
        i += 1  
    return users

def GlobalSort(users, sort=[], s=0, up=0):
    i = 1
    logging.info(s)
    for srts in sort:
        if s == i:
            #for srt in srts:
            #    logging.info("%s%s" % ("-" if up==1 else "", srts[0]))
            #    users = users.order_by("%s%s" % ("-" if up==1 else "", srt))
            if len(srts) == 1:
                users = users.order_by("%s%s" % ("-" if up == 1 else "", srts[0]))
            elif len(srts) == 2:
                users = users.order_by("%s%s" % ("-" if up == 1 else "", srts[0]), "%s%s" % ("-" if up == 1 else "", srts[1]))
            elif len(srts) == 3:
                users = users.order_by("%s%s" % ("-" if up == 1 else "", srts[0]), "%s%s" % ("-" if up == 1 else "", srts[1]), "%s%s" % ("-" if up == 1 else "", srts[2]))
            elif len(srts) == 4:
                users = users.order_by("%s%s" % ("-" if up == 1 else "", srts[0]), "%s%s" % ("-" if up == 1 else "", srts[1]), "%s%s" % ("-" if up == 1 else "", srts[2]), "%s%s" % ("-" if up == 1 else "", srts[3])) 
        i += 1
    return users

#БОЛЬШЕ НЕ использовать эту функцию, взамен просто c.getCameras(filter_active=True)
def getIdActCameras():
    cams = Camera.objects.all()
    from videoclient import models
    comms = models.Communicator.objects.filter(active = True)
    SERVERC = ''
    PORTC = ''
    COMMUNICATORS = []
    for comm in comms:
        COMMUNICATORS.append({'host': comm.host, 'port': comm.port, 'id': comm.id, 'commun': comm})
    from videoclient.communicator import Communicator
    ids_cam = []
    for communicator in COMMUNICATORS:
        c_connect = False
        try:
            c = Communicator(communicator["host"], int(communicator["port"]))
            c_connect = True
        except:
            logging.info("getIdActCameras: communicator connection is failed: " + str(sys.exc_info()))
        cameras = []
        cam_num = 0
        if c_connect:
            get_cameras = False
            try:
                cameras = c.getCameras()
                get_cameras = True
            except:
                get_cameras = False
                logging.info("getIdActCameras: c.getCameras is failed: " + str(sys.exc_info()))
        for cam in cameras:
            nickname = []
            try:
                nickname = cams.get_or_create(ip=cam["ip"], type=cam["type"])[0]
                ids_cam.append({'id': nickname.id, 'host': communicator['host'], 'port': communicator['port'], 'numcamera': cam['numcamera']})
            except:
                logging.info("getIdActCameras: nickname creation is failed: " + str(sys.exc_info()))      
    return ids_cam   

def getFoundFaceInJournal(f):
    face_found = f.split(',')
    face = map(lambda x: float(x), face_found) 
    result = {'face_quad':{
                           'top_left_corner':{'x':face[0], 'y':face[1]},
                            'top_right_corner':{'x':face[2], 'y':face[3]},
                            'bottom_right_corner':{'x':face[4], 'y':face[5]},
                            'bottom_left_corner':{'x':face[6], 'y':face[7]},
                            'sure': bool(face[8])}, 
               'right_eye': {
                             'x':face[9],
                             'y':face[10],
                             'sure': bool(face[11])},
               'left_eye': {
                            'x':face[12],
                            'y':face[13],
                            'sure': bool(face[14])},
               'nose': {
                            'x':face[15],
                            'y':face[16],
                            'sure': bool(face[17])},                               
               'chin': {
                            'x':face[18],
                            'y':face[19],
                            'sure': bool(face[20])}
               }
    return result

def getFilteredJournals(request, journals):
    form = TestDataJournal(request.GET, request.FILES) 
    now = datetime.datetime.now()
    today = datetime.date(year=int(now.strftime("%Y")), month=int(now.strftime("%m")), day=int(now.strftime("%d")))
    data = dict()
    data["timeBegin"] = {"hour":"0","minute":"0","second":"0"}
    data["timeEnd"] = {"hour":"23","minute":"59","second":"59"} 
    data["dateBegin"] = today
    data["dateEnd"] = today
   
    if form.is_valid():  
        data["start"] = form.cleaned_data["start"]

        if form.cleaned_data["id_record"]!=None:
            id = form.cleaned_data["id_record"]
            if id.isdigit():
                journals = journals.filter(agregate__id=id)
                data["id_record"] = form.cleaned_data["id_record"]
        
        if form.cleaned_data["no_date"]:            
            pass
        else:
            if form.cleaned_data["dateBegin"]:
                dateBegin = form.cleaned_data["dateBegin"]
            else:
                dateBegin = today
            
            if not (form.cleaned_data["hour_beg"] == None or form.cleaned_data["min_beg"] == None  or form.cleaned_data["sec_beg"] == None):
                dateBegin2 = dateBegin
                dateBegin = datetime.datetime(dateBegin2.year, dateBegin2.month, dateBegin2.day, int(form.cleaned_data["hour_beg"]), int(form.cleaned_data["min_beg"]), int(form.cleaned_data["sec_beg"]))
                data["timeBegin"] = {"hour":str(dateBegin.hour),"minute":str(dateBegin.minute),"second":str(dateBegin.second)}
                if dateBegin.hour!=0 or dateBegin.minute!=0 or dateBegin.second!=0:
                    data["time_check"] = True
            data["dateBegin"] = dateBegin
            journals = journals.filter(dt_first_fixed__gte=dateBegin)
                        
            if form.cleaned_data["dateEnd"]:
                dateEnd = form.cleaned_data["dateEnd"]
            else:
                dateEnd = today
                       
            if not (form.cleaned_data["hour_end"] == None or form.cleaned_data["min_end"] == None or form.cleaned_data["sec_end"] == None):
                dateBegin2 = dateEnd
                dateEnd = datetime.datetime(dateBegin2.year, dateBegin2.month, dateBegin2.day, int(form.cleaned_data["hour_end"]), int(form.cleaned_data["min_end"]), int(form.cleaned_data["sec_end"]))
                data["timeEnd"] = {"hour":str(dateEnd.hour),"minute":str(dateEnd.minute),"second":str(dateEnd.second)}
                if dateEnd.hour!=23 or dateEnd.minute!=59 or dateEnd.second!=59:
                    data["time_check"] = True
                journals = journals.filter(dt_last_fixed__lte=dateEnd)
            else:
                journals = journals.filter(dt_last_fixed__lt=dateEnd + datetime.timedelta(days=1))    
            data["dateEnd"] = dateEnd


        if form.cleaned_data["defined"]:
            if form.cleaned_data["defined"] == 'on':
                journals = journals.filter(person__id__gte=0)
            elif form.cleaned_data["defined"] == 'off':
                journals = journals.filter(person=None)
            data["defined"] = form.cleaned_data["defined"] 

        if form.cleaned_data["id_person"]!=None:
            i = form.cleaned_data["id_person"]
            if i.isdigit():
                journals = journals.filter(person__id = i)
                data["id_person"] = form.cleaned_data["id_person"]            

        if form.cleaned_data["cameras"]:
            import json
            try:
                cam_filter = json.loads(form.cleaned_data["cameras"])                                    
                journals = journals.filter(camera__id__in=cam_filter)
                data["cameras"]=cam_filter
            except:
                pass
             
        data["filter"] = form.cleaned_data["filter"]
        if form.cleaned_data["filter"]: #and not form.cleaned_data["filter"].lower() in ["поиск","search"]:
            fs = u"" + form.cleaned_data["filter"]
            fs = fs.split()
            i = 0
            while i < len(fs):
                f = fs[i]
                if i == 0:
                    journals = journals.filter(Q(agregate__id__icontains=f) | 
                                           Q(person__person__first_name__icontains=f) | 
                                           Q(person__person__last_name__icontains=f) | 
                                           Q(person__person__middle_name__icontains=f) | 
                                           Q(person__person__status__name__icontains=f) | 
                                           
                                           Q(person__person__category__name__icontains=f) | 
                                           
                                           Q(operator__last_name__icontains=f) | 
                                           Q(operator__middle_name__icontains=f) | 
                                           Q(operator__status__name__icontains=f) | 
                                           
                                           Q(camera__type__icontains=f) | 
                                           Q(camera__ip__icontains=f) |
                                           Q(operator__person__first_name__icontains=f) | 
                                           Q(operator__person__last_name__icontains=f) | 
                                           Q(operator__person__middle_name__icontains=f))
                else:
                    journals = journals.filter(#Q(agregate__id__icontains=f) | 
                                           Q(person__person__first_name__icontains=f) | 
                                           Q(person__person__last_name__icontains=f) | 
                                           Q(person__person__middle_name__icontains=f) | 
                                           Q(person__person__status__name__icontains=f) | 
                                           
                                           Q(person__person__category__name__icontains=f) | 
                                           
                                           Q(operator__last_name__icontains=f) | 
                                           Q(operator__middle_name__icontains=f) | 
                                           Q(operator__status__name__icontains=f) | 
                                           
                                           Q(camera__type__icontains=f) | 
                                           Q(camera__ip__icontains=f) |
                                           Q(operator__person__first_name__icontains=f) | 
                                           Q(operator__person__last_name__icontains=f) | 
                                           Q(operator__person__middle_name__icontains=f))
                i += 1
                
        if form.cleaned_data["fio"]:
            fs = u"" + form.cleaned_data["fio"]
            fs = fs.split()
            i = 0
            while i < len(fs):
                f = fs[i]
                journals = journals.filter(Q(person__person__first_name__icontains=f) | 
                                       Q(person__person__last_name__icontains=f) | 
                                       Q(person__person__middle_name__icontains=f))
                i += 1
            data["fio"]=form.cleaned_data["fio"]
                
        if form.cleaned_data["no_date"] and len(journals):
            
            j = journals.order_by('dt_first_fixed')
            
            StrDate = str(j[0].dt_first_fixed).split(' ')[0]
            arrData = StrDate.split('-')
            data['dateBegin'] = datetime.date(year=int(arrData[0]), month=int(arrData[1]), day=int(arrData[2]))            
            
            StrDate = str(j[len(j)-1].dt_last_fixed).split(' ')[0]
            arrData = StrDate.split('-')
            data['dateEnd'] = datetime.date(year=int(arrData[0]), month=int(arrData[1]), day=int(arrData[2]))     
            del j
    else:
        journals = journals.filter(dt_first_fixed__gte=data["dateBegin"]).filter(dt_last_fixed__lte=data["dateEnd"] + datetime.timedelta(days=1))
    return journals, data

def dataJournal(request, journalid=None, makezip=False):
#    try:
#        cursor = connection.cursor()
#        cursor.execute("create view videoclient_journal_agregate_view as select agregate_id, min(dt_first_fixed) as dt_first_fixed_min, max(dt_last_fixed) as dt_last_fixed_max,  count(*) as count_records from videoclient_journal group by agregate_id;")
#        transaction.commit_unless_managed()
#    except DatabaseError:
#        transaction.rollback_unless_managed()
#    except:
#        transaction.rollback_unless_managed()
#        logging.exception(str(sys.exc_info()))
        
    data = dict()
    sort = [["agregate"],
            ["dt_last_fixed", "agregate"], 
            ["dt_last_fixed", "agregate"],
            #["dt_first_fixed", "dt_last_fixed"],
            ["positions_status__name"],
            ["camera__ip"],
            ["person__person__first_name", "person__person__last_name", "person__person__middle_name"],
            ["person__person__status__name"],
            ["operator__person__first_name", "operator__person__last_name", "operator__person__middle_name"]]    
    s = 0
    up = 0    
    csm = float(get_value_defaultparams(journalBoundCoeff)) * 100
    if journalid: data["journal"] = Journal.objects.get(id=journalid)    
    else:
        journals = Journal.objects.exclude(agregate=None)
        
        param_aggregator = ParamAggregator.getRecord()
        
        journals = journals.filter(id__gt=param_aggregator.getParam(ParamAggregator.PARAM_JOURNAL_FIRST_ID))
        journals = journals.filter(id__lte=param_aggregator.getParam(ParamAggregator.PARAM_JOURNAL_LAST_ID))
        
        journals_count = journals.extra(where=['id = agregate_id'])
        
        data["journals_count"] = param_aggregator.getParam(ParamAggregator.PARAM_JOURNAL_COUNT)
        data["journals_ident_count"] = param_aggregator.getParam(ParamAggregator.PARAM_JOURNAL_IDENT_COUNT)
        
        #journals.query.group_by = ['agregate_id']
        
        journals, d = getFilteredJournals(request, journals)
        data.update(d)
        
        if request.GET.has_key('countrows'):
            data["all_countrows"] = journals.count()
        
        journals = journals.extra(where=['videoclient_journal.id = videoclient_journal.agregate_id'])
        if request.GET.has_key('countrows'):
            journals_count = journals.extra(where=['agregate_id = videoclient_journal.id'])
            data["all_users"] = journals_count.count()
        data['all_cameras'] = Camera.objects.filter(active=True).order_by('-available', 'delete', '-id').exclude(type="IMPORT")
            
        journals_count = journals.extra(where=['agregate_id = videoclient_journal.id'])
        
        form = TestDataJournal(request.GET, request.FILES) 
        if form.is_valid():
            if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
            if form.cleaned_data["sorto"] is not None and form.cleaned_data["sorto"] < len(sort): s = form.cleaned_data["sorto"]
            else: 
                s = 1
                up = 1
            args = []
            i = 0
            while i < len(sort[s]):
                args.append("%s%s" % ("-" if up == 1 else "", sort[s][i]))
                i += 1
            journals = journals.order_by(*args)             
            data["up"] = up
            data["sorto"] = s    

        COL_JOURNAL_PAGES = 3
        limits = [18,27,36,45]
        if request.GET.has_key('per_page'):
            try:
                limit = int(request.GET['per_page'])
            except:
                limit = limits[0]
        else:
            limit = limits[0]
        if not request.GET.has_key('countrows') and not makezip:     
            if form.cleaned_data["all_pages"]:     
                data["all_users"] = journals_count.count()
                ident_journals = journals_count.exclude(person=None)
                data["all_ident_users"] = ident_journals.count()
                data["all_pages"] = form.cleaned_data["all_pages"]
                if data["all_users"] > COL_JOURNAL_PAGES * limit:
                    data["need_button"] = True
            else:
                journals = list(journals[:COL_JOURNAL_PAGES * limit + 1])
                if len(journals) > COL_JOURNAL_PAGES * limit:
                    data["all_users"] = COL_JOURNAL_PAGES * limit
                    data["need_button"] = True
                else:
                    data["all_pages"] = 'True'
                    data["all_users"] = len(journals)
                    ident_journals = journals_count.exclude(person=None)
                    data["all_ident_users"] = ident_journals.count()
                
        data['status_enter'] = status_enter
        if not makezip:
            data.update(dataNavigation(request, data['all_users'], limits=limits))
            journals = journals[data['start'] - 1:data['finish'] - 1]
        import Image
        faces = []
        for journal in journals:
            face = journal.found_face.split(',')
            face = map(lambda x: float(x), face)
            filename = WWW_ROOT + 'files/%s' % journal.original
            try:
                img = Image.open(filename)
                width, height = img.size
                face.extend([width, height]) 
            except:
                face.extend([300,300])
            faces.extend([face])
        data["faces"] = faces
        data["users"] = journals
    return data


class TestDataLogDetectJournal(forms.Form):
    dateBegin = forms.DateField(required=False, input_formats=('%d.%m.%Y',),)
    dateEnd = forms.DateField(required=False, input_formats=('%d.%m.%Y',),)
    defined = forms.CharField(required=False)

    hour_beg = forms.IntegerField(required=False)
    min_beg = forms.IntegerField(required=False)
    hour_end = forms.IntegerField(required=False)
    min_end = forms.IntegerField(required=False)
    
    id_record = forms.CharField(required=False)

    type = forms.IntegerField(required=False)

    description = forms.CharField(required=False)
    
    cameras = forms.CharField(required=False)
    
    delo = forms.IntegerField(required=False)
    concato = forms.IntegerField(required=False)
    sorto = forms.IntegerField(required=False)    
    start = forms.IntegerField(required=False)
    up = forms.IntegerField(required=False)
    communicator = forms.IntegerField(required=False)
    camera = forms.IntegerField(required=False)

def dataVAJournal(request, journalid=None):
    data = dict()
    sort = [[], ["dt_detect"],
            ["dt_detect"],
            ["dt_detect"],
            ["frame"],
            ["camera__type", "camera__ip", "camera__name"],
            ["detector_type"],
            ["description"]]    
    s = 0
    up = 0    
    if journalid: data["journal"] = DetectorLog.objects.get(id=journalid)    
    else: 
        journals = DetectorLog.objects.all()
        data["journals_count"] = journals.count()   
        data["types"] = Detector.objects.all()   
        form = TestDataLogDetectJournal(request.GET, request.FILES)      
        data['all_cameras'] = Camera.objects.filter(active=True).order_by('-available', 'delete', '-id').exclude(type="IMPORT")    
        if form.is_valid():  
            data["start"] = form.cleaned_data["start"]
            now = datetime.datetime.now()
            today = datetime.date(year=int(now.strftime("%Y")), month=int(now.strftime("%m")), day=int(now.strftime("%d")))
             
            if form.cleaned_data["dateBegin"]:
                dateBegin = form.cleaned_data["dateBegin"]
            else:
                dateBegin = today
            data["timeBegin"] = {"hour":"0","minute":"0"}
            if not (form.cleaned_data["hour_beg"] == None or form.cleaned_data["min_beg"] == None):
                dateBegin2 = dateBegin
                dateBegin = datetime.datetime(dateBegin2.year, dateBegin2.month, dateBegin2.day, int(form.cleaned_data["hour_beg"]), int(form.cleaned_data["min_beg"]), 0)
                data["timeBegin"] = {"hour":str(dateBegin.hour),"minute":str(dateBegin.minute)}
                if dateBegin.hour!=0 or dateBegin.minute!=0:
                    data["time_check"] = True
            data["dateBegin"] = dateBegin
            journals = journals.filter(dt_detect__gte=dateBegin)

            if form.cleaned_data["dateEnd"]:
                dateEnd = form.cleaned_data["dateEnd"]
            else:
                dateEnd = today
            data["timeEnd"] = {"hour":"23","minute":"59"}            
            time_delta = datetime.timedelta(days=1)
            if not (form.cleaned_data["hour_end"] == None or form.cleaned_data["min_end"] == None):
                dateBegin2 = dateEnd
                dateEnd = datetime.datetime(dateBegin2.year, dateBegin2.month, dateBegin2.day, int(form.cleaned_data["hour_end"]), int(form.cleaned_data["min_end"]), 59)
                time_delta = datetime.timedelta(microseconds=1)
                data["timeEnd"] = {"hour":str(dateEnd.hour),"minute":str(dateEnd.minute)}
                if dateEnd.hour!=23 or dateEnd.minute!=59:
                    data["time_check"] = True
            data["dateEnd"] = dateEnd
            journals = journals.filter(dt_detect__lte=dateEnd + time_delta) 
             
            if form.cleaned_data["id_record"]:
                id = form.cleaned_data["id_record"]
                if id.isdigit():
                    journals = journals.filter(id=id)
                    data["id_record"] = form.cleaned_data["id_record"]
            if form.cleaned_data["type"]:
                type = form.cleaned_data["type"]
                if type != "0": 
                    data["type"] = type
                    journals = journals.filter(detector_type__id=type) 
            
            if form.cleaned_data["description"]:
                data["description"] = form.cleaned_data["description"]
                fs = u""+form.cleaned_data["description"]
                fs = fs.split()
                i = 0
                while i < len(fs):
                    f = fs[i]
                    journals = journals.filter(Q(description__icontains=f))
                    i = i+1
                                 #map(lambda x: "%s%s" % ("-" if up==1 else "", x), sort[s])
            if form.cleaned_data["cameras"]:
                import json
                try:
                    cam_filter = json.loads(form.cleaned_data["cameras"])                                    
                    journals = journals.filter(camera__id__in=cam_filter)
                    data["cameras"]=cam_filter
                except:
                    pass
            if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
            if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]
            else: 
                s = 1
                up = 1      
            args = []
            i = 0
            while i < len(sort[s]):
                args.append("%s%s" % ("-" if up == 1 else "", sort[s][i]))
                i += 1
            journals = journals.order_by(*args)            
#        journals = GlobalSort(journals, sort, s, up)
        data["up"] = up
        data["sorto"] = s                     
#        journals = getDictUsers(journals.order_by("-id"))

        data["all_users"] = journals.count()
        #data["all_ident_users"] = journals.exclude(person=None).count()
        data["users"] = journals
    return data

def dataAccess(request, journalid=None):
    try:
        data = dict()
        data["access"] = False    
        if journalid: 
            journal = Journal.objects.get(id=journalid)
            if journal.person and journal.person.active == 1:
                if journal.person.person.status.division.id == division_visitor:                    
                    vc = VisitingCard.objects.filter(dt_enter__lte=journal.dt_first_fixed, dt_exit__gte=journal.dt_last_fixed, visitor=journal.person)                   
                    if vc.count() > 0: 
                        dt = datetime.datetime.now()
                        vci = -1
                        i = 0
                        while i < vc.count() and vci == -1:
                            v = vc[i]
                            if v.dt_enter.strftime("%Y-%m-%d") != v.dt_exit.strftime("%Y-%m-%d") and v.active:
                                if v.dt_enter.strftime("%H:%M:S") <= dt.strftime("%H:%M:S") and v.dt_exit.strftime("%H:%M:S") >= dt.strftime("%H:%M:S"): vci = i
                            else: vci = i
                            i += 1
                        if vci == -1:
                            data["vc"] = vc[0]
                            return data
                        data["vc"] = vc[vci]
                        data["access"] = True
                    else: 
                        vc = VisitingCard.objects.filter(visitor=journal.person).order_by("-dt_exit")
                        if vc.count() > 0: data["vc"] = vc[0]
                elif journal.person.person.status.division.id != division_person: data["access"] = True
                if journal.camera:
                    jbuf = Journal.objects.filter(person=journal.person, positions_status__lt=status_notdefined).order_by("-id")
                    if jbuf.count() > 0 and jbuf[0].positions_status.id == status_enter and journal.camera.position in [camera_exit, camera_all]: data["status_movement"] = PositionsStatus.objects.get(id=status_exit).name
                    elif  (jbuf.count() == 0 or jbuf[0].positions_status.id == status_exit) and journal.camera.position in [camera_enter, camera_all]: data["status_movement"] = PositionsStatus.objects.get(id=status_enter).name
                    else: data["access"] = False
        logging.info(data["access"])
        return data
    except:
        logging.exception("dateAccess " + str(sys.exc_info()))
        return data
    
def getVisitorInfo(request):
    data = dict()
    if request.GET.has_key('group'):
        group_id = int(request.GET['group'])
        data["visitor"] = PersonId.objects.filter(person__status__division__id=division_visitor, active=1, person__group__id=group_id)
    else:
        data["visitor"] = PersonId.objects.filter(person__status__division__id=division_visitor, active=1)
        
    
    data["person"] = PersonId.objects.filter(person__status__division__id=division_person, active=1)
    data["employee"] = PersonId.objects.filter(person__status__division__id=division_employee, active=1)
    return data

def dataVisitors(request, vcid=None):
    data = dict()
    sort = [["id"],
            ["visitor__person__first_name", "visitor__person__last_name", "visitor__person__middle_name"],
            ["visitor__person__status__name"],
            ["visitor__person__document__name"],
            ["person__person__first_name", "person__person__last_name", "person__person__middle_name"],
            ["ground__name"],
            ["dt_enter"],
            ["dt_enter"],
            ["dt_exit"]]    
    s = 0
    up = 0    
    if vcid: 
        data["visitingcard"] = VisitingCard.objects.get(id=vcid)
        data["dt_enter_hour"] = data["visitingcard"].dt_enter.strftime("%H")
        data["dt_enter_min"] = data["visitingcard"].dt_enter.strftime("%M")
        data["dt_exit_hour"] = data["visitingcard"].dt_exit.strftime("%H")
        data["dt_exit_min"] = data["visitingcard"].dt_exit.strftime("%M")        
        return data 
    
    if request.GET.has_key('group'):
        group_id = int(request.GET['group'])
        data["group"] = group_id
        vc = VisitingCard.objects.filter(visitor__person__group__id=group_id)
        data["visitor_count"] = PersonId.objects.filter(active=1, person__status__division__id=division_visitor, person__group__id=group_id).count()
    else:
        vc = VisitingCard.objects.filter()
        data["visitor_count"] = PersonId.objects.filter(active=1, person__status__division__id=division_visitor).count()
    
    form = TestDataJournal(request.GET, request.FILES)  
    if form.is_valid():
        data["start"] = form.cleaned_data["start"]
        logging.info("vc" + str(form.cleaned_data["delo"])) 
        if form.cleaned_data["delo"]:            
            for rp in range(1, int(form.cleaned_data["delo"]) + 1):
                try:
                    if "vc" + str(rp) in request.GET: VisitingCard.objects.get(id=int(request.GET["vc" + str(rp)])).delete()
                except: logging.exception(sys.exc_info())
            if request.GET.has_key('group'):
                vc = VisitingCard.objects.filter(visitor__person__group__id=group_id)
            else:                    
                vc = VisitingCard.objects.filter()
        if form.cleaned_data["dateBegin"]:
            data["dateBegin"] = form.cleaned_data["dateBegin"]
            vc = vc.filter(dt_enter__gte=form.cleaned_data["dateBegin"])            
        if form.cleaned_data["dateEnd"]:
            data["dateEnd"] = form.cleaned_data["dateEnd"]
            vc = vc.filter(dt_enter__lte=form.cleaned_data["dateEnd"] + datetime.timedelta(days=1))
        data["filter"] = form.cleaned_data["filter"]
        if form.cleaned_data["filter"] and form.cleaned_data["filter"].lower() != "поиск":
            f = form.cleaned_data["filter"]
            vc = vc.filter(Q(ground__name__icontains=f) | 
                           Q(visitor__person__status__name__icontains=f) | 
                           Q(visitor__person__document__name__icontains=f) | 
                           Q(person__person__first_name__icontains=f) | 
                           Q(person__person__last_name__icontains=f) | 
                           Q(person__person__middle_name__icontains=f) | 
                           Q(visitor__person__first_name__icontains=f) | 
                           Q(visitor__person__last_name__icontains=f) | 
                           Q(visitor__person__middle_name__icontains=f))    
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]
    vc = GlobalSort(vc, sort, s, up)
    data["up"] = up
    data["sorto"] = s            
    data["visitingcard"] = vc
    data['dt_enter_hour'] = data["visitingcard"].dt_enter.strftime("%H")
    data["dt_enter_min"] = data["visitingcard"].dt_enter.strftime("%M")
    data["dt_exit_hour"] = data["visitingcard"].dt_exit.strftime("%H")
    data["dt_exit_min"] = data["visitingcard"].dt_exit.strftime("%M")    
    data["users"] = vc
    data["vc_count"] = vc.count()
    return data

def staffFilter(staff, f):
    return staff.filter(Q(person__person__first_name__icontains=f) | 
                        Q(person__person__last_name__icontains=f) | 
                        Q(person__person__middle_name__icontains=f) | 
                        Q(person__person__status__name__icontains=f) | 
                        Q(camera__kpp__name__icontains=f))     

def dataStaff(request):
    data = dict()
    sort = [["id"],
            ["person__person__first_name", "person__person__last_name", "person__person__middle_name"],
            ["person__person__status__name"],
            ["dt_first_fixed"],
            ["camera__kpp"],
            ["dt_first_fixed"],
            ["camera__kpp"]]    
    s = 0
    up = 0
    
    if request.GET.has_key('group'):
        group_id = int(request.GET['group'])
        data["group"] = group_id
        data["employee_count"] = PersonId.objects.filter(person__status__division__id=division_employee, active=1, person__group__id=group_id).count()
        staffs = Journal.objects.filter(positions_status=status_enter, person__person__status__division__id=division_employee, person__person__group__id=group_id)
    else:
        data["employee_count"] = PersonId.objects.filter(person__status__division__id=division_employee, active=1).count()
        staffs = Journal.objects.filter(positions_status=status_enter, person__person__status__division__id=division_employee)
    
    form = TestDataJournal(request.GET, request.FILES)  
    if form.is_valid():
        data["start"] = form.cleaned_data["start"]
        if form.cleaned_data["dateBegin"]:
            data["dateBegin"] = form.cleaned_data["dateBegin"]
            staffs = staffs.filter(dt_first_fixed__gte=form.cleaned_data["dateBegin"])                        
        if form.cleaned_data["dateEnd"]:
            data["dateEnd"] = form.cleaned_data["dateEnd"]
            staffs = staffs.filter(dt_first_fixed__lte=form.cleaned_data["dateEnd"] + datetime.timedelta(days=1))
        data["filter"] = form.cleaned_data["filter"]
        if form.cleaned_data["filter"] and form.cleaned_data["filter"].lower() != "поиск":
            f = form.cleaned_data["filter"]
            staffs = staffs.filter(Q(person__person__status__name__icontains=f) | 
                                 Q(person__person__first_name__icontains=f) | 
                                 Q(person__person__last_name__icontains=f) | 
                                 Q(person__person__middle_name__icontains=f) | 
                                 Q(camera__kpp__name__icontains=f))            
            staffs = staffFilter(staffs, f)
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]                 
    i = 0
    staffs = GlobalSort(staffs, sort, s, up)    
    staff_result = []    
    for staff in staffs:
        if form.is_valid() and form.cleaned_data["dateEnd"]:
            j = Journal.objects.filter(person=staff.person, positions_status=status_exit, id__gt=staffs[i].id, dt_first_fixed__lte=form.cleaned_data["dateEnd"] + datetime.timedelta(days=1))
            if form.cleaned_data["filter"] and form.cleaned_data["filter"].lower() != "поиск": j = staffFilter(j, f)
#            if j.count() == 0: ok = False
        else: j = Journal.objects.filter(person=staff.person, positions_status=status_exit, id__gt=staffs[i].id)                
        if j.count() > 0:
            setattr(staff, "dt_exit", j[0].dt_first_fixed)
            if j[0].camera: setattr(staff, "kpp_exit", j[0].camera.kpp)
        staff_result.append(staff)        
        i += 1
    data["up"] = up
    data["sorto"] = s
    #cmp=lambda x, y: x.kpp_exit < y.kpp_exit         
    #staff_result.sort(cmp)
    data["staffs"] = staff_result
    return data

def DeletePerson(request, person_id=0):
    
    if person_id:
                        logging.info("person_id: " + str(person_id))
                        dirname = LEARNING_IMAGES + '%s/' % (person_id)
                        if os.path.isdir(dirname):
                            import shutil 
                            shutil.rmtree(dirname) 
                        pid = PersonId.objects.filter(id=int(person_id))
                        logging.info("pid: " + str(pid))
                        if not DeletePersonFromFr(pid[0]): return False
                        pid.update(active=0)
                        pid.update(bal_id=None)
                        p = pid[0].person
                        try:
                            user = User.objects.filter(id=request.user.id)
                        except:
                            user = None
                        try:
                            photoexif = PhotoExifData.objects.filter(person_id=int(person_id))
                            photoexif.delete()
                        except:
                            pass
                        pnew = Person.objects.create(date=p.date,
                                                     id_person=p.id_person,
                                                     user=None if user is None or user.count() == 0 else user[0],
                                                     action=action_delete,
                                                     first_name=p.first_name,
                                                     last_name=p.last_name,
                                                     middle_name=p.middle_name,
                                                     birthday=p.birthday,
                                                     passport_series=p.passport_series,
                                                     passport_number=p.passport_number,
                                                     passport_note=p.passport_note,
                                                     passport_date=p.passport_date,
                                                     address=p.address,
                                                     phone_work=p.phone_work,
                                                     phone_home=p.phone_home,
                                                     phone_mobile=p.phone_mobile,
                                                     note=p.note,
                                                     group=p.group,
                                                     status=p.status,
                                                     goto=p.goto,
                                                     document=p.document,
                                                     passport_code=p.passport_code,
                                                     address_temp=p.address_temp,
                                                     category=p.category,
                                                     number=p.number,
                                                     article=p.article,
                                                     article_part=p.article_part,
                                                     article_item=p.article_item,
                                                     room_facility=p.room_facility)
                        p = pnew   


def getSearchStaffs(request, division=division_employee):
    data = dict()
    s = 0
    up = 0
    sort = [["id"],
            ["person__first_name", "person__last_name", "person__middle_name"],
            ["person__status__name"]]
    form = TestDataJournal(request.GET, request.FILES)     
    if form.is_valid():
        data["start"] = form.cleaned_data["start"]
        
        if form.cleaned_data["concato"]:
            data['concato'] = 1
            newPerson = None
            persons = []
            for rp in range(1, form.cleaned_data["concato"] + 1):
                try:                   
                    if "pi" + str(rp) in request.GET:
                        person = getBalIdByName(int(request.GET["pi" + str(rp)]))
                        persons.append(person)
                except: logging.exception(sys.exc_info())
            from videoclient.balancer import Balancer
            from videoclient.views import initBalancer
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            try:
                b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
                newPerson = b.concatenatePersons(persons)
                b.close()
                del b
            except:
                logging.exception("concat person: " + str(sys.exc_info()))
                
            if newPerson:
                from videoclient.views import createPerson 
                createPerson(newPerson)
            if newPerson:                 
                for rp in range(1, form.cleaned_data["concato"] + 1):
                    try:                   
                        if "pi" + str(rp) in request.GET: DeletePerson(request, int(request.GET["pi" + str(rp)]))
                    except: logging.exception(sys.exc_info())
        elif form.cleaned_data["delo"]:
            data['delo'] = 1            
            for rp in range(1, form.cleaned_data["delo"] + 1):
                try:                   
                    if "pi" + str(rp) in request.GET: DeletePerson(request, int(request.GET["pi" + str(rp)]))
                except: logging.exception(sys.exc_info())
                
        if request.REQUEST.has_key('group'):
            group_id = int(request.REQUEST['group'])
            data["group"] = group_id
            users = PersonId.objects.filter(person__status__division__id=division, active=1, person__group__id=group_id)
        else:
            users = PersonId.objects.filter(person__status__division__id=division, active=1)
        
        data["all_staffs"] = users.count()
        data["filter"] = form.cleaned_data["filter"]        
        if form.cleaned_data["filter"]:
            fs = u"" + form.cleaned_data["filter"]
            fs = fs.split()
            i = 0
            while i < len(fs):
                f = fs[i]
                if f.isdigit():
                    ff = int(f)
                    users = users.filter(Q(person__status__name__icontains=f) | 
                                 Q(person__first_name__icontains=f) | 
                                 Q(person__last_name__icontains=f) | 
                                 Q(person__middle_name__icontains=f)|
                                 Q(id=ff))
                else:
                    users = users.filter(Q(person__status__name__icontains=f) | 
                                 Q(person__first_name__icontains=f) | 
                                 Q(person__last_name__icontains=f) | 
                                 Q(person__middle_name__icontains=f))
                i += 1
            data['filter_staff'] = users.count()  
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]
        else: 
            s = 1
            up = 1                                              
    else: 
        users = PersonId.objects.filter(person__status__division__id=division, active=1)
        data["all_staffs"] = users.count()    
    users = GlobalSort(users, sort, s, up)
#    users = GlobalSortUser(users, sort, s, up)
    data["up"] = up
    data["sorto"] = s
    data["users"] = users
    return data

def getSearchPerson(request):
    data = dict()
    s = 0
    up = 0
    sort = [["id"],
            ["person__first_name", "person__last_name", "person__middle_name"],
            ["person__status__name"],
            ["person__category__name"],
            ["person__article__name", "person__article_part__name", "person__article_item__name"],
            ["person__room_facility"]]
    form = TestDataJournal(request.GET, request.FILES)     
    if form.is_valid():
        data["start"] = form.cleaned_data["start"]
        if form.cleaned_data["delo"]:            
            data['delo'] = 1
            for rp in range(1, form.cleaned_data["delo"] + 1):
                try:
                    if "pi" + str(rp) in request.GET: DeletePerson(request, int(request.GET["pi" + str(rp)]))
                except: logging.exception("new error: " + str(sys.exc_info()))
        if request.GET.has_key('group'):
            group_id = int(request.GET['group'])
            data["group"] = group_id
            users = PersonId.objects.filter(person__status__division__id=division_person, active=1, person__group__id=group_id)
        else:
            users = PersonId.objects.filter(person__status__division__id=division_person, active=1)
        data["all_persons"] = users.count()
        if form.cleaned_data["filter"]:
            data["filter"] = form.cleaned_data["filter"]  
            fs = u"" + form.cleaned_data["filter"]
            fs = fs.split()
            i = 0
            while i < len(fs):
                f = fs[i]
                if f.isdigit():
                    ff = int(f)
                    users = users.filter(Q(person__status__name__icontains=f) | 
                                 Q(person__first_name__icontains=f) | 
                                 Q(person__last_name__icontains=f) | 
                                 Q(person__middle_name__icontains=f) | 
                                 Q(person__status__name__icontains=f) | 
                                 Q(person__category__name__icontains=f) | 
                                 Q(person__article__name__icontains=f) | 
                                 Q(person__article_part__name__icontains=f) | 
                                 Q(person__article_item__name__icontains=f) | 
                                 Q(person__room_facility__icontains=f)|
                                 Q(id=ff))
                else:
                    users = users.filter(Q(person__status__name__icontains=f) | 
                                 Q(person__first_name__icontains=f) | 
                                 Q(person__last_name__icontains=f) | 
                                 Q(person__middle_name__icontains=f) | 
                                 Q(person__status__name__icontains=f) | 
                                 Q(person__category__name__icontains=f) | 
                                 Q(person__article__name__icontains=f) | 
                                 Q(person__article_part__name__icontains=f) | 
                                 Q(person__article_item__name__icontains=f) | 
                                 Q(person__room_facility__icontains=f))
                i += 1 
            data['filter_persons'] = users.count()  
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]
        else: 
            s = 1
            up = 1
    else: 
        users = PersonId.objects.filter(person__status__division__id=division_person, active=1)
        data["all_persons"] = users.count()
    users = GlobalSort(users, sort, s, up)
    data["up"] = up
    data["sorto"] = s            
    data["users"] = users
    return data


def getSearchEvent(request):
    data = dict()
    
    events = Event.objects.filter(profile=None)
    data['all_events'] = events.count()
    
    s = 0
    up = 0
    sort = [["id"],
            ["name"],
            ["sound__name"],
            ["signal__name"]]
    form = TestDataJournal(request.GET, request.FILES)     
    if form.is_valid():
        data["start"] = form.cleaned_data["start"]
        data["filter"] = form.cleaned_data["filter"]        
        if form.cleaned_data["filter"] and form.cleaned_data["filter"].lower() != "поиск":
            f = form.cleaned_data["filter"]            
            events = events.filter(Q(name__icontains=f) | 
                                 Q(sound__name__icontains=f) | 
                                 Q(signal__name__icontains=f))
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]
        else: 
            s = 1
            up = 1
        
    events = GlobalSort(events, sort, s, up)
    
    data["up"] = up
    data["sorto"] = s
    data['events'] = events            
    return data

def getSearchVisitors(request):
    data = dict()
    s = 0
    up = 0
    sort = [["id"],
            ["person__first_name", "person__last_name", "person__middle_name"],
            ["person__status__name"],
            ["person__document__name"]]   
    form = TestDataJournal(request.GET, request.FILES)     
    if form.is_valid():
        data["start"] = form.cleaned_data["start"]
        logging.info("del person " + str(form.cleaned_data["delo"])) 
        if form.cleaned_data["delo"]: 
            data['delo'] = 1           
            for rp in range(1, int(form.cleaned_data["delo"]) + 1):
                try:
                    logging.info("del person ===" + str("pi" + str(rp)))
                    if "pi" + str(rp) in request.GET:
                        logging.info("del person " + str(request.GET["pi" + str(rp)])) 
                        DeletePerson(request, int(request.GET["pi" + str(rp)]))
                except: logging.exception(sys.exc_info())
        if request.GET.has_key('group'):
            group_id = int(request.GET['group'])
            data["group"] = group_id
            users = PersonId.objects.filter(person__status__division__id=division_visitor, active=1, person__group__id=group_id)
        else:
            users = PersonId.objects.filter(person__status__division__id=division_visitor, active=1)    
                      
        
        data["all_visitors"] = users.count()
        data["filter"] = form.cleaned_data["filter"]        
        if form.cleaned_data["filter"]:
            fs = u"" + form.cleaned_data["filter"]
            fs = fs.split()
            i = 0
            while i < len(fs):
                f = fs[i]
                if f.isdigit():
                    ff = int(f)
                    users = users.filter(Q(person__status__name__icontains=f) | 
                                 Q(person__first_name__icontains=f) | 
                                 Q(person__last_name__icontains=f) | 
                                 Q(person__middle_name__icontains=f) | 
                                 Q(person__document__name__icontains=f)|
                                 Q(id=ff))
                else:
                    users = users.filter(Q(person__status__name__icontains=f) | 
                                 Q(person__first_name__icontains=f) | 
                                 Q(person__last_name__icontains=f) | 
                                 Q(person__middle_name__icontains=f) | 
                                 Q(person__document__name__icontains=f))
                i += 1
            data['filter_visitors'] = users.count()  
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]
        else: 
            s = 1
            up = 1                    
    else: 
        users = PersonId.objects.filter(person__status__division__id=division_visitor, active=1)
        data["all_visitors"] = users.count()
    users = GlobalSort(users, sort, s, up)       
    data["up"] = up
    data["sorto"] = s             
    data["users"] = users
    return data

def UserFilterFIO(f=""):
    farray = f.strip().split(" ") # массив из слов поиска
    sobject = "staff in (select vpi.id from videoclient_personid as vpi join videoclient_person as vp on vp.id=vpi.person_id where "
    i = False
    for fs in farray:
        sobject = "%s %s vp.first_name like '%%%s%%' or vp.last_name like '%%%s%%' or vp.middle_name like '%%%s%%'" % (sobject, " or " if i else "", fs, fs, fs)
        i = True            
    sobject = "%s)" % (sobject)
    sobject = sobject.replace("%", "%%")
    return User.objects.extra(where=[sobject])

def UserFilterUserKpp(f=""):
    farray = f.strip().split(" ") # массив из слов поиска
    users2 = User.objects.filter(id=0, is_active=True)
    for fs in farray: 
        users2 = users2 | User.objects.filter(Q(kpp__name__icontains=fs), is_active=True)           
    return users2

def LJFilterFIO(f=""):
    farray = f.strip().split(" ") # массив из слов поиска
    users2 = LoginJournal.objects.filter(id=0)
    for fs in farray: 
        users2 = users2 | LoginJournal.objects.filter(Q(user__first_name__icontains=fs) | Q(user__last_name__icontains=fs) | Q(user__middle_name__icontains=fs))           
    return users2    
#    farray = f.strip().split(" ") # массив из слов поиска
#    sobject = "user_id in (select vu.user_ptr_id from videoclient_user as vu join videoclient_personid as vpi on vu.staff=vpi.id join videoclient_person as vp on vp.id=vpi.person_id where "
#    i = False
#    for fs in farray:
#        sobject = "%s %s vp.first_name like '%%%s%%' or vp.last_name like '%%%s%%' or vp.middle_name like '%%%s%%'" % (sobject, " or " if i else "", fs, fs, fs)
#        i = True            
#    sobject = "%s)" % (sobject)
#    sobject = sobject.replace("%", "%%")
#    return LoginJournal.objects.extra(where=[sobject])

def LJFilterKpp(f=""):
    farray = f.strip().split(" ") # массив из слов поиска
    users2 = LoginJournal.objects.filter(id=0)
    for fs in farray: 
        users2 = users2 | LoginJournal.objects.filter(Q(user__kpp__name__icontains=fs))           
    return users2

def getSearchKpp(request):
    data = dict()
    s = 0
    up = 0
    sort = [["id"],
            ["user__kpp__name"],
            ["user__kpp__name"],
            ["login"],
            ["login"],
            ["logout"],
            ["logout"],
            ["user__first_name", "user__last_name", "user__middle_name"],
            ["user__status"]
            ]     
    users = LoginJournal.objects.all()
    #.extra(select={'staff_name': 'select concat(vp.first_name, " ", vp.last_name, " ", vp.middle_name) from videoclient_person as vp join videoclient_personid as vpid on vpid.person_id=vp.id join videoclient_user as vu on vu.staff=vpid.id where vu.user_ptr_id=videoclient_loginjournal.user_id'})
    data["all_loginjournal"] = users.count()
    form = TestDataJournal(request.GET, request.FILES)
    if form.is_valid():
        logging.info("filter " + str(form.cleaned_data["filter"]))
        data["start"] = form.cleaned_data["start"]  
        now = datetime.datetime.now()
        today = datetime.date(year=int(now.strftime("%Y")), month=int(now.strftime("%m")), day=int(now.strftime("%d")))  
        
        if form.cleaned_data["filter"] and form.cleaned_data["filter"].lower() != "поиск" and form.cleaned_data["filter"].lower() != "search":
            data["filter"] = form.cleaned_data["filter"]
            f = form.cleaned_data["filter"]
            users = LJFilterKpp(f) | LJFilterFIO(f)

        if form.cleaned_data["dateBegin"]:
            dateBegin = form.cleaned_data["dateBegin"]
        else:
            dateBegin = today
        data["dateBegin"] = dateBegin
        users = users.filter(login__gte=dateBegin)                    
        
        if form.cleaned_data["dateEnd"]:
            dateEnd = form.cleaned_data["dateEnd"]
        else:
            dateEnd = today
        data["dateEnd"] = dateEnd
        users = users.filter(login__lte=dateEnd + datetime.timedelta(days=1)) 
              
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): 
            s = form.cleaned_data["sorto"]
        else:
            s = 1
            up = 1
    #users = GlobalSort(users, sort, s, up)
    data["up"] = up
    data["sorto"] = s
    data["users"] = users
    return data

def getSearchHistory(request):
    data = dict()
    s = 0
    up = 0
    sort = [["date"],
            ["action"],
            ["user__first_name", "user__last_name", "user__middle_name"],
            ["first_name", "last_name", "middle_name"],
            ["status__name"]]
    users = Person.objects.extra(select={'staff_name': "select vp.first_name ||' '|| vp.last_name ||' '|| vp.middle_name from videoclient_person as vp join videoclient_personid as vpid on vpid.person_id=vp.id join videoclient_user as vu on vu.staff=vpid.id join videoclient_person as vp2 on vp2.user_id=vu.user_ptr_id where vp2.id=videoclient_person.id"})
    data["all_history"] = users.count()
    form = TestDataJournal(request.GET, request.FILES)     
    if form.is_valid():                
        data["start"] = form.cleaned_data["start"]
        
        now = datetime.datetime.now()
        today = datetime.date(year=int(now.strftime("%Y")), month=int(now.strftime("%m")), day=int(now.strftime("%d")))
        if form.cleaned_data["dateBegin"]:
            dateBegin = form.cleaned_data["dateBegin"]
        else:   
            dateBegin = today
        users = users.filter(date__gte=dateBegin)            
        data["dateBegin"] = dateBegin
        if form.cleaned_data["dateEnd"]:
            dateEnd = form.cleaned_data["dateEnd"]
        else:
            dateEnd = today    
        users = users.filter(date__lte=dateEnd + datetime.timedelta(days=1))
        data["dateEnd"] = dateEnd

        if form.cleaned_data["filter"] and form.cleaned_data["filter"].lower() != "поиск" and form.cleaned_data["filter"].lower() != "search":
            data["filter"] = form.cleaned_data["filter"]
            fs = form.cleaned_data["filter"]
            fs = fs.split()
            i = 0
            while i < len(fs):
                f = fs[i]
                users = users.filter(#Q(staff_name__icontains=f) |
                                     Q(first_name__icontains=f) | 
                                     Q(last_name__icontains=f) | 
                                     Q(middle_name__icontains=f) | 
                                     Q(status__name__icontains=f) |
                                     Q(user__first_name__icontains=f) | 
                                     Q(user__last_name__icontains=f) | 
                                     Q(user__middle_name__icontains=f)) 
                
                i = i + 1
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]
        else:
            s = 1
            up = 1            
    users = GlobalSort(users, sort, s, up)
    data["up"] = up
    data["sorto"] = s        
    data["users"] = users
    return data

def UserFilterFIOStatus(f=""):
    farray = f.strip().split(" ") # массив из слов поиска
    users2 = User.objects.filter(id=0, is_active=True)
    for fs in farray: 
        users2 = users2 | User.objects.filter(Q(first_name__icontains=fs) | Q(last_name__icontains=fs) | Q(middle_name__icontains=fs), is_active=True)           
    return users2    
    
#    farray = f.strip().split(" ") # массив из слов поиска
#    sobject = "staff in (select vpi.id from videoclient_personid as vpi join videoclient_person as vp on vp.id=vpi.person_id join videoclient_statususer as vs on vs.id=vp.status_id where "
#    i = False
#    for fs in farray:
#        sobject = "%s %s vp.first_name like '%%%s%%' or vs.name like '%%%s%%' or vp.last_name like '%%%s%%' or vp.middle_name like '%%%s%%'" % (sobject, " or " if i else "", fs, fs, fs, fs)
#        i = True            
#    sobject = "%s)" % (sobject)
#    sobject = sobject.replace("%", "%%")
#    return User.objects.extra(where=[sobject])

def UserFilterUserName(f=""):
    farray = f.strip().split(" ") # массив из слов поиска
    users2 = User.objects.filter(id=0, is_active=True)
    for fs in farray: 
        users2 = users2 | User.objects.filter(Q(username__icontains=fs), is_active=True)           
    return users2

def UserFilterUserStatus(f=""):
    farray = f.strip().split(" ") # массив из слов поиска
    users2 = User.objects.filter(id=0, is_active=True)
    for fs in farray: 
        users2 = users2 | User.objects.filter(Q(status__name__icontains=fs), is_active=True)           
    return users2

def getSearchUsers(request):
    data = dict()
    s = 0
    up = 0
    sort = [["id"],
            ["first_name", "last_name", "middle_name"],
            ["username"],
            [],
            ["status__name"],
            ["kpp__name"]]    
    users = User.objects.filter(is_active=True)
    data["all_users_count"] = users.count()
    form = TestDataJournal(request.GET, request.FILES)     
    if form.is_valid():                
        data["start"] = form.cleaned_data["start"]
        logging.info("delo=" + str(form.cleaned_data["delo"]))
        if form.cleaned_data["delo"]:       
            data['delo'] = 1     
            for rp in range(1, form.cleaned_data["delo"] + 1):
                try:
                    if "u" + str(rp) in request.GET:
                        id = request.GET["u" + str(rp)]
                        logging.info("u=" + str(id))
                        User.objects.filter(id=int(id)).update(is_active=False)
                except: logging.exception(sys.exc_info())
        users = User.objects.filter(is_active=True)
        if form.cleaned_data["filter"] and form.cleaned_data["filter"].lower() != "поиск":
            data["filter"] = form.cleaned_data["filter"]
            f = form.cleaned_data["filter"]            
            users = UserFilterUserName(f) | UserFilterUserKpp(f) | UserFilterFIOStatus(f) | UserFilterUserStatus(f)
            users = users.filter(is_active=True)
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]
        else:
            s = 1
            up = 1           
    #users = GlobalSort(users, sort, s, up)
    data["up"] = up
    data["sorto"] = s        
    data["users"] = users
    return data

def getDataDivision(request):
    data = dict()
    data["division_person"] = division_person
    data["division_employee"] = division_employee
    data["division_visitor"] = division_visitor
    return data


def dataHistory(request=None):
    data = dict()
    data['histroy'] = getDictByModel(Person)
    return data

def jobForCron():
    return #Отклчючение пересылки Orange Согласовано с Алексеем Хивиным.
    try:
        journals = Journal.objects.filter(transfer=None) #person__exact = None
        if journals.count() > 0 :
            url = get_value_defaultparams(settings.transfer_alerts_url)
            server, port = url.split(':')
            logging.info("server, port" + str(server) + " " + str(port))
            
            for journal in journals:
                try:
                    journal.transfer = 1;
                    journal.save()
                    
                    if journal.person and get_value_defaultparams(settings.transfer_alerts) == "1":
                        from videoclient.orange import recognition
                        person = journal.person
                        personId = porson.bal_id if person and journal.person.bal_id else None
                        camera = journal.camera.ip + " " + journal.camera.type if journal.camera and journal.camera.ip and journal.camera.type else None
                        name = "%s %s %s" % (person.person.first_name, person.person.last_name, person.person.middle_name) if person and person.person else None
                        from videoclient.models import List
                        lists = List.objects.filter(type__division=person.person.status.division, group=person.person.group)
                        level = lists[0].level if lists.count() > 0 else "Level0"
                        #level = person.person.category.level if person and person.person and person.person.category and person.person.category.level else 0
                        recognition(server, port, personId, 0, journal.coeff, camera, name, level)
                except:
                    logging.exception("jobForCron: " + str(sys.exc_info()))
    except:
        pass
        #logging.exception("jobForCron: "+str(sys.exc_info()))
        
def clearForCron():
    try:
        import datetime
        from videoclient.models import TimeTest
        ts = get_value_defaultparams(time_span_time_test)
        TimeTest.objects.filter(dt_fixed__lt=datetime.datetime.now() - datetime.timedelta(milliseconds=int(ts))).delete()
    except:
        logging.exception("clearForCron: " + str(sys.exc_info()))
        
ACTION_CHANGE = '_change'
ACTION_CREATE = '_create'        
        
def getDataAnketaList(request, id=None):
    data = dict()
    
    if id:
        list = get_object_or_404(List, id=int(id))
        data['list'] = list
        data['action'] = ACTION_CHANGE
    else:
        data['list'] = dict()
        data['action'] = ACTION_CREATE
    
    if request.REQUEST.has_key(ACTION_CHANGE) or request.REQUEST.has_key(ACTION_CREATE):
        if request.REQUEST.has_key(ACTION_CHANGE):
            form = ListForm(request.REQUEST, instance=list)
        else:
            form = ListForm(request.REQUEST)
        if form.is_valid():
            list = form.save(commit=False)
            g1, create = GroupPerson.objects.get_or_create(id=list.id)
            g1.name = list.name
            g1.save()
            list.group = g1
            list.active = True    
            list.save()
            data['redirect'] = "/lists/"#"/anketalist/%s/" %list.id
        else:
            data['errors'] = form.errors
            
    data['all_types'] = Types.objects.all().exclude(url = '/autolist/')
    
    return data

def getDataPhotosView(request, users):
    data = dict()
    view = 1
    if request.REQUEST.has_key("view"):
        view = request.REQUEST["view"]
    elif request.COOKIES.has_key("view"):
        view = request.COOKIES['view']
            
    if int(view) > 0:
        data["view"] = view
    else:
        view = 1
    try:
        from videoclient.utils import updateBalId
        updateBalId()
        for user in users:
            photos = getAllPhotosByName(user["id"], int(view), bal_id_update=False)
            user["photos"] = photos
    except:
        logging.exception("getDataPhotosView: " + str(sys.exc_info()))
    return data
    

def getDataVideo(request):
    data = dict()
    sort = [[], ["id"],
            ["com__host"],
            ["camera__ip"],
            ["dt_start"],
            ["tm_start"],
            ["dt_stop"],
            ["tm_stop"],
            ["filename"],
            ]
    s = 0
    up = 0    
    
    logging.info("/video/")
    
    rollers = Roller.objects.exclude(tm_stop=None)
    data["all_rollers"] = rollers.count()
    
    form = TestDataJournal(request.REQUEST)          
    if form.is_valid():
        logging.info("delo=" + str(form.cleaned_data["delo"]))
        if form.cleaned_data["delo"]:       
            data['delo'] = 1     
            for rp in range(1, form.cleaned_data["delo"] + 1):
                try:
                    if "pi" + str(rp) in request.REQUEST:
                        id = request.REQUEST["pi" + str(rp)]
                        logging.info("pi=" + str(id))
                        dRollers = Roller.objects.filter(id=int(id))
                        for dRoller in dRollers:
                            try:
                                filename = VIDEO_CLIP_PATH + dRoller.filename
                                os.remove(filename)
                            except:
                                logging.exception("delete file: " + str(sys.exc_info()))
                        dRollers.delete()
                except: logging.exception(sys.exc_info())
            rollers = Roller.objects.exclude(tm_stop=None)
            data["all_rollers"] = rollers.count()
        data["start"] = form.cleaned_data["start"]
        now = datetime.datetime.now()
        today = datetime.date(year=now.year, month=now.month, day=now.day)

        if form.cleaned_data["dateBegin"]:
            dateBegin = form.cleaned_data["dateBegin"]
        else:
            dateBegin = today 
        data["dateBegin"] = dateBegin
        rollers = rollers.filter(dt_start__gte=dateBegin)
        if form.cleaned_data["dateEnd"]:
            dateEnd = form.cleaned_data["dateEnd"]
        else:
            dateEnd = today
        data["dateEnd"] = dateEnd
        rollers = rollers.filter(dt_start__lte=dateEnd) 
         
        if form.cleaned_data["communicator"]:
            communicator = form.cleaned_data["communicator"]
            data["communicator"] = communicator
            rollers = rollers.filter(com__id=communicator)            
            
        if form.cleaned_data["camera"]:
            camera = form.cleaned_data["camera"]
            data["camera"] = camera
            rollers = rollers.filter(camera__id=camera)            
            
        data["filter"] = form.cleaned_data["filter"]
        if form.cleaned_data["filter"] and form.cleaned_data["filter"].lower() != "поиск":
            fs = u"" + form.cleaned_data["filter"]
            fs = fs.split()
            i = 0
            while i < len(fs):
                f = fs[i]
                rollers = rollers.filter(Q(com__host__icontains=f) | 
                                        Q(com__port__icontains=f) | 
                                        Q(camera__ip__icontains=f) | 
                                        Q(camera__type__icontains=f))# |
                                        #Q(dt_start__icontains=f) |
                                        #Q(tm_start__icontains=f) |
                                        #Q(dt_stop__icontains=f) |
                                        #Q(tm_stop__icontains=f)) 
                i = i + 1                                                                 #map(lambda x: "%s%s" % ("-" if up==1 else "", x), sort[s])
        if form.cleaned_data["up"]: up = 1 if form.cleaned_data["up"] and form.cleaned_data["up"] == 1 else 0            
        if form.cleaned_data["sorto"] and form.cleaned_data["sorto"] > 0 and form.cleaned_data["sorto"] <= len(sort): s = form.cleaned_data["sorto"]
        else: 
            s = 1
            up = 1      
        rollers = rollers.order_by("%s%s" % ("-" if up == 1 else "", sort[s][0]))        
        #rollers = GlobalSort(rollers, sort, s, up)
        data["up"] = up
        data["sorto"] = s
    else:   
        logging.info("getDataVideo:" + str(form.errors))                     
    
    data["found_rollers"] = rollers.count()
    
    for video_clip in rollers:
        if os.path.isfile(settings.VIDEO_CLIP_PATH + video_clip.filename):
        #if os.path.isfile(settings.WWW_ROOT[:-1] + "/files/detects/test.jpg"):
            setattr(video_clip, "file_exists", True)
        else:
            setattr(video_clip, "file_exists", False)
            
    data["rollers"] = rollers
    data["communicators"] = comModels.Communicator.objects.all()
    data["dcameras"] = comModels.Camera.objects.all()
    return data

def circleWithColor(draw, point, color, radius=4):
    draw.ellipse((point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius), outline = color)
    draw.ellipse((point[0] - radius+1, point[1] - radius + 1, point[0] + radius - 1, point[1] + radius - 1), outline = color)

def draw_face_on_image(canvas, eye1=None, eye2=None, nose=None, chin=None, quad=None, factor=1, color=(255, 0, 0)):
    if eye1:
            circleWithColor(canvas, (eye1[0] * factor, eye1[1] * factor),  color)
            
    if eye2:
        circleWithColor(canvas, (eye2[0] * factor, eye2[1] * factor),  color)
    
    if nose:
        circleWithColor(canvas, (nose[0] * factor, nose[1] * factor),  color)
    
    if chin:
        circleWithColor(canvas, (chin[0] * factor, chin[1] * factor),  color)
    
    if quad:
        corner_length = ((quad[2]*factor) - (quad[0]*factor) * 35) / 100
        canvas.line((quad[0]*factor, quad[1]*factor, quad[0]*factor - corner_length, quad[1]*factor), fill=color, width=1)
        canvas.line((quad[2]*factor, quad[3]*factor, quad[2]*factor + corner_length, quad[3]*factor), fill=color, width=1)
        canvas.line((quad[4]*factor, quad[5]*factor, quad[4]*factor + corner_length, quad[5]*factor), fill=color, width=1)
        canvas.line((quad[6]*factor, quad[7]*factor, quad[6]*factor - corner_length, quad[7]*factor), fill=color, width=1)
        
        canvas.line((quad[0]*factor, quad[1]*factor, quad[0]*factor, quad[1]*factor - corner_length), fill=color, width=1)
        canvas.line((quad[2]*factor, quad[3]*factor, quad[2]*factor, quad[3]*factor - corner_length), fill=color, width=1)
        canvas.line((quad[4]*factor, quad[5]*factor, quad[4]*factor, quad[5]*factor + corner_length), fill=color, width=1)
        canvas.line((quad[6]*factor, quad[7]*factor, quad[6]*factor, quad[7]*factor + corner_length), fill=color, width=1)

    return canvas

def translit(locallangstring):
    conversion = {
        u'\u0410' : 'A',    u'\u0430' : 'a',
        u'\u0411' : 'B',    u'\u0431' : 'b',
        u'\u0412' : 'V',    u'\u0432' : 'v',
        u'\u0413' : 'G',    u'\u0433' : 'g',
        u'\u0414' : 'D',    u'\u0434' : 'd',
        u'\u0415' : 'E',    u'\u0435' : 'e',
        u'\u0401' : 'Yo',   u'\u0451' : 'yo',
        u'\u0416' : 'Zh',   u'\u0436' : 'zh',
        u'\u0417' : 'Z',    u'\u0437' : 'z',
        u'\u0418' : 'I',    u'\u0438' : 'i',
        u'\u0419' : 'Y',    u'\u0439' : 'y',
        u'\u041a' : 'K',    u'\u043a' : 'k',
        u'\u041b' : 'L',    u'\u043b' : 'l',
        u'\u041c' : 'M',    u'\u043c' : 'm',
        u'\u041d' : 'N',    u'\u043d' : 'n',
        u'\u041e' : 'O',    u'\u043e' : 'o',
        u'\u041f' : 'P',    u'\u043f' : 'p',
        u'\u0420' : 'R',    u'\u0440' : 'r',
        u'\u0421' : 'S',    u'\u0441' : 's',
        u'\u0422' : 'T',    u'\u0442' : 't',
        u'\u0423' : 'U',    u'\u0443' : 'u',
        u'\u0424' : 'F',    u'\u0444' : 'f',
        u'\u0425' : 'H',    u'\u0445' : 'h',
        u'\u0426' : 'Ts',   u'\u0446' : 'ts',
        u'\u0427' : 'Ch',   u'\u0447' : 'ch',
        u'\u0428' : 'Sh',   u'\u0448' : 'sh',
        u'\u0429' : 'Sch',  u'\u0449' : 'sch',
        u'\u042a' : '"',    u'\u044a' : '"',
        u'\u042b' : 'Y',    u'\u044b' : 'y',
        u'\u042c' : '\'',   u'\u044c' : '\'',
        u'\u042d' : 'E',    u'\u044d' : 'e',
        u'\u042e' : 'Yu',   u'\u044e' : 'yu',
        u'\u042f' : 'Ya',   u'\u044f' : 'ya',
    }
    translitstring = []
    for c in locallangstring:
        translitstring.append(conversion.setdefault(c, c))
    return ''.join(translitstring)

def parseFaceString(text):
    res = dict()
    
    params = map(lambda x: float(x), text.split(','))
    
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

def getEyesDistance(face_params):
    from math import sqrt
    eyes_distance = 0
    try:
        eyes_distance = round(float(sqrt(((float(face_params["eye1"][0]) - float(face_params["eye2"][0]))**2) + ((float(face_params["eye1"][1]) - float(face_params["eye2"][1]))**2))), 2)
    except:
        return 0
    return eyes_distance

def getCameraByUUID(uuid):
    c = None
    try:
        c = Camera.objects.filter(uuid=uuid)[0]
    except:
        c = None
    return c

from videoclient.views import learning
from videoclient.models import ParamAggregator # добавил для того чтобы в эклипс нижеидущие строки не подчеркивались красным.

def updateJournalStatistic():
    try:
        param_aggregator = ParamAggregator.getRecord()
        
        first_id = param_aggregator.getParam(ParamAggregator.PARAM_JOURNAL_LAST_ID)
        last_id = Journal.objects.exclude(agregate=None, id__gt=param_aggregator.getParam(ParamAggregator.PARAM_JOURNAL_FIRST_ID)).order_by('-id')[:1][0].id
        
        updateJournalStatisticById(first_id=first_id, last_id=last_id, param_aggregator=param_aggregator)
        
    except:
        logging.exception(str(sys.exc_info()))
    

# В качестве параетра передается id последней обработанной записи
def updateJournalStatisticById(first_id=0, last_id=0, param_aggregator=None):
    
    from django.db.models import Max, Count
    journals = Journal.objects.exclude(agregate=None)
    journals = journals.filter(id__gt=first_id)
    journals = journals.filter(id__lte=last_id)
    
    journals_count = journals.extra(where=['videoclient_journal.id = videoclient_journal.agregate_id'])
    param_aggregator.setParam(ParamAggregator.PARAM_JOURNAL_COUNT, param_aggregator.getParam(ParamAggregator.PARAM_JOURNAL_COUNT)+journals_count.count())
    journals_count = journals_count.exclude(person=None)
    param_aggregator.setParam(ParamAggregator.PARAM_JOURNAL_IDENT_COUNT, param_aggregator.getParam(ParamAggregator.PARAM_JOURNAL_IDENT_COUNT)+journals_count.count())
    param_aggregator.setParam(ParamAggregator.PARAM_JOURNAL_LAST_ID, last_id)
    
    journals = journals.exclude(person=None)
    journals = journals.extra(where=['videoclient_journal.id <> videoclient_journal.agregate_id'])
    journals = journals.values('agregate').annotate(count=Count('agregate'), dt_last_fixed=Max('dt_last_fixed'))
    
    for journal in journals:
        j = Journal.objects.filter(id = journal["agregate"])
        if len(j) > 0:
            j = j[0]
            j.photos_count = j.photos_count+journal["count"]
            j.dt_last_fixed = journal["dt_last_fixed"]
            j.save()

    