# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from videoclient.utils import *
from videoclient.models import *
from videoclient.views import initBalancer, initCommunicators, tester, render_to_response_ex
from videoclient.communicator import Communicator
from django import forms
from videoclient.settings import division_person, division_employee, division_visitor, division_auto, wait_unidentified_person, last_journal_update
from videoclient.settings import status_notdefined, status_enter, status_exit, camera_enter, camera_exit, camera_all
import logging
from django.contrib.auth.decorators import permission_required
import sys
import datetime

@tester
@permission_required('user_perms.perm_lists')
def anketaclear(request):
    
    data = getDefaultParams(request, 'anketaclear')
    data['learn'] = True
    return render_to_response_ex(request, "po4anketaclear.html", data)

@tester
@permission_required('user_perms.perm_lists')
def help(request):

    data = getDefaultParams(request, 'help')
    return render_to_response_ex(request, "po4help.html", data)

@tester
@permission_required('user_perms.perm_logs')
def historychange(request, project=None):
    
    data = getDefaultParams(request, 'historychange', project)
    data.update(getSearchHistory(request))    
    data.update(dataGuards(None, data["users"], is_person=True))
    data.update(dataNavigation(request, data['all_users']), is_person=True)
    if project is not None:
        return render_to_response_ex(request, project+"historychange.html", data)
    else:
        return render_to_response_ex(request, "historychange.html", data)

@tester
@permission_required('user_perms.perm_lists')
def historychangep1(request):

    data = getDefaultParams(request, 'historychangep1')
    return render_to_response_ex(request, "po4historychangep1.html", data)

@tester
@permission_required('user_perms.perm_lists')
def journal(request):
    
    data = getDefaultParams(request, 'journal')
    data.update(dataJournal(request))
    data.update(getDataDivision(request))
    data.update(dataNavigation(request, data['all_users']))
    data.update(dataGet(request))
    if request.GET.has_key('data'):
        return render_to_response_ex(request, "po4datajournal.html", data)
    else:
        return render_to_response_ex(request, "po4journal.html", data)

@tester
@permission_required('user_perms.perm_logs')
@permission_required('user_perms.perm_logs_sessions')
def kppadd(request):
    
    data = getDefaultParams(request, 'kppadd')
    return render_to_response_ex(request, "po4kppadd.html", data)

@tester
@permission_required('user_perms.perm_logs')
@permission_required('user_perms.perm_logs_sessions')
def kppedit(request):
    
    data = getDefaultParams(request, 'kppedit')
    return render_to_response_ex(request, "po4kppedit.html", data)

@tester
@permission_required('user_perms.perm_logs')
@permission_required('user_perms.perm_logs_sessions')
def kpp(request, project=None):
    
    data = getDefaultParams(request, 'kpp', project)
    data.update(getSearchKpp(request))
    data.update(dataGuards(None, data["users"]))
    sort = [
            ["j_id"],
#            ["user", "kpp", "name"],
            ["kpp"],
#            ["user", "kpp", "name"],
            ["kpp"],            
            ["login"],
            ['logint_time'],
#            ["login"],
            ["logout"],
            ['logout_time'],
#            ["logout"],
#            ["staff", "person", "fio"]]
            ["fio"],
            ["status"]]
    data["users"] = GlobalSortUser(data["users"], sort, data["sorto"], data["up"])     
    data.update(dataNavigation(request, data['all_users']))    
    if project is not None:
        return render_to_response_ex(request, project+"kpp.html", data)
    else:
        return render_to_response_ex(request, "kpp.html", data)

@tester
@permission_required('user_perms.perm_lists')
def pageemployee(request):
    
    data = getDefaultParams(request, 'pageemployee')
    return render_to_response_ex(request, "po4pageemployee.html", data)


def getStrRedirect(data, url, project):
    str_redirect = ""
    if project is not None:
        str_redirect = '/'+project+url
    else:
        str_redirect = url
    if data.has_key('group'):
        str_redirect = str_redirect+"?group="+str(data['group'])
    return str_redirect            


@tester
@permission_required('user_perms.perm_lists')
def persons(request, project=None):

    data = getDefaultParams(request, 'persons', project)
    
    data.update(getSearchPerson(request))
    data.update(dataNavigation(request, data['users'].count()))
    data["users"] = data["users"][data['start']-1:data['finish']-1]
    data.update(dataGuards(None, data["users"]))
    if 'delo' in data and data['delo']:
        return HttpResponseRedirect(getStrRedirect(data, '/persons/', project))
    data.update(getDataPhotosView(request, data["users"]))
    if project is not None:
        return render_to_response_ex(request, project+"persons.html", data)
    else:
        return render_to_response_ex(request, "persons.html", data)

@tester
@permission_required('user_perms.perm_lists')
def photosuser(request):
    
    data = getDefaultParams(request, 'photosuser')
    return render_to_response_ex(request, "po4photosuser.html", data)

@tester
@permission_required('user_perms.perm_settings')
def users(request, project=None):
    data = dict()
    data.update(getDefaultParams(request, 'users', project))
    data.update(getSearchUsers(request))
    data.update(dataGuards(None, data["users"]))
    sort = [["id"],
            ["fio"],
            ["username"],
            [],
            ["status"],
            ["kpp"]] 
    data["users"] = GlobalSortUser(data["users"], sort, data["sorto"], data["up"])
    data.update(dataNavigation(request, data['all_users']))
    if 'delo' in data and data['delo']: 
        return HttpResponseRedirect(getStrRedirect(data, '/settings/users/', project))
    if project is not None:
        return render_to_response_ex(request, project+"users.html", data)
    else:
        return render_to_response_ex(request, "users.html", data)

