# coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from videoclient.settings import log_videoarchive as logging
import sys
import os
import re
import Image
import StringIO
from videoarchive import settings
from videoarchive.models import Users
from videoarchive.person import models
from videoarchive.person import config
from videoarchive.balancer import views as bviews
from videoarchive.balancer import balancer
#from videoarchive.communicator import views as cviews
#from videoarchive.communicator import communicator
from videoarchive import utils
from videoarchive.person import forms

CHANGE = '_change'
CREATE = '_create'
ADDPHOTO = '_addphoto'
LIMIT = config.LIMIT

def genPages(count, start, limit=LIMIT):
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

def dataNavigation(request, count):
    data = dict()
   
    start = 1
    if request.GET.has_key('start'):
        start = int(request.GET['start'])
    
    if start>count:
        start = count/LIMIT*LIMIT+1
    
    if start <= 0:
        start = 1
        
    data['page'], data['allpages'], data['pages'] = genPages(count, start, LIMIT)
    data['start'] = start
    data['finish'] = start+LIMIT
    return data


def getDefaultPerson(request):
    data = dict()
    data["project_url"] = "/person"
    return data


def getUserID(username):
    user = None
    try:
        user = Users.objects.get(username = username)
        if user: user = user.id
    except:
        user = None
    return user

def getBalIdByName(person_name):
    if person_name <= 0:
        return -1
    if len(str(person_name)) == 0 :
        return -1
#    person_name = idToName(person_name) 
 #   logging.info(person_name)

    HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
    try:
        b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        ids, names, photos = b.getPersons()
        b.close()
        del b
    except:
        logging.exception("person_name: Error"+str(sys.exc_info()))
        return -1

#    fount = -1
    i=0;
    logging.info(names)
    while i<len(names):
        if names[i] == str(person_name):
#            found = i
            return ids[i]
            break
        i = i+1
    return -1

def getAllPhotosByName(person_name):
    id = getBalIdByName(person_name)
    logging.info(id)
    photos = []
    if id>0:
        return getAllPhotos(id)
    return {'id':id, 'photos': [], 'count': 0}    

def getAllPhotos(id=0):
    if id>0:        
        try:
            HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
            b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            num_photos = b.getPersonPhotos(id)[0]

            num_photos.sort()
            photos = []
            for photo in num_photos:
                images = b.getPersonPhoto(id, photo)
                if len(images)>0:
                    image = images[0]
                    img = Image.open(StringIO.StringIO(image))
                    width, height = img.size
                else:
                    width = ''
                    height = ''
                photos.append({'num': photo, 'size': {'width': width, 'height': height}})
        except:
            logging.exception("getallphotosbyname "+str(sys.exc_info()))            
        finally:
            b.close()
            del b
            return {'id':id, 'photos': photos, 'count': len(photos), 'size': {'width': 120, 'height': 120}}
    return {'id':id, 'photos': [], 'count': 0}

 
def getPersonPhotosByName(person_name):
    try:
        logging.info("pn="+str(person_name))
        person = models.Person.objects.filter(id=person_name)[0]
        logging.info("bal_id="+str(person.bal_id))
        if person.bal_id: data = getAllPhotos(person.bal_id)
        else: data = getAllPhotosByName(person_name)        
        if("id" in data and data['id']>0 and 'photos' in data):
            return data['id'], data['photos'][0]['num'] if len(data['photos'])>0 else 0, len(data['photos'])
    except:
        logging.exception("getPersonPhotosByName "+str(sys.exc_info()))
    return -1, -1, -1

def dataPerson(request, id=None):
    data = dict()
    data["save"] = False
    form = forms.PersonChangeForm(request.POST, request.FILES)
    data['user'] = dict()
    if request.POST.has_key(CHANGE):
        if not form.is_valid():
            data['errors'] = form.errors
        else:
            id = form.saveUser(id)
            data["save"] = True

    if request.POST.has_key(CREATE):
        if not form.is_valid():
            data['errors'] = form.errors
        else:
            id = form.addUser()
            data["save"] = True
    if not id:
        if request.POST.has_key("id"):
            id = request.POST["id"]
   
    if id:
        user = models.Person.objects.get(id = int(id))
        data['user'] = user
        data['action'] = CHANGE
    else:
        data['action'] = CREATE
        for p in request.POST:
            data['user'][p] = request.POST[p]

    data['id'] = id

#    data['allstatus'] = getDictByModel(StatusUser, param)
#    data['alldivision'] = getDictByModel(DivisionUser)
#    data['allposition'] = getDictByModel(PositionUser, param)
#    data['allkpp'] = getDictByModel(Kpp)
#    data['allcategory'] = getDictByModel(Category)
    data['alldocuments'] = models.Document.objects.all()
