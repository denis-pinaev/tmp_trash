# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import loader
from django.contrib.auth.decorators import login_required
from django import forms
from math import ceil
import os
import sys
import re
import logging
from control_settings import config
from videoclient.balancer import Balancer
from control_settings import models
from videoclient.models import Balancer as modBalancer
from utils import getDefaultParams
from videoclient import settings
import time
project = None
from utils import get_value_defaultparams
from django.forms.util import ErrorList
from videoclient.views import tester, render_to_response_ex
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _

def get_permit():
    try:
        return str(get_value_defaultparams(settings.permit_control_system_params)) == "1"
    except:
        return False

def get_NotEditable():
    try:
        all_permit = get_permit()
        return [] if all_permit else models.NotEditableParams.objects.filter(permit=False).values("code")
    except:
        return models.NotEditableParams.objects.filter(permit=False).values("code")        

def initBalancer():
    if modBalancer.objects.filter(active = True).count()>0:
        bal = modBalancer.objects.filter(active=True)[0]
        HOST = bal.host
        PORT = bal.port
        LOGIN = bal.login
        PASSWD = bal.passwd
        USER = bal.user
        return HOST, PORT, LOGIN, PASSWD, USER
    return '', '', '', '', ''

def numerate(c={}, num=1, all_count=0, p=20):
    try:
        if num == "": 
            num = 1
            c["pref"] = True
        else: num = int(num)
#        p = 20
        p2 = 4
        n = int(ceil(float(all_count)/p))
        if n<num: num = 1
        c["n"] = n          
        c["ind_start"] = (num-1)*p
        c["ind_end"] = num*p
        if c!={} and n>0 and num>0 and n>1:            
            c["first"] = 1
            c["last"] = n
            if num>1: c["prev"] = num-1
            if num<n: c["next"] = num+1
            start = max(1, num-p2)
            end = min(n, start+p2*2)
            c["start"] = start
            c["end"] = end
            c["end1"] = end+1
            c["num"] = num
            c["range"] = range(start, end+1)
        return c
    except:     
        logging.exception("numerate "+str(sys.exc_info()))
        return c
    
def get_params_info(val=None):
    if val == None: return config.number, config.step    
    if re.match(r'^[0-9]+$', val): return config.number, 1    
    elif re.match(r'^[0-9]+[,|.][0-9]+$', val): return config.number, 0.1
    elif val.lower() in ["true", "false"]: return config.boolean, 1
    else: return config.text, 1    
    
def get_params_value(p={}, sname=""):    
    params_value = models.Params.objects.filter(code=sname)
    if params_value.count()==0:
        if "val" in p: 
            type, step = get_params_info(p["val"])
            params_value = models.Params.objects.create(code=sname, type=type, step=step)
        else:
            params_value = models.Params.objects.create(code=sname, type=config.text)
    else: params_value = params_value[0]
    p["code"] = params_value.code
    p["info"] = params_value.name
    p["min_val"] = params_value.min_val
    p["max_val"] = params_value.max_val
    p["step"] = params_value.step
    p["type"] = params_value.type
    p["permit"] = False if get_permit() else models.NotEditableParams.objects.filter(code=sname, permit=False).count()>0
    return p
    
@tester
@permission_required('user_perms.perm_system_settings') 
def user_list(request, uid=None, num=1):
    if num == None: num = 1
    data = dict()
    data = getDefaultParams(request, 'control_settings_users', project)
    data["select_page"] = 'control_settings_users'
    data["user"] = request.user
    data["page"] = "user"
    try:
        HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
        data["HOST"] = HOST
        data["PORT"] = PORT        
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        if uid:
            data["ulogin"] = uid                
            params = b.getLoginParameters(uid)
            data["params"] = params
            data["number"] = config.number
            data["boolean"] = config.boolean
            data["text"] = config.text 
            post = request.POST
            save = False
            if "save" in post: save = True
            i = 0
            for base in params["bases"]:
                base["index"] = "params"
                base["params"] = sorted(base["params"], key=lambda x: x["name"]) 
                for p in base["params"]:
                    p["spin_id"] = i                
                    i += 1
                    p = get_params_value(p, p["name"])
                    s = "%s_%s" % (base["name"], p["name"])
                    p["id"] = s                    
                    if save:                    
                        if s in post:                      
                            if str(post[s] if post[s] != "" else "None") != str(p["val"]):
                                posts = post[s] #if post[s] != "" else False
                                if b.setParameter(value=posts, param=p["name"], toBase=base["name"]): p["val"] = posts
                                else: p["error"] = "ошибка параметра"
            b.close()
            del b
            return render_to_response_ex(request, "control_settings_user.html", data)
        users = b.getLogins()
        data["all_count"] = len(users)
        b.close()
        del b
        data = numerate(data, num=num, all_count=len(users))
        data["users"] = users[data["ind_start"]:data["ind_end"]]
        return render_to_response_ex(request, "control_settings_users.html", data)
    except:
        logging.exception("user_list "+str(sys.exc_info()))
        data["us_error"] = str(sys.exc_info())
        return render_to_response_ex(request, "control_settings_users.html", data)

