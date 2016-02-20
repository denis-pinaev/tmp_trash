# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django import forms
from sender import Sender
import json
import sys
import logging
from config import *
from videoclient.utils import GlobalSortUser
from videoclient.views import tester, render_to_response_ex
from django.contrib.auth.decorators import permission_required
from utils import getDefaultParams

SUCCESS = 200
ERROR = 1
ERROR400 = 400

#reterned status
OK = 0
FORM_ERR = 2
LOGIN_ERR = 3
IP_ERR = 4
NO_DATA = 5


def json_response(data):
    return HttpResponse(json.dumps(data))

class UsersForm(forms.Form):
    filter = forms.CharField(required=False)
    sorto = forms.IntegerField(required=False)  
    up = forms.IntegerField(required=False)
    page = forms.IntegerField(required=False)


def getUsersList(): 
    
    from models import WebApiSetting
    
    web_api_settings = WebApiSetting.objects.all();
    if len(web_api_settings)>0:
        
        sd = Sender(web_api_settings[0].host,web_api_settings[0].port, web_api_settings[0].users_url)
        kwargs = {'action':  'get_users'}
        status, reason, resp_str = sd.sendData(kwargs)    
        #print '>>',resp_str
        #resp_str = '{"users":[{"login": "farLogin", "daemon_restrictions":{"detect":{"rpsec":10,"rpmin":10},"detect_and_identification":{"rpsec":10,"rpmin":10},"fanstudio":{"rpsec":10,"rpmin":10}},"ip_list":["192.168.0.166","192.168.0.152"]},{"login": "apicon", "daemon_restrictions":{"detect":{"rpsec":10,"rpmin":10},"detect_and_identification":{"rpsec":10,"rpmin":10},"fanstudio":{"rpsec":10,"rpmin":10}},"ip_list":["192.168.0.166","192.168.0.152","192.168.0.6","192.168.1.1","192.168.0.55","192.168.0.2","192.16.0.166","19.16.0.1","192.168.0.3","192.168.0.152","192.168.1.166","192.168.1.2"]}]}'
        if status != SUCCESS:
            resp = {}
        else:
            resp = json.loads(resp_str)
        
        if 'users' in resp:
            users = resp["users"]
        else:
            users = []
    else:
        users = []
    return users

@tester
@permission_required('user_perms.perm_settings')
def getPageUsers(request):
    form = UsersForm(request.REQUEST, request.FILES)
    users = getUsersList()
    data = dict()
    data['all_users'] = len(users)
    data.update(getDefaultParams(request, 'settings_web_api'))
    if form.is_valid():
        filter_str = form.cleaned_data["filter"]

        #выбор пользователей, содержащих в логине или ip листе строку filter_str        
        if filter_str:  
            users = filter(lambda x: x["login"].lower().find(filter_str.lower()) >= 0 or 
                       len(filter(lambda ip: ip.lower().find(filter_str.lower()) >= 0, x["ip_list"])) > 0, users)
         
        #Список полей, по которым возможна сортировка
        sort_fields = ["login"]
        sorto = form.cleaned_data["sorto"]
        #сортируем
        if sorto > 0 and sorto <= len(sort_fields):
            sort = [[sort_fields[sorto - 1]]]    
            users = GlobalSortUser(users, sort, 1, up=form.cleaned_data["up"])

        data.update(form.cleaned_data)
    for user in users:
        if len(user["ip_list"]) > COL_IP_FOR_USERS_LIST:
            user["light_ip_list"] = user["ip_list"][0:COL_IP_FOR_USERS_LIST + 1] 
        else:
            user["light_ip_list"] = user["ip_list"]        
    
    data["users"] = users
    return render_to_response_ex(request, 'webapi_users.html', data, context_instance=RequestContext(request))        



class UserForm(forms.Form):
    user_login = forms.CharField(required=True)
    sorto = forms.IntegerField(required=False)  
    up = forms.IntegerField(required=False)
    