#    data['user'].update(getDictDivision(param))
    #data['user']['user'] = getUserID(request.user.username)
    #data['user']['user'] = request.user
    data['addphoto'] = ADDPHOTO
#    data['articleList'] = Article.objects.order_by("id")
#    data['articleItem'] = ArticleItem.objects.order_by("id")
#    data['articlePart'] = ArticlePart.objects.order_by("id")

    id_person = id
    logging.info("id_person="+str(id_person))
    logging.info(getPersonPhotosByName(id_person))
    data['photoid'], data['photoname'], data['photocount'] = getPersonPhotosByName(id_person)

#    if id2:
#        user = models.Person.objects.get(id = int(id2))
#        data['user2'] = user
#    else:
#    data['user2'] = data['user']
    """
    if request.REQUEST.has_key('group'):
        data['group'] = request.REQUEST['group']

    if id and (not request.POST.has_key(CREATE)):
        vc = VisitingCard.objects.filter(visitor__person__id = int(id))
        if vc.count()> 0:
            vcid = vc[0].id
        else:
            vcid = None
    else:
    
    vcid = None
    
    from videoclient.po4.views import getDataVisitorCard
    errors = None
    if data.has_key('errors'):
        errors = data['errors']
    data.update(getDataVisitorCard(request, vcid, id))
    if data.has_key('errors'):
        if errors is not None:
            data['errors'].update(errors)
    """
    return data

#
# TODO
# Добавить проверку прав, так же сделать с отсальными views, можно просмотреть через urls.py или поиском по регулярному вырожению def\s[a-zA-Z0-9_]*\(request
#
def anketa(request, pid=None):
#    if not check_rule(request, True, is_moderator=True):
#        return HttpResponseRedirect("/")
    data = dict()
    data.update(getDefaultPerson(request))
    data.update(utils.getDefaultParams(request, 'anketa'))
    data.update(dataPerson(request, pid))
    data['learn'] = True
    if request.POST.has_key(ADDPHOTO) and "id" in data and len(str(data["id"]))>0 and data["id"]>0:
#        str_redirect = ""
        str_redirect = '/person/addphotoperson/person/%s/' %int(data["id"])
        #if data.has_key('group'):
        return HttpResponseRedirect(str_redirect)
#        return HttpResponseRedirect(getStrRedirect(data, '/addphotoperson/visitors/%s/' %int(data['user']['id_person']), project))
    return render_to_response("anketavisitor.html", data)

def photosvisitor(request):
#    if not check_rule(request, True, is_moderator=True):
        #return HttpResponseRedirect("/")
    data = dict()
    data.update(getDefaultPerson(request))
    data.update(utils.getDefaultParams(request, 'photosvisitor'))
    return render_to_response("photosvisitor.html", data)

def getBalNameById(id):
    try:
        id = int(id)
        HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
        
        try:
            b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            ids, names, photos = b.getPersons()
            b.close()
            del b
        except:
            logging.exception("getBalNameById, getPerson: "+str(sys.exc_info()))
            return ""
       
        i=0;
        while i<len(ids):
            if int(ids[i]) == id:
                return names[i]
            i = i+1
    except:
        logging.exception("getBalNameById: "+str(sys.exc_info()))
    return ""

def getNamePersonByBalId(id):
    try:
        if models.Person.objects.filter(bal_id = int(id)).count() == 1:
            person = models.Person.objects.get(bal_id = int(id))
        else:
            bal_name = getBalNameById(id)
            person_id = int(bal_name)
            if models.Person.objects.filter(id = int(person_id)).count() == 1:
                person = models.Person.objects.get(id = person_id)
                person.bal_id = int(id)
                person.save()
            else:
                person = None
            
        if person is not None:
            person_name = person.first_name if person.first_name else ""
            person_name = person_name + (" " if len(person_name)>0 and person.last_name else "") + (person.last_name if person.last_name else "")
            person_name = person_name + (" " if len(person_name)>0 and person.middle_name else "") + (person.middle_name if person.middle_name else "")
            return person_name
    except:
        logging.exception("getNamePersonByBalId: "+str(sys.exc_info()))
    return ""

def url_name_person(request):
    if request.GET.has_key('id'):
        try:
            id = request.GET['id']
            name = getNamePersonByBalId(id)
            return HttpResponse(name)
        except:
            logging.exception(sys.exc_info())
            
    return HttpResponse("")