@tester
@permission_required('user_perms.perm_settings')
def anketauser(request, id = None, project = None):
    
    data = dict()
    data.update(getDefaultParams(request, 'anketauser', project))
    data.update(dataUser(request, id))
    data['learn'] = True
    return render_to_response_ex(request, "anketauser.html", data)

@tester
@permission_required('user_perms.perm_lists')
def anketaperson(request, id = None, id2 = None, project=None):
    
    data = getDefaultParams(request, 'anketaperson', project)
    data.update(dataPerson(request, id, 'Персоны', id2, one=1))
    data['learn'] = True
    if request.POST.has_key(ADDPHOTO) and len(str(data['user']['id_person']))>0 and data['user']['id_person']>0:
        return HttpResponseRedirect(getStrRedirect(data, '/addphotoperson/persons/%s/' %int(data['user']['id_person']), project))
    if request.POST.has_key("first_name") and len(str(data['user']['id']))>0 and data['user']['id']>0:
        str_redirect = ""
        if project is not None:
            str_redirect = '/'+project+'/anketaperson/%s/?save=1' %int(data['user']['id'])
        else:
            str_redirect = '/anketaperson/%s/?save=1' %int(data['user']['id'])
        if data.has_key('group'):
            str_redirect = str_redirect+"&group="+str(data['group'])            
        if data.has_key('istraining') and data['istraining'] and data.has_key('learned'):
            str_redirect = str_redirect+"&learned="+str(data['learned'])
        return HttpResponseRedirect(str_redirect)
    if project is not None:        
        return render_to_response_ex(request, project+"anketaperson.html", data)
    else:
        return render_to_response_ex(request, "anketaperson.html", data)

@tester
@permission_required('user_perms.perm_lists')
def photosperson(request, id, project=None):
    
    person = PersonId.objects.get(id = int(id)).person
    p = PersonId.objects.get(id = int(id))
    division = person.status.division.name
    
    if division == "Персоны":
        select_page = 'photosperson'
    elif division == "Посетители":
        select_page = 'photosvisitor'
    elif division == "Сотрудники":
        select_page = 'photosstaff'
    elif division == "Автообученные":
        select_page = 'photosauto'
        
    
    data = getDefaultParams(request, select_page, project)
    data.update(dataPhotoById(id))
    data.update(dataPerson(request, int(person.id), division))
    data['photos_'] = data['allphotos']['photos']
    data['person_id'] = p.id
    if request.COOKIES.has_key("eyes") and request.COOKIES["eyes"] == "true": 
        data["eyes"] = "true"
    
    if project is not None:
        return render_to_response_ex(request, project+"photosperson.html", data, context_instance=RequestContext(request))
    else:
        return render_to_response_ex(request, "photosperson.html", data, context_instance=RequestContext(request))

@tester
@permission_required('user_perms.perm_lists')
def addphotoperson(request, select_page, id, project=None, distortion=None):
    
    data = dict()
    from videoclient.views import ChooseCamera
    
    data.update(ChooseCamera(request, False, None, return_data = True))

    data.update(getDefaultParams(request, select_page, project))
    
    if request.GET.has_key('dist_settings'):
        dist_settings = request.GET['dist_settings']
        
    data['id'] = id
    data['addperson'] = idToName(id)
    person = PersonId.objects.get(id = int(id)).person
    data['user'] = person.getDict()
    data['learn'] = True
    data['distortions'] = Distortion.objects.all()
    if request.GET.has_key('dist_settings'):
        try:
            dist_str = request.GET['dist_settings']
            dist_settings = map(lambda x: float(x), dist_str.split(','))
            data.update({'d1': str(dist_settings[0]).replace(',', '.'), 'd2': str(dist_settings[1]).replace(',', '.'), 'd3': str(dist_settings[2]).replace(',', '.'), 'd4': str(dist_settings[3]).replace(',', '.')})
        except:
            data.update({'d1': '0', 'd2': '0', 'd3': '0.5', 'd4': '0.5'})
    else:
        data.update({'d1': '0', 'd2': '0', 'd3': '0.5', 'd4': '0.5'})
        
    if distortion:
        return render_to_response_ex(request, "addphotoperson_distortion.html", data)
    else:
        if project is not None:
            return render_to_response_ex(request, project+"addphotoperson.html", data)
        else:
            response = render_to_response_ex(request, "addphotoperson.html", data)
            response.set_cookie("distr1", data["d1"])
            response.set_cookie("distr2", data["d3"])
            response.set_cookie("distr3", data["d4"])
            response.set_cookie("distr4", data["d2"])
            response.set_cookie("count_distr", "5")
            response.set_cookie("choose_model", "2")
            response.set_cookie("param_distr", "4")
            return response

