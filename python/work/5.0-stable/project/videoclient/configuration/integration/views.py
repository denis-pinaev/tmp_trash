#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from videoclient import utils
from videoclient.views import initBalancer, JsonResponse, tester, render_to_response_ex
from videoclient.balancer import Balancer
import logging
from django.contrib.auth.decorators import permission_required
import sys

def getFirstData():
    data = dict()
    data['system_control_smtp_mail_port'] = 25
    data['system_control_smtp_identification_alert_timeout'] = 30000
    data['system_control_smtp_mail_auth'] = "false"
    data['default_control_smtp_password'] = ""
    data['default_control_smtp_identification_alert_subject'] = ""
    data['system_control_smtp_subject'] = ""
    
    
    data['system_control_snmp_timeout'] = 10000
    data['system_control_snmp_area'] = ""
    data['system_control_snmp_identification_alert_timeout'] = 120000
    data['system_control_snmp_trap_version'] = 'version2'
    data['system_control_snmp_trap_type'] = 'inform'
    data['system_control_snmp_need_alert'] = 'false' 
    
    return data

def getAllParamsForBase(base = "system"):
    data = dict()
    try:
        HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
        data['HOST'] = HOST
        data['PORT'] = PORT
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        params = b.getAllParameters()
        
        allparam = map(lambda x: x["params"], filter(lambda x: x["name"]==base, params))
        if allparam: allparam = allparam[0]
        allparam = sorted(allparam, key=lambda x: x["name"])
        for param in allparam:
            name = param['name']
            value = param['val']
            if value is None:
                value = ""
            name = "%s_%s" %(base, name.replace('.', '_'))
            data[name] = value
            if name == "default_control_smtp_identification_alert_subject": data[name] = data[name].capitalize()
        b.close()
        del b
        return data
    except:
        logging.exception("all_params "+str(sys.exc_info()))
        data["us_error"] = str(sys.exc_info())
    return data

def getAllParams():
    data = dict()
    data["params"] = dict()
    data["params"].update(getFirstData())
    data["params"].update(getAllParamsForBase("system"))
    data["params"].update(getAllParamsForBase("default"))
    if "default_control_snmp_common_udp" in data["params"]:
        data["params"]["default_control_snmp_common_udp"] = data["params"]["default_control_snmp_common_udp"].split('/162')[0] 
    return data

@tester
@permission_required('user_perms.perm_settings')
def saveAllParams(request):
    try:
        HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        for param in request.REQUEST:
            args = param.split('_')
            if len(args)>=2 and args[0] in ["system", "default"]:
                base = args[0]
                param_name = '.'.join(args[1:])
                value = request.REQUEST[param]
                if value is None or value == "None":
                    value = ""
                if param_name.count("control.snmp.common.udp"):
                    value = "%s/162" %value
                res = b.setParameter(value=value, param = param_name, toBase=base)
        b.close()
        del b
        return {"status": True}                        
    except:
        logging.exception(str(sys.exc_info()))
        return {"status": False, "error": str(sys.exc_info())}
    
@tester
@permission_required('user_perms.perm_settings')
def universal(request):
    data = dict()
    data.update(utils.getDefaultParams(request, 'integration_universal'))
    data.update(getAllParams())
    if "save" in request.REQUEST:
        return JsonResponse(saveAllParams(request))
    return render_to_response_ex(request, "integration_universal.html", data)    

@tester
@permission_required('user_perms.perm_settings')
def smtp(request):
    data = dict()
    data.update(utils.getDefaultParams(request, 'integration_smtp'))
    data.update(getAllParams())
    if "save" in request.REQUEST:
        return JsonResponse(saveAllParams(request))
    return render_to_response_ex(request, "integration_smtp.html", data)

@tester
@permission_required('user_perms.perm_settings')
def snmp(request):
    data = dict()
    data.update(utils.getDefaultParams(request, 'integration_snmp'))
    data.update(getAllParams())
    if "save" in request.REQUEST:
        return JsonResponse(saveAllParams(request))
    return render_to_response_ex(request, "integration_snmp.html", data)