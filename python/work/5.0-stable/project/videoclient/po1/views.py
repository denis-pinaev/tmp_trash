# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from django.http import HttpResponse

from videoclient.views import *
from videoclient.settings import *


def persons(request):
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
    
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    params = request.POST
    
    filter = ''
    if request.POST.has_key('filter'):
        filter = request.POST['filter']

    allcount = pers.start(b, filter)

    ids, persons, photos = pers.res()
    
    start = 1
    if request.GET.has_key('start'):
        start = int(request.GET['start'])
    else:
        if 'start' in request.COOKIES:
            start = int(request.COOKIES['start'])
            
    if start>len(persons):
        start = len(persons)-LIMIT+1
        if start <= 0:
            start = 1
    
    start = start/LIMIT*LIMIT+1
    
    if len(filter)>0:
        start = 1    
    
    page, allpages, pages = genPages(len(persons), start)
    
    i = start-1
    out = []
    w, h = SIZE
    while i<len(persons) and i<start+LIMIT-1:
        person = persons[i]
        
        id = ids[i]
        photo = int(photos[i])
        
        getPreviewByName(person, photo)
        
        urlsmal = MEDIA_URL+'photos.like2/'+person+'/%04d_%dx%d.jpg' %(photo, w, h)
        urlbig = MEDIA_URL+'photos.like2/'+person+'/%04d.jpg' %photo
        
        countphoto = 0
        try:
            countphoto = len(b.getPersonPhotos(id)[0])
        except:
            pass
        smalperson = person
        if len(smalperson) > MAX_NAME_LEN:
            smalperson = '%s...' % smalperson[:MAX_NAME_LEN-3]
        out.append({'url': {'big': urlbig, 'smal': urlsmal}, 'person': {'smal': smalperson, 'big':person}, 'id': id, 'countphoto': countphoto, 'photo': photo})
        i = i+1
    response = render_to_response_ex(request,  "po1persons.html", {'allcount': allcount, 'count': len(persons), 'limit': LIMIT, 'start' : start, 
                                                'pages': pages, 'allpages': allpages, 'page': page, 
                                                'out': out, 'host': HTTP_HOST, 'user': request.user.username,
                                                'select_page': 'persons', 'filter': filter})
    if request.GET.has_key('start'):
        start = int(request.GET['start'])
        response.set_cookie("start", start)
        
    b.close()
    del b
    
    return response

def personsadd(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    response = render_to_response_ex(request, "po1anketaclear.html", {'host': HTTP_HOST,  'select_page': 'persons', 'user': request.user.username,})    
    return  response

def personsaddphoto(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    response = render_to_response_ex(request, "po1anketaaddphotos.html", {'host': HTTP_HOST,  'select_page': 'persons', 'user': request.user.username,})    
    return  response

def person_def(request, person, id, is_photos = False):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    initBalancer()
    
    params = request.POST
    debug = ''
    
    
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    for p in params:
        if p.count('photo'):
            name = p[5:]
            b.deleting(id, name)
            pers.init = False
    photos = b.getPersonPhotos(id)[0]
    b.close()
    del b
    
    photos.sort()
    
    #if len(photos) == 0:
    #    return HttpResponseRedirect("/persons/")
   
    smalperson = person
    if len(smalperson) > MAX_NAME_LEN:
        smalperson = '%s...' % smalperson[:MAX_NAME_LEN-3]
    
    start = 1
    if request.GET.has_key('start'):
        start = int(request.GET['start'])
        
    if start>len(photos):
        start = len(photos)-LIMIT+1
        if start <= 0:
            start = 1
            
    start = start/LIMIT*LIMIT+1
        
    page, allpages, pages = genPages(len(photos), start)
    
    out = []
    i = start-1
    w, h = SIZE
    while i<len(photos)  and i<start+LIMIT-1:
        photo = int(photos[i])
        getPreviewByName(person, photo)
        urlsmal = MEDIA_URL+'photos.like2/'+person+'/%04d_%dx%d.jpg' %(photo, w, h)
        urlbig = MEDIA_URL+'photos.like2/'+person+'/%04d.jpg' %photo
        out.append({'name': photo, 'url': {'big': urlbig, 'smal': urlsmal}})
        i = i+1
        
    template_name = "po1anketa.html"
    if is_photos:
        template_name = "po1person.html"
    

    return render_to_response_ex(request, template_name, {'person': {'smal': smalperson, 'big':person}, 'id': id, 
                                               'out': out, 'firstout': out[0], 'host': HTTP_HOST,
                                               'page': page, 'allpages': allpages, 'pages': pages,
                                               'user': request.user.username, 'count': len(photos),
                                               'debug': debug, 'select_page': 'person'})
    
def person(request, person, id):
    return person_def(request, person, id, False)    
    
def profile(request):
    return person_def(request, None, None, False)

def photos(request, person, id):
    return person_def(request, person, id, True)

def journal(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    response = render_to_response_ex(request, "po1journal.html", {'host': HTTP_HOST,  'select_page': 'journal', 'user': request.user.username,})    
    return  response

def pageemployee(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    response = render_to_response_ex(request, "po1pageemployee.html", {'host': HTTP_HOST,  'select_page': 'journal', 'user': request.user.username,})    
    return  response


def signal(request, param=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    templatename = "po1signal.html"
    if param == '1' or param == '2':
        templatename = "po1signal%s.html" %(param)
    response = render_to_response_ex(request, templatename, {'host': HTTP_HOST,  'select_page': 'signal', 'user': request.user.username,})    
    return  response

def wanted(request, param = None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    templatename = "po1wanted.html"
    if param == "anketa":
        templatename = "po1anketawanted.html"
    if param == "report":
        templatename = "po1reportwanted.html"
    if param == "photos":
        templatename = "po1wantedphotos.html"
    response = render_to_response_ex(request, templatename, {'host': HTTP_HOST,  'select_page': 'wanted', 'user': request.user.username,})    
    return  response

def record(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    response = render_to_response_ex(request, "po1record.html", {'host': HTTP_HOST,  'select_page': 'record', 'user': request.user.username,})    
    return  response

def kpp(request, param = None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    templatename = "po1kpp.html"
    if param=="base":
        templatename = "po1kpp.html"
    if param=="edit":
        templatename = "po1kppedit.html"
    if param=="add":
        templatename = "po1kppadd.html"
    
    response = render_to_response_ex(request, templatename, {'host': HTTP_HOST,  'select_page': 'kpp', 'user': request.user.username,})    
    return  response

def help(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    response = render_to_response_ex(request, "po1help.html", {'host': HTTP_HOST,  'select_page': 'help', 'user': request.user.username,})    
    return  response  
    