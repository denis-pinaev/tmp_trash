# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
import logging
from videoclient import models
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from videoclient import settings
from videoclient.settings import PATH_SMILART 
from videoclient.control_settings.balancer import Balancer
import sys
from videoclient.views import tester, JsonResponse, render_to_response_ex
import json
from wizard import models as wModels
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from videoclient import utils as vcUtils
from django.utils.translation import ugettext as _
from videoclient.communicator.models import Communicator
from videoarchive.va import models as aModels 
from videoarchive.archive_settings import views as ArchSettings
from django.contrib.auth.decorators import permission_required
from videoarchive.archive import archive as vArchive
from videoarchive.va import models as VaModels

def getWizardData(request):
    data = dict()
    data.update(vcUtils.getCurrentTime())
    data.update(vcUtils.getVersion())
    if getShowVideoAnalytics():
        data["all_steps"] = 5
    else: data["all_steps"] = 4
    return data

@tester
@permission_required('user_perms.perm_wizard')
def settings_fin(request):
    
    data = dict()
    data.update(getWizardData(request))
    return render_to_response_ex(request, 'settings_fin.html', data)

def check_other_balancer_daemons(id_balancer, show_videoanalitycs=True):
    b_daemons_type=[]
    try:
        from videoclient import balancer
        from videoclient.views import initBalancer
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        
        if show_videoanalitycs:
            try:
                value = b.getParameter(param="balancer.%s.stay.analytics" %(id_balancer-1), fromBase="system")
            except:
                value = "false"
            
            if value == "true": b_daemons_type.append('Videoanalytics Daemon')
        
        try: 
            value = b.getParameter(param="balancer.%s.stay.recording" %(id_balancer-1), fromBase="system")
        except:
            value = "false"
        if value == "true": b_daemons_type.append('SaveVideo')
            
        b.close()
        del b
    except:
        logging.exception(str(sys.exc_info()))
    return b_daemons_type

@tester
@permission_required('user_perms.perm_wizard')
def getBalancersLastSysInfo(request):
    try:
        all_settings = wModels.Settings.objects.all()
        if all_settings.count()>0 and request.REQUEST.has_key("action"):
            balancers = json.loads(all_settings[0].value)
        if not balancers: return getBalancersSysInfo(request)
        
        show_videoanalitycs = getShowVideoAnalytics()
        balancers["show_videoanalitycs"] = show_videoanalitycs
        
        server_ind = 1
        useDU = request.REQUEST.get("userDU", False) or False
        for balancer in balancers["balancer"]:
            b_daemons_type=[]
            if request.REQUEST.has_key("server%s_sdd" %server_ind): b_daemons_type.append('Skin Detection Daemon')
            if request.REQUEST.has_key("server%s_ddd" %server_ind): b_daemons_type.append('Dupp Detection Daemon')
            if show_videoanalitycs and request.REQUEST.has_key("videoanalytics%s" %server_ind): b_daemons_type.append('Videoanalytics Daemon')
            cpu = request.REQUEST.get("cpu_on%s" %server_ind, 0)
            openmp = 0
            count_streams = request.REQUEST.has_key("count_streams%s" %server_ind)
            if cpu and int(cpu) > 0: 
                if not "CPU DU Daemon" in b_daemons_type: b_daemons_type.append('CPU DU Daemon')
                if count_streams:
                    openmp = request.REQUEST.get("server%s_videocard_du" %(server_ind), 1)
                    openmp = openmp if str(openmp).isdigit() and openmp > 0 else 1
                userDU = True
            if request.REQUEST.has_key("record") and str(request.REQUEST["record"]) == str(server_ind): b_daemons_type.append('SaveVideo')
            balancer["daemons_type"] = b_daemons_type
            vcard_ind = 1

            for videocard in balancer["videocards"]:
                daemons_type = []
                if request.REQUEST.has_key("server%s_videocard%s_du" %(server_ind,vcard_ind)): 
                    userDU = True
                    if count_streams: videocard["openmp-max-threads"] = openmp
                    else: videocard["openmp-max-threads"] = request.REQUEST.get("server%s_videocard%s_du" %(server_ind,vcard_ind), 1)
                    daemons_type.append('DU Daemon (FD-FR-FS)')
                if request.REQUEST.has_key("server%s_videocard%s_fdd" %(server_ind,vcard_ind)): daemons_type.append('Face Detection Daemon')
                if request.REQUEST.has_key("server%s_videocard%s_frd" %(server_ind,vcard_ind)): daemons_type.append('Face Recognition Daemon')
                if request.REQUEST.has_key("server%s_videocard%s_fsd" %(server_ind,vcard_ind)): daemons_type.append('Fan Studio Daemon')
                videocard["daemons"] = []
                videocard["daemons_type"] = daemons_type
                vcard_ind += 1
            server_ind += 1
        balancers["useDU"] = useDU
        
        json_balancers = json.dumps(balancers)
        if all_settings.count() == 0:
            wModels.Settings.objects.create(value=json_balancers)
        else:
            all_settings.update(value=json_balancers)
        
        return balancers
    except:
        logging.exception('getBalancerSysLastInfo: '+str(sys.exc_info()))
    return None        

def deleteAllElement(b_daemons_type, element):
    try:
        while element in b_daemons_type:
            i = b_daemons_type.index(element)
            del b_daemons_type[i]
    except:
        logging.exception(sys.exc_info())
    return b_daemons_type

def getShowVideoAnalytics():
    return int(vcUtils.get_value_defaultparams("show_videoanalitycs", 1)) == 1