class AddUserChangeForm(forms.Form):    
    fullname = forms.RegexField(label=u"Full name", max_length=64, regex=u'^[а-яА-ЯёЁ\w\s0-9.@+-s]+$',
        help_text = ("Может содержать только буквы, цифры и  @/./+/-/_ символы."),
        error_messages = {'invalid': ("Может содержать только буквы, цифры и  @/./+/-/_ символы.")})
    user = forms.CharField( max_length=30, label=u'Пользователь', required=False)
    login = forms.CharField( max_length=30, label=u'Логин', required=True)
    password1 = forms.CharField( max_length=30, label=u'Пароль', required=True)
    password2 = forms.CharField( max_length=30, label=u'Повтор пароля', required=True)

@tester
@permission_required('user_perms.perm_system_settings') 
def add_user(request):
    data = dict()
    data = getDefaultParams(request, 'control_settings_users', project)
    data["user"] = request.user
    data["page"] = "user"
    data["select_page"] = 'control_settings_users'
    data["password_wrong"] = False
    HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
    data["HOST"] = HOST
    data["PORT"] = PORT
            
    try:
        if "login" in request.REQUEST:
            b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
            users = b.getLogins()
            login_check = True
            for user in users:
                if str(user["login"]).lower() == str(request.REQUEST["login"]).lower():
                    login_check = False
            b.close()
            del b

            form = AddUserChangeForm(request.REQUEST, request.FILES)
            if form.is_valid() and login_check:
                if form.cleaned_data["password1"] != form.cleaned_data["password2"]: 
                    data["password_wrong"] = True
                else:                    
                    b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
                    full_name = form.cleaned_data["fullname"]
                    user = form.cleaned_data["user"]
                    login = form.cleaned_data["login"]
                    password = form.cleaned_data["password1"]
                    create = b.registration(login, password, user if user else USER, full_name)
                    b.close()
                    if create == True: return HttpResponseRedirect(reverse("user", args=[login]))
            else:
                if not login_check:
                    form._errors['login'] = ErrorList([u'Пользователь с таким логином уже существует'])
                data["errors"] = form.errors
    except:
        logging.exception("add_user "+str(sys.exc_info()))
    
    data["fullname"] = request.REQUEST["fullname"] if "fullname" in request.REQUEST else ""
    data["login"] = request.REQUEST["login"] if "login" in request.REQUEST else ""
    data["user"] = request.REQUEST["user"] if "user" in request.REQUEST else ""
    return render_to_response_ex(request, "control_settings_add_user.html", data)

class AddParamsForm(forms.Form):    
    param_name = forms.RegexField(label=u"Param name", max_length=64, regex=u'^[-\w0-9.]+$',
        help_text = ("Может содержать только буквы, цифры и '.'."),
        error_messages = {'invalid': ("Может содержать только буквы, цифры и  '.'.")}, 
        required=True)
    param_value0 = forms.CharField( max_length=255, label=u'Параметр значение', required=False)
    param_value1 = forms.BooleanField(label=u'Параметр значение', required=False)
    param_value2 = forms.FloatField(label=u'Параметр значение', required=False)
    param_info = forms.CharField( max_length=255, label=u'Параметр описание', required=False)
    max_val = forms.IntegerField(required=True)
    min_val = forms.IntegerField(required=True)
    step = forms.FloatField(required=True)
    type = forms.ChoiceField(choices=models.TYPES, required=True)
    base = forms.CharField(max_length=10, required=True)

