# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string 
from django.core.urlresolvers import reverse
from django.template import RequestContext
from videoarchive import utils as aUtils
from videoclient import utils as cUtils
from videoarchive.archive import utils as archiveUtils
from videoarchive.archive import archive as vArchive
from videoarchive.va import models as vaModels
from videoclient import models as vcModels
from videoarchive import forms as vaForms
from videoarchive.archive_settings import forms
from videoclient.views import tester
from django.contrib.auth.decorators import permission_required
from videoclient.settings import log_videoarchive as logging
from videoclient import settings
import json
import sys

# Получение списка архивов с параметрами по активному (либо первому) видеоархиву 
def get_archive_params(request, id=None):
    data = dict()
    if not id: 
       form = vaForms.CheckIdForm(request.REQUEST)
       if form.is_valid():
           id = form.cleaned_data["id"]
    va_servers, va_ports, videoarchives = archiveUtils.getVideoArchives()
    data['archives'] = videoarchives    
    if id and int(id):
        arch = vaModels.VaArchive.objects.filter(id=int(id), active=True)
        if arch.count() > 0:
            va_servers, va_ports, videoarchives = archiveUtils.getVideoArchives(arch[0])
        else:
            va_servers, va_ports, videoarchives = archiveUtils.getVideoArchives()

    if videoarchives and len(videoarchives) > 0:  
        archive_selected = videoarchives[0]
        data['archive_selected'] = archive_selected
        try: 
            archive = vArchive.Archive(archive_selected["host"], archive_selected["port"])
            archive.open()
            if archive.connect:
                data["connect"] = True
                data['settings'] = archive.getSettings()
                data["params"] = vaModels.VaArchiveParams.objects.filter(archive_selected["host"], archive_selected["port"])
            archive.close()
            del archive
        except:
            logging.exception(str(sys.exc_info()))
    return data

# Страница настроек видеоархива
@tester
@permission_required('user_perms.perm_videoarchive')
@permission_required('user_perms.perm_videoarchive_settings')
def archive(request, id = None):
    if not cUtils.check_rule(request):
        return HttpResponseRedirect(reverse("archive_page", args=["page_interface/"]))
    data = dict()
    data.update(aUtils.getDefaultParams(request, 'archive_settings_archive'))
    data.update(get_archive_params(request, id))

    return render_to_response('archive_settings/archive.html', data, context_instance=RequestContext(request))

@tester
@permission_required('user_perms.perm_videoarchive')
@permission_required('user_perms.perm_videoarchive_settings')
def tasks(request):
    data = dict()
    data.update(aUtils.getDefaultParams(request, 'archive_settings_tasks'))
    data["gop_size"] = cUtils.get_value_defaultparams("gop_size")
    data["compress"] = cUtils.get_value_defaultparams("compress")
    data["bitrate"] = cUtils.get_value_defaultparams("bitrate")
    data["blur"] = cUtils.get_value_defaultparams("blur")
    return render_to_response('archive_settings/tasks.html', data, context_instance=RequestContext(request))

@tester
@permission_required('user_perms.perm_videoarchive')
@permission_required('user_perms.perm_videoarchive_settings')
def communicators(request):
    data = dict()
    data.update(aUtils.getDefaultParams(request, 'archive_settings_communicators'))    
    form = vaForms.CheckJournalSortForm(request.GET)
    logging.info(form.errors)
    if form.is_valid():
        data["sort"] = form.cleaned_data["sort"]
        data["order"] = form.cleaned_data["order"]
    else:
        data.update({"order": 0, "sort": 0})
    s = "" if data["order"] == 0 else "-"
    if data["sort"] == 0: data["communicators"] = vcModels.Communicator.objects.filter(active=True).order_by(s+"id")
    else: data["communicators"] = vcModels.Communicator.objects.filter(active=True).order_by(s+"host", s+"port")
    return render_to_response('archive_settings/communicators.html', data, context_instance=RequestContext(request))

@tester
@permission_required('user_perms.perm_videoarchive')
@permission_required('user_perms.perm_videoarchive_settings')
def compliteArchiveParams(request, archive, domen=None):
    if not domen:
        domen = cUtils.get_value_defaultparams(settings.local_host_name)    
    if str(domen) == "0": 
         balancer = vcModels.Balancer.objects.all()
         logging.info(balancer)
         if balancer.count()>0: domen = balancer[0].host
         else: domen = request.META["HTTP_HOST"]
    logging.info(domen)
         
    add = True
    try:
        va = vArchive.Archive(archive.ip, archive.port)
        params = [{'name': 'adminDomen', 'value': domen}]
        logging.info(params)
        if va.setDaemonSettings(params=params): add = False
        va.close()
        del va
    except:
        logging.exception("setDomenToVideoarchive archive "+str(sys.exc_info()))
    finally:
        logging.info(add)
        if add:
            try:
                params, create = vaModels.VaArchiveParams.objects.get_or_create(name="adm_domen", id_archive=archive)
                params.value = domen
                params.save()
            except:
                logging.exception("setDomenToVideoarchive create_archive_params: "+str(sys.exc_info()))         
    """
    logging.info(domen)
    params = [{"name": "adm_domen", "value": domen}]
    for p in params:
        param, create = vaModels.VaArchiveParams.objects.get_or_create(id_archive=archive, name=p["name"])
        if create:
            param.value = p["value"]
            param.save()
        else:
            if param.value != p["value"]: 
                param.value = p["value"]
                param.save()
    """