@tester
@permission_required('user_perms.perm_wizard')
def getBalancersSysInfo(request):
    try:
        all_settings = wModels.Settings.objects.all()
        server_list = []
        if all_settings.count()>0 and request.POST.get("action", None):
            balancers = json.loads(all_settings[0].value)
            if request.POST.get("action", None) == "back": return balancers
            for b in balancers["balancer"]:
                server_list.append({"ip": b["address"], "videocard": b["video_count"]})
        else:
            from videoclient import balancer
            from videoclient.views import initBalancer
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = balancer.Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            balancers = b.getSystemInfo()
            b.close()
            del b
        if not balancers:
            balancers = dict()

        show_videoanalitycs = getShowVideoAnalytics()
        balancers["show_videoanalitycs"] = show_videoanalitycs 
        
        servers = dict()
        count_servers = int(request.REQUEST.get("count_servers", 0)) or 0
        if count_servers > 0:
            server_list = []
            i = 1
            while i<=count_servers:
                if request.REQUEST.has_key("ip_server%s" %i):
                    server = request.REQUEST["ip_server%s" %i]
                    cpu = request.REQUEST.get("cpu_on%s" %i, 0)
                    if cpu and int(cpu) > 0: videocard = cpu
                    else: videocard = request.REQUEST["videocard%s" %i]
                    servers[server] = videocard
                    server_list.append({"ip": server, "videocard": videocard})
                i=i+1
        newBalancer = []
        tree_balancers = dict()
        if balancers and balancers.has_key("balancer"):
            for balancer in balancers["balancer"]:
                if not (balancer["address"] in servers) and len(servers)>0:
                    continue
                tree_balancers[balancer["address"]] = balancer

        for_balancers = server_list
        if len(server_list) == 0:
            for_balancers = tree_balancers
   
        s = 0
        for f_balancer_ind in for_balancers:
            s += 1
            if len(server_list) == 0: f_balancer = f_balancer_ind
            else: f_balancer = f_balancer_ind["ip"]

            if not tree_balancers.has_key(f_balancer):
                tree_balancers[f_balancer] = {'address': f_balancer, 'daemons': []}
            balancer = tree_balancers[f_balancer]
            balancer["cpu"] = False
            balancer["servers"] = servers
            if not (balancer["address"] in servers) and len(servers)>0:
                continue

            b_daemons_type =  []
            if request.REQUEST.has_key("count_servers"):
                if balancer.has_key("daemons_type"):
                    b_daemons_type = balancer["daemons_type"]
                                
            openmp = 0
            count_streams = request.REQUEST.has_key("count_streams%s" %s)
                                
            if request.REQUEST.has_key("server%s_sdd" %s): b_daemons_type.append('Skin Detection Daemon')
            if request.REQUEST.has_key("server%s_ddd" %s): b_daemons_type.append('Dupp Detection Daemon')
            if show_videoanalitycs and request.REQUEST.has_key("videoanalytics%s" %s): b_daemons_type.append('Videoanalytics Daemon')
            if request.REQUEST.has_key("cpu_on%s" %s):
                if int(request.REQUEST.get("cpu_on%s" %s, 0)) > 0: b_daemons_type.append('CPU DU Daemon')
                else: b_daemons_type = deleteAllElement(b_daemons_type, 'CPU DU Daemon')
                if count_streams:
                    openmp = request.REQUEST.get("server%s_videocard_du" %(s), 1)
                    openmp = openmp if str(openmp).isdigit() and openmp > 0 else 1
            if request.REQUEST.has_key("record") and str(request.REQUEST["record"]) == str(s): b_daemons_type.append('SaveVideo')
                
            videocards = dict()

            if not ((request.REQUEST.has_key('action') and request.REQUEST["action"] == "back") or balancer.has_key("daemons_type")):
                b_daemons_type.extend(check_other_balancer_daemons(s, show_videoanalitycs=show_videoanalitycs))
          
            video_count = dict()
            for daemons in balancer["daemons"]:
                if not isinstance(daemons, dict):
                    continue
                for daemon in daemons["daemon"]:
                    if daemon.has_key("device"):
                        if daemon["type"] == "DU Daemon (FD-FR-FS)" and daemon["name"] == "CPU":
                            if (((request.REQUEST.has_key("cpu_on%s" %s) and 
                                  int(request.REQUEST.get("cpu_on%s" %s, 0)) > 0) or
                                 not request.REQUEST.has_key("cpu_on%s" %s)) and
                                not "CPU DU Daemon" in b_daemons_type): 
                                b_daemons_type.append("CPU DU Daemon")
                            balancer["cpu"] = True
                            continue
                        else:
                            if not (int(daemon["device"]) in videocards):
                                videocards[int(daemon["device"])] = dict()
                                videocards[int(daemon["device"])]["daemons"] = []
                                videocards[int(daemon["device"])]["daemons_type"] = []
                                videocards[int(daemon["device"])]["name"] = None
                            #if not request.REQUEST.has_key("action"):
                            videocards[int(daemon["device"])]["daemons"].append(daemon)
                            videocards[int(daemon["device"])]["daemons_type"].append(daemon["type"])
                            if daemon.has_key("name") and daemon.get("name", None) != "CPU":
                                videocards[int(daemon["device"])]["name"] = daemon["name"]
                        video_count[str(daemon["device"])] = True                                      
                    else:
                        if not ((request.REQUEST.has_key('action') and request.REQUEST["action"] == "back") or balancer.has_key("daemons_type")):
                            if daemon.get("type", None) == "DU Daemon (FD-FR-FS)" and daemon.get("name", None) == "CPU":
                                if not "CPU DU Daemon" in b_daemons_type: b_daemons_type.append("CPU DU Daemon")
                            elif not daemon["type"] in b_daemons_type: b_daemons_type.append(daemon["type"])
                        
            balancer["daemons_type"] = b_daemons_type

            if balancer.has_key("daemons_type") and ('DU Daemon (FD-FR-FS)' in balancer["daemons_type"] or "CPU DU Daemon" in balancer["daemons_type"]):
                balancers["useDU"]=True
            
            if balancer.has_key("videocards"):
                old_videocards = balancer["videocards"]
            else:
                old_videocards = None
                
            balancer["videocards"] = []
            ind = 0
            for videocard in videocards:
                videocards[videocard]["device"] = videocard
                balancer["videocards"].append(videocards[videocard])
                if request.REQUEST.has_key("count_servers"):
                    ind = len(balancer["videocards"])-1
                    maxind = ind
                    if old_videocards and ind<len(old_videocards) and old_videocards[ind].has_key("daemons_type"):
                        balancer["videocards"][ind]["daemons_type"] = old_videocards[ind]["daemons_type"]
            
               
            if not request.REQUEST.has_key("count_servers") and old_videocards:
                ind = len(balancer["videocards"])
                while old_videocards and ind<len(old_videocards) and old_videocards[ind].has_key("daemons_type"):
                    balancer["videocards"].append(old_videocards[ind])
                    ind=ind+1
                    
            i = len(balancer["videocards"])
            if servers.has_key(f_balancer) and len(servers)> 0:
                while i<int(servers[f_balancer]):
                    balancer["videocards"].append({'daemons': [], 'device': 0, 'daemons_type': []})
                    if request.REQUEST.has_key("count_servers"):
                        ind = len(balancer["videocards"])-1
                        maxind = ind
                        if old_videocards and ind<len(old_videocards) and old_videocards[ind].has_key("daemons_type"):
                            balancer["videocards"][ind]["daemons_type"] = old_videocards[ind]["daemons_type"]
                    i=i+1
                balancer["video_count"] = max(len(balancer["videocards"]), int(servers[f_balancer]))
            else:
                if not balancer.has_key("video_count"):
                    balancer["video_count"] = len(balancer["videocards"])
            v = 0
            for videocard in balancer["videocards"]:
                v = v+1
                daemons_type = []
                if request.REQUEST.has_key("server%s_videocard%s_du" %(s,v)): 
                    balancers["useDU"]=True
                    if count_streams: videocard["openmp-max-threads"] = openmp
                    else: videocard["openmp-max-threads"] = request.REQUEST.get("server%s_videocard%s_du" %(s,v), 1)
                    daemons_type.append('DU Daemon (FD-FR-FS)')
                if request.REQUEST.has_key("server%s_videocard%s_fdd" %(s,v)): daemons_type.append('Face Detection Daemon')
                if request.REQUEST.has_key("server%s_videocard%s_frd" %(s,v)): daemons_type.append('Face Recognition Daemon')
                if request.REQUEST.has_key("server%s_videocard%s_fsd" %(s,v)): daemons_type.append('Fan Studio Daemon')
                
                if not request.REQUEST.has_key("count_servers") and request.REQUEST.has_key("action"):
                    videocard["daemons_type"] = daemons_type
                if balancer.has_key("daemons_type") and 'DU Daemon (FD-FR-FS)' in videocard["daemons_type"]:
                    balancers["useDU"]=True
                    
            if balancer.has_key("daemons_type") and 'DU Daemon (FD-FR-FS)' in balancer["daemons_type"]:
                balancers["useDU"]=True
            
            newBalancer.append(balancer)

        if not request.REQUEST.has_key("count_servers") and request.REQUEST.has_key("action"): 
            balancers["useDU"] = "useDU" in request.REQUEST
            
        balancers["balancer"] = newBalancer
        
        json_balancers = json.dumps(balancers)
        if all_settings.count() == 0:
            wModels.Settings.objects.create(value=json_balancers)
        else:
            all_settings.update(value=json_balancers)
        
        return balancers
    except:
        logging.exception('getBalancerSysInfo: '+str(sys.exc_info()))
    return None

