# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django import forms
from datetime import datetime
import settings
import logging
import commands
import sys
import os
import re
from time import time


def check_dir(dname=""):
    try:
        lst = os.listdir(dname)
        if len(lst)>0: return 1
        return 0
    except:
        logging.error("check_dir "+str(sys.exc_info()))
        return -1
    
def main(request, result=None):
    logging.info(result)
    data = dict()
    data["select_page"] = "upload"
    sl = settings.server_list     
    try:
        for server in sl:
            server["check"] = settings.result_val[check_dir(server["check_dir"])]
    except:
        logging.error("main "+str(sys.exc_info()))
    data["servers"] = sl
    if os.path.exists(settings.log_updates_file):
        data["log"] = settings.log_updates_file    
    if result == "0": data["result"] = "Обновление прошло не удачно" 
    elif result == "1": data["result"] = "Обновление удачно"
    else: data["result"] = ""
    
    return render_to_response("update.html", data)

class TestDataUpload(forms.Form):
    updates = forms.FileField(required=True)

def upload(request):
    try:
        form = TestDataUpload(request.POST, request.FILES)
        r = 0
        if form.is_valid():
            filename = "%suploads%s" % (settings.dir_updates, time())
            f = open(filename, "w")
            for t in form.cleaned_data["updates"]: f.write(t)
            f.close()
            if settings.command_after_load:
                r = commands.getoutput(settings.command_after_load % (filename))
    except:
        logging.info("upload "+str(sys.exc_info()))
    logging.info(r)
    return HttpResponseRedirect(reverse("main", args=[r if r in ("0", "1") else 0]))

def export(request, project=None):
    data = dict()
    data["select_page"] = "export"
    dd =  os.path.dirname(settings.script_export_info)
    logging.info(dd)
    sys.path.append(dd)
    import config_export
    lst = os.listdir(config_export.tar_dir)
    tar = []  
    for l in lst:
        m = re.match(r'^.*.tar$', l)
        if m: tar.append({"name": config_export.info_value[l], 
                          "url": config_export.media_url+l, 
                          "dt": datetime.fromtimestamp(os.path.getmtime(config_export.tar_dir+l)).strftime("%d.%m.%Y %H:%M:%S")
                          }) 
    data["tar"] = tar
    return render_to_response("export.html", data)

class TestExportData(forms.Form):
    fr = forms.BooleanField(required=False)
    journal = forms.BooleanField(required=False)
    admin = forms.BooleanField(required=False)
    db = forms.BooleanField(required=False)
    version = forms.BooleanField(required=False)

def exportinfo(request, project=None):
    import commands
    form = TestExportData(request.REQUEST, request.FILES)
    if form.is_valid():
        s = []
        if "fr" in form.cleaned_data and form.cleaned_data["fr"]: s.append("fr")
        if "admin" in form.cleaned_data and form.cleaned_data["admin"]: s.append("admin")
        if "db" in form.cleaned_data and form.cleaned_data["db"]: s.append("db_dump")
        if "version" in form.cleaned_data and form.cleaned_data["version"]: s.append("version")
        if "journal" in form.cleaned_data and form.cleaned_data["journal"]: s.append("journal")
        data = commands.getoutput("%s %s" % (settings.script_export_info, " ".join(s)))
        c = data.find("TarURL:")
        if c>0: c += 7
        return HttpResponse(str(data[c:]))
    return HttpResponse("")

def reboot(request):
    data = dict()
    data["select_page"] = "reboot"
    return render_to_response("reboot.html", data)

def rebootsystem(request):
    if settings.REBOOT_SYSTEM: os.system(settings.REBOOT_SYSTEM)
    return HttpResponse(True)