@tester
@permission_required('user_perms.perm_system_settings') 
def add_param(request):
        HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        error_add = True
        try:
            form = AddParamsForm(request.POST, request.FILES)
            if form.is_valid():
                param_name = form.cleaned_data["param_name"]
                base = form.cleaned_data["base"]
                type = form.cleaned_data["type"]
                param_info = form.cleaned_data["param_info"]
                param_value = ""
                if type == "0" and "param_value0" in form.cleaned_data: param_value = form.cleaned_data["param_value0"]
                elif type == "1" and "param_value1" in form.cleaned_data: param_value = str(form.cleaned_data["param_value1"]).lower()
                elif type == "2" and "param_value2" in form.cleaned_data: param_value = form.cleaned_data["param_value2"]
                else: error_add = "Ошибка типа добавляемого параметра."                
                if base in ("system", "default") and error_add == True:
                    not_editable = get_NotEditable() 
                    if len(filter(lambda x: x["code"] == param_name, not_editable))==0:
                        if b.setParameter(value=param_value, param = param_name, toBase=base):
                            params =  models.Params.objects.filter(code=param_name)
                            if params.count()==0:
                                min_val = form.cleaned_data["min_val"]
                                max_val = form.cleaned_data["max_val"]
                                step = form.cleaned_data["step"]
                                models.Params.objects.create(code=param_name, name=param_info, type=int(type), step=step, min_val=str(min_val), max_val=str(max_val))
                        else: error_add = "Ошибка добавления параметра"           
                    else: error_add = "Параметр запрещен для редактирования"
                else: error_add = "Ошибка добавления параметра"                    
            else:
                s = ""
                for e in form.errors:
                    s += "error_%s;%s;" % (e, form.errors[e])
                error_add = s
        except:
            logging.exception("control_settings add new param "+str(sys.exc_info()))
            error_add = "Ошибка добавления параметра."
        b.close()
        return HttpResponse(str(error_add))

class DeleteParamsForm(forms.Form):    
    param_name = forms.RegexField(label=u"Param name", max_length=64, regex=u'^[-\w0-9.]+$',
        help_text = ("Может содержать только буквы, цифры и '.'."),
        error_messages = {'invalid': ("Может содержать только буквы, цифры и  '.'.")}, 
        required=True)
    base = forms.CharField(max_length=10, required=True)

@tester
@permission_required('user_perms.perm_system_settings') 
def delete_param(request):
    error_delete = False 
    try:           
        form = DeleteParamsForm(request.POST, request.FILES)
        if form.is_valid():
            HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
            params = b.getAllParameters()
            base = form.cleaned_data["base"]
            allparam = map(lambda x: x["params"], filter(lambda x: x["name"]==base, params))[0]
            param_name = form.cleaned_data["param_name"]
            allparam = map(lambda x: x["name"], filter(lambda x: x["name"].find(param_name)>=0, allparam))
            not_editable = get_NotEditable()
            for param in allparam:
                try:
                    if len(filter(lambda x: x["code"] == param, not_editable))==0:
                        b.deleteParameter(param=param, toBase=base)
                except:
                    logging.exception("b.deleteParameter %s %s" % (param, str(sys.exc_info())))
            b.close()
            #return render_to_response_ex(request, "control_settings_param.html", data)
            error_delete = True
    except:
        logging.exception("delete_params "+str(sys.exc_info()))
    return HttpResponse(str(error_delete))

class RenameParamsForm(forms.Form):    
    param_name = forms.RegexField(label=u"Param name", max_length=64, regex=u'^[-\w0-9.]+$',
        help_text = ("Может содержать только буквы, цифры и '.'."),
        error_messages = {'invalid': ("Может содержать только буквы, цифры и  '.'.")}, 
        required=True)
    new_param_name = forms.RegexField(label=u"New param name", max_length=64, regex=u'^[-\w0-9.]+$',
        help_text = ("Может содержать только буквы, цифры и '.'."),
        error_messages = {'invalid': ("Может содержать только буквы, цифры и  '.'.")}, 
        required=True)
    base = forms.CharField(max_length=10, required=True)