def addphotoperson(request, select_page=None, id=None):
#    if not check_rule(request, False, is_moderator=True):
#        return HttpResponseRedirect("/")
    data = dict()
    data.update(getDefaultPerson(request))
    data.update(utils.getDefaultParams(request, select_page))

    data['id'] = id
    data['addperson'] = idToName(id)
    person = models.Person.objects.get(id = int(id))
    data['user'] = person
    data['learn'] = True
    return render_to_response("addphotoperson.html", data)

def idToNameForPerson(id):
    person = models.Person.objects.get(id = id)
    fio = "%s_%s_%s" %(person.first_name, person.last_name, person.middle_name)
    return fio
    #return "%s_%05d" %(fio, int(person.id_person))
    return int(person.id)

def idToName(id):
    try:
        person = models.Person.objects.get(id = id)
        if person:
            res = idToNameForPerson(person.id)
            return res
        return None
    except:
        return None
    
def renamePerson(oldName, newName):
    if oldName == newName: return False
    HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
    try:
        b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        CMD_RENAME = [{'name':'person_name', 'param':oldName}, {'name':'value', 'param':newName}]
        b.renamePerson(CMD_RENAME)
        b.close()
        del b
        return True
    except:
        return False
    return False
        
def renameFR(oldName, newName):
#    oldName = idToNameForPerson(id)
#    newName = idToNameForPerson(id2)
    return renamePerson(oldName, newName)