@tester
@permission_required('user_perms.perm_settings')    
def getPageIp(request):
    form = UserForm(request.REQUEST, request.FILES) 
    data = dict()
    data.update(getDefaultParams(request, 'settings_web_api'))
    if form.is_valid():
        login = form.cleaned_data["user_login"]
        data["user_login"] = login
    else:
        data["user_login"] = ''
        data["error"] = FORM_ERR
    data['page']= 'user_ip'
    return render_to_response_ex(request, 'webapi_user_ip.html', data, context_instance=RequestContext(request))

@tester
@permission_required('user_perms.perm_settings')
def getTableIp(request): 
    form = UserForm(request.REQUEST, request.FILES) 
    data = dict()       
    ips = []
    if form.is_valid():
        login = form.cleaned_data["user_login"]
        sorto = form.cleaned_data["sorto"]
        up = form.cleaned_data["up"]
        
        data.update(form.cleaned_data)
        
        kwargs = {'action':  'get_ip', 'user':  login}
        
        from models import WebApiSetting
    
        web_api_settings = WebApiSetting.objects.all();
        if len(web_api_settings)>0:
        
            sd = Sender(web_api_settings[0].host,web_api_settings[0].port, web_api_settings[0].users_url)
            

            status, reason, resp_str = sd.sendData(kwargs)  
    
            if status == ERROR400:        
                data["error"] = LOGIN_ERR
            elif status != SUCCESS:
                data["error"] = ERROR
            else: 
                resp = json.loads(resp_str)
                if 'ip_list' in resp:
                    ips = resp['ip_list']
        else:
            logging.error("videoclient.configuration.web_api_users.wiews.getTableIp(connection failed) :" + 'Отсутствуют настройки для WEB API')
            data["error"] = ERROR

    else:
        data["user_login"] = ''
        data["error"] = FORM_ERR
    if 'error' in data:
        return json_response({'status': data["error"], 'result': ''}) 

    #сортируем
    sort_fields = ["ip"]
    sorto = form.cleaned_data["sorto"]
    if sorto > 0 and sorto <= len(sort_fields):    
        ips = sorted(ips, reverse=(up == 0))
    data["ip_list"] = ips
    from django.template import loader
    result = loader.render_to_string('ip_table.html', data, context_instance=RequestContext(request))
    return json_response({'status': OK, 'result': result}) 

@tester
@permission_required('user_perms.perm_settings')
def getPageIpAdd(request):
    form = UserForm(request.REQUEST, request.FILES) 
    data = dict()
    data.update(getDefaultParams(request, 'settings_web_api'))
    if form.is_valid():
        login = form.cleaned_data["user_login"]
        data["user_login"] = login
    else:
        data["user_login"] = ''
        data["error"] = FORM_ERR
    data['page']= 'user_ip'
    return render_to_response_ex(request, 'webapi_user_add_ip.html', data, context_instance=RequestContext(request))


class IpForm(forms.Form):
    user_login = forms.CharField(required=True)
    ip_list = forms.CharField(required=True)  