@tester
@permission_required('user_perms.perm_lists')
def choose_camera(request, select_page, id, project=None):
            
    from videoclient.views import initBalancer, initCommunicators
    from videoclient.communicator import *
    from videoclient.balancer import *
    from videoclient import models    
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
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
    c = Communicator(COMMUNICATORS[index]['host'], COMMUNICATORS[index]['port'])
    cameras = []
    firstActive = None
    try:
        cameras = c.getCameras()
        for camera in cameras:
            camera['mode'] = int(c.getModeScheduler(camera['numcamera']))
            if firstActive == None and camera['active'] == '1':
                firstActive = int(camera['numcamera'])
    except:
        logging.exception("choose_camera: "+str(sys.exc_info()))
        error = True
        firsrActive = 0
    
    c.close()
    del c
    
    dis_eye = None
        
    data = {'host': HTTP_HOST, 'select_page': 'learn',
                              'select_subpage': 'learn', 'user': request.user.username,
                              'communicators': COMMUNICATORS, 'cameras': cameras,
                              'name': '%s:%s' %(COMMUNICATORS[index]['host'], COMMUNICATORS[index]['port']),
                              'error': error, 'index': index, 'modes': [0, 1, 2, -1],
                              'dis_eye': dis_eye, 'firstActive': firstActive,
                              'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}}
    
    if project is not None:
        name_template = project+'choose_camera2.html'
    else:
        name_template = 'choose_camera2.html'
    data['person'] = idToName(id)

    data.update(getDefaultParams(request, select_page, project))
    
    data['id'] = id
    data['addperson'] = idToName(id)
    person = PersonId.objects.get(id = int(id)).person
    data['user'] = person.getDict()
    data['learn'] = True
    data.update(dataNavigation(request, len(cameras)))
    
    response = render_to_response_ex(request, name_template, data) 

    response.set_cookie("index", index)
    
    return response

@tester
@permission_required('user_perms.perm_lists')
def learn_camera(request, select_page, communicator, numcamera, person, project=None):
    
    from videoclient.views import initBalancer, initCommunicators
    from videoclient.communicator import *
    from videoclient.balancer import *
    from videoclient import models
    
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
    
    server = COMMUNICATORS[int(communicator)]['host']
    port = COMMUNICATORS[int(communicator)]['port']
    
    mode = 0
    
    try:
        c = Communicator(server, int(port))
        mode = c.getModeScheduler(numcamera)
        c.close()
        del c
    except:
        pass
    
    
    user = request.user.username
    
    host = HTTP_HOST
    host2f = host.replace('/', '\%2F')
    
    data = {'user': request.user.username,
                        'communicator': communicator, 'person': person, 'server': server, 'port':port, 
                        'numcamera': numcamera, 'mode': mode,
                        'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}}
    
    id = int(person)
    data['person'] = idToName(id)

    data.update(getDefaultParams(request, select_page, project))
    
    data['id'] = id
    data['addperson'] = idToName(id)
    person = PersonId.objects.get(id = int(id)).person
    data['user'] = person.getDict()
    data['learn'] = True
    if project is not None:
        return render_to_response_ex(request, project+"learn_camera2.html", data)
    else:
        return render_to_response_ex(request, "learn_camera2.html", data)

@tester
@permission_required('user_perms.perm_lists')
def anketaclearuser(request):
    
    data = getDefaultParams(request, 'anketaclearuser')
    data['learn'] = True
    return render_to_response_ex(request, "po4anketaclearuser.html", data)

@tester
@permission_required('user_perms.perm_lists')
def visitors(request, project=None):
    
    data = dict()
    data.update(getDefaultParams(request, 'visitors', project))
    data.update(dataVisitors(request))
    data.update(dataNavigation(request, len(data['visitingcard'])))
    if project is not None:    
        return render_to_response_ex(request, project+"visitors.html", data)
    else:
        return render_to_response_ex(request, "visitors.html", data)

@tester
@permission_required('user_perms.perm_lists')
def visitorslist(request, project=None):
    
    data = getDefaultParams(request, 'visitorslist', project)
    
    data.update(getSearchVisitors(request))
    data.update(dataNavigation(request, data['users'].count()))
    data["users"] = data["users"][data['start']-1:data['finish']-1]
    data.update(dataGuards(None, data["users"]))
    if 'delo' in data and data['delo']:
        return HttpResponseRedirect(getStrRedirect(data, '/visitorslist/', project))
    data.update(getDataPhotosView(request, data["users"]))
    if project is not None:
        return render_to_response_ex(request, project+"visitorslist.html", data)
    else:
        return render_to_response_ex(request, "visitorslist.html", data)

@tester
@permission_required('user_perms.perm_lists')
def anketavisitor(request, id=None, id2 = None, project = None):
    
    data = dict()
    data.update(getDefaultParams(request, 'anketavisitor', project))
    data.update(dataPerson(request, id, 'Посетители', id2, one = 1))
    data['learn'] = True
    if request.POST.has_key(ADDPHOTO) and len(str(data['user']['id_person']))>0 and data['user']['id_person']>0:
        str_redirect = ""
        if project is not None:
            str_redirect = '/'+project+'/addphotoperson/visitors/%s/' %int(data['user']['id_person'])
        else:
            str_redirect = '/addphotoperson/visitors/%s/' %int(data['user']['id_person'])
        if data.has_key('group'):
            str_redirect = str_redirect+"?group="+str(data['group'])            
        return HttpResponseRedirect(str_redirect)
        #return HttpResponseRedirect(getStrRedirect(data, '/addphotoperson/visitors/%s/' %int(data['user']['id_person']), project))
    
    if request.POST.has_key("first_name") and len(str(data['user']['id']))>0 and data['user']['id']>0:#first_nameADDPHOTO
        str_redirect = ""
        if project is not None:
            str_redirect = '/'+project+'/anketavisitor/%s/?save=1' %int(data['user']['id'])
        else:
            str_redirect = '/anketavisitor/%s/?save=1' %int(data['user']['id'])
        if data.has_key('group'):
            str_redirect = str_redirect+"&group="+str(data['group'])            
        if data.has_key('istraining') and data['istraining'] and data.has_key('learned'):
            str_redirect = str_redirect+"&learned="+str(data['learned'])
        return HttpResponseRedirect(str_redirect)
    
    if project is not None:
        return render_to_response_ex(request, project+"anketavisitor.html", data)
    else:
        return render_to_response_ex(request, "anketavisitor.html", data)

@tester
@permission_required('user_perms.perm_lists')
def photosvisitor(request):

    data = dict()
    data.update(getDefaultParams(request, 'photosvisitor'))
    return render_to_response_ex(request, "po4photosvisitor.html", data)

@tester
@permission_required('user_perms.perm_lists')
def staff(request, project=None):
    
    data = dict()
    data.update(getDefaultParams(request, 'staff', project))
    data.update(dataStaff(request))
    data.update(dataNavigation(request, len(data['staffs'])))
    if project is not None:
        return render_to_response_ex(request, project + "staff.html", data)
    else:
        return render_to_response_ex(request, "staff.html", data)

@tester
@permission_required('user_perms.perm_lists')
def stafflist(request, project = None):

    data = getDefaultParams(request, 'stafflist', project)
    
    data.update(getSearchStaffs(request))
    data.update(dataNavigation(request, data['users'].count()))
    data["users"] = data["users"][data['start']-1:data['finish']-1]
    data.update(dataGuards(None, data["users"]))
        
    if 'delo' in data and data['delo']:
        return HttpResponseRedirect(getStrRedirect(data, '/stafflist/', project))
    
    data.update(getDataPhotosView(request, data["users"]))
    if project is not None:
        return render_to_response_ex(request, project + "stafflist.html", data)
    else:
        return render_to_response_ex(request, "stafflist.html", data)
    
@tester
@permission_required('user_perms.perm_lists')
def autolist(request, project = None):
    
    data = getDefaultParams(request, 'autolist', project)
    
    data.update(getSearchStaffs(request, division_auto))
    data.update(dataNavigation(request, data['users'].count()))
    data["users"] = data["users"][data['start']-1:data['finish']-1]
    data.update(dataGuards(None, data["users"]))
    if ('delo' in data and data['delo']) or ('concato' in data and data['concato']):
        return HttpResponseRedirect(getStrRedirect(data, '/autolist/', project))
    data.update(getDataPhotosView(request, data["users"]))
    if project is not None:
        return render_to_response_ex(request,project + "autolist.html", data)
    else:
        return render_to_response_ex(request,"autolist.html", data)
    
@tester
@permission_required('user_perms.perm_lists')
def anketastaff(request, id=None, id2 = None, project=None):
    
    data = dict()
    data.update(getDefaultParams(request, 'anketastaff', project))
    data.update(dataPerson(request, id, 'Сотрудники', id2, one=1))
    data['learn'] = True
    if request.POST.has_key(ADDPHOTO) and len(str(data['user']['id_person']))>0 and data['user']['id_person']>0:
        return HttpResponseRedirect(getStrRedirect(data, '/addphotoperson/staff/%s/' %int(data['user']['id_person']), project))
    if request.POST.has_key("first_name") and len(str(data['user']['id']))>0 and data['user']['id']>0:
        str_redirect = ""
        if project is not None:
            str_redirect = '/'+project+'/anketastaff/%s/?save=1' %int(data['user']['id'])
        else:
            str_redirect = '/anketastaff/%s/?save=1' %int(data['user']['id'])
        if data.has_key('group'):
            str_redirect = str_redirect+"&group="+str(data['group'])            
        if data.has_key('istraining') and data['istraining'] and data.has_key('learned'):
            str_redirect = str_redirect+"&learned="+str(data['learned'])
        return HttpResponseRedirect(str_redirect)
    if project is not None:
        return render_to_response_ex(request,project + "anketastaff.html", data)
    else:
        return render_to_response_ex(request,"anketastaff.html", data)
    
@tester
@permission_required('user_perms.perm_lists')    
def anketaauto(request, id=None, id2 = None, project=None):
    
    data = dict()
    data.update(getDefaultParams(request, 'anketaauto', project))
    data.update(dataPerson(request, id, 'Автообученные', id2, one=1))
    data['learn'] = True
    if request.POST.has_key(ADDPHOTO) and len(str(data['user']['id_person']))>0 and data['user']['id_person']>0:
        return HttpResponseRedirect(getStrRedirect(data, '/addphotoperson/auto/%s/' %int(data['user']['id_person']), project))
    if project is not None:
        return render_to_response_ex(request,project + "anketaauto.html", data)
    else:
        return render_to_response_ex(request,"anketaauto.html", data)    

@tester
@permission_required('user_perms.perm_lists')
def photosstaff(request):

    data = dict()
    data.update(getDefaultParams(request, 'photosstaff'))
    return render_to_response_ex(request, "po4photosstaff.html", data)

class TestVisitorCard(forms.Form):
    active = forms.IntegerField(required=False)
    vcid = forms.IntegerField(required=False)
    person = forms.IntegerField(required=False)
    visitor = forms.IntegerField(required=False)
    ground = forms.IntegerField(required=True)
    dateVisit1 = forms.DateField(required=True)
    dateVisit2 = forms.DateField(required=True)
    time11 = forms.IntegerField(required=True) 
    time12 = forms.IntegerField(required=True)
    time21 = forms.IntegerField(required=True) 
    time22 = forms.IntegerField(required=True)
    
    def clean_dateVisit2(self):
        d1 = self.cleaned_data["dateVisit1"]
        d2 = self.cleaned_data["dateVisit2"]
        if d1>d2:
            raise forms.ValidationError("Некорректно введена дата окончания посещения")
        return d2
    def clean_time22(self):
        h1 = self.cleaned_data["time11"]
        h2 = self.cleaned_data["time21"]
        m1 = self.cleaned_data["time12"]
        m2 = self.cleaned_data["time22"]
        if (h1>h2) or ((h1==h2) and (m1 >= m2)):
            raise forms.ValidationError("Некорректно введено время окончания посещения")
        return m2
    
def getDataVisitorCard(request, vcid=None, h_visitor = None, id_person = None):
    
    data = dict()    
    form = TestVisitorCard(request.POST, request.FILES)
    
    if form.is_valid():
        dt1 = "%s %s:%s:00" % (form.cleaned_data["dateVisit1"], form.cleaned_data["time11"], form.cleaned_data["time12"])
        dt2 = "%s %s:%s:00" % (form.cleaned_data["dateVisit2"], form.cleaned_data["time21"], form.cleaned_data["time22"])
        visitor = ''
        vcActive = form.cleaned_data["active"] == 1
        if form.cleaned_data["visitor"]:
            visitor = form.cleaned_data["visitor"]
        else:
            if h_visitor:
                vis_o = PersonId.objects.filter(person__id = int(h_visitor))
                if vis_o.count()>0:
                    visitor = int(vis_o[0].id)
                          
        if form.cleaned_data["person"]:
            id_person = form.cleaned_data["person"]
        if id_person != None and visitor:
            if form.cleaned_data["vcid"] :
                if vcActive:
                    VisitingCard.objects.filter(id=form.cleaned_data["vcid"]).update(active=vcActive, visitor=PersonId.objects.get(id=visitor), person=PersonId.objects.get(id=id_person), ground=Ground.objects.get(id=form.cleaned_data["ground"]), dt_enter=dt1, dt_exit=dt2)
                else:
                    VisitingCard.objects.filter(id=form.cleaned_data["vcid"]).update(active=vcActive)
            else: vcid = VisitingCard.objects.create(active=vcActive, visitor_id=visitor, person_id=id_person, ground_id=form.cleaned_data["ground"], dt_enter=dt1, dt_exit=dt2).id
    else: logging.info(form.errors)
    data.update(getVisitorInfo(request))
    data.update(getGround(request))
    data.update(getDataDivision(request))
    if vcid: data.update(dataVisitors(request, vcid))
    dt = dict()
    data['learn'] = True
    dt["errors"] = form.errors
    dt["post"] = True if request.POST else False    
    data.update(dt)
    return data    
    
@tester
@permission_required('user_perms.perm_lists')
def visitorcard(request, vcid=None, project = None):
    
    data = dict()    
    data.update(getDefaultParams(request, 'visitors', project))    
    form = TestVisitorCard(request.POST, request.FILES)
    if form.is_valid():
        dt1 = "%s %s:%s:00" % (form.cleaned_data["dateVisit1"], form.cleaned_data["time11"], form.cleaned_data["time12"])
        dt2 = "%s %s:%s:00" % (form.cleaned_data["dateVisit2"], form.cleaned_data["time21"], form.cleaned_data["time22"])
        if form.cleaned_data["visitor"] and form.cleaned_data["person"]:
            if form.cleaned_data["vcid"]:
                VisitingCard.objects.filter(id=form.cleaned_data["vcid"]).update(visitor=PersonId.objects.get(id=form.cleaned_data["visitor"]), person=PersonId.objects.get(id=form.cleaned_data["person"]), ground=Ground.objects.get(id=form.cleaned_data["ground"]), dt_enter=dt1, dt_exit=dt2)
            else: vcid = VisitingCard.objects.create(visitor_id=form.cleaned_data["visitor"], person_id=form.cleaned_data["person"], ground_id=form.cleaned_data["ground"], dt_enter=dt1, dt_exit=dt2)
    else: logging.info(form.errors)
    data.update(getVisitorInfo(request))
    data.update(getGround(request))
    data.update(getDataDivision(request))
    if vcid: data.update(dataVisitors(request, vcid))
    dt = dict()
    data['learn'] = True
    dt["errors"] = form.errors
    dt["post"] = True if request.POST else False    
    data.update(dt)
    if project is not None:
        return render_to_response_ex(request, project + "visitorcard.html", data)
    else:
        return render_to_response_ex(request, "visitorcard.html", data)

@tester
@permission_required('user_perms.perm_lists')
def repeatRecognition(request):
    try:
        j = Journal.objects.filter(person=None).order_by("-id")
        if j.count()>0:            
            Journal.objects.filter(id=j[0].id).update(show_info=0, dt_continue = datetime.datetime.now()+datetime.timedelta(seconds=int(get_value_defaultparams(wait_unidentified_person))))
    except:
        logging.exception(sys.exc_info())
    return HttpResponse(True)

@tester
@permission_required('user_perms.perm_lists')
def movementProcess(request, journalid=None):
    try:
        journal = Journal.objects.filter(id=journalid, person__active=1)        
        if journal.count()>0 and journal[0].camera and journal[0].person:
            jbuf = Journal.objects.filter(person=journal[0].person, positions_status__lt=status_notdefined).order_by("-id")
            logging.info('operator_id: '+str(request.user.id))
            users = User.objects.filter(id = int(request.user.id))
            logging.info('operator_id: '+str(users))
            if len(users)>0:
                user = users[0]
            else:
                user = None
            logging.info('operator_id: '+str(user))                
            if jbuf.count()>0 and jbuf[0].positions_status.id == status_enter and journal[0].camera.position in [camera_exit, camera_all]: journal.update(positions_status=status_exit, operator=user)
            elif (jbuf.count()==0 or jbuf[0].positions_status.id == status_exit) and journal[0].camera.position in [camera_enter, camera_all]: journal.update(positions_status=status_enter, operator=user)
    except:
        logging.exception(sys.exc_info())
    return HttpResponse(True)

@tester
@permission_required('user_perms.perm_lists')
def ident(request):
    
    return settingspage(request, ident=True)
    data = dict()
    from videoclient.views import getIdentData
    data.update(getIdentData(request))
    data.update(getDefaultParams(request, 'ident'))
    return render_to_response_ex(request, "po4ident.html", data)

@tester
@permission_required('user_perms.perm_lists')
def settingspage(request, ident=False):
        
    from videoclient import models
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
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
    c = Communicator(COMMUNICATORS[index]['host'], COMMUNICATORS[index]['port'])
    cameras = []
    try:
        cameras = c.getCameras()
        for camera in cameras:
            models.Camera.objects.get_or_create(ip = camera['ip'], type = camera['type'])
            camera['mode'] = int(c.getModeScheduler(camera['numcamera']))
    except:
        error = True
    
    c.close()
    del c
    
    
    
    dis_eye = None
    
    data = {'host': HTTP_HOST, 'select_page': 'settings',
                              'select_subpage': 'cameras', 'user': request.user.username,
                              'communicators': COMMUNICATORS, 'cameras': cameras,
                              'name': '%s:%s' %(COMMUNICATORS[index]['host'], COMMUNICATORS[index]['port']),
                              'error': error, 'index': index, 'modes': [0, 1, 2, -1],
                              'dis_eye': dis_eye,
                              'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}
                              }
    
    data.update(getDefaultParams(request, 'settingspage'))
    data.update(dataNavigation(request, len(cameras)))
    
    if ident:
        from videoclient.views import getIdentData
        data.update(getIdentData(request))
        data.update(getDefaultParams(request, 'ident'))
        response =  render_to_response_ex(request, "po4ident.html", data)
    else:
        response =  render_to_response_ex(request, "po4settingspage.html", data)

    response.set_cookie("index", index) 
    
    return response


@tester
@permission_required('user_perms.perm_lists')
def camera(request, communicator, numcamera):
        
    communicator = int(communicator)
    
    from videoclient import models
    from videoclient.balancer import Balancer
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
    
    c = None

    error = ''
    try:
        c = Communicator(COMMUNICATORS[communicator]['host'], COMMUNICATORS[communicator]['port'])
        c.open()
    except:
        error = 'communicator'
    
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
    
    try:
        resolution = c.getResolutionCamera(numcamera)
    except:
        pass
    try:
        capture_rect = c.getCaptureRectCamera(numcamera)
    except:
        pass
    try:
        brightness  = c.getBrightnessCamera(numcamera)
    except:
        pass
    try:
        saturation = c.getSaturationCamera(numcamera)
    except:
        pass
    try:
        sharpness = c.getSharpnessCamera(numcamera)
    except:
        pass
    try:
        contrast = c.getContrastCamera(numcamera)
    except:
        pass
    try:
        quality = c.getQualityCamera(numcamera)
    except:
        pass
    try:
        gamma = c.getGammaCamera(numcamera)
    except:
        pass
    try:
        light_hz = c.getLightHZCamera(numcamera)
    except:
        pass
    try:
        night_mode = c.getNightModeCamera(numcamera)
    except:
        pass
    try:
        illumination = c.getIlluminationMode(numcamera)
    except:
        pass
    try:
        low_light = c.getLowLight(numcamera)
    except:
        pass
    try:
        short_exposures = c.getShortexposures(numcamera)
    except:
        pass
    try:
        scheduler = c.getParamsScheduler(numcamera)
    except:
        pass
    try:
        cameramode = int(c.getModeScheduler(numcamera))
    except:
        pass
        
    type = ''
    source = ''
    
    camera = None
    try:
        camera = c.getCameras()[int(numcamera)]
        
    except:
        if error == '':
            error = 'camera'
   
    if error == '': 
        source  = camera['ip']
        type = camera['type']
        c.close();
        del c
    
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    dstr1 = 0
    dstr2 = 0
    dstr3 = 0
    dstr4 = 0
    try:
        dstr1, dstr2, dstr3, dstr4 = b.getCameraParameter(source, type)
    except:
        pass
    b.close()
    del b
    
    distorsion = {'p1': dstr1, 'p2': dstr2, 'p3': dstr3, 'p4': dstr4}
   
    com ={'host': '', 'port': ''}
    try:
        com = {'host': COMMUNICATORS[communicator]['host'],
               'port': COMMUNICATORS[communicator]['port'],
               }
    except:
        error = 'communicator'
                                      
    data = {'host': HTTP_HOST, 'select_page': 'settings','com': com,
                            'numcamera': numcamera, 'select_subpage': 'camera', 'camera': camera,
                            'resolution': resolution, 'capture_rect': capture_rect, 'brightness': brightness,
                            'saturation': saturation, 'sharpness': sharpness, 'contrast': contrast,
                            'quality': quality, 'gamma': gamma, 'light_hz': light_hz,
                            'night_mode': night_mode, 'illumination': illumination,
                            'low_light': low_light, 'short_exposures': short_exposures,
                            'distorsion': distorsion, 'source': source, 'type': type, 'cameramode': cameramode, 
                            'user' :  request.user.username, 'scheduler': scheduler,
                            'error': error, 'communicator': communicator,
                            'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}}
                            
    data.update(getDefaultParams(request, 'camera'))
        
    return render_to_response_ex(request, "camera.html", data)                            
    response.set_cookie('comhost', com['host'])
    response.set_cookie('comport', com['port'])
    response.set_cookie('numcamera', numcamera)
    return response

@tester
@permission_required('user_perms.perm_lists')
def distortion_settings(request, communicator, numcamera, cameramode):
        
    from videoclient import models
    from videoclient.balancer import Balancer
    from videoclient.communicator import Communicator
    
    COMMUNICATORS = []
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
    
    error = ''
    camera = ''
    c = None
    server = ''
    port = ''
    try:
        server = COMMUNICATORS[int(communicator)]['host']
        port = COMMUNICATORS[int(communicator)]['port']
        c = Communicator(COMMUNICATORS[int(communicator)]['host'], COMMUNICATORS[int(communicator)]['port'])
        c.open()
        camera = c.getCameras()[int(numcamera)]
    except:
        error = 'communicator'
        del c
        
    models.Camera.objects.get_or_create(ip = camera['ip'], type = camera['type'])
        
    if error == '':
        c.close()
        del c
        
    data = {'host': HTTP_HOST,  'select_page': 'settings',
                                'select_subpage': 'distortion', 'user': request.user.username, 
                                'server': server, 'port': port, 'error': error, 'communicator': communicator,
                                'numcamera': numcamera, 'cameramode': cameramode, 'camera': camera,
                                'bal' : {'host':HOST, 'port':PORT, 'login':LOGIN, 'passwd':PASSWD, 'user':USER}}

    data.update(getDefaultParams(request, 'distortion'))
            
    return render_to_response_ex(request, "po4distortion.html", data)

@tester
@permission_required('user_perms.perm_lists')
def settings_recognition(request):
    
    from videoclient import models
    from videoclient.balancer import Balancer
    from videoclient.communicator import Communicator
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
    
    
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    dis_eye = None
    journalBoundCoeff = None
    minBoundCoeffForLearn = None
    maxBoundCoeffForLearn = None
    try:
        dis_eye = b.getParameter()
    except:
        dis_eye = 0
    try:
        journalBoundCoeff = b.getParameter('journalBoundCoeff')
    except:
        journalBoundCoeff = 0
    try:
        minBoundCoeffForLearn = b.getParameter('minBoundCoeffForLearn')
    except:
        minBoundCoeffForLearn = 0
    try:
        maxBoundCoeffForLearn = b.getParameter('maxBoundCoeffForLearn')
    except:
        maxBoundCoeffForLearn = 0
        
    
    b.close()
    del b
    
    data = {'host': HTTP_HOST,  'select_page': 'settings',
                                'select_subpage': 'recognition', 'user': request.user.username,
                                'dis_eye': dis_eye, 'journalBoundCoeff': journalBoundCoeff, 
                                'minBoundCoeffForLearn': minBoundCoeffForLearn, 'maxBoundCoeffForLearn': maxBoundCoeffForLearn}
    
    data.update(getDefaultParams(request, 'recognition'))
    
    return render_to_response_ex(request, "po4settings_recognition.html", data)    

@tester
@permission_required('user_perms.perm_lists')
def special(request, project=None):
        
    import os
    from videoclient.settings import * 
    
    data = getDefaultParams(request, 'special', project)
    
    if not os.path.exists(SCRIPTS_ROOT):
        os.makedirs(SCRIPTS_ROOT)
    
    if request.POST.has_key('ping'):
        # TO DO check file complite
        if os.path.isfile(SCRIPTS_ROOT+S_COMPLITE):
            return HttpResponse('True')
            os.unlink(SCRIPTS_ROOT+S_COMPLITE)
        else:
            return HttpResponse('False')
    
    if request.POST.has_key('cmd'):
        if os.path.isfile(SCRIPTS_ROOT+S_COMPLITE):
            os.unlink(SCRIPTS_ROOT+S_COMPLITE) 
            
        if request.POST.has_key('path'):
            path = request.POST['path']
            if reguest.POST.has_key('action'):
                if reguest.POST['action'] == '0':
                    os.system("%s %s" %(S_COMMAND+SCRIPTS_ROOT+S_BACKUP, path))
                    return HttpResponse('backup');
                else:
                    os.system("%s %s" %(S_COMMAND+SCRIPTS_ROOT+S_RESTORE, path))
                    return HttpResponse('restore');
        elif request.POST.has_key('restart'):
            os.system(S_COMMAND+SCRIPTS_ROOT+S_RESTART)
            return HttpResponse('restart')
        elif request.POST.has_key('reboot'):
            os.system(S_COMMAND+SCRIPTS_ROOT+S_REBOOT)
            return HttpResponse('reboot')
                 
    return render_to_response_ex(request, "special.html", data)


class SoundFrom(forms.Form):
    name = forms.CharField(max_length=32)
    file = forms.FileField(required=False)
    ext = forms.CharField(max_length=8)

@tester
@permission_required('user_perms.perm_lists')
def events(request):
        
    if request.POST.has_key('save'):
        name_profile = request.POST['save'] 
        events = Event.objects.filter(profile = None).order_by("-id")
        profile = ProfileEvent.objects.create(name = name_profile)
        for event in events:
            new_event = Event(object = event)
            new_event.profile = profile
            new_event.save()
        return HttpResponse(True)
    
    if request.POST.has_key('load'):
        id = request.POST['load'] 
        Event.objects.filter(profile = None).delete()
        if id == "default":
            profile = ProfileEvent.objects.get(name_id = id)
        else:
            profile = ProfileEvent.objects.get(id = int(id))
        events = Event.objects.filter(profile = profile)
        for event in events:
            new_event = Event(object = event)
            new_event.profile = None
            new_event.save()
        return HttpResponse(True)
    
    if request.POST.has_key('change') and request.POST.has_key('id'):
        event = Event.objects.get(id = int(request.POST['id']))
        if request.POST.has_key('sound'):
            if int(request.POST['sound']) == 0:
                event.sound = None
            else:
                event.sound = Sound.objects.get(id = int(request.POST['sound']))
        elif request.POST.has_key('signal'):
            if int(request.POST['signal']) == 0:
                event.signal = None
            else:
                event.signal = Signal.objects.get(id = int(request.POST['signal']))
        elif request.POST.has_key('active'):
            event.active = request.POST['active'] == 'true'
        event.save()
        return HttpResponse(True)
    
    if request.POST.has_key('name'):
        form = SoundFrom(request.POST, request.FILES)
        if form.is_valid(): 
            fname = form.cleaned_data["name"]
            sound = Sound.objects.create(name = fname)
            sound.save()
            
            ext = form.cleaned_data["ext"]
            filename = get_journal_path(gen_filename("."+ext))
            ffile = form.cleaned_data["file"]
            
            sound.sound.save(filename, ffile)
            sound.url = filename
            sound.save()

    data = dict()
    data.update(getDefaultParams(request, 'events'))    
    data.update(getSearchEvent(request))
    
    data['sounds'] = Sound.objects.all()
    data['signals'] = Signal.objects.all()
    data['profiles'] = ProfileEvent.objects.filter(name_id = "")
        
    from videoclient import settings
    data['media_url'] = settings.MEDIA_URL
    
    data.update(dataNavigation(request, len(data['events'])))
    
    return render_to_response_ex(request, "po4events.html", data)

class FloatFieldWithComma(forms.FloatField):
    def clean(self, value):
        if value: value = value.replace(",",  ".")
        return super(FloatFieldWithComma,  self).clean(value)

class SettingsInterfaceFrom_start(forms.Form):
    save = forms.CharField(required=True)
    isMirror = forms.BooleanField(required=False)
    facebox = forms.BooleanField(required=False)
    eyes = forms.BooleanField(required=False)
    nouse = forms.BooleanField(required=False)
    hats = forms.BooleanField(required=False)
    clientMode = forms.IntegerField(required=True)
    frameDelay = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    frameCoeff = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    hatDelay = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    hatCoeff = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    corelation = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    timeCheck = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    
class SettingsInterfaceFrom(forms.Form):
    save = forms.CharField(required=True)
    isMirror = forms.BooleanField(required=False)
    facebox = forms.BooleanField(required=False)
    eyes = forms.BooleanField(required=False)
    nouse = forms.BooleanField(required=False)
    hats = forms.BooleanField(required=False)
    clientMode = forms.IntegerField(required=True)    
    frameDelay = FloatFieldWithComma(required=False)
    frameCoeff = FloatFieldWithComma(required=False)
    hatDelay = FloatFieldWithComma(required=False)
    hatCoeff = FloatFieldWithComma(required=False)
    corelation = FloatFieldWithComma(required=False)
    timeCheck = FloatFieldWithComma(required=False)
    
    class Meta:
        model = SettingsInterfaceFrom_start 
    
@tester
@permission_required('user_perms.perm_settings')
def settings_interface(request, project=None):
    from xml.dom.minidom import parseString

    data = getDefaultParams(request, 'settings_interface', project)
    
    if request.REQUEST.has_key('position'):
        position = request.POST['position']
        dp = DefaultParams.objects.get_or_create(name="ident_window_position")
        dp[0].value = position
        dp[0].save() 
        return HttpResponse(True)
    if request.REQUEST.has_key('res_interface'):
        position = request.POST['res_interface']
        dp = DefaultParams.objects.get_or_create(name="res_interface")
        dp[0].value = position
        dp[0].save() 
        return HttpResponse(True)

    form = SettingsInterfaceFrom(request.POST, request.FILES)
    if form.is_valid():
        info = form.cleaned_data
        if "frameDelay" in info: info["frameDelay"] = info["frameDelay"]*1000
        if "hatDelay" in info: info["hatDelay"] = info["hatDelay"]*1000
        data["info"] = info
        data["info"]["timeCheck"] = int(data["info"]["timeCheck"])
        logging.info(data["info"])
        template_name = "params_template.html"
        from django.template import loader
        txt = loader.render_to_string(template_name, dictionary=data)
        f = open(settings.CONFIG_IDENT_SWF, "w+b")
        f.write(str(txt))
        f.close()
    else: logging.exception(form.errors)

    try:
        if os.path.exists(settings.CONFIG_IDENT_SWF):
            f = open(settings.CONFIG_IDENT_SWF, "r")
            info = parseString(f.read())
            f.close()
            xml_info = info.getElementsByTagName("config")
            out = {}
            if xml_info:
                out["settings"] = {}
                for xml_inf in xml_info:
                    try:
                        out[xml_inf.getAttribute("id")] = xml_inf.getAttribute("content")
                        attr_id = xml_inf.getAttribute("id")
                        
                        if attr_id == "displayFrameSettings":
                            out["facebox"], out["eyes"], out["nouse"], out["hats"] = xml_inf.getAttribute("content").split(",")
                        elif attr_id in ("timeCheckSettings", "frameCoeffSettings", "hatCoeffSettings", "frameDelaySettings", "hatDelaySettings"):
                            outp = {}
                            outp["min"], outp["max"], outp["step"] = xml_inf.getAttribute("content").split(",")
                            out["settings"][attr_id] = outp
                        elif attr_id in ("frameDelay", "hatDelay"):
                            out[attr_id] = str(float(out[attr_id])/1000) 
                    except: logging.exception("parse ident config "+str(sys.exc_info()))
            data["info"] = out           
    except:
        logging.exception("parse xml "+str(sys.exc_info()))

    return render_to_response_ex(request, "po4settings_interface.html", data)