@tester
@permission_required('user_perms.perm_wizard')
def save_servers(request):
    error_msg = ""
    try:
        all_params = getAllParameters()
        
        balancer = models.Balancer.objects.all();
        balancer = balancer[0]
    
        try:
            b = Balancer(balancer.host, balancer.port, balancer.login, balancer.passwd, balancer.user)          
            for param in all_params:
                res = b.setParameter(value=all_params[param], param = param, toBase="system")
            b.close()
            del b
        except:
            logging.exception("wizard "+str(sys.exc_info()))
            error_msg += _("Ошибка задания настроек системы.") +str(sys.exc_info())        
        
    except:
         logging.exception("wizard "+str(sys.exc_info()))
    return HttpResponse(error_msg)


@tester
@permission_required('user_perms.perm_wizard')
def settings_balancer(request):

    if not "save_balancer" in request.POST and request.POST.get("action", None) == "next":
        balancers = getBalancersLastSysInfo(request)
    else: balancers = getBalancersSysInfo(request)

    if "save_balancer" in request.POST and "settings" in request.REQUEST and request.REQUEST["settings"] != "block_file_upload":
        data = locals()
        data.update(getWizardData(request))
        return render_to_response_ex(request, 'settings_videocards.html', data)
    elif "save_balancer" in request.POST and "settings" in request.REQUEST and request.REQUEST["settings"] == "block_file_upload":
        from videoclient.control_settings import views as cViews
        return  cViews.import_settings(request) 
    #HttpResponseRedirect("/wizard/fin")
        #return render_to_response_ex(request, 'settings_balancer.html', locals())
        #return save_servers(request)
    elif "action" in request.REQUEST and request.REQUEST["action"] == "next":
        return save_servers(request)
        #return HttpResponseRedirect("/wizard/fin/")
        #return render_to_response_ex(request, 'settings_videocards.html', locals()) 
    else:
        data = locals()
        data.update(getWizardData(request))
        return render_to_response_ex(request, 'settings_balancer.html', data)
    