@tester
@permission_required('user_perms.perm_videoarchive')
@permission_required('user_perms.perm_videoarchive_settings')
def updateArchiveIdentCoeff(coeff=0):
    varchives = vaModels.VaArchive.objects.all()
    for arch in varchives:
        status = True
        try:
            va = vArchive.Archive(arch.ip, arch.port)
            va.open()
            
            if va.connect:
                params = [{'name': 'identThreshold', 'value': coeff}]
                if va.setDaemonSettings(params=params): status = False
            va.close()
            del va
        except:
            logging.exception(sys.exc_info())
        if status: vaModels.VaArchiveParams.objects.filter(id_archive=arch, name="ident_threshold").update(value=coeff)

@tester
@permission_required('user_perms.perm_videoarchive')
@permission_required('user_perms.perm_videoarchive_settings')
def add_archive(request):
    status = False
    error = ""
    try:
        form = forms.TestAddArchiveForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data["ip"]
            url = form.cleaned_data["url"]
            id = form.cleaned_data.get("id", 0)
            arch, create = vaModels.VaArchive.objects.get_or_create(ip=ip, port=settings.DEFAULT_VIDEOARCHIVE_PORT)
            if create: 
                arch.url=url                
                arch.save_dir = settings.DEFAULT_VIDEOARCHIVE_SAVE_DIR
                arch.save()
                compliteArchiveParams(request, arch, None)
                status = True
                va_servers, va_ports, videoarchives = archiveUtils.getVideoArchives()
                select_arch = vaModels.VaArchive.objects.filter(id=id)
                archi = None
                if select_arch.count()>0: archi = select_arch[0]
                error = render_to_string("archive_settings/archive_list.html", {"archives": videoarchives, "archive_selected": archi}) 
            elif arch.active: error = "dublicate"
            else: 
                arch.active = True
                arch.url=url                
                arch.save()
                status = True
                va_servers, va_ports, videoarchives = archiveUtils.getVideoArchives()
                select_arch = vaModels.VaArchive.objects.filter(id=id)
                archi = None
                if select_arch.count()>0: archi = select_arch[0]
                error = render_to_string("archive_settings/archive_list.html", {"archives": videoarchives, "archive_selected": archi})
    except:
        logging.exception("add_archive "+str(sys.exc_info()))
    return HttpResponse(json.dumps({"status": status, "error": error}))
    
@tester
@permission_required('user_perms.perm_videoarchive')
@permission_required('user_perms.perm_videoarchive_settings')
def delete_archive(request):
    status = False
    try:
        form = forms.TestDeleteArchiveForm(request.POST)
        logging.info(form.errors)
        if form.is_valid():
            arch = vaModels.VaArchive.objects.filter(id=form.cleaned_data["id"]) 
            if arch.count() > 0:
                arch.update(active=False)
                status = True    
    except:
        logging.exception("delete_archive "+str(sys.exc_info()))
    return HttpResponse(json.dumps({"status": status}))                

def initCommunicators():
    #global SERVERC, PORTC, COMMUNICATORS 
    COMMUNICATORS = []
    comms = models.Communicator.objects.filter(active = True)
    SERVERC = ''
    PORTC = ''

    for comm in comms:
        COMMUNICATORS.append({'host': comm.host, 'port': comm.port})
        SERVERC = SERVERC + str(comm.host)+'*'
        PORTC = PORTC + str(comm.port)+'*'

    if len(SERVERC)>0:
        SERVERC = SERVERC[0:len(SERVERC)-1]
    if len(PORTC)>0:
        PORTC = PORTC[0:len(PORTC)-1]
    return SERVERC, PORTC, COMMUNICATORS

@tester
@permission_required('user_perms.perm_videoarchive')
@permission_required('user_perms.perm_videoarchive_settings')
def add_communicator(request):    
    try:
        form = forms.TestAddCommunicatorForm(request.POST)
        if form.is_valid():
            comm = vcModels.Communicator.objects.filter(host=form.cleaned_data["host"], port=form.cleaned_data["port"])
            if comm.count()>0:
                if comm[0].active: return HttpResponse("dublicate")
                else: comm.update(active = True)
            else: vcModels.Communicator.objects.create(host=form.cleaned_data["host"], port=form.cleaned_data["port"])
            communicators = models.Communicator.objects.filter(active=True).order_by("host", "port")
            return HttpResponse(render_to_string("archive_settings/communicator_list.html", {"communicators": communicators}))
    except:
        logging.exception("add_communicator: "+str(sys.exc_info()))
    return HttpResponse("error")
    
@tester
@permission_required('user_perms.perm_videoarchive')
@permission_required('user_perms.perm_videoarchive_settings')
def delete_communicator(request):
    try:
        form = forms.TestDeleteCommunicatorForm(request.POST)
        if form.is_valid():
            ids = request.REQUEST['ids'].split(',')
            if len(ids) == 0: return HttpResponse("error")
            ids = ids[:-1]
            i = 0
            comms = vcModels.Communicator.objects.filter(id__in = ids)
            comms.update(active = False)

            communicators = vcModels.Communicator.objects.filter(active=True).order_by("host", "port")
            return HttpResponse(render_to_string("archive_settings/communicator_list.html", {"communicators": communicators}))
    except:
        logging.exception("delete_communicators: "+str(sys.exc_info()))
    return HttpResponse("error")