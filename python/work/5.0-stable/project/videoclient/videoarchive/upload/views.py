#coding=utf-8
from django.http import HttpResponse
import forms
import json
import sys
import os
import models
from videoclient.settings import log_videoarchive as logging
from videoclient import settings
from django.shortcuts import get_object_or_404

def ping(request):
    return HttpResponse("ping")

def JsonResponse(data):
    return HttpResponse(json.dumps(data), mimetype="application/json")

def JavaScriptResponse(data):
    return HttpResponse(json.dumps(data), mimetype="application/javascript")

def file(request):
    try:
        if request.REQUEST.has_key("id"):
            file = get_object_or_404(models.Files, id=int(request.REQUEST["id"]))
            form = forms.FileUploadForm(request.REQUEST, request.FILES, instance = file)
        else:
            form = forms.FileUploadForm(request.REQUEST, request.FILES)
        if not form.is_valid():
            return JavaScriptResponse({"status": False, "error": form.errors})
        
        file = form.save(commit = False)
        file.size = 0#len(form.cleaned_data["file"])
        file.save()
        
        return JavaScriptResponse({"status": True, "size": len(form.cleaned_data["file"]), "url": file.file.path})
    except:
        logging.exception(str(sys.exc_info()))
        return JavaScriptResponse({"status": False, "error": str(sys.exc_info())})
    return JavaScriptResponse({"status": False})

def new_id(request):
    try:
        id = models.Files.getNewId()
        return HttpResponse(str(id))
    except:
        logging.exception(str(sys.exc_info()))
    return HttpResponse("0")

def check(request, id):
    try:
        file = get_object_or_404(models.Files, id=id)
        if os.path.isfile(file.file.path):
            f = open(file.file.path, "r+b")
            size = len(f.read())
            f.close()
        else:
            size = 0
        return HttpResponse(float(size)/float(file.size)*100)
    except:
        logging.exception(str(sys.exc_info()))
    return HttpResponse(0)