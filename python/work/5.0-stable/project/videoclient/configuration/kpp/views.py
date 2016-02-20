#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.core.urlresolvers import reverse
from videoclient.views import render_to_response_ex, tester
from utils import getDefaultParams, REVISION, VERSION, check_rule
from django.utils import simplejson
from videoclient.configuration.kpp import forms
from django.shortcuts import get_object_or_404
from videoclient import models
import logging
import sys

def get_cameras(kpp):
    cameras = models.Camera.objects.filter(kpp=kpp)
    setattr(kpp, "cameras", cameras)
    return kpp

@tester
def view_kpp(request):
    data = dict()
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    data = dict()
    kpp_list = models.Kpp.objects.all().order_by("-id")
    data["kpp_list"] = kpp_list
    data["kpp_list_count"] = models.Kpp.objects.all().count()
    data.update(getDefaultParams(request, 'settings'))
    data.update({'select_subpage': 'kpp_list'})
    return render_to_response_ex(request, "kpp_lists.html", data)

@tester
def new(request, id=None):
    data = dict()
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    data.update(getDefaultParams(request, 'settings'))
    data.update({'select_subpage': 'kpp_list'})
    status = False
    if id:
        kpp = models.Kpp.objects.filter(id=int(id))
        if kpp:
            data["kpp"] = kpp[0]    
    return render_to_response_ex(request, "kpp_form.html", data)

@tester
def update(request, id=None):
    data = dict()
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    data = dict()
    error = ""
    status = False
    form = forms.CheckKpp(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        location = form.cleaned_data.get("location", "")    
        if id:
            kpp = models.Kpp.objects.filter(id=int(id))
            if kpp: 
                kpp.update(name=name, location=location)
            else:
                models.Kpp.objects.create(name=name, location=location)
        else:
            models.Kpp.objects.create(name=name, location=location)

    else: 
        error = form.errors
        data["error"] = error
        return render_to_response_ex(request, "kpp_form.html", data)
    
    return HttpResponseRedirect(reverse("kpp_list", args=[]))
    
@tester
def change_camera_cpp(request):
    data = dict()
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    
    data = dict()
    error = ""
    status = False
    formid = forms.ChangeCameraKpp(request.POST)
    if formid.is_valid():
        camera_id = formid.cleaned_data["camera_id"]
        kpp_id = formid.cleaned_data["kpp_id"]
        kpp = models.Kpp.objects.filter(id=int(kpp_id))
        camera = models.Camera.objects.filter(id=int(camera_id))
        if camera and kpp:
            camera.update(kpp=kpp[0])
            status = "success"
    else: 
        error = formid.errors
    
    data["error"] = error
    data["result"] = status
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')