@tester
@permission_required('user_perms.perm_settings')
def postIpAdd(request):
    form = IpForm(request.REQUEST, request.FILES)
    if not form.is_valid():
        return json_response({"status": FORM_ERR, "result": 'Ошибка формы'})
    try:
        #получаем список адресов данного пользователя:
        login = form.cleaned_data['user_login']
        kwargs = {'action': 'get_ip', 'user':  login}
        
        from models import WebApiSetting
    
        web_api_settings = WebApiSetting.objects.all();
        if len(web_api_settings)>0:
        
            sd = Sender(web_api_settings[0].host,web_api_settings[0].port, web_api_settings[0].users_url)

            status, reason, resp = sd.sendData(kwargs)
            if status == ERROR400:
                return json_response({"status":LOGIN_ERR, "result": "Неверное указано имя пользователя"})   
            elif status != SUCCESS:
                logging.error("videoclient.configuration.web_api_users.wiews.post_ip_add(connection failed) :" + 'Ошибка соединения при получении списка ip адресов пользователя')
                return json_response({"status":ERROR, "result": "Повторите запрос позже"})
               
            ips = json.loads(resp)['ip_list']
            
            #IP добавляемые пользователем:
            add_ips = json.loads(form.cleaned_data['ip_list'])    
              
            #IP которые будут добавлены:
            ip_list = []
            for ip in add_ips:
                a = ip.split('.')
                add_ip = ''
                
                if len(a) == 4:
                    err = False
                    for i in a:
                        try:
                            octet = int(i)
                        except:
                            octet = 256
                        if not (0 <= octet and octet < 256):
                            err = True
                        add_ip += '%s' % ('.' if add_ip else '') + str(octet) 
                    if not err and not add_ip in ips and not add_ip in ip_list:
                        ip_list.append(add_ip)
            
            if not ip_list:
                return json_response({"status":IP_ERR, "result": "Новых IP-адресов не добавлено."})

            #добавляем адреса
            kwargs = {'action':'add_ip', 'user':  login, 'ip_list': '{ip_list:' + json.dumps(ip_list) + '}'}
            status, reason, resp = sd.sendData(kwargs)
            if status != SUCCESS:   
                return json_response({"status":ERROR, "result": "Повторите запрос позже"})
                   
            return json_response({"status":OK, "result":  ip_list})
        else:
            logging.error("videoclient.configuration.web_api_users.wiews.postIpAdd(connection failed) :" + 'Отсутствуют настройки для WEB API')
            return json_response({"status":ERROR, "result": "Повторите запрос позже"})
            
    except:
        logging.error("addIpList" + str(sys.exc_info()))
        return json_response({"status":ERROR, "result": "Повторите запрос позже"})

@tester
@permission_required('user_perms.perm_settings')
def postIpDel(request):
    form = IpForm(request.REQUEST, request.FILES)
    if not form.is_valid():
        return json_response({"status": FORM_ERR, "result": 'Ошибка формы'})
    login = form.cleaned_data['user_login']

    del_ips = json.loads(form.cleaned_data['ip_list'])
    kwargs = {'action': 'del_ip', 'user':  login, 'ip_list': '{ip_list:' + json.dumps(del_ips) + '}'}
    
    from models import WebApiSetting
    web_api_settings = WebApiSetting.objects.all();
    if len(web_api_settings)>0:
    
        sd = Sender(web_api_settings[0].host,web_api_settings[0].port, web_api_settings[0].users_url)

        status, reason, resp = sd.sendData(kwargs)
        if status == ERROR400:
            return json_response({"status":LOGIN_ERR, "result": "Неверное указано имя пользователя"})   
        elif status != SUCCESS:
            logging.error("videoclient.configuration.web_api_users.wiews.postIpDel(connection failed) :" + 'Ошибка соединения при получении списка ip адресов пользователя')
            return json_response({"status":ERROR, "result": "Повторите запрос позже"})
    else: 
        logging.error("videoclient.configuration.web_api_users.wiews.postIpDel(connection failed) :" + 'Отсутствуют настройки для WEB API')    
        return json_response({"status":ERROR, "result": "Повторите запрос позже"})
    
    return json_response({"status": OK, "result": "IP-адреса удалены (" + str(len(del_ips)) + ')'})

@tester
@permission_required('user_perms.perm_settings')
def getPageRestrictions(request):
    form = UserForm(request.REQUEST, request.FILES) 
    data = dict()
    data.update(getDefaultParams(request, 'settings_web_api'))
    if form.is_valid():
        login = form.cleaned_data["user_login"]
        data["user_login"] = login
    else:
        data["user_login"] = ''
        data["error"] = FORM_ERR
    data['page']= 'user_restrictions'
    return render_to_response_ex(request, 'webapi_user_restrictions.html', data, context_instance=RequestContext(request))