@tester
@permission_required('user_perms.perm_system_settings') 
def rename_param(request):
    error_delete = False 
    try:           
        form = RenameParamsForm(request.POST, request.FILES)
        if form.is_valid():
            HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
            params = b.getAllParameters()
            base = form.cleaned_data["base"]
            allparam = map(lambda x: x["params"], filter(lambda x: x["name"]==base, params))[0]
            param_name = form.cleaned_data["param_name"]
            new_param_name = form.cleaned_data["new_param_name"]
            allparam = map(lambda x: x["name"], filter(lambda x: x["name"].find(param_name)==0, allparam))
            i = 0
            not_editable = get_NotEditable()          
            for param in allparam:
                try:
                    new_param = param.replace(param_name, new_param_name)
                    if len(filter(lambda x: x["code"] in (param, new_param), not_editable))==0:
                        if b.renameParameter(param=param, new_param=new_param, toBase=base): 
                            i += 1
                            #models.Params.objects.filter(code=new_param).delete()
                            #models.Params.objects.filter(code=param).update(code=new_param)
                except:
                    logging.exception("b.renameParameter %s %s" % (param, str(sys.exc_info())))
            b.close()
            if i == 0:
                return HttpResponse("False")
            elif i<len(allparam): 
                return HttpResponse("Not all")
            else:
                return HttpResponse("True")
    except:
        logging.exception("rename_params "+str(sys.exc_info()))
    return HttpResponse(str(error_delete))

@tester
@permission_required('user_perms.perm_system_settings') 
def copy_param(request):
    error_delete = False 
    try:           
        form = RenameParamsForm(request.POST, request.FILES)
        if form.is_valid():
            HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
            params = b.getAllParameters()
            base = form.cleaned_data["base"]
            allparam = map(lambda x: x["params"], filter(lambda x: x["name"]==base, params))[0]
            param_name = form.cleaned_data["param_name"]
            new_param_name = form.cleaned_data["new_param_name"]
            allparam = map(lambda x: x, filter(lambda x: x["name"].find(param_name)>=0, allparam))
            i = 0
            not_editable = get_NotEditable()
            for param in allparam:
                try:
                    new_param=param["name"].replace(param_name, new_param_name)
                    if len(filter(lambda x: x["code"] == new_param, not_editable))==0:
                        if b.setParameter(value=param["val"], param = new_param, toBase=base):
                            i += 1
                        else:
                            error_add = "Ошибка добавления параметра." 
                    else:
                        error_add = "Параметр запрещен для изменения."                             
                except:
                    logging.exception("b.copyParameter %s %s" % (param, str(sys.exc_info())))
            b.close()
            if i == 0: return HttpResponse("False")
            elif i<len(allparam): return HttpResponse("Not all")
            else: return HttpResponse("True")
    except:
        logging.exception("copy_params "+str(sys.exc_info()))
    return HttpResponse(str(error_delete))


@tester
@permission_required('user_perms.perm_system_settings') 
def save_params(request):    
    post = request.POST
    base = False        
    try:
        if "base" in post and post["base"] in ("system", "default"): base = post["base"]
        if not base: return HttpResponse("False")
        HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        params = b.getAllParameters()
        allparam = map(lambda x: x["params"], filter(lambda x: x["name"]==base, params))
        if allparam: allparam = allparam[0]
        allparam = sorted(allparam, key=lambda x: x["name"])
        save = False
        if "save" in post and post["save"]=="1": save = True
        
        allparam = map(lambda x: get_fullinfo(x), allparam)
        if save and base:
            not_editable = get_NotEditable()
            for param in allparam:
                s = param["name"]
                if s in post and len(filter(lambda x: x["code"] == param["name"], not_editable))==0:
                    if str(post[s] if post[s] != "" else "None") != str(param["val"]):
                        posts = post[s]
                        if b.setParameter(value=posts, param=param["name"], toBase=base): param["val"] = posts
                        else: param["error"] = "ошибка параметра"
        else: return HttpResponse("False")         
    except:
        logging.exception("all_params "+str(sys.exc_info()))
        return HttpResponse("False")
    finally:
        if b:
            b.close()
            del b                        
    return HttpResponse("True")