class SettingsCommunicatorForm(forms.Form):
    host = forms.CharField( max_length=256, label=u'Хост', required=True)


PATH_DAEMONS = PATH_SMILART+"daemons/"
PATH_CONFIG = PATH_SMILART+"config/"

def create_DU_params(id_balancer, gpu, index=0, cpu=0):
    params = dict()
    params["balancer.%s.daemon.DU.count"%id_balancer] = "%s" %(index+1)
    
    params["balancer.%s.daemon.FD.distortion3"%id_balancer] = "false"
    params["balancer.%s.daemon.FD.global"%id_balancer] = "true"
    
    #params["balancer.%s.daemon.FD.histogram32"%id_balancer] = "true"
    #params["balancer.%s.daemon.FD.noisefactor"%id_balancer] = "true"
    #params["balancer.%s.daemon.FD.focus_factor"%id_balancer] = "true"    
    #params["balancer.%s.daemon.FD.noise_standard_deviation"%id_balancer] = "true"
    
    params["balancer.%s.daemon.FD.use.preprocessing.notation"%id_balancer] = "true"
    
    params["balancer.%s.daemon.FS.convert.request.to.bitmap"%id_balancer] = "false"
    params["balancer.%s.daemon.FS.convert.result.from.bitmap"%id_balancer] = "true"
    
    params["balancer.%s.daemon.DU.%s.barbars"%(id_balancer, index)] = "%sdfu/barbars.db" %PATH_CONFIG
    params["balancer.%s.daemon.DU.%s.key_checking_attempts_number"%(id_balancer, index)] = "10"
    params["balancer.%s.daemon.DU.%s.key_checking_interval"%(id_balancer, index)] = "3"
    params["balancer.%s.daemon.DU.%s.fd_type"%(id_balancer, index)] = "light"
    params["balancer.%s.daemon.DU.%s.log4cxx"%(id_balancer, index)] = "%sdfu/%s/log4cxx.xml"%(PATH_CONFIG, index)
    params["balancer.%s.daemon.DU.%s.path"%(id_balancer, index)] = "%sdfu/dfuni5p"%PATH_DAEMONS
    params["balancer.%s.daemon.DU.%s.settings"%(id_balancer, index)] = "%sdfu/settings.ini"%PATH_CONFIG
    params["balancer.%s.daemon.DU.%s.socket"%(id_balancer, index)] = "127.0.0.1:20%03d" %index
    params["balancer.%s.daemon.DU.%s.sysdir"%(id_balancer, index)] = "%sdata/dfu/%s/" %(PATH_SMILART, index)
    if cpu > 0:        
        params["balancer.%s.daemon.DU.%s.target"%(id_balancer, index)] = "CPU"
        params["balancer.%s.daemon.DU.%s.openmp-max-threads"%(id_balancer, index)] = cpu
        params["balancer.%s.daemon.DU.%s.start"%(id_balancer, index)] = "socket,sysdir,log4cxx,settings,barbars,fd_type,key_checking_attempts_number,key_checking_interval,target,openmp-max-threads"
    elif gpu >= 0:
        params["balancer.%s.daemon.DU.%s.gpu"%(id_balancer, index)] = gpu
        params["balancer.%s.daemon.DU.%s.start"%(id_balancer, index)] = "socket,sysdir,log4cxx,settings,barbars,fd_type,key_checking_attempts_number,key_checking_interval,gpu"
    else:
        params["balancer.%s.daemon.DU.%s.start"%(id_balancer, index)] = "socket,sysdir,log4cxx,settings,barbars,fd_type,key_checking_attempts_number,key_checking_interval"
    
    return params
        
def create_FD_params(id_balancer, gpu, index=0):
    params = dict()
    params["balancer.%s.daemon.FD.count"%id_balancer] = "%s" %(index+1)
    params["balancer.%s.daemon.FD.distortion3"%id_balancer] = "false"
    params["balancer.%s.daemon.FD.global"%id_balancer] = "true"
    params["balancer.%s.daemon.FD.histogram32"%id_balancer] = "true"
    params["balancer.%s.daemon.FD.noisefactor"%id_balancer] = "true"
    params["balancer.%s.daemon.FD.focus_factor"%id_balancer] = "true"    
    params["balancer.%s.daemon.FD.noise_standard_deviation"%id_balancer] = "true"
    params["balancer.%s.daemon.FD.use.preprocessing.notation"%id_balancer] = "true"

    params["balancer.%s.daemon.FD.%s.key_checking_attempts_number"%(id_balancer, index)] = "10"
    params["balancer.%s.daemon.FD.%s.key_checking_interval"%(id_balancer, index)] = "3"
    
    params["balancer.%s.daemon.FD.%s.socket"%(id_balancer, index)] = "127.0.0.1:15%03d" %index
    params["balancer.%s.daemon.FD.%s.path"%(id_balancer, index)] = "%sfd/dfdet5p"%PATH_DAEMONS
    params["balancer.%s.daemon.FD.%s.sysdir"%(id_balancer, index)] = "%sdata/fd/__so_all"%PATH_SMILART
    params["balancer.%s.daemon.FD.%s.log4cxx"%(id_balancer, index)] = "%sfd/%s/log4cxx.properties"%(PATH_DAEMONS, index)
    params["balancer.%s.daemon.FD.%s.gpu"%(id_balancer, index)] = gpu
    params["balancer.%s.daemon.FD.%s.start"%(id_balancer, index)] = "socket,sysdir,log4cxx,gpu"
    return params

