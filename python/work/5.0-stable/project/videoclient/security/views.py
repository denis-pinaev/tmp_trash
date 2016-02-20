# -*- coding: utf-8 -*-
import sys
import datetime, time
from django.utils import simplejson

from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from videoclient.utils import *
from videoclient import settings
from videoclient.views import tester, render_to_response_ex
from videoclient.models import Journal, VisitingCard, PositionsStatus, User, Camera
from videoclient.configuration import turnstiles
from django.contrib.auth.decorators import permission_required
from models import Decision
from django.db.models import Max, Min

monthArrayMed = ["Янв" ,"Фев", "Март", "Апр", "Май", "Июнь", "Июль", "Авг","Сент", "Окт", "Нояб", "Дек"]

def JsonResponse(data):
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

@tester
@permission_required('user_perms.perm_security')
def movementProcess(request, journal_id=None, status=None, timeout=None):
    try:
        journal = Journal.objects.filter(id=journal_id, person__active=1)    
        if journal.count()>0: 
            first_node = Journal.objects.filter(id=journal[0].agregate.id)
            if first_node[0].camera and first_node[0].person:
                jbuf = Journal.objects.filter(person=first_node[0].person).order_by("-id")
                users = User.objects.filter(id=int(request.user.id))
                if len(users) > 0:
                    user = users[0]
                else:
                    user = None
                try:    
                    Decision.objects.create(person=first_node[0].person, operator=user, state = status,camera = first_node[0].camera, dt = datetime.datetime.now())
                except:
                    logging.exception('create Decision ' + str(sys.exc_info()))
                if jbuf.count() > 0  and first_node[0].camera.position in [settings.camera_exit, settings.camera_all]:         
                    if status == settings.status_exit:
                        first_node.update(positions_status=settings.status_exit, operator=user)
                    if status == settings.status_enter:
                        first_node.update(positions_status=settings.status_enter, operator=user)
                        for j in journal:
                            turnstiles.sendEnterForCamera(j.camera.uuid, timeout )
                elif jbuf.count() == 0  and first_node[0].camera.position in [settings.camera_exit, settings.camera_all]:
                    if status == settings.status_exit:
                        first_node.update(positions_status=settings.status_exit, operator=user)
                    if status == settings.status_enter:
                        first_node.update(positions_status=settings.status_enter, operator=user)
                        for j in journal:
                            turnstiles.sendEnterForCamera(j.camera.uuid, timeout)

    except:
        logging.exception(sys.exc_info())
    return True

def getCurrentDate():
    data = dict()
    now = datetime.datetime.now()
    data['now_day'] = str(now.day)
    data['now_month'] = monthArrayMed[now.month-1]
    data['now_year'] = str(now.year)
    data['now'] = now
    return data

class SecurityForm(forms.Form):
    agregate_id = forms.IntegerField(required=True)
    
    id = forms.IntegerField(required=False)
    id_person = forms.IntegerField(required=False)
    action = forms.CharField(required=False)

@tester
@permission_required('user_perms.perm_security')
def security(request):

    data = dict()
    person_id = False
        
    users = User.objects.filter(id=int(request.user.id))
    if len(users) > 0 and users[0].kpp:
        user = users[0]
        
        kpp = user.kpp
        setattr(kpp, "cameras", Camera.objects.filter(kpp = kpp))
        data["kpp"] = kpp
                
        now = datetime.datetime.now()
        default_delay_for_create_new_group = int(get_value_defaultparams(settings.delay_for_create_new_group))
        time_delta = datetime.timedelta(seconds=default_delay_for_create_new_group)
        time_opened = int(get_value_defaultparams("time_opened_turnstiles"))

        form = SecurityForm(request.REQUEST, request.FILES)
        if form.is_valid():
            agregate_id = form.cleaned_data["agregate_id"]
    
            journals = Journal.objects.filter(dt_first_fixed__gte=now - time_delta, agregate__id__gt=agregate_id)
            journals = journals.filter(camera__kpp__id=user.kpp.id)
            journals = journals.exclude(agregate=None)
            journals = journals.exclude(person=None) 
            if form.cleaned_data["id_person"]:
                id_person = form.cleaned_data["id_person"]
                t_opened = datetime.timedelta(seconds=time_opened)
                #Было ли решение для этой персоны
                last_decision = Decision.objects.filter(person__id = id_person, dt__gte = now - t_opened)
                if len(last_decision) > 0:
                    uuids_last_decision = last_decision.values('camera')
                    ids = []
                    for l in uuids_last_decision:
                        ids.append(l["camera"])
                    journals = journals.exclude(camera__id__in = ids, person__id = id_person)            
            min_aggregate_id = journals.aggregate(Min("agregate__id"))["agregate__id__min"]
            
            if min_aggregate_id:
                journals = Journal.objects.filter(agregate__id=min_aggregate_id)
                journals = journals.filter(camera__kpp__id=user.kpp.id)
                journals = journals.order_by('-id')[:1]
                if journals.count() > 0:
                    journal_id = journals[0].agregate.id
                    person_id = journals[0].person.id
                    data.update(dataJournal(request, journals[0].id))
                    data.update(dataAccess(request, journals[0].id))
                    data.update(getDataDivision(request))
                    data['journalid'] = journal_id
                    data['agregate_id'] = journal_id
            else:
                data['agregate_id'] = agregate_id            

            id = form.cleaned_data.get("id", None)
            if id:
                if form.cleaned_data["action"] == 'ban':
                    movementProcess(request, id, settings.status_exit, time_opened)
                if form.cleaned_data["action"] == 'solve':
                    movementProcess(request, id, settings.status_enter, time_opened)
        else:
            journal = Journal.objects.all().order_by('-id')[:1]
            if journal:
                data['agregate_id'] = journal[0].agregate.id
    
    try:
        data['id_curr_person'] = form.cleaned_data["id_person"]
    except:
        data['id_curr_person'] = False
    if person_id:
        data['id_curr_person'] = person_id
    data.update(getCurrentDate())
    if request.GET.has_key('data'):
        return render_to_response_ex(request, "security_control_content.html", data)    
    return render_to_response_ex(request, 'security_control.html', data)    