@tester
@permission_required('user_perms.perm_system_settings') 
def all_params(request):    
    data = dict()
    data = getDefaultParams(request, 'control_settings_settings', project)
    data["select_page"] = 'control_settings_settings'
    data["user"] = request.user
    data["page"] = "settings"
    data["title"] = _("Общие настройки")
    data["number"] = config.number
    data["boolean"] = config.boolean
    data["text"] = config.text
    post = request.POST
    base = "system"    
    data["base"] = base
    data["max_length"] = config.max_text_width
    data["min_length"] = config.min_text_width
    data["val_length"] = config.text_length   
    try:
        HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
        data["HOST"] = HOST
        data["PORT"] = PORT
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        params = b.getAllParameters()
        
        allparam = map(lambda x: x["params"], filter(lambda x: x["name"]==base, params))
        if allparam: allparam = allparam[0]
        data["number"] = config.number
        data["boolean"] = config.boolean
        data["text"] = config.text
        allparam = sorted(allparam, key=lambda x: x["name"])
        allparam = map(lambda x: get_fullinfo(x), allparam)
        data["params"] = allparam
        if "update" in post: 
            return render_to_response_ex(request, "control_settings_param.html", data)
        data["params"] = allparam    
        #data["info"] = {"info": get_plist(request, allparam, "system")}        
    except:
        logging.exception("all_params "+str(sys.exc_info()))
        data["us_error"] = str(sys.exc_info())
    finally:
        try:
            if b:
                b.close()
                del b
        except: pass
    return render_to_response_ex(request, "control_settings_settings.html", data)

def get_fullinfo(obj, error=None):
            param = {"name": obj["name"], "val": obj["val"], "id":obj["name"], "error": error}
            param = get_params_value(param, obj["name"])          
            return param

def get_full_info(sparam, val, id, error):
            param = {"name": sparam, "val": val, "id":id, "error": error}
            param = get_params_value(param, sparam)
            return param

@tester
@permission_required('user_perms.perm_system_settings') 
def default_params(request):
    data = dict()
    data = getDefaultParams(request, 'control_settings_default', project)
    data["select_page"] = 'control_settings_default'
    data["user"] = request.user    
    data["page"] = "settings"
    data["title"] = _("Настройки по умолчанию")
    data["number"] = config.number
    data["boolean"] = config.boolean
    data["text"] = config.text
    post = request.POST
    base = "default"    
    data["base"] = base    
    data["max_length"] = config.max_text_width
    data["min_length"] = config.min_text_width
    data["val_length"] = config.text_length      
    try:
        HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
        data["HOST"] = HOST
        data["PORT"] = PORT    
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        """
        try:    
            if "add" in post: 
                form = AddParamsForm(post, request.FILES)
                if form.is_valid():
                    if not b.setParameter(value=form.cleaned_data["param_value"], param = form.cleaned_data["param_name"], toBase=base):
                        data["error_add"] = "Ошибка добавления параметра"
                        data["param_name"] = form.cleaned_data["param_name"]
                        data["param_value"] = form.cleaned_data["param_value"]
                else:
                    data["error_add"] = form.errors
        except:
            logging.exception("control_settings add new param "+str(sys.exc_info()))
            data["error_add"] = "Ошибка добавления параметра"    
        """
        params = b.getAllParameters()
        allparam = map(lambda x: x["params"], filter(lambda x: x["name"]==base, params))[0]
        allparam = sorted(allparam, key=lambda x: x["name"])
        #allparam = map(get_fullinfo, allparam)
       
        allparam = map(lambda x: get_fullinfo(x), allparam)
        data["params"] = allparam
        if "update" in post: 
            return render_to_response_ex(request, "control_settings_param.html", data) 
        #data["info"] = {"info": get_plist(request, allparam, "default")}
        b.close()
        del b
    except:
        logging.exception("default_params "+str(sys.exc_info()))
        data["us_error"] = str(sys.exc_info())
    return render_to_response_ex(request, "control_settings_settings.html", data)