def choose_camera(request, select_page, id, project=None):
#    if not check_rule(request, False, is_moderator=True):
#        return HttpResponseRedirect("/")
    name_template = 'choose_camera2.html'
    data = dict()
    try:
        HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
        SERVERC, PORTC, COMMUNICATORS = cviews.initCommunicators()
        index = 0
        if request.GET.has_key('index'):
            index = int(request.GET['index'])
        else:
            if 'index' in request.COOKIES:
                index = int(request.COOKIES['index'])
        if index < 0:
            index = 0
        if index >= len(COMMUNICATORS):
            index = len(COMMUNICATORS)-1

        error = False
        cameras = []    
        c_host = None
        c_port = None
        firstActive = None
        if index >= 0:      
            c = communicator.Communicator(COMMUNICATORS[index]['host'], COMMUNICATORS[index]['port'])
            c_host = COMMUNICATORS[index]['host']
            c_port = COMMUNICATORS[index]['port']        
            try:
                cameras = c.getCameras()
                for camera in cameras:
                    #models.Camera.objects.get_or_create(ip = camera['ip'], type = camera['type']) 
                    camera['mode'] = int(c.getModeScheduler(camera['numcamera']))
                    if firstActive == None and camera['active'] == '1':
                        firstActive = int(camera['numcamera'])
            except: 
                logging.exception("choose_camera: "+str(sys.exc_info()))
                error = True
                firstActive = 0
            
            c.close()
            del c

        dis_eye = None
        data = {'select_page': 'learn',
                                  'select_subpage': 'learn', 'user': request.user.username,
                                  'communicators': COMMUNICATORS, 'cameras': cameras,
                                  'name': '%s:%s' %(c_host, c_port),
                                  'error': error, 'index': index, 'modes': [0, 1, 2, -1],
                                  'dis_eye': dis_eye, 'firstActive': firstActive,
                                  'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}}
        """
        if project is not None:
        name_template = project+'choose_camera2.html'
    else:
        name_template = 'choose_camera2.html'
        """
        data['person'] = idToName(id)
        
        data.update(utils.getDefaultParams(request, select_page))

        data['id'] = id
        data['addperson'] = idToName(id)
        person = models.Person.objects.get(id = int(id))
        data['user'] = person
        data['learn'] = True
        data.update(dataNavigation(request, len(cameras)))
        data.update(getDefaultPerson(request))
        response = render_to_response(name_template, data)

        response.set_cookie("index", index)    
    except:
        logging.exception("choose_camera "+str(sys.exc_info()))
        response = render_to_response(name_template, data)
    return response     
 
  
def learn_camera(request, select_page, communicator, numcamera, person, project=None):
    communicator_id = communicator
#    if not check_rule(request, False, is_moderator=True):
#        return HttpResponseRedirect("/")


    HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
    SERVERC, PORTC, COMMUNICATORS = cviews.initCommunicators()

    server = COMMUNICATORS[int(communicator_id)]['host']
    port = COMMUNICATORS[int(communicator_id)]['port']

    mode = 0

    try:
        c = communicator.Communicator(server, int(port))
        mode = c.getModeScheduler(numcamera)
        c.close()
        del c
    except:
        pass
    
#    user = request.user.username

#    host = settings.HTTP_HOST
#    host2f = host.replace('/', '\%2F')

   
    data = {'user': request.user.username,
                        'communicator': communicator_id, 'person': person, 'server': server, 'port':port,
                        'numcamera': numcamera, 'mode': mode,
                        'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}}

    id = int(person)
#    data['person'] = idToName(id)
    
    data.update(utils.getDefaultParams(request, select_page))
    data.update(getDefaultPerson(request))

    data['id'] = id
    data['addperson'] = idToName(id)
    person = models.Person.objects.get(id = int(id))
    data['user'] = person
    data['learn'] = True
    return render_to_response("learn_camera2.html", data)
   
def dataPhotoById(id):
    data = dict()
    personId = models.Person.objects.get(id = id)
    data['allphotos'] = getAllPhotosByName(personId.id)
    data['user'] = personId
    return data
    
   
def photosperson(request, id=None):
#    if not check_rule(request, True, is_moderator=True):
#        return HttpResponseRedirect("/")

    #person = models.Person.objects.get(id = int(id))
#    division = person.status.division.name
    """
    if division == "Персоны":
        
    elif division == "Посетители":
        select_page = 'photosvisitor'
    elif division == "Сотрудники":
        select_page = 'photosstaff'
    """
    
    select_page = 'photosperson'
    data = dict()
    data.update(getDefaultPerson(request))    
    data.update(utils.getDefaultParams(request, select_page))
    data.update(dataPhotoById(id))
    data.update(dataPerson(request, int(id)))
    data.update(dataNavigation(request, len(data['allphotos']['photos'])))

    return render_to_response("photosperson.html", data)


def exportPath(person = None, photo = None, url=False):
    if url:
        base = config.URL_EXPORT
    else:
        base = config.EXPORT_PATH

    if person:
        if photo:
            return "%s%s.png" %(base, photo)
        else:
            return "%s" %(base)
    else:
        return base

def export(request):

    HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
    persons = []
    if request.POST.has_key('persons'):
        persons = request.REQUEST['persons'].split(',')
    photos = None
    if request.POST.has_key('photos'):
        photos = request.REQUEST['photos'].split(',')
    urltarname = 'True'
    if len(persons)>0:
        try:
            b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            for person in persons:
                if photos == None:
                    pass
                #b.deleting(person) 
                else:

                    path = os.path.dirname(exportPath(person))
                    if not os.path.exists(path):
                        os.makedirs(path)

                    tarname = exportPath(person)+person+".tar.bz2";
                    #urltarname = exportPath(person, None, True)+person+".tar.bz2"; 
                    urltarname = "/person/exportfile/?person="+person

                    import tarfile
                    tar = tarfile.open(tarname, "w:bz2")
                    for photo in photos:
                        image = b.getPersonPhoto(person, photo)[0]
                        filename = exportPath(person, photo)
                        img = open(filename, "w+b")
                        img.write(image)
                        img.close()
                        tar.add(filename, photo+'.png')
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

    
def exportfile(request):
    try:
        if not request.REQUEST.has_key('person'):
            raise Http404

        person = request.REQUEST['person']
        tarname = exportPath(person)+person+".tar.bz2";

        if not os.path.isfile(tarname):
            raise Http404

        ftar = open(tarname, 'r+b')
        datatar = ftar.read()
        ftar.close()
        response = HttpResponse(datatar, content_type='application/x-tar') #. 
        response['Content-Length'] = len(datatar)
        response['Content-Disposition'] = 'attachment;filename=%s.tar.bz2' %(person)
        response['Content-Encoding'] = 'x-bzip2'

        os.unlink(tarname)

        return response
    except:
        raise Http404
        logging.exception("exportfile: "+str(sys.exc_info()))

def getShortFileName(session_key):
    return settings.MEDIA_ROOT + 'tmp/%s/pre/' % (session_key)

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

def learning(data_file, name_person):
    res = {}
    try:
        HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
        b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        res = b.learning(data_file, name_person)
        b.close()
        del b
    except:
        return False

    name_person = name_person.encode("utf-8")
    if res.has_key('photo_name'):
        photo_name = int(res['photo_name'])
        filename = settings.LEARNING_IMAGES + '%s/%04d.jpg'  % (name_person, photo_name)
        path = os.path.dirname(filename)
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(filename, 'w+b')
        f.write(data_file)
        f.close()
        return True
    return False


def upload(request, session_key, name_person):
#    SERVERC, PORTC, COMMUNICATORS = communicator.initCommunicators()
    try:
        count = 0
        for p in request.FILES:
            img = request.FILES[p]
            data_file = img.read()
            if len(data_file)>0:
                filename = getFileName(session_key, 'Filename', True)
                path = os.path.dirname(filename)
                if not os.path.exists(path):
                    os.makedirs(path)
                f = open(filename, 'w+b')
                f.write( data_file)
                f.close()
                exVideo = ['.avi', '.flv', '.mp4']
                isVideo = False
                for e in exVideo:
                    if filename.count(e)>0:
                        isVideo = True
                        break
                if isVideo:
                    fname = request.POST['Filename']
                    short_fname = fname[0: len(fname)-4]
                    os.system("ffmpeg -i "+str(filename)+" -r "+str(config.COUNT_FRAME)+" "+str(path)+"/"+short_fname+"%05d.png")
                    os.unlink(filename)
                if len(name_person)>0:
#                    first_name_person = name_person
                    for f in os.listdir(path):
                        filename = "%s/%s" % (path, f)
                        if os.path.isdir(filename):
                            continue
                        f = open(filename, 'r+b')
                        data_file = f.read()
                        if learning(data_file, name_person):
                            count = count +1
                        f.close()
                        os.unlink(filename)
                    os.rmdir(path)
        return HttpResponse(count)
    except:
        return HttpResponse('-1')

def image(request):
    #if not request.user.is_authenticated():        
    #    return Http404 
    try:
        HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
#        SERVERC, PORTC, COMMUNICATORS = cviews.initCommunicators()

        id = int(request.GET['id'])
        photo = int(request.GET['photo'])
        b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        wrapper = None
        if request.GET.has_key('big'):
            wrapper = b.getPersonPhoto(id,photo)[0]
        else:
            wrapper = b.getPreview(id, photo)[1][0]
        b.close()
        del b

        response = HttpResponse(wrapper, content_type='image/jpg')
        response['Content-Length'] = len(wrapper)
        response['Content-Disposition'] = 'attachment;filename=photo%s_%s.jpg' %(id, photo)
        return response
    except:
        logging.exception("image "+str(sys.exc_info()))

def delete_person(request):
#    if not request.user.is_authenticated():
#        return Http404

    HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
    persons = request.POST['persons'].split(',')
    photos = None
    if request.POST.has_key('photos'):
        photos = request.POST['photos'].split(',')

    #try: 
    b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    for person in persons:
        if photos == None:
            p = models.Person.objects.filter(id = person)[0] 
            b.deleting(p.bal_id)
            p.delete()
        else:
            for photo in photos:
                b.deleting(person, photo)
    b.close()
    del b
    return HttpResponse('True')

def changepersonname(request):
#    if not request.user.is_authenticated():
#        return Http404
    try:
        form = forms.ChangePersonNameForm(request.POST, request.FILES)
        if form.is_valid():
            person = models.Person.objects.filter(id=form.cleaned_data['person'])[0]
            name = form.cleaned_data['name']
            m = re.match(r'^([^ ]+) *([^ ]+) *([^ ]+)$', name)
            if m and m.group(1) and m.group(2) and m.group(3):
                old_name = idToNameForPerson(person.id)
                person.first_name = m.group(1)
                person.last_name = m.group(2)
                person.middle_name = m.group(3) 
                person.save()           
                new_name = name.replace(" ", "_")
                renameFR(old_name, new_name)
                return HttpResponse('True')
    except:
        logging.exception("change person name "+str(sys.exc_info()))
    return HttpResponse('False')

def execute_method(request):
#    if not request.user.is_authenticated():
#        return Http404
    
    SERVERC, PORTC, COMMUNICATORS = cviews.initCommunicators()
    
    args = []
    i = 1
    while request.POST.has_key('arg'+str(i)):
        args.append(request.POST['arg'+str(i)])
        i= i+1 
    
    name = request.POST['name']
            
    index = 0
    try:
        index = int(request.POST['index'])
    except:
        index = int(request.COOKIES['index'])        
    
    c = communicator.Communicator(COMMUNICATORS[index]['host'], COMMUNICATORS[index]['port'])
    error = c.executeMethodByName(name, args)
    c.close();
    del c
        
    return HttpResponse(error)

def execute_method_balancer(request):
#    if not request.user.is_authenticated():
#        return Http404
    
    HOST, PORT, LOGIN, PASSWD, USER = bviews.initBalancer()
    
    args = []
    i = 1
    while request.POST.has_key('arg'+str(i)):
        args.append(request.POST['arg'+str(i)])
        i= i+1 
    
    name = request.POST['name']
    
    
    b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)            
    res = b.executeMethodByName(name, args)
    b.close()
    del b
        
    return HttpResponse(res)