def create_FR_params(id_balancer, gpu, index=0):
    params = dict()    

    params["balancer.%s.daemon.FR.count"%id_balancer] = "%s" %(index+1)
    #сокет обязательный параметр
    
    params["balancer.%s.daemon.FR.%s.key_checking_attempts_number"%(id_balancer, index)] = "10"
    params["balancer.%s.daemon.FR.%s.key_checking_interval"%(id_balancer, index)] = "3"

    
    params["balancer.%s.daemon.FR.%s.socket"%(id_balancer, index)] = "127.0.0.1:16%03d" %index
    params["balancer.%s.daemon.FR.%s.path"%(id_balancer, index)] = "%sfr/dfrec5p" %PATH_DAEMONS
    params["balancer.%s.daemon.FR.%s.sysdir"%(id_balancer, index)] = "%sdata/fr/%s/" %(PATH_SMILART, index)
    params["balancer.%s.daemon.FR.%s.log4cxx"%(id_balancer, index)] = "%sfr/%s/log4cxx.properties"%(PATH_DAEMONS, index)
    params["balancer.%s.daemon.FR.%s.settings"%(id_balancer, index)] = "%sfr/settings.ini"%PATH_DAEMONS
    params["balancer.%s.daemon.FR.%s.barbars"%(id_balancer, index)] = "%sfr/barbars.db"%PATH_DAEMONS
    params["balancer.%s.daemon.FR.%s.ident"%(id_balancer, index)] = "firstIdent"
    params["balancer.%s.daemon.FR.%s.gpu"%(id_balancer, index)] = gpu
    #параметры запуска демона (если нет такой строки - демон запускаться не будет)
    params["balancer.%s.daemon.FR.%s.start"%(id_balancer, index)] = "socket,sysdir,log4cxx,settings,barbars,gpu"
    return params
    
def create_FS_params(id_balancer, gpu, index=0):
    params = dict()    
    
    params["balancer.%s.daemon.FS.count"%id_balancer] = "%s" %(index+1)
    params["balancer.%s.daemon.FS.distortion3"%id_balancer] = "true"
    
    #сокет обязательный параметр
    
    params["balancer.%s.daemon.FS.%s.key_checking_attempts_number"%(id_balancer, index)] = "10"
    params["balancer.%s.daemon.FS.%s.key_checking_interval"%(id_balancer, index)] = "3"
    
    params["balancer.%s.daemon.FS.%s.socket"%(id_balancer, index)] = "127.0.0.1:17%03d" %index
    params["balancer.%s.daemon.FS.%s.path"%(id_balancer, index)] = "%sfs/dfans2p"%PATH_DAEMONS
    params["balancer.%s.daemon.FS.%s.log4cxx"%(id_balancer, index)] = "%sfs/%s/log4cxx.properties"%(PATH_DAEMONS, index)
    params["balancer.%s.daemon.FS.%s.gpu"%(id_balancer, index)] = gpu
    params["balancer.%s.daemon.FS.%s.start"%(id_balancer, index)] = "socket,log4cxx,gpu"
    
    params["balancer.%s.daemon.FS.convert.request.to.bitmap"%id_balancer] = "false"
    params["balancer.%s.daemon.FS.convert.result.from.bitmap"%id_balancer] = "true"
    #параметры запуска демона (если нет такой строки - демон запускаться не будет)
    
    return params

def create_balancer_params(id_balancer, ip):
    params = dict()
    params["balancer.%s.address"%id_balancer] = ip
    params["balancer.%s.port"%id_balancer] = "16545"
    return params

def create_SD_params(id_balancer, index=0):
    params = dict()

    params["balancer.%s.daemon.SD.count"%id_balancer] = "%s" %(index+1)
    #сокет обязательный параметр
    
    params["balancer.%s.daemon.SD.%s.key_checking_attempts_number"%(id_balancer, index)] = "10"
    params["balancer.%s.daemon.SD.%s.key_checking_interval"%(id_balancer, index)] = "3"
    
    params["balancer.%s.daemon.SD.%s.socket"%(id_balancer, index)] = "127.0.0.1:18%03d" %index
    params["balancer.%s.daemon.SD.%s.path"%(id_balancer, index)] = "%ssd/dskin2ps"%PATH_DAEMONS
    params["balancer.%s.daemon.SD.%s.log4cxx"%(id_balancer, index)] = "%ssd/log4cxx.properties"%PATH_DAEMONS
    #параметры запуска демона (если нет такой строки - демон запускаться не будет)
    params["balancer.%s.daemon.SD.%s.start"%(id_balancer, index)] = "socket,log4cxx"
    return params