@tester
@permission_required('user_perms.perm_settings')
def postTableRestrictions(request):
    form = UserForm(request.REQUEST, request.FILES) 

    if not form.is_valid():
        return json_response({"status": FORM_ERR, "result": 'Ошибка формы'})
    data = dict()
    login = form.cleaned_data["user_login"]
    
    users = getUsersList()        
    user = filter(lambda x: x["login"] == login, users)
    if user:       
        data['restrictions'] = user[0]['daemon_restrictions']
    else:
        return json_response({"status":ERROR, "result": "Повторите запрос позже"})
        
    from django.template import loader
    result = loader.render_to_string('restrictions_table.html', data)
    return json_response({'status': OK,'result': result})         

@tester
@permission_required('user_perms.perm_settings')
def getPageSecurity(request):
    form = UserForm(request.REQUEST, request.FILES)
    data = dict()                
    data.update(getDefaultParams(request, 'settings_web_api'))
    if form.is_valid():
        login = form.cleaned_data["user_login"]
        data["user_login"] = login
    else:
        data["user_login"] = ''
        data["error"] = FORM_ERR
    data['page']= 'user_security'
    return render_to_response_ex(request, 'webapi_user_security.html', data, context_instance=RequestContext(request))

@tester
@permission_required('user_perms.perm_settings')
def getPageStatistics(request):
    form = UserForm(request.REQUEST, request.FILES)
    data = dict()                
    data.update(getDefaultParams(request, 'settings_web_api'))
    if form.is_valid():
        login = form.cleaned_data["user_login"]
        data["user_login"] = login
    else:
        data["user_login"] = ''
        data["error"] = FORM_ERR
    return render_to_response_ex(request, 'webapi_user_statistics.html', data, context_instance=RequestContext(request))


class StatisticForm(forms.Form):
    start_date = forms.CharField(required=True)  
    end_date = forms.CharField(required=True)
    query = forms.CharField(required=True)
    user_login = forms.CharField(required=True)
    sorto = forms.IntegerField(required=False)  
    up = forms.IntegerField(required=False)
    
@tester
@permission_required('user_perms.perm_settings')    
def postTableStatistics(request):
    form = StatisticForm(request.REQUEST, request.FILES)
    if not form.is_valid():
        return json_response({"status": FORM_ERR, "result": 'Повторите запрос позже'})
    data = dict()
    login = form.cleaned_data['user_login']
    s_date = form.cleaned_data['start_date']
    e_date = form.cleaned_data['end_date']
    query = form.cleaned_data['query']
    sorto = form.cleaned_data["sorto"]
    data['sorto'] = sorto
    data['up'] = form.cleaned_data['up']
    
    kwargs = {'user':  login, 'query':  query, 'start_date': s_date, 'end_date': e_date}
    
    from models import WebApiSetting
    web_api_settings = WebApiSetting.objects.all();
    if len(web_api_settings)==0:
        logging.error("videoclient.configuration.web_api_users.wiews.postIpDel(connection failed) :" + 'Отсутствуют настройки для WEB API')
        return json_response({"status": ERROR, "result": 'Стастистика временно недоступна. Повторите запрос позже.'})
    
    sd = Sender(web_api_settings[0].host,web_api_settings[0].port, web_api_settings[0].stat_url)
    status, reason, resp = sd.sendData(kwargs)
    del sd
    
    if status == ERROR400:   
        return json_response({"status": LOGIN_ERR, "result": 'Неизвестный пользователь'})
    if status != SUCCESS:
        return json_response({"status": ERROR, "result": 'Стастистика временно недоступна. Повторите запрос позже.'})
    ipstat = json.loads(resp)
    
    #вычисляем суммы столбцов и строк таблицы
    total = {}
    column_list = ['detect', 'detect_and_identification', 'fanstudio']    
    for column_name in column_list:
        total[column_name] = 0    
    total['total'] = 0
    for host in ipstat:
        host['total'] = 0
        for column_name in column_list:
            total[column_name] += host[column_name]
            total['total'] += host[column_name]
            host['total'] += host[column_name]
            
    #сортируем
    sort_fields = ["ip", 'detect', 'detect_and_identification', 'fanstudio', 'total']        
    if sorto > 0 and sorto <= len(sort_fields):
        sort = [[sort_fields[sorto - 1]]] 
        ipstat = GlobalSortUser(ipstat, sort, 1, up=form.cleaned_data["up"])
    
    data['table'] = ipstat
    data['total'] = total

    from django.template import loader
    if ipstat:
        result = loader.render_to_string('stat_table.html', data)
    else:
        result = False
    return json_response({'result': result, 'status': OK})        

