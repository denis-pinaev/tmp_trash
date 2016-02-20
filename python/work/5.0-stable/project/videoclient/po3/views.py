# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from videoclient.models import *
from videoclient.views import *
from django import forms
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _
from django.http import HttpResponseRedirect
from videoclient.utils import *


#
# TODO
# Удалить этот файл ПО3 в КПП не требуется, создавался тольк для демонстрации
#

def wanted(request):
    data = dict()
    #HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    SERVERC, PORTC, COMMUNICATORS = initCommunicators()
    
    ids = []
    
    from videoclient.balancer import Balancer
    try:
        bal = Balancer(initBalancer())
        data['allcount'] = pers.start(b, '')
        ids, persons, photos = pers.res()
        data['persons'] = bal.getPersons()
        bal.close()
        del bal
    except:
        pass
    
    data = dict()
    data['users'] = getDictUsers(Person.objects.all())
        
    return render_to_response_ex(request, "po3wanted.html", data)

def wantedphotos(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render_to_response_ex(request, "po3wantedphotos.html", {})

def pageemployee(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render_to_response_ex(request, "po3pageemployee.html", {})

def help(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render_to_response_ex(request, "po3help.html", {})

def anketawanted(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render_to_response_ex(request, "po3anketawanted.html", {})

def anketawantedclear(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render_to_response_ex(request, "po3anketawantedclear.html", {})

def anketawantedclear(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render_to_response_ex(request, "po3anketawantedclear.html", {})

def guards(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    data = dataGuards()
    
    return render_to_response_ex(request, "po3guards.html", data)


def anketaguard(request, id = None):
    data = dict()
    data.update(getDefaultParams(request, 'anketaguard'))
    data.update(dataUser(request, id))
        
    return render_to_response_ex(request, "po3anketaguard.html", data)

def guardphotos(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render_to_response_ex(request, "po3guardphotos.html", {})