def create_DD_params(id_balancer, index=0):
    params = dict()

    params["balancer.%s.daemon.DD.count"%id_balancer] = "%s" %(index+1)
    params["balancer.%s.daemon.DD.param.coeff"%id_balancer] = "0.95"
    params["balancer.%s.daemon.DD.param.crops"%id_balancer] = "0"
    params["balancer.%s.daemon.DD.param.dupps"%id_balancer] = "1"
    params["balancer.%s.daemon.DD.param.loose"%id_balancer] = "1"
    params["balancer.%s.daemon.DD.param.mode"%id_balancer] = "0"
    params["balancer.%s.daemon.DD.param.report"%id_balancer] = "0"
    params["balancer.%s.daemon.DD.param.flips"%id_balancer] = "0"
    params["balancer.%s.daemon.DD.param.cw90s"%id_balancer] = "0"
    # сокет обязательный параметр
    
    params["balancer.%s.daemon.DD.%s.key_checking_attempts_number"%(id_balancer, index)] = "10"
    params["balancer.%s.daemon.DD.%s.key_checking_interval"%(id_balancer, index)] = "3"
    
    params["balancer.%s.daemon.DD.%s.socket"%(id_balancer, index)] = "127.0.0.1:19%03d" %index
    params["balancer.%s.daemon.DD.%s.path"%(id_balancer, index)] = "%sdd/ddupp2"%PATH_DAEMONS
    params["balancer.%s.daemon.DD.%s.sysdir"%(id_balancer, index)] = "%sdata/dd"%PATH_SMILART
    params["balancer.%s.daemon.DD.%s.log4cxx"%(id_balancer, index)] = "%sdd/log4cxx.properties"%PATH_DAEMONS
    # параметры запуска демона (если нет такой строки - демон запускаться не будет)
    params["balancer.%s.daemon.DD.%s.start"%(id_balancer, index)] = "socket,sysdir,log4cxx"
    return params

def create_Videoanalytics_params(id_balancer, value = "false"):
    params = dict()
    params["balancer.%s.stay.analytics" %id_balancer] = value  
    return params

def create_SaveVideo_params(id_balancer, value = "false"):
    params = dict()
    params["balancer.%s.stay.recording" %id_balancer] = value
    return params

#balancer.0.daemon.HR.count=1
##сокет обязательный параметр
#balancer.0.daemon.HR.0.socket=192.168.0.233:16001
#balancer.0.daemon.HR.0.path=/opt/smilart/daemons/fr/builds/310/dfrec5
#balancer.0.daemon.HR.0.sysdir=/opt/smilart/data/fr/3/
#balancer.0.daemon.HR.0.log4cxx=/opt/smilart/daemons/fr/3/log4cxx.properties
#balancer.0.daemon.HR.0.settings=/opt/smilart/config/fr/settings181k.ini
#balancer.0.daemon.HR.0.gpu=2
##параметры запуска демона (если нет такой строки - демон запускаться не будет)
#balancer.0.daemon.HR.0.start=socket,sysdir,log4cxx,settings,gpu


    
def getAllParameters():
    data = dict()
    all_settings = wModels.Settings.objects.all()
    balancers = json.loads(all_settings[0].value)
    b = 0
    data["balancers.count"] = "%d" %len(balancers["balancer"])
       
    for balancer in balancers["balancer"]:
        du_index = 0
    
        fd_index = 0
        fr_index = 0
        fs_index = 0
    
        sd_index = 0
        dd_index = 0
                
        gpu = 0
        d = create_balancer_params(b, balancer["address"])
        data.update(d)
        if "Skin Detection Daemon" in balancer["daemons_type"]:
            data.update(create_SD_params(b, sd_index))
            sd_index+=1
        if "Dupp Detection Daemon" in balancer["daemons_type"]:
            data.update(create_DD_params(b, dd_index))
            dd_index+=1
            
        if "Videoanalytics Daemon" in balancer["daemons_type"]:
            data.update(create_Videoanalytics_params(b, "true"))
        else:
            data.update(create_Videoanalytics_params(b, "false"))
            
        if "SaveVideo" in balancer["daemons_type"]:
            data.update(create_SaveVideo_params(b, "true"))
        else:
            data.update(create_SaveVideo_params(b, "false"))
        
        cpu = "CPU DU Daemon" in balancer["daemons_type"]
        for videocard in balancer["videocards"]:
                if "DU Daemon (FD-FR-FS)" in videocard["daemons_type"]: 
                    data.update(create_DU_params(b, gpu, du_index, videocard.get("openmp-max-threads", 0) if cpu else 0))
                    du_index+=1 
                else:
                    if "Face Detection Daemon" in videocard["daemons_type"]: 
                        data.update(create_FD_params(b, gpu, fd_index))
                        fd_index+=1 
                    if "Face Recognition Daemon" in videocard["daemons_type"]: 
                        data.update(create_FR_params(b, gpu, fr_index))
                        fr_index+=1
                    if "Fan Studio Daemon" in videocard["daemons_type"]:
                        data.update(create_FS_params(b, gpu, fs_index))
                        fs_index+=1
                gpu = gpu+1
        b = b+1
    return data

def make_answer(answer=None, error=None):
    if answer is None:
        return {"status": True, "errors": []}
    elif error is not None:
        if "errors" not in answer:
            answer["errors"] = []
        answer["errors"].append(error)
        answer["status"]= False
    return answer