@tester
@permission_required('user_perms.perm_settings')
def postDataStatistics(request):
    form = StatisticForm(request.REQUEST, request.FILES)
    data = dict()
    if not form.is_valid():
        return json_response({"status": FORM_ERR, "result": 'Повторите запрос позже'})
    
    login = form.cleaned_data["user_login"]
    s_date = form.cleaned_data['start_date']
    e_date = form.cleaned_data['end_date']
    query = form.cleaned_data['query']
    
    data["user_login"] = login  
    kwargs = {'user':  login, 'query':  query, 'start_date': s_date, 'end_date': e_date}
       
    from models import WebApiSetting
    web_api_settings = WebApiSetting.objects.all();
    if len(web_api_settings)==0:
        logging.error("videoclient.configuration.web_api_users.wiews.postDataStatistics(connection failed) :" + 'Отсутствуют настройки для WEB API')
        return json_response({"status": ERROR, "result": 'Стастистика временно недоступна. Повторите запрос позже.'})
    sd = Sender(web_api_settings[0].host,web_api_settings[0].port, web_api_settings[0].stat_url)
    
    status, reason, resp = sd.sendData(kwargs)
    
    del sd
    if status == ERROR400:   
        return json_response({"status": LOGIN_ERR, "result": 'Неизвестный пользователь'})
    if status != SUCCESS:
        return json_response({"status": ERROR, "result": 'Стастистика временно недоступна. Повторите запрос позже.'})    
    stat = json.loads(resp)
    #если данных для отображения на графике нет, то выводим сообщение
    if not filter(lambda x: len(filter(lambda x:x[1] > 0, x['data'])) > 0, stat):
        return json_response({"status": NO_DATA, "result": 'Отсутствуют данные за указанный период'})
    
    e = {}        
    e['resp'] = resp
    return json_response({'result': e, 'status': OK})
    

def passgen(size=8):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(size))

@tester
@permission_required('user_perms.perm_settings')
def postChangeKeyAccess(request):
    form = UserForm(request.REQUEST, request.FILES) 

    if not form.is_valid():
        return json_response({"status": FORM_ERR, "result": 'Ошибка формы'})
    login = form.cleaned_data["user_login"]
    new_key = passgen(16)
        
    kwargs = {'action':  'change_password', 'login':  login, 'new_password': new_key}
    from models import WebApiSetting
    web_api_settings = WebApiSetting.objects.all();
    if len(web_api_settings)==0:
        logging.error("videoclient.configuration.web_api_users.wiews.postChangeKeyAccess(connection failed) :" + 'Отсутствуют настройки для WEB API')
        return json_response({"status": ERROR, "result": 'Повторите запрос позже'})
    sd = Sender(web_api_settings[0].host,web_api_settings[0].port, web_api_settings[0].users_url)
    
    status, reason, resp = sd.sendData(kwargs)
    
    if status == ERROR400:
        return json_response({"status":LOGIN_ERR, "result": "Неверное указано имя пользователя"})   
    elif status != SUCCESS:
        logging.error("videoclient.configuration.web_api_users.wiews.changeKeyAccess(connection failed) :" + 'Ошибка соединения при получении списка ip адресов пользователя')
        return json_response({"status":ERROR, "result": "Повторите запрос позже"})
    return json_response({'status': OK, 'result': str(new_key)})