@tester
@permission_required('user_perms.perm_system_settings') 
def rebootsystem(request):
    try:
        if config.script_reboot_system: 
            os.system(config.script_reboot_system)
            return HttpResponse(True)
        return HttpResponse(False)
    except: 
        logging.exception("rebootsystem "+str(sys.exc_info()))
        return HttpResponse(False)

@tester
@permission_required('user_perms.perm_system_settings') 
def export_settings(request):
    tarurl = ""
    response = ""
    filename = ""
    try:
        #from videoclient.settings import EXPORT_PATH, URL_EXPORT
        HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
        data = b.getAllParameters(return_xml=True)
        b.close()
        del b        
        #import tarfile
        #t = str(time.time())
#        fname = "%s/control_settings_%s" % (EXPORT_PATH, t)
        #tarname = "%s.tar.bz2" % (fname)
        #tar = tarfile.open(tarname, "w:bz2")
 #       filename = "%s.zip" % (fname)
  #      img = open(filename, "w+b")
   #     img.write(data)
    #    img.close()
        #tar.add(filename, str(t)+'.txt')
        #tar.close()
        #ftar = open(tarname, 'r+b')
        #datatar = ftar.read()
        #ftar.close()
        response = HttpResponse(data, content_type='text/plain')
        response['Content-Length'] = len(data)
        response['Content-Disposition'] = 'attachment;filename=settings.xml'
        #response['Content-Encoding'] = 'x-bzip2'        
        #os.unlink(filename)
        #os.unlink(tarname)
        #tarurl = "%s/control_settings_%s.zip" % (URL_EXPORT, t)
    except:
        logging.exception("export_settings "+str(sys.exc_info()))
        response = HttpResponse("", content_type='text/plain')
        response['Content-Length'] = len("")
        response['Content-Disposition'] = 'attachment;filename=settings.xml'
    return response

class TestImportFrom(forms.Form):
    importfile = forms.FileField(required=True)
        
    def save_images(self):
        file_field = self.files
        data = self.cleaned_data        
        name = "importfile"
        fn = "" 
        if name in data and data[name] and name in file_field and file_field[name]:
                #self.upload_image(data[name], compose_file_name(settings.FOTO_ROOT, login, proc, file_field[name]))
                fn = "%s/%s_%s" % (settings.EXPORT_PATH, str(time.time()), os.path.basename(str(file_field[name])))                 
                self.upload_image(data[name], fn)                           
                return fn
        return fn
            
    def upload_image(self, imgdata="", filename=""):        
        dist = open(filename, "w")
        for t in imgdata: dist.write(t)
        dist.close()
              

@tester
@permission_required('user_perms.perm_system_settings') 
def import_settings(request):
    
    try:
    #if True:
        from xml.dom.minidom import parseString
        form = TestImportFrom(request.POST, request.FILES)
        if form.is_valid():
            filename = form.save_images()
            if filename:
                img = open(filename, "r")
                data = img.read()
                img.close()
                os.unlink(filename)
                if data:
                    HOST, PORT, LOGIN, PASSWORD, USER = initBalancer()
                    b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
                    data = b.splitXmlParams(parseString(data))
                    params = b.getAllParameters()
                    not_editable = get_NotEditable()
                    for base in data:
                        for param in base["params"]:                           
                            if len(filter(lambda x: x["code"] == param["name"], not_editable))==0:
                                #logging.info("setParameter: %s %s" %(param["val"], param["name"]))
                                b.setParameter(value=param["val"], param = param["name"], toBase=base["name"])
                    for base in params:
                        f = filter(lambda x: x["name"] == base["name"], data)
                        del_param = len(f) == 0
                        for param in base["params"]:
                            if len(filter(lambda x: x["code"] == param["name"], not_editable))==0:
                                if not del_param:                                
                                    del_param = len(filter(lambda x: x["name"] == param["name"], f[0]["params"])) == 0
                                if del_param: b.deleteParameter(param=param["name"], toBase=base["name"])
                    return HttpResponse(True)
        return HttpResponse(False)     
    except:
        logging.exception("import_settings "+str(sys.exc_info()))
#    finally:
#        try:
#            if b:
#                b.close()
#                del b            
#        except: pass
    return HttpResponse(False)
    