@tester
@permission_required('user_perms.perm_wizard')
def settings_communicator(request, step=2):
        
    HOST = ''
    form = SettingsCommunicatorForm(request.POST, request.FILES)
    balancer = models.Balancer.objects.all();
    if balancer.count()>0: HOST = balancer[0].host
    error_msg = ""
    if "save" in request.POST:
        from videoclient.views import JsonResponse
        answer = make_answer()
        if form.is_valid():
            host = form.cleaned_data["host"]
            settings_videoarchive(host)       
            
            try:
                b = Balancer(host, settings.DEFAULT_BALANCER_PORT, settings.DEFAULT_BALANCER_LOGIN, settings.DEFAULT_BALANCER_PASSWORD, settings.DEFAULT_BALANCER_USER)           
                res = b.setParameter(value=settings.DEFAULT_CONTROL_CLIENTS_COUNT, param = 'control.clients.count', toBase="system")
                res = b.setParameter(value=settings.DEFAULT_CONTROL_CLIENT_0_TYPE, param = 'control.client.0.type', toBase="system")
                res = b.setParameter(value=host, param = 'control.client.0.address', toBase="system")
                res = b.setParameter(value=settings.DEFAULT_CONTROL_CLIENT_0_PORT, param = 'control.client.0.port', toBase="system")
                res = b.setParameter(value=settings.DEFAULT_CONTROL_CLIENT_0_USER, param = 'control.client.0.user', toBase="system")
                res = b.setParameter(value=host, param = 'control.communicator.address', toBase="system")
                
                #res = b.setParameter(value='http://'+host+'/logperson/', param = 'alerterServer', toBase="default")
                res = b.setParameter(value='http://'+host+'/logdetector_package/', param = 'control.detector.alert.server', toBase="default")
                res = b.setParameter(value='http://'+host+'/logperson_package/', param = 'control.alert.packet.url', toBase="default")
                #for param in all_params:
                #    res = b.setParameter(value=all_params[param], param = param, toBase="system")
                b.close()
                del b
            except:
                logging.exception("wizard "+str(sys.exc_info()))
                answer = make_answer(answer, _("Ошибка задания настроек. Управляющая система недоступна."))
            
            if answer["status"]:
                try:
                    if balancer.count() == 0: 
                        models.Balancer.objects.create(host=host, port=settings.DEFAULT_BALANCER_PORT, active=True, login=settings.DEFAULT_BALANCER_LOGIN, passwd=settings.DEFAULT_BALANCER_PASSWORD, user=settings.DEFAULT_BALANCER_USER)
                    else: 
                        balancer.update(host=host, port=settings.DEFAULT_BALANCER_PORT, active=True, login=settings.DEFAULT_BALANCER_LOGIN, passwd=settings.DEFAULT_BALANCER_PASSWORD, user=settings.DEFAULT_BALANCER_USER)
                except:
                    logging.exception("wizard "+str(sys.exc_info()))
                    answer = make_answer(answer, _("Ошибка задания управлящей системы."))
                
                try:
                    from configuration.web_api_users.models  import WebApiSetting
                    from configuration.web_api_users import config
                    web_api_settings = WebApiSetting.objects.all();
                    if web_api_settings.count() == 0: 
                        WebApiSetting.objects.create(host = host, port = config.PORT, users_url = config.U_URL, stat_url = config.ST_URL )
                    else:
                        web_api_settings.update(host = host, port = config.PORT, users_url = config.U_URL, stat_url = config.ST_URL )
                except:
                    logging.exception("wizard "+str(sys.exc_info()))
                    answer = make_answer(answer, _("Ошибка задания WEB API."))
                
                try:
                    communicator = models.Communicator.objects.filter(active=True)
                    if communicator.count() == 0:
                        Communicator.objects.create(host=host, port=settings.DEFAULT_COMMUNICATOR_PORT, mjpeg_port=settings.DEFAULT_COMMUNICATOR_MJPEG_PORT, active=True)
                    else:
                        if communicator.count() > 1:
                            id = communicator[0].id
                            communicator.update(active=False)
                            communicator = models.Communicator.objects.filter(id=id)     
                        communicator.update(host=host, port=settings.DEFAULT_COMMUNICATOR_PORT, mjpeg_port=settings.DEFAULT_COMMUNICATOR_MJPEG_PORT, active=True)
                except:
                    logging.exception("wizard "+str(sys.exc_info()))
                    answer = make_answer(answer, _("Ошибка задания коммуникатора."))
                    
        else:
            answer = make_answer(answer, _("\"Адрес\" - обязательное поле"))
        return JsonResponse(answer)
    data = locals()
    data.update(getWizardData(request))
    return render_to_response_ex(request, 'settings_communicator.html', data)

@tester
@permission_required('user_perms.perm_wizard')    
def settings_user(request, id = None):
    
    data = dict()
    from videoclient import utils
    data.update(utils.getDefaultParams(request, 'anketauser', None))
    data.update(utils.dataUser(request, id))
    data['learn'] = True
    if "ajax" in request.REQUEST:
        
        data_send = dict()
        data_send["status"] = "errors" not in data
        if not data_send["status"]:
            data_send["errors"] = data["errors"]
        return JsonResponse(data_send)
    else:
        data.update(getWizardData(request))
        return render_to_response_ex(request, 'settings_user.html', data)

@login_required
def restart_cs(request):
    import os
    try:
        os.system("%s" % settings.RESTART_CS_CMD)
    except:
        logging.exception("wizard restartCS: "+str(sys.exc_info()))
    return HttpResponse('Control system restarted')

"""
@tester
@permission_required('user_perms.perm_wizard')
def settings_videoarchive(request):
    
    videoarchives = aModels.VaArchive.objects.filter(active=True)
    if "action" in request.REQUEST and request.REQUEST["action"] == "next":        
        return save_videoarchives(request)
    else:
        videoarchive_port = settings.DEFAULT_VIDEOARCHIVE_PORT        
        data = locals()
        data.update(getWizardData())
        return render_to_response_ex(request, 'settings_videoarchive.html', data)
    
@tester
@permission_required('user_perms.perm_wizard')    
def save_videoarchives(request):
    from videoarchive.archive_settings import forms   
    error_msg = ""
    if request.REQUEST.has_key("count_servers"):
        i = 1
        count_servers = int(request.REQUEST["count_servers"])            
        servers = []
        try:
            while i<= count_servers:
                if request.REQUEST.has_key("ip_server%s" %i) and request.REQUEST.has_key("url_server%s" %i):
                    server = {"ip": request.REQUEST.get("ip_server%s" %i, None),
                              "port": settings.DEFAULT_VIDEOARCHIVE_PORT,
                              "url": request.REQUEST.get("url_server%s" %i, None),
                              "save_dir": settings.DEFAULT_VIDEOARCHIVE_SAVE_DIR}
                    form = forms.TestAddArchiveForm(server)
                    if form.is_valid():
                        servers.append(server)
                        arch, create = aModels.VaArchive.objects.get_or_create(ip=server["ip"], port=server["port"]) 
                        if create: 
                            arch.url = server["url"]
                            arch.save_dir = server["save_dir"]
                            arch.save()
                            ArchSettings.compliteArchiveParams(request, arch, None)
                        else:
                            if arch:
                                arch.active = True
                                if arch.url != server["url"] or arch.save_dir != server["save_dir"]:                                
                                    arch.url = server["url"]
                                    #arch.save_dir = server["save_dir"]
                                arch.save()
                                
                i=i+1
            videoarchives = aModels.VaArchive.objects.all()
            for archive in videoarchives:
                if len(filter(lambda x: archive.ip==x["ip"] and str(archive.port)==str(x["port"]), servers)) == 0:
                    aModels.VaArchive.objects.filter(id=archive.id).update(active=False)
        except:
            logging.exception("wizard archive "+str(sys.exc_info()))
            error_msg += "Ошибка задания настроек видеоархива." +str(sys.exc_info())

    return HttpResponse(error_msg)
"""

@tester
@permission_required('user_perms.perm_wizard')
def setDomenToVideoarchive(request, domen):
        videoarchives = aModels.VaArchive.objects.all()
        for v_archive in videoarchives:
            try:
                ArchSettings.compliteArchiveParams(request, v_archive, domen)
            except:
                logging.exception("wizard setDomenToVideoarchive: "+str(sys.exc_info()))

def settings_videoarchive(host=None):
    from videoclient.monitoring.utils import saveMonitoringMessage
    if not host: return False
    videoarchives = VaModels.VaArchive.objects.all()
    for v_archive in videoarchives:
        try:
            compliteArchiveParams(v_archive, host) 
        except:
            logging.exception("wizard videoarchive_params: "+str(sys.exc_info()))
            params = {'host':v_archive.host, 'port':v_archive.port}
            saveMonitoringMessage(id = 'videoarchive_settings_error', params = params, type='accident_components', description=_("Ошибка задания параметров демона видеоархива, демон %(host)s:%(port)s") % params, show=True)
    return True

def compliteArchiveParams(archive, domen=None):
        va = vArchive.Archive(archive.ip, archive.port)
        params = [{'name': 'adminDomen', 'value': domen},
                  {'name': 'adminAlertUrl', 'value': "/monitoring/alert/"},
                  {'name': 'identThreshold', 'value': vcUtils.get_value_defaultparams(settings.journalBoundCoeff)},
                  {'name': 'delOlderDays', 'value': 14},
                  {'name': 'thresholdFreeSpaceNotif', 'value': 25},
                  {'name': 'thresholdFreeSpaceDel', 'value': 20},
                  {'name': 'delIntervalHours', 'value': 1},
                  {'name': 'bitrate', 'value': 1500},
                  {'name': 'blur', 'value': 0.6},
                  {'name': 'compress', 'value': 0.8},
                  {'name': 'gopSize', 'value': 2},
                  {'name': 'socketTimeout', 'value': 1000}]
        if domen != archive.ip and archive.ip != '127.0.0.1':
            url = "http://%s/files/archive/" % (archive.ip.replace("http://", ""))
            VaModels.VaArchive.objects.filter(id=archive.id).update(url=url)
        elif archive.url != '/files/archive/':
            VaModels.VaArchive.objects.filter(id=archive.id).update(url='/files/archive/')
        va.setDaemonSettings(params=params)
        va.close()
        del va

@tester
@permission_required('user_perms.perm_wizard')
def settings_globalparams(request):    
    from videoclient.balancer import Balancer
    from videoclient import views as vcViews
    
    data = dict()
    data.update(getWizardData(request))
    frame_minification = 1
    try:
        HOST, PORT, LOGIN, PASSWD, USER = vcViews.initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        b.open()    
        if b.connect:
            p = request.REQUEST.get("frame_minification", None)
            if p and str(p).isdigit():
                res = b.setParameter(p, "control.daemon.VA.frame-minification")
                return HttpResponse("")
            res = b.getParameter("control.daemon.VA.frame_minification")
            if res: frame_minification = res
        b.close()
        del b
    
    except:
        logging.exception(sys.exc_info())
    data["frame_minification"] = frame_minification
    return render_to_response_ex(request, 'settings_global_params.html', data)