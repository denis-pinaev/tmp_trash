#coding=utf-8

from django.http import Http404
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import permission_required
from django.template.loader import render_to_string 
from django.shortcuts import get_object_or_404
from django.db import connection, transaction
from django.db.models import Q
from django.template import Context, loader
import datetime
import time
import tempfile
import json
import tarfile
import zipfile
import urllib
import random
import commands
import uuid
import math
import re
import os
import sys

from videoarchive import models, settings, forms
from videoclient.settings import log_videoarchive as logging
from videoarchive.va import models as vaModels
from videoarchive.person import models as pModels
from videoarchive.archive import archive, utils as aUtils
from videoclient.communicator import models as comModels
from videoclient.communicator import Communicator
from videoclient.views import initBalancer
from videoclient.balancer import Balancer
from videoclient import models as vcModels, utils as cUtils
from videoclient import utils as vcUtils
from videoclient.settings import journalBoundCoeff
from videoarchive.templatetags import a_templatetags  


SVN_REVISION = '$Revision:1972 $'#######

VERSION_PREFIX = settings.VERSION_PREFIX
BRANCH = settings.BRANCH
REVISION = vcUtils.REVISION
VERSION = '%s.%s.%s' %(VERSION_PREFIX, BRANCH, REVISION)

ACTION_CHANGE = '_change'
ACTION_CREATE = '_create'
TASKS_PAGE = 'page_tasks'
USERS_PAGE = 'page_users'


def get_limits(limits=[[9], [12]]):
    """ Получение набора чисел элементов на странице.
    Чсло элементов зависит от разрешения страницы.
    """
    try:
        return limits[int(getParamFromBase(settings.RES_INTERFACE))]
    except:
        logging.exception("get_limits "+str(sys.exc_info()))
        return limits[0]

def getRevision(svn_revision):
    """ Получить номер ревизии """
    revision = 0
    m = re.match(r'[^0-9]*([0-9]+)[^0-9]*', svn_revision)
    if m and m.group(1): revision = m.group(1)
    return revision

def getDefaultParams(request, page=None):
    data = dict()
    data['login_user'] = request.user.username
    data['select_page'] = page
    data['all_weeks'] = models.Week.objects.all().order_by("number")
    
    now = datetime.datetime.now()
    data['now_hour'] = now.strftime('%H')
    data['now_minute'] = now.strftime('%M')
    data['now_second'] = now.strftime('%S')
    data['version'] = VERSION
    
    users = vcModels.User.objects.filter(id=request.user.id)
    if len(users) > 0:
        data['access'] = users[0].status.name
    
    request_params = []
    for r in request.REQUEST:
        request_params.append("%s=%s" %(r, request.REQUEST[r]))
    data['request_params'] = "&".join(request_params)
    data[settings.RES_INTERFACE] = getParamFromBase(settings.RES_INTERFACE)
    if settings.ARCHIVE_URL != "":
        data['root_path'] = '/%s' %settings.ARCHIVE_URL
    
    HOST, PORT, LOGIN, PASSWORD, USER, Error = initBalancer(True)                                                                                                                                                     
    if Error: data["balancer_need_configure"] = True    
    
    return data

def getParamFromBase(name):
    try:
        if name:
            if models.Settings.objects.filter(name = name).count()==1:
                params = models.Settings.objects.get(name = name)
                return params.value if params and params.value else 0
    except:
        logging.exception("getParamFromBase: "+ str(sys.exc_info())+" name: "+str(name))
    return 0

def getDays(request):
    result = ""
    week = models.Week.objects.all()
    for w in week:
        result += request.REQUEST.get(w.str_id, "")
    return result

def getCameraResolutions(request, id=0):
    data = dict()
    try: 
        if not id:
            form = forms.CheckIdForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data["id"]

        resol = getCameraResolution(int(id))
        if resol: 
                data['all_resolutions'] = models.Resolutions.objects.filter(width__lte=resol["max_width"], height__lte=resol["max_height"]).order_by("width", "height")
                data["width"] = resol["width"]
                data["height"] = resol["height"]
                data["camera_resolution"] = "%s*%s" % (resol["width"], resol["height"])                
        else: 
                resols = models.Resolutions.objects.all().order_by("width", "height")
                data['all_resolutions'] = resols
                if resols.count() > 0:
                    data["width"] = resols[0].width
                    data["height"] = resols[0].height
                    data["camera_resolution"] = "%s*%s" % (resols[0].width, resols[0].height)
                else:
                    data["width"] = 1280
                    data["height"] = 1024                    
        logging.info(data)
    except: 
        logging.info(sys.exc_info())
    return data

def getCameraResolution(id):
    resol = {}
    try:
       cam = comModels.Camera.objects.filter(id=id).exclude(type="IMPORT")       
       if cam.count() > 0:
            c = Communicator()
            resolution = c.getResolutionCamera(uuid=cam[0].uuid)            
            c.close()
            del c
            if resolution["success"]: resol = resolution["answer"]
    except:
        logging.info(sys.exc_info())
    return resol

@permission_required('user_perms.perm_videoarchive_add_task')
def getPageCopyTask(request, id = None):
    return getPageTask(request, id)

def changeTaskData(request, task=None, field_list=None):
    data = dict()
    if (request.REQUEST.has_key(ACTION_CHANGE) or request.REQUEST.has_key(ACTION_CREATE)) and request.user.has_perm("user_perms.perm_videoarchive_add_task"):
        user = None
        if request.REQUEST.has_key(ACTION_CHANGE):
            change = True
            user = task.user
            form = forms.TaskForm(request.REQUEST, instance = task)
        else:
            change = False            
            form = forms.TaskForm(request.REQUEST)
        data["errors"] = form.errors
        if form.is_valid():
            task = form.save(commit=False)
            task.days = getDays(request)
            if task.repeat_task:
                task.start_date = form.cleaned_data["repeat_start_date"]
                task.stop_date = form.cleaned_data["repeat_stop_date"]
                task.start_time = form.cleaned_data["repeat_start_time"]
                task.stop_time = form.cleaned_data["repeat_stop_time"]
            logging.info(change)
            if not change:
                users = vcModels.User.objects.filter(id=request.user.id)
                task.user = users[0] if users.count()>0 else None  
            else: task.user = user
            task.save()
            data['redirect'] = "/%s/" %TASKS_PAGE
            if settings.ARCHIVE_URL != "":
                data['redirect'] = "/%s/%s/" %(settings.ARCHIVE_URL, TASKS_PAGE)
            field_list_new = task.get_fields()
            change_filter = filter(lambda x: field_list[x]!=field_list_new[x] and x!="idtask", field_list)
            if change and task and task.process and len(change_filter) > 0:
                try:
                    if not task.repeat_task and (len(change_filter) == 1 and "stop_date" in change_filter or "stop_time" in change_filter) or ( len(change_filter) == 2 and "stop_date" in change_filter and "stop_time" in change_filter):
                        ContinueTaskWork(task, getTimestamp(task.stop_date, task.stop_time))
                    else: 
                        kill = killPrecesses(task.process.id)
                
                        va_servers, va_ports, videoarchives = aUtils.getVideoArchives()
                        if len(videoarchives)>0:
                            va = getWorkingArchive(videoarchives)
                            if va: process = startProcess(va, task)
                            va.close()
                            del va
                except:
                    logging.exception("getPageTask: "+str(sys.exc_info()))
        else:
            data['errors'] = form.errors
    return data

@permission_required('user_perms.perm_videoarchive_tasks')
def getPageTask(request, id = None):
    data = dict()
    task = None
    field_list = []
    if id:
        task = get_object_or_404(models.Tasks, id = int(id))
        field_list = task.get_fields()
        data['task'] = task
        """
        data['start_hour'] = task.start_time.strftime('%H')
        data['start_minute'] = task.start_time.strftime('%M')
        data['start_second'] = task.start_time.strftime('%S')
        data['stop_hour'] = task.stop_time.strftime('%H')
        data['stop_minute'] = task.stop_time.strftime('%M')
        data['stop_second'] = task.stop_time.strftime('%S')
        """
        data['delimiter_hour'] = int(task.video_delimiter/3600)
        data['delimiter_minute'] = int(task.video_delimiter%3600/60)
        data['delimiter_second'] = int(task.video_delimiter%60)
        data['fps'] = int(task.fps)
        data['gop'] = int(task.gop)
        data['compress'] = str(task.compress or vcUtils.get_value_defaultparams("compress")).replace(",", ".")
        data['bitrate'] = int(task.bitrate or vcUtils.get_value_defaultparams("bitrate"))
        data['blur'] = str(task.blur or vcUtils.get_value_defaultparams("blur")).replace(",", ".")
        data['duration'] = int(task.duration)
        data['duration_hour'] = int(task.duration)
        data['duration_minute'] = int(math.ceil(60*(task.duration-int(task.duration))))
        data['duration'] = str(task.duration).replace(",", ".")
        data['action'] = ACTION_CHANGE
    else:
        data['fps'] = 10
        data['gop'] = vcUtils.get_value_defaultparams("gop_size")
        data['compress'] = vcUtils.get_value_defaultparams("compress")
        data['bitrate'] = vcUtils.get_value_defaultparams("bitrate")
        data['blur'] = vcUtils.get_value_defaultparams("blur")
        data['duration'] = 1
        data['delimiter_hour'] = 1
        data['delimiter_minute'] = 0
        data['delimiter_second'] = 0
        date = datetime.datetime.now()
        data['start_hour'] = date.strftime('%H')
        data['start_minute'] = date.strftime('%M')
        data['start_second'] = date.strftime('%S')
        data['stop_hour'] = date.strftime('%H')
        data['stop_minute'] = date.strftime('%M')
        data['stop_second'] = date.strftime('%S')
        data['task'] = dict()
        data['action'] = ACTION_CREATE


    data.update(changeTaskData(request, task=task, field_list=field_list))

    #data['all_cameras'] = models.Cameras.objects.filter(archive__active = True)
    data['all_cameras'] = comModels.Camera.objects.filter(active=True).order_by('-available', 'delete', '-id').exclude(type="IMPORT")
    data['all_signals'] = models.Signals.objects.exclude(str_id__in = ("import", "sensor1"))
    data['all_resolutions'] = models.Resolutions.objects.all().order_by("width", "height")
    if task: 
        data["enother_resolution"] = models.Resolutions.objects.filter(name=task.resolution).count()==0
        data["width"], data["height"] = task.resolution.split("*")
    else: 
        data["camera_resolution"] = True
        if data['all_resolutions'].count()>0: data["width"], data["height"] = data['all_resolutions'][0].name.split("*")
    data['all_codecs'] = models.Codecs.objects.all()
    data['default_codec'] = settings.DEFAULT_VIDEOARCHIVE_VIDEO_CODEC
    data['all_repeats'] = models.REPEAT_DICT
    data['weeks'] = models.Week.objects.all().order_by("number")
    data['work_days'] = models.Week.objects.filter(is_work=True).order_by("number")
    data['not_work_days'] = models.Week.objects.filter(is_work=False).order_by("number")
    data["action_create"] = ACTION_CREATE
    return data

@permission_required('user_perms.perm_videoarchive_add_task')
def startTask(request, id=0):
    status = False
    try:
        tasks = models.Tasks.objects.filter(id=int(id))
        if tasks.count() == 0: return {"status": status}
        task = tasks[0]
        va_servers, va_ports, videoarchives = aUtils.getVideoArchives()
        if len(videoarchives) > 0:
           va = getWorkingArchive(videoarchives)
           if va: 
               status = startProcess(va, task)
               if status: 
                   tasks.update(last_kill_process=None)
           va.close()
           del va
    except:
        logging.error(sys.exc_info())
    return {"status": status}

@permission_required('user_perms.perm_videoarchive_tasks')
def getPageTasks(request):
    checkTasks()
    data = dict()
    all_tasks = models.Tasks.objects.all()
    for task in all_tasks:
        try:
            if task.process and task.process.id:
                id = task.process.id
        except vaModels.VaCommandRoller.DoesNotExist:
            task.process = None
            task.save()
    form = forms.CheckJournalSortForm(request.GET, request.FILES)
    if form.is_valid():         
        sort_arr = [["id"],
                    ["name"],
                    ["camera__ip", "camera__name"], 
                    ["repeat"],
                    ["interval", "start_date"],
                    ["interval", "stop_date"],
                    ["start_time"],
                    ["stop_time"],
                    ["dt_create"],
                    ["user__first_name", "user__last_name", "user__middle_name"],
                    ["signal__name"]]
        sort_id = form.cleaned_data["sort"]
        order = 1 if form.cleaned_data["order"] == 1 else 0
        data["sort"] = sort_id
        data["order"] = order
        if sort_id < len(sort_arr) and sort_id>=0:
            st = []
            for s in sort_arr[sort_id]: st.append("%s%s" % ("-" if order else "", s))
            if len(st)>2:
                tasks = models.Tasks.objects.filter(active=True).order_by(st[0], st[1], st[2])
            elif len(st)>1:
                tasks = models.Tasks.objects.filter(active=True).order_by(st[0], st[1])
            else:
                tasks = models.Tasks.objects.filter(active=True).order_by(st[0])
        else: tasks = models.Tasks.objects.filter(active=True).order_by('-id')
    else: tasks =  models.Tasks.objects.filter(active=True).order_by('-id')
    data['all_tasks'] = tasks.count()
    processes = getAllActiveProceses()
    processes_tasks = getProcesesTasks(processes)
    tasks_error = False
    stop_tasks = False
    data.update(getNavigation(request, tasks, 'tasks', navigation_title = _("Количество задач на странице")))
    for task in data['tasks']:
        if task.process and processes.has_key(str(task.process.id)):
            if task.process.tm_start <= datetime.datetime.now():
                setattr(task, "run", True)
        elif task.idtask in processes_tasks:
            setattr(task, "wait", True)
        elif task.last_kill_process and task.last_kill_process >= datetime.datetime.now().date():
            setattr(task, "stop", True)
            stop_tasks = True
        elif task.last_error and (not task.last_run or task.last_error > task.last_run):
            tasks_error = True
        elif (not task.repeat_task and getTimestamp(task.stop_date, task.stop_time)<datetime.datetime.now()) or (task.repeat_task and task.interval and getTimestamp(task.stop_date, task.stop_time)<datetime.datetime.now()):
            setattr(task, "time_error", True)
    data['tasks_error'] = tasks_error
    data['stop_tasks'] = stop_tasks
    return data

def getNavigation(request, data_list=None, name="", limits=[10, 20, 30, 40 ,50], get = [], navigation_title=None, len_data_list=0):
    data = dict()
    page = 1
    per_page = limits[0]
    form = forms.NavigationDataForm(request.REQUEST)
    if form.is_valid():
        page = form.cleaned_data.get("page", page) or page
        per_page = form.cleaned_data.get("per_page", limits[0]) or limits[0]
    if per_page<1:
        per_page = 1
    if data_list: len_data_list = len(data_list)
    #pages = len(data_list)/per_page + (1 if len(data_list)%per_page else 0)
    pages = len_data_list/per_page + (1 if len_data_list%per_page else 0)
    if page>pages or page<1:
        page=1
    
    start = (page-1) * per_page
    finish = page*per_page
    start_page = max(page-3, 1)
    finish_page = min(max(page+3, start_page+6), pages)
    start_page = max(min(page-3, finish_page-6), 1)
    pages_list = []
    i = start_page
    while i<=finish_page:
        pages_list.append(i)
        i=i+1    
        
    if per_page != limits[0]:
        data['per_page'] = per_page
    i = 0
    while i<len(limits):
        data["limit%s" %i] = limits[i] 
        i=i+1

    and_get = ''
    for g in get:
        and_get = "%s&%s=%s" %(and_get, g, get[g])        
        
    data['limits'] = limits
    data['page'] = page
    data['start'] = start
    data['finish'] = finish
    data['start_page'] = start_page
    data['finish_page'] = finish_page
    data['pages_list'] = pages_list
    data['pages'] = pages
    data['find_%s' %name] = len_data_list
    if data_list: data[name] = data_list[start:finish]
    else: data[name] = {}
    data['and_get'] = and_get
    data['navigation_title'] = navigation_title 
    
    return data

def getAllActiveProceses():
    processes = dict()
    try:
        va_servers, va_ports, videoarchives = aUtils.getVideoArchives()        
        for videoarchive in videoarchives:
            va = archive.Archive(videoarchive["host"], videoarchive["port"])
            va.open()
            if va.connect:
                ps = va.activeProcesses()
                if ps: processes.update(ps)
            va.close()
            del va
    except:
        logging.exception("getAllActiveProceses "+str(sys.exc_info()))        
    return processes

@permission_required('user_perms.perm_videoarchive_processes')
def getPageRecords(request):
    data = dict()
    
    checkTasks()
    
    a_processes = getAllActiveProceses()
    in_processes = '0'
    in_idtasks = "'0'"
    for a_process in a_processes:        
        if a_process == "0" and "idTask" in a_processes[a_process]: in_idtasks = "%s,'%s'" %(in_idtasks, a_processes[a_process]["idTask"])
        else: in_processes = '%s,%s' %(in_processes, a_process)
#    in_processes = in_processes+")"    
    form = forms.CheckJournalSortForm(request.GET, request.FILES)
    sort_str = "id desc"
    if form.is_valid():         
        sort_arr = [["id"],
                ["ip", "type"],
                ["signal_name"],
                ["va_start"],
                ["tm_stop"],
                ["roller_count"],
                ["task_name"],
               ]
        sort_id = form.cleaned_data["sort"]
        order = 1 if form.cleaned_data["order"] == 1 else 0
        data["sort"] = sort_id
        data["order"] = order    
        if sort_id < len(sort_arr) and sort_id>=0:
            sort_str = ""
            i = 0
            for s in sort_arr[sort_id]:
                sort_str = "%s %s %s" % ("%s," % (sort_str) if i>0 else "", s, "asc" if order else "desc")
                i += 1
    #sql = 'select va_commands.id as id, videoarchive_signals.name as signal_name, va_commands.tm_start as va_start, va_commands.tm_stop as tm_stop, count(va_rollers.id) as roller_count, communicator_camera.ip as ip, communicator_camera.type as type, va_t.name as task_name, va_t.id as task_id from va_commands left join videoarchive_taskscommandroller as va_tcr on va_commands.id=va_tcr.id_command_id left join videoarchive_tasks as va_t on va_t.id=va_tcr.id_task_id left join va_rollers on va_rollers.id_command = va_commands.id left join videoarchive_signals on videoarchive_signals.id = va_commands.id_signal, communicator_camera where va_commands.id in %s and va_commands.id_camera = communicator_camera.id group by va_commands.id, signal_name, va_commands.tm_start, va_commands.tm_stop, communicator_camera.ip, communicator_camera.type, va_t.name, va_t.id order by %s;' %(in_processes, sort_str)
    """
    sql = "select * from " 
    sql += " (select va_commands.id as id, videoarchive_signals.name as signal_name, va_commands.tm_start as va_start, va_commands.tm_stop as tm_stop, count(va_rollers.id) as roller_count, communicator_camera.id as cameraid, communicator_camera.ip as ip, communicator_camera.type as type, va_t.name as task_name, va_t.id as task_id, va_t.idtask as idtask from videoarchive_tasks as va_t left join videoarchive_taskscommandroller as va_tcr on va_t.id=va_tcr.id_task_id left join va_commands on va_commands.id=va_tcr.id_command_id left join va_rollers on va_rollers.id_command = va_commands.id left join videoarchive_signals on videoarchive_signals.id = va_t.signal_id left join communicator_camera on va_t.camera_id = communicator_camera.id where va_commands.id in (%(in_processes)s) group by va_commands.id, va_t.idtask, signal_name, va_commands.tm_start, va_commands.tm_stop, communicator_camera.ip, communicator_camera.type, va_t.name, va_t.id, idtask, cameraid ) as t1"
    if in_idtasks != "'0'":
        sql += " union"
        sql += " (select 0 as id, videoarchive_signals.name as signal_name, null as va_start, null as tm_stop, 0 as roller_count, communicator_camera.id as cameraid, communicator_camera.ip as ip, communicator_camera.type as type, va_t.name as task_name, va_t.id as task_id, va_t.idtask as idtask from videoarchive_tasks as va_t left join videoarchive_signals on videoarchive_signals.id = va_t.signal_id left join communicator_camera on va_t.camera_id = communicator_camera.id where va_t.idtask in (%(in_idtasks)s))  "
    sql += " order by %(sort_str)s;"  
    sql = sql %({"in_processes": in_processes, "sort_str": sort_str, "in_idtasks": in_idtasks})    
    """
    sql = "select * from " 
    sql += " (select va_commands.id as id, videoarchive_signals.name as signal_name, va_commands.tm_start as va_start, va_commands.tm_stop as tm_stop, count(va_rollers.id) as roller_count, communicator_camera.id as cameraid, communicator_camera.ip as ip, communicator_camera.type as type, communicator_camera.name as camera_name, va_t.name as task_name, va_t.id as task_id, va_t.idtask as idtask from va_commands left join videoarchive_taskscommandroller as va_tcr on va_commands.id=va_tcr.id_command_id left join videoarchive_tasks as va_t on va_t.id=va_tcr.id_task_id  left join va_rollers on va_rollers.id_command = va_commands.id left join videoarchive_signals on videoarchive_signals.id = va_commands.id_signal left join communicator_camera on va_commands.id_camera = communicator_camera.id where va_commands.id in (%(in_processes)s) group by va_commands.id, va_t.idtask, signal_name, va_commands.tm_start, va_commands.tm_stop, communicator_camera.ip, communicator_camera.type, camera_name, va_t.name, va_t.id, idtask, cameraid ) as t1"
    if in_idtasks != "'0'":
        sql += " union"
        sql += " (select 0 as id, videoarchive_signals.name as signal_name, null as va_start, null as tm_stop, 0 as roller_count, communicator_camera.id as cameraid, communicator_camera.ip as ip, communicator_camera.type as type, va_t.name as task_name, va_t.id as task_id, va_t.idtask as idtask from videoarchive_tasks as va_t left join videoarchive_signals on videoarchive_signals.id = va_t.signal_id left join communicator_camera on va_t.camera_id = communicator_camera.id where va_t.idtask in (%(in_idtasks)s))  "
    sql += " order by %(sort_str)s;"  
    sql = sql %({"in_processes": in_processes, "sort_str": sort_str, "in_idtasks": in_idtasks})    #processes = models.TasksCommandRoller.objects.filter(id_command__id__in=a_processes.keys()).extra(select={"roller_count": "count(va_rollerss.id)"}, tables=["va_rollerss"], where=["va_rollerss.id_command=va_commands.id) group by (videoarchive_taskscommandroller.id), (videoarchive_taskscommandroller.id_command_id), (videoarchive_taskscommandroller.id_task_id"], order_by=sort_arr[sort_id])
    processes = vaModels.VaCommandRoller.objects.raw(sql)
    processes = list(processes)
        
    #processes = models.TasksCommandRoller.objects.filter(id_command__id__in=a_processes.keys()).extra(select={"roller_count": "count(va_rollers.id)"}, tables=["va_roller"], where=["va_rollers.id_command=va_commands.id) group by (videoarchive_taskscommandroller.id), (videoarchive_taskscommandroller.id_command_id), (videoarchive_taskscommandroller.id_task_id"], order_by=sort_arr[sort_id])
    data["all_processes"] = len(processes)
#    data["processes"] = processes
    data.update(getNavigation(request=request, data_list=processes, name='processes', limits=[10, 20, 30, 40, 50], navigation_title = _("Количество процессов на странице")))
    for process in data["processes"]:
        if (str(process.id)) in a_processes:
            setattr(process, 'state', a_processes[str(process.id)]['state'])
        else:            
            l = filter(lambda x: "idTask" in a_processes[x] and a_processes[x]["idTask"]==process.idtask, a_processes)
            if len(l) > 0: setattr(process, 'state', a_processes[l[0]]['state'])
#    logging.info(processes)
#    tasks = models.Tasks.objects.filter(process__id__in = processes)
#    logging.info(tasks)
#    data["all_tasks"] = tasks.count()
#    data["tasks"] = tasks
#    for task in tasks:
#        logging.info("processes")
#        logging.info(processes)
#        logging.info(task.process.id)
#        logging.info(processes[str(task.process.id)]["state"])
#        setattr(task, "state", processes[str(task.process.id)]["state"])
    return data

@permission_required('user_perms.perm_videoarchive_journal')
def getPageJournal(request):
    data = dict()
    form = forms.CheckJournalSortForm(request.GET, request.FILES)
    sort_str = "va_commands.id desc"
    sort_arr = ["va_commands.id", 
                "va_commands.tm_start",
                "va_commands.tm_stop",
                "communicator_camera.name",
                "signal_name",                                         
                "roller_count",
                "task_name"
               ]
    if form.is_valid():        
        sort_id = form.cleaned_data["sort"]
        order = 1 if form.cleaned_data["order"] == 1 else 0
        data["sort"] = sort_id
        data["order"] = order       
        if sort_id < len(sort_arr) and sort_id>=0:
            sort_str = "%s %s" % (sort_arr[sort_id], "asc" if order else "desc")
    
    processes = vaModels.VaCommandRoller.objects.raw('select va_commands.id as id, va_commands.tm_start, va_commands.tm_stop, communicator_camera.name, videoarchive_signals.name as signal_name, sum(case when va_rollers.tm_stop is NULL then 0 else 1 end) as roller_count, sum(case when va_rollers.tm_stop is NULL then 1 else 0 end) as record_count, va_t.name as task_name from va_commands left join videoarchive_taskscommandroller as va_tcr on va_commands.id=va_tcr.id_command_id left join videoarchive_tasks as va_t on va_t.id=va_tcr.id_task_id left join va_rollers on va_rollers.id_command=va_commands.id join communicator_camera on va_commands.id_camera = communicator_camera.id left join videoarchive_signals on videoarchive_signals.id = va_commands.id_signal group by va_commands.id, va_commands.tm_start, va_commands.tm_stop, communicator_camera.name, signal_name, task_name order by %s;' % (sort_str))   
#    processes = vaModels.VaRoller.objects.raw('select va_commands.id as id, va_commands.tm_start, va_commands.tm_stop, communicator_camera.ip, communicator_camera.type, communicator_camera.name as camera_name, communicator_camera.id as camera_id, videoarchive_signals.name as signal_name, videoarchive_signals.id as signal_id, sum(case when va_rollers.tm_stop is NULL then 0 else 1 end) as roller_count, sum(case when va_rollers.tm_stop is NULL then 1 else 0 end) as record_count from va_commands left join va_rollers on va_rollers.id_command=va_commands.id join communicator_camera on va_commands.id_camera = communicator_camera.id left join videoarchive_signals on videoarchive_signals.id = va_commands.id_signal group by va_commands.id, va_commands.tm_start, va_commands.tm_stop, communicator_camera.ip, communicator_camera.type, camera_name, camera_id, signal_name, signal_id order by %s;' % (sort_str))
    logging.info(processes.query)
    processes = list(processes)
    data['all_processes'] = len(processes)
    data.update(getNavigation(request=request, data_list=processes, name='processes', limits=[10, 20, 30, 40, 50], navigation_title = _("Количество строк на странице")))
    a_processes = getAllActiveProceses()         
    for process in data['processes']:
        if a_processes.has_key(str(process.id)):
            setattr(process, 'state', a_processes[str(process.id)]['state'])
    now = datetime.datetime.now().strftime("%d.%m.%Y")
    data["date_from"] = now
    data["date_to"] = now 
    return data

def dataParams(str):
    data = dict()
    try:
        params = str.split(',')
        for param in params:
            name, value = param.split('=')
            data[name] = value
    except:
        logging.exception("dataParams "+str(sys.exc_info()))
    return data

def checkDataParamValue(value, arg):
    params = dataParams(value)
    if params.has_key(arg):
        return params[arg]
    else:
        return ""

def getDateForPageVideo(request, now=datetime.datetime.now()):
    form = forms.CheckPageVideoForm(request.REQUEST)
    if form.is_valid():
        date = form.cleaned_data["date"] 
    else:
        date = datetime.date(now.year, now.month, now.day)
    return date

def getConditionForPageVideo(request, params={}):
    #{"date": datetime.datetime.now().strftime("%Y-%m-%d")}
    if params.get("dateBegin"): params["dateBegin_s"] = params["dateBegin"].strftime("%Y-%m-%d")
    if params.get("dateEnd"): params["dateEnd_s"] = params["dateEnd"].strftime("%Y-%m-%d")
    if params.get("date"): params["date_s"] = params["date"].strftime("%Y-%m-%d")
    param_value = {"date_s": "DATE(va_rollers.tm_start)='%(p)s'",
                   "source": "communicator_camera.id='%(p)s'",
                   "cr": "va_rollers.id_command='%(p)s'",
                   "resol": "communicator_camera.id='%(p)s'",
                   "signal": "videoarchive_signals.id='%(p)s'",
                   "dateBegin_s": "DATE(va_rollers.tm_start)>='%(p)s'", 
                   "dateEnd_s": "DATE(va_rollers.tm_start)<='%(p)s'",
                   "signal_type": "videoarchive_signals.str_id='%(p)s'",
                  }
    if params.get("timeBegin", 0) and params.get("timeEnd", 0):
        if params["timeBegin"] < params["timeEnd"]:
            param_value["timeBegin"] = "(va_rollers.tm_start::time<='%(p)s' and va_rollers.tm_stop::time>='%(p)s' or va_rollers.tm_start::time>='%(p)s')" 
            param_value["timeEnd"] = "(va_rollers.tm_stop::time<='%(p)s' or va_rollers.tm_stop::time>='%(p)s' and va_rollers.tm_start::time<='%(p)s')"
        else:
            param_value["timeBegin"] = "(va_rollers.tm_start::time>='%(tbegin)s' and va_rollers.tm_stop::time<='23:59:59' or va_rollers.tm_start::time>='00:00:00' and va_rollers.tm_stop::time<='%(tend)s' or va_rollers.tm_start::time>='%(tbegin)s' and va_rollers.tm_stop::time<='%(tend)s')" % ({"tbegin": params["timeBegin"], "tend": params["timeEnd"]})  
    where = ""
    for p in params:
        if p in param_value:            
            where = "%s and %s" % (where, param_value[p] % ({"p": params[p]}))
    return where

def getCountRollersForPageVideo(where=""):
    query_count = "select count(*) from va_rollers join va_commands on va_rollers.id_command = va_commands.id left join videoarchive_signals on va_commands.id_signal = videoarchive_signals.id join va_archives on va_commands.id_archive = va_archives.id join communicator_camera on va_commands.id_camera = communicator_camera.id  where va_rollers.tm_stop is not NULL %s;" % (where)
    logging.info(query_count)
    cursor = connection.cursor()    
    cursor.execute(query_count)
    count = cursor.fetchall()[0][0]
    cursor.close()
    return count

def getRollersForPageVideo(where="", limit=""):
    query = "select va_rollers.id as id, va_rollers.tm_start as tm_start, va_rollers.tm_stop as tm_stop, case va_rollers.tm_start when va_rollers.tm_stop then 1 else extract(epoch FROM cast(va_rollers.tm_stop AS timestamp) - cast( va_rollers.tm_start AS timestamp)) end as dt_time, location, params, signal_type, videoarchive_signals.name as signal_name, va_archives.url as url, va_archives.ip as archive_ip, communicator_camera.ip as ip, communicator_camera.type as type, communicator_camera.id as camera_id from va_rollers join va_commands on va_rollers.id_command = va_commands.id left join videoarchive_signals on va_commands.id_signal = videoarchive_signals.id join va_archives on va_commands.id_archive = va_archives.id join communicator_camera on va_commands.id_camera = communicator_camera.id  where va_rollers.tm_stop is not NULL %s order by va_rollers.id desc %s;" % (where, limit)
    logging.info(query)
    rollers = vaModels.VaRoller.objects.raw(query)
    return rollers

def getCamerasForPageVideo(request, date = datetime.datetime.now()):
    cameras = comModels.Camera.objects.raw("select id_camera as id from va_rollers join va_commands on va_rollers.id_command = va_commands.id where DATE(va_rollers.tm_start) = '%s' group by va_commands.id_camera;" %(date.strftime("%Y-%m-%d")))
    return cameras

def getCamerasForPeriod(request, date1 = datetime.datetime.now(), date2 = datetime.datetime.now()):
    """ Выбор камер, с которых есть записи за указанный период дат """
    cameras = comModels.Camera.objects.raw("select id_camera as id from va_rollers join va_commands on va_rollers.id_command = va_commands.id where DATE(va_rollers.tm_start) >= '%s' and DATE(va_rollers.tm_start) <= '%s' group by va_commands.id_camera;"
                                           % (date1.strftime("%Y-%m-%d"), date2.strftime("%Y-%m-%d")))
    return cameras    
    
def getFilterVideo(request, date, type=None, limit=True):
    """ Выьбор данных с применение фильтров """
    form = forms.CheckRollerSearchForm(request.GET)
    data = dict()
    params = {}
    cd = {}
    if form.is_valid():
        cd = form.cleaned_data
        if int(cd.get("source", 0) or 0)>0: params["source"] = cd["source"]
        if "cr" in cd and cd["cr"] and int(cd["cr"])>0: params["cr"] = cd["cr"]
        if type: params["signal_type"] = type
        elif int(cd.get("signal", 0) or 0)>0: params["signal"] = cd["signal"]
        if "interval" in cd and cd["interval"] and int(cd["interval"])==1:
            params["interval"] = int(cd["interval"])
            logging.info("interval")
            logging.info(params["interval"])
            #if int(cd["interval"]) == 1:
            if "dateBegin" in cd and cd["dateBegin"]: params["dateBegin"] = cd["dateBegin"]
            if "dateEnd" in cd and cd["dateEnd"]: params["dateEnd"] = cd["dateEnd"]
        if "period_date" in cd and cd["period_date"] and int(cd["period_date"]) == 1:
                params["period_date"] = int(cd["period_date"])
            #if int(cd["period_date"]) == 1:
                if "hour1" in cd and "minute1" in cd and "second1" in cd and cd["hour1"]>=0 and cd["minute1"]>=0 and cd["second1"]>=0: 
                    params["timeBegin"] = "%02d:%02d:%02d" % (cd["hour1"], cd["minute1"], cd["second1"])
                    params["hour1"] = "%02d" % (cd["hour1"])
                    params["minute1"] = "%02d" % (cd["minute1"])
                    params["second1"] = "%02d" % (cd["second1"])
                if "hour2" in cd and "minute2" in cd and "second2" in cd and cd["hour1"]>=0 and cd["minute1"]>=0 and cd["second1"]>=0: 
                    params["timeEnd"] = "%02d:%02d:%02d" % (cd["hour2"], cd["minute2"], cd["second2"])
                    params["hour2"] = "%02d" % (cd["hour2"])
                    params["minute2"] = "%02d" % (cd["minute2"])
                    params["second2"] = "%02d" % (cd["second2"])
        if "date" in cd and cd["date"]: 
            params["dateBegin"] = date
            params["dateEnd"] = date
            params["interval"] = 1  
    else:
        params["date"] = date
        params["dateBegin"] = date
        params["dateEnd"] = date
        params["interval"] = 1      

    where = getConditionForPageVideo(request, params)
    query_limit = ""
    if limit:
        data['found_rollers'] = getCountRollersForPageVideo(where)
        limits = get_limits([[9, 15, 21, 30, 45], [12, 20, 32, 48, 64]])
        data.update(getNavigation(request, name='rollers', limits=limits, get = params,
                                  navigation_title = _("Количество видеороликов на странице"),
                                  len_data_list=data['found_rollers']))
        sstart = data.get("start", 0) or "0"
        slimit = data.get("per_page", limits[0]) or limits[0]
        query_limit = " limit %(limit)s offset %(start)s " % {"limit": slimit, "start": sstart}
        logging.info("limit="+str(query_limit))

    rollers = getRollersForPageVideo(where, query_limit)
    data["rollers"] = list(rollers)
    return rollers, params, cd, data

def getPageVideoInfo(request, type=None):
    data = dict()
    now = datetime.datetime.now()
    date = getDateForPageVideo(request, now)

    rollers, params, cd, data = getFilterVideo(request, date, type, True)
    and_get = params
    and_get_change = False

    #cameras = getCamerasForPageVideo(request, date)
    if "cr" in cd and cd["cr"] and int(cd["cr"])>0:
        croller = vaModels.VaCommandRoller.objects.filter(id=cd["cr"])
        if croller.count()>0:
            croller = croller[0]
            and_get = {"cr": croller.id}
            and_get_change = True
            params["dateBegin"] = croller.tm_start
            params["dateEnd"] = croller.tm_stop
            params["timeBegin"] = croller.tm_start.strftime("%H.%M.%S")
            params["timeEnd"] = croller.tm_stop.strftime("%H.%M.%S")
            params["interval"] = 1
            params["source"] = croller.id_camera.id
            params["signal"] = croller.id_signal
            params["period_date"] = 1
            params["hour1"] = "%02d" % (int(croller.tm_start.strftime("%H")))
            params["minute1"] = "%02d" % (int(croller.tm_start.strftime("%M")))
            params["second1"] = "%02d" % (int(croller.tm_start.strftime("%S")))
            params["hour2"] = "%02d" % (int(croller.tm_stop.strftime("%H")))
            params["minute2"] = "%02d" % (int(croller.tm_stop.strftime("%M")))
            params["second2"] = "%02d" % (int(croller.tm_stop.strftime("%S")))
    else:
        if "date" in cd and cd["date"]:
            date = cd["date"] 
            params["dateBegin"] = date
            params["dateEnd"] = date
            params["interval"] = 1
        else:
            if "interval" in cd and cd["interval"]==1:
                if "dateBegin" in cd and cd["dateBegin"]: params["dateBegin"] = cd["dateBegin"]
                if "dateEnd" in cd and cd["dateEnd"]: params["dateEnd"] = cd["dateEnd"]
        and_get = params
        and_get_change = True
        
    if params.get("dateBegin"): params["dateBegin"] = params["dateBegin"].strftime("%d.%m.%Y")
    if params.get("dateEnd"): params["dateEnd"] = params["dateEnd"].strftime("%d.%m.%Y")
    if params.get("date"): params["date"] = params["date"].strftime("%d.%m.%Y")

    if and_get_change:
        get = ''
        for g in and_get:
            get = "%s&%s=%s" %(get, g, and_get[g])
        data["and_get"] = get   
    
    data["params"] = params

    data['all_signals'] = models.Signals.objects.all()
    data['all_rollers'] = vaModels.VaRoller.objects.exclude(tm_stop = None).count()
#    data['all_signals'] = models.Signals.objects.exclude(str_id__in = ("import", "sensor1"))
    data['all_resolutions'] = models.Resolutions.objects.all().order_by("width", "height")
    data['all_codecs'] = models.Codecs.objects.all()
    data['default_codec'] = settings.DEFAULT_VIDEOARCHIVE_VIDEO_CODEC
    data["gop_size"] = vcUtils.get_value_defaultparams("gop_size")
    data['compress'] = vcUtils.get_value_defaultparams("compress")
    data['all_repeats'] = models.REPEAT_DICT
    data['fps'] = 10
    
    archives = vaModels.VaArchive.objects.all()
    if archives.count()>0:
        videoarchive = archives[random.randint(0, len(archives)-1)]
        data["videoarchive"] = videoarchive
    else: data["videoarchive"] = None    
    data['cameras'] = comModels.Camera.objects.filter(active=True)
    return data, rollers

@permission_required('user_perms.perm_videoarchive_videos')
def getPageVideo(request):
    data, rollers = getPageVideoInfo(request)
    return data

@permission_required('user_perms.perm_videoarchive')
def getPageAnalysis(request):
    data, rollers = getPageVideoInfo(request, type="import")
    import_id = models.Signals.objects.get(str_id="import").id
    data['all_rollers'] = vaModels.VaRoller.objects.filter(id_command__id_signal=import_id).exclude(tm_stop=None).count()
    data['not_show_import_signal'] = True
    return data

@permission_required('user_perms.perm_videoarchive_videos')
def getVideoCountFace(request, id=None):
    count_face = 0
    count_person = 0
    try:
        k_cs = vcUtils.get_value_defaultparams(journalBoundCoeff)
        r = vaModels.VaRoller.objects.get(id=id)
        count_face = vaModels.VaPersonsFrame.objects.filter(id_archive=r.id_command.id_archive.id, id_camera=r.id_command.id_camera.id, tm_dt__gte=r.tm_start, tm_dt__lte=r.tm_stop).count()
        count_person = vaModels.VaPersonsFrame.objects.filter(id_archive=r.id_command.id_archive.id, id_camera=r.id_command.id_camera.id, tm_dt__gte=r.tm_start, tm_dt__lte=r.tm_stop, k_cs__gte=k_cs).count()
        return {"status": True, "count_faces": count_face, "count_persons": count_person}
    except:
        logging.exception(sys.exc_info())
    return {"status": False, "count_faces": count_face, "count_persons": count_person}

@permission_required('user_perms.perm_videoarchive_videos')
def getPageViewVideo(request, id=None):
    data = dict()
    if not id:
        raise Http404
    
    count_face = None
    roller = get_object_or_404(vaModels.VaRoller, id = int(id))
    camera = get_object_or_404(comModels.Camera, id = int(roller.id_command.id_camera.id))
    
    if roller:
        count_face = int(checkDataParamValue(roller.params, "fcs"))
#    va_servers, va_ports, videoarchives = aUtils.getVideoArchives(roller.id_command.id_archive)
#    videoarchive = videoarchives[0]
#    va = archive.Archive(videoarchive["host"], videoarchive["port"])
#    va.flv(id=id)
#    va.close()
#    del va
    
    data['roller'] = roller
    data['camera'] = camera
    data["count_face"] = count_face
    #data['frames_count'] = vaModels.VaFramesRoller.objects.filter(id_roller=int(id)).count()
    
    return data

def getDetailVideo(id=None):
    try:    
        if not id: return False    
        journal = vcModels.Journal.objects.get(id = int(id))        
        camera = journal.camera
        delta_seconds = 15 
        #frames = vaModels.VaPersonsFrame.objects.filter(id_camera=camera.id, tm_dt__range=(journal.dt_first_fixed-datetime.timedelta(seconds=delta_seconds), journal.dt_first_fixed+datetime.timedelta(seconds=delta_seconds)))
        #if frames.count() > 0:
        rollers = vaModels.VaRoller.objects.filter(id_command__id_camera=camera, tm_start__lte=journal.dt_first_fixed, tm_stop__gte=journal.dt_first_fixed).order_by("-tm_start", "-tm_stop")
        if rollers.count() > 0: return rollers[0].id
    except:
        logging.exception("getDetailVideo: "+str(sys.exc_info()))
    return False

@permission_required('user_perms.perm_videoarchive_videos')
def getPageViewDetailVideo(request, id=None):
    data = dict()
    if not id:
        raise Http404
    
    journal = get_object_or_404(vcModels.Journal, id = int(id))    
    camera = journal.camera
    
    params = {"camera_id": camera.id, "dt_first": journal.dt_first_fixed, "dt_last": journal.dt_last_fixed}
    rollers = list(vaModels.VaRoller.objects.raw("select va_r.id, case when va_r.tm_stop>'%(dt_last)s' then extract(epoch FROM cast(va_r.tm_stop AS timestamp)-cast('%(dt_last)s' AS timestamp)) else 0 end as df_stop, extract(epoch FROM cast('%(dt_first)s' AS timestamp)-cast(va_r.tm_start AS timestamp)) as df_start from va_rollers as va_r inner join va_commands as va_cr on va_r.id_command=va_cr.id and va_cr.id_camera=%(camera_id)s where va_r.tm_start<'%(dt_first)s' and (va_r.tm_stop>='%(dt_last)s' or (va_r.tm_stop<'%(dt_last)s' and va_r.tm_stop>='%(dt_first)s')) order by df_start desc, df_stop desc limit 1" % (params))) 
#    rollers = list(vaModels.VaRoller.objects.raw("select va_r.id, if(va_r.tm_stop>'%(dt_last)s', timestampdiff(second, va_r.tm_stop, '%(dt_last)s'), 0) as df_stop, timestampdiff(second, va_r.tm_start, '%(dt_first)s') as df_start from va_rollers as va_r inner join va_commands as va_cr on va_r.id_command=va_cr.id and va_cr.id_camera=%(camera_id)s where va_r.tm_start<'%(dt_first)s' and (va_r.tm_stop>='%(dt_last)s' or (va_r.tm_stop<'%(dt_last)s' and va_r.tm_stop>='%(dt_first)s')) order by df_start desc, df_stop desc limit 1" % (params)))
    if len(rollers) > 0:
        roller = rollers[0]
        data['roller'] = roller            
        data['camera'] = camera
        delta_seconds = 5
        tm = (time.mktime(journal.dt_first_fixed.timetuple())-time.mktime(roller.tm_start.timetuple())-delta_seconds)
        data['start_time'] = str(tm).replace(",", ".")
    
    return data

def getNamePersonByBalName(name):
    try:
        id = int(name)
        if pModels.Person.objects.filter(id = int(id)).count() != 1:
            return name
        person = pModels.Person.objects.get(bal_id = int(id))
        if not person: return name
        
        person_name = person.first_name if person.first_name else ""
        person_name = person_name + (" " if len(person_name)>0 and person.last_name else "") + (person.last_name if person.last_name else "")
        person_name = person_name + (" " if len(person_name)>0 and person.middle_name else "") + (person.middle_name if person.middle_name else "")
        return person_name
    except:
        logging.exception("getNamePersonByBalName: "+str(sys.exc_info()))
    return name

def getRollerInfo(roller):
    try:        
        camera = roller.id_command.id_camera        
        params = ["%s %s %s %s %s" % (roller.tm_start.strftime("%d.%m.%Y"), _("с"), roller.tm_start.strftime("%H:%M:%S"), _("до"), roller.tm_stop.strftime("%H:%M:%S")),
                  "%s: %s %s" % (_("Источник"), camera.ip, camera.type),
                  "%s: %s" % (_("Запуск задачи"), a_templatetags.sygnal_name(roller.id_command.signal_type)),
                  "%s: %s %s" % (_("Частота кадров"), checkDataParamValue(roller.params, "fps"), _("кадр/сек")),
                  "%s: %s %s" % (_("Размер"), round(a_templatetags.fdiv(a_templatetags.fdiv(checkDataParamValue(roller.params, "sz"), 1024), 1024), 3), _("Мб")),
                  "%s: %s" % (_("Формат"), checkDataParamValue(roller.params, "fmt")),  
                  "%s: %sx%s" % (_("Разрешение"), checkDataParamValue(roller.params, "w"), checkDataParamValue(roller.params, "h")),
               ]
        return  ". ".join(params)
    except:
        logging.exception("getRollerInfo: "+str(sys.exc_info()))
    return ""

def getBalPersons():
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        
    try:
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        ids, names, photos = b.getPersons()
        b.close()
        del b
        return ids, names
    except:
        logging.exception("getBalNameById, getPerson: " + str(sys.exc_info()))
    return [], []

def getNamePersonByBalIds(id, balIds, balNames):
    try:
        p = vcModels.PersonId.objects.filter(bal_id=int(id))
        if p.count() == 1: person = p[0].person
        else:
            person = None
            if id in balIds:
                p = vcModels.PersonId.objects.filter(id=int(balNames[balIds.index(id)]))
                if p.count() == 1:
                    personId = p[0]
                    personId.bal_id = int(id)
                    personId.save()
                    person = personId.person
        if person is not None:
            person_name = person.first_name if person.first_name else ""
            person_name = person_name + (" " if len(person_name) > 0 and person.last_name else "") + (person.last_name if person.last_name else "")
            person_name = person_name + (" " if len(person_name) > 0 and person.middle_name else "") + (person.middle_name if person.middle_name else "")
            return person_name
    except:
        logging.exception("getNamePersonByBalIds: " + str(sys.exc_info()))
    return ""

@permission_required('user_perms.perm_videoarchive_videos')
def getRollerData(request):
 try:
    data = dict()
    form = forms.RollerDataForm(request.REQUEST)
    if not form.is_valid():
        data["errors"] = form.errors
        logging.info("getRollerData: "+str(form.errors))
        return data
    id = form.cleaned_data['id']
    #sql = 'select * from (select id_frame, num from va_frames_roller t1 where t1.id_roller = %d and t1.num>=%d and t1.num<%d) s1 join  va_frame_info t2 on s1.id_frame = t2.id_frame join va_frame t3 on s1.id_frame = t3.id;' %(id, frame, frame+count)
#    sql = 'select * from va_rollers, va_frame_info, va_commands where va_rollers.id = %d and va_rollers.id_command = va_commands.id and va_commands.id_camera = va_frame_info.id_camera and va_rollers.tm_start <= va_frame_info.tm_dt and va_frame_info.tm_dt <= va_rollers.tm_stop;' %(id)
    sql = 'select va_rollers.id as id, * from va_rollers inner join  va_commands on  va_rollers.id_command = va_commands.id inner join va_frame_info on va_commands.id_camera = va_frame_info.id_camera where va_rollers.id = %d and va_rollers.tm_start <= va_frame_info.tm_dt and va_frame_info.tm_dt <= va_rollers.tm_stop order by tm_dt;' %(id)
    raw_rollers = list(vaModels.VaRoller.objects.raw(sql))
    rollers = []
    fio_cs = {}
    id_cs = {}
    k_cs = float(vcUtils.get_value_defaultparams(journalBoundCoeff))
    if len(raw_rollers) > 0:
        balIds, balNames = getBalPersons()
        for raw_roller in raw_rollers:
            try:
                roller = dict()
                if raw_roller.location_photo: roller["location_photo"] = raw_roller.location_photo
                if raw_roller.id_cs: roller["id_cs"] = raw_roller.id_cs
                try:
                    if raw_roller.k_cs and float(raw_roller.k_cs) >= k_cs:
                        roller["k_cs"] = raw_roller.k_cs
                        if raw_roller.fio_cs:
                            if not raw_roller.fio_cs in fio_cs: fio_cs[raw_roller.fio_cs] = getNamePersonByBalName(raw_roller.fio_cs) 
                            roller["fio_cs"] = fio_cs[raw_roller.fio_cs]
                        elif raw_roller.id_cs:
                            if not raw_roller.id_cs in id_cs: id_cs[raw_roller.id_cs] = getNamePersonByBalIds(int(raw_roller.id_cs), balIds, balNames)
                            roller["fio_cs"] = id_cs[raw_roller.id_cs]
                        if raw_roller.photo_cs: roller["photo_cs"] = raw_roller.photo_cs
                except:
                    logging.exception(str(sys.exc_info()))
                if raw_roller.face: roller["face"] = raw_roller.face
                if raw_roller.id_like: roller["id_like"] = raw_roller.id_like
                if raw_roller.tm_dt: roller["tm"] = raw_roller.tm_dt.strftime("%Y%m%d%H%M%S")
                if raw_roller.tm_ms: roller["tm"] = "%s%04d" % (roller["tm"], int(raw_roller.tm_ms))
                if raw_roller.w: roller["width"] = raw_roller.w
                if raw_roller.h: roller["height"] = raw_roller.h
                rollers.append(roller)
            except:
                logging.exception(str(sys.exc_info()))
    data["frames"] = rollers
    roller = vaModels.VaRoller.objects.get(id = id)
    data["params"] = roller.params
    data["source"] = "%sfiles/video%s" % (roller.id_command.id_archive.url, roller.location)
    data["info"] = getRollerInfo(roller)
    data["tm_start"] = roller.tm_start.strftime("%Y%m%d%H%M%S")
    data["ms_start"] = roller.ms_start
 except:
     logging.exception("getRollerData: "+str(sys.exc_info()))
 return data

@permission_required('user_perms.perm_videoarchive_videos')
def getRollersData(request):
    data = dict()
    try:
        form = forms.RollerDataForm(request.REQUEST)
        if not form.is_valid():
            data["errors"] = form.errors
            logging.info("getRollersData: "+str(form.errors))
            return data
        id = form.cleaned_data['id']
        roller = vaModels.VaRoller.objects.get(id=id)
        if roller and models.Signals.objects.get(str_id == "import").id == roller.id_command.id_signal:
            rollers = vaModels.VaRoller.objects.filter(id_command__id_camera=roller.id_command.id_camera).order_by("tm_start")
        else:
            task = models.TasksCommandRoller.objects.get(id_command=roller.id_command)
            if not task: return data
            condition = "videoarchive_taskscommandroller.id_command_id=va_rollers.id_command and videoarchive_taskscommandroller.id_task_id=%s and va_rollers.tm_stop is not null " % (task.id_task.id)
            rollers = vaModels.VaRoller.objects.extra(tables=["videoarchive_taskscommandroller"], where=[condition], order_by=["tm_start"])
        d = []
        for roller in rollers:
            d.append({"start_time": roller.tm_start.strftime("%Y%m%d%H%M%S"), 
                      "duration": (roller.tm_stop-roller.tm_start).seconds, 
                      "id": roller.id,
                      "face_count": checkDataParamValue(roller.params, "fcs"),
                      "person_count": checkDataParamValue(roller.params, "pcs"),})
        data["rollers"] = d
    except:
        logging.exception("getRollersData: "+str(sys.exc_info()))
    return data

@permission_required('user_perms.perm_videoarchive_videos')
def getRollerUrl(request):
    data = dict()
    try:
        form = forms.RollerDataForm(request.REQUEST)
        if not form.is_valid():
            data["errors"] = form.errors            
            return data
        id = form.cleaned_data['id']
        logging.info(id)
        roller = vaModels.VaRoller.objects.get(id=id)
        if roller: data["url"] = "%sfiles/video%s" % (roller.id_command.id_archive.url, roller.location)
    except:
        logging.exception("getRollersData: "+str(sys.exc_info()))
    return data

def killPrecesses(id):
    try:
        process = get_object_or_404(vaModels.VaCommandRoller, id = int(id))
        archi = get_object_or_404(vaModels.VaArchive, id = int(process.id_archive.id))
        camera = get_object_or_404(comModels.Camera, id = process.id_camera.id)
        
        va_servers, va_ports, videoarchives = aUtils.getVideoArchives(archi)
        videoarchive = videoarchives[0]
        va = archive.Archive(videoarchive["host"], videoarchive["port"])
        status = va.stopProcess(uuid=camera.uuid, params=[{"name":"id", "value":id}])
        va.close()
        del va
        
        if status:
            tasks = models.Tasks.objects.filter(process = process)
            if tasks.count()>0:
                task = tasks[0]
                task.last_kill_process = datetime.datetime.now()
                task.save()
        return status
    except:
        logging.exception('killProcess: '+str(sys.exc_info()))
    return False

@permission_required('user_perms.perm_videoarchive_stop_process')
def getKillProcessesData(request, id):
    data = dict()
    if not id:
        raise Http404
    data["status"] = killPrecesses(id)
    return data

def chackActiveProcesses(request, id):
    try:
        processes = getAllActiveProceses()
        logging.info(processes)
        return processes.has_key(id)
    except:
        return "Error"

# Получение работающих видеоархивов
def getWorkingArchive(videoarchives):
    try:
        while len(videoarchives)>0:
            i = random.randint(0, len(videoarchives)-1)
            videoarchive = videoarchives[i]
            va = archive.Archive(videoarchive["host"], videoarchive["port"])
            va.open()
            if va.connect: return va
            del va
            del videoarchives[i]
    except:
        logging.error(sys.exc_info())
    return False

"""
# Получение работающих видеоархивов для указанной камеры
def getArchive(camera):
    import random
    videoarchives = comModels.ArchiveCommunicator.objects.filter(id_communicator__active=True).extra(tables=["communicator_vacameracommunicator"], where=["communicator_vacameracommunicator.id_communicator_id=communicator_archivecommunicator.id_communicator_id and communicator_vacameracommunicator.id_camera_id=%i" % (camera.id)])
    try:
        while len(videoarchives)>0:
            i = random.randint(0, len(videoarchives)-1)
            videoarchive = videoarchives[i]
            logging.info(videoarchive)
            va = archive.Archive(videoarchive.id_archive.ip, videoarchive.id_archive.port)
            va.open()
            if va.connect: return va, videoarchive.id_communicator
            del va
            del videoarchives[i]
    except:
        logging.error(sys.exc_info())
    return False, None
"""

# Получение управляющей системы для указанной камеры
def getControlSystem(camera):     
    try:
        communicator = getCommunicator(camera)
        if communicator:
            cs = vcModels.Balancer.objects.filter(host=communicator.host, active=True)
            if cs.count()>0: return cs[0]            
        cs = vcModels.Balancer.objects.filter(active=True)
        if cs.count()>0: return cs[0]
    except:
        logging.error(sys.exc_info())
    return None

# Получение комуникаторов для указанной камеры
def getCommunicator(camera):
    communicators = comModels.Camera.objects.filter(commun__active=True, id=camera.id)
    try:
        if len(communicators) > 0:           
            return communicators[0].commun
    except:
        logging.error(sys.exc_info())
    return None

def getActiveProceses(videoarchives):
    processes = dict()
    v = []
    try:       
        i = 0        
        for videoarchive in videoarchives:
            try:            
                va = archive.Archive(videoarchive["host"], videoarchive["port"])
                va.open()
                if va.connect:
                    ps = va.activeProcesses()
                    if ps != False: 
                        processes.update(ps)
                        v.append(videoarchive)
                va.close()
                del va
            except:
                logging.exception("get_ActiveProceses "+str(sys.exc_info()))
            i += 1
    except:
        logging.exception("getActiveProceses "+str(sys.exc_info()))
    return processes, v

def getTimestamp(dt, tm):
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime('%s %s' % (dt.strftime("%Y.%m.%d"), tm), "%Y.%m.%d %H:%M:%S")))

def getProcesesTasks(processes):
     return map(lambda x: "idTask" in processes[x] and str(processes[x]["idTask"]) or "0", processes)

def getTaskProcessDateStart(task, now, next=False):    
    dt_start = now - datetime.timedelta(hours=getDuration(task))
    s_date = now
    work_days = map(lambda x: x["number"], models.Week.objects.filter(is_work=True).values("number"))
    not_work_days = map(lambda x: x["number"], models.Week.objects.filter(is_work=False).values("number"))
    rep_dict = models.REPEAT_DICT
    while (dt_start <= s_date):
         day_number = s_date.date().weekday()+1
         if task.repeat in (rep_dict['every'], rep_dict["always"]) or (rep_dict['work']==task.repeat and day_number in work_days) or (rep_dict['week_end']==task.repeat and day_number in not_work_days) or (rep_dict['days']==task.repeat and task.days.find(str(day_number))>=0):
             tm = getTimestamp(s_date, task.start_time)
             logging.info(str(tm)+" "+str(now)+" "+str(next))
             if tm <= now or next: return tm
         s_date = s_date - datetime.timedelta(days=1)            
         s_date = max(s_date, getTimestamp(s_date, task.start_time))
    return None

def startProcess(va, task, now=datetime.datetime.now(), dt_start=None, dt_stop=None):
    try:
        logging.info(dt_stop)
        if not dt_stop or not dt_start:
            dt_start = getTaskProcessDateStart(task, now) 
            dt_stop = getTimestamp(dt_start+datetime.timedelta(hours=getDuration(task)), task.stop_time)
        logging.info("min "+str(dt_stop)+" "+str(getTimestamp(task.stop_date, task.stop_time)))
        if task.interval: dt_stop = min(getTimestamp(task.stop_date, task.stop_time), dt_stop)
        logging.info(dt_stop)
        dt_start = max(now, dt_start)
        logging.info(dt_start)
        logging.info(dt_stop)
        #comm = getCommunicator(task.camera)
        #if not comm: return False
        comm = task.camera.commun        
        if not task.idtask:
            task.idtask = models.get_task_code()
            task.save()
        size = task.resolution
        size = size.split("*")
        #(now.strftime("%Y%m%d")+(task.start_time.strftime("%H%M%S") if task.start_time else "000000"))
        params = [{"name":"interval", "value":task.video_delimiter},
              {"name":"tmStart", "value":dt_start.strftime("%Y%m%d%H%M%S")},
              {"name": "tmStop", "value":dt_stop.strftime("%Y%m%d%H%M%S")},
              {"name":"fps", "value":task.fps},
              {"name":"width", "value":size[0]},
              {"name":"height", "value":size[1]},
              {"name":"codec", "value":task.codec.number}, # Добавлен кодек, указанный в задаче.
              {"name":"gopSize", "value":task.gop}, # Добавлена частота ключевых кадров, указанная в задаче.
              #{"name":"compress", "value":task.compress}, # Степень сжатия кадров
              #{"name":"bitrate", "value":task.bitrate}, # Пропускная способность при записи видеоролика
              #{"name":"blur", "value":task.blur}, # Коэффициент сглаживания изображения
              {"name":"idTask", "value":task.idtask}, # Код задачи
              {"name":"com_ip", "value":comm.host}, # адрес коммуникатора
              {"name":"com_port", "value":comm.port}, # порт коммуникатора              
             ]
        logging.info(params)
        """
        if task.duration < 24 or task.interval:
            if task.stop_time:
                if task.duration == 24:
                    tmstop = task.stop_date.strftime("%Y%m%d") + task.start_time.strftime("%H%M%S")
                else:
                    tmstop = (now if task.start_time and task.stop_time>task.start_time else now+datetime.timedelta(days=1)).strftime("%Y%m%d") + task.stop_time.strftime("%H%M%S")
                #(now + datetime.timedelta(hours=task.duration)).strftime("%Y%m%d%H%M%S")
                #(now if task.start_time and task.stop_time >= task.start_time else now+datetime.timedelta(days=1)).strftime("%Y%m%d") + task.stop_time.strftime("%H%M%S")
            else:
                tmstop = now.strftime("%Y%m%d")+"235959"
            params.append({"name":"tmStop", "value":tmstop})
        """    
        process =  va.startProcess(uuid = task.camera.uuid, signal = task.signal.short_name, signal_id = task.signal.id, params = params)
        logging.info('process: '+str(process))
        if int(process)>0:
            logging.info('process: '+str(process))
            p = vaModels.VaCommandRoller(id=int(process))
            logging.info('p: '+str(p))
            task.process = p
            task.last_run = datetime.datetime.now()
            task.save()
            models.TasksCommandRoller.objects.get_or_create(id_task=task, id_command=p)
            logging.info('task: '+str(task))
        else:
            task.last_error = datetime.datetime.now()
            task.error = int(process)
            task.save()
        return True
    except:
        logging.exception("startProcess "+str(sys.exc_info()))
    return False

def getDuration(task):
    logging.info(str(task.duration_type)+" "+str(task.duration))
    if task.duration_type == 0: return task.duration/60
    elif task.duration_type == 2: return task.duration*24
    else: return task.duration        

def ContinueTaskWork(task, dt_stop):
    logging.info("Continue!!!")
    status = False
    va = archive.Archive(task.process.id_archive.ip, task.process.id_archive.port)
    if va:
        status = va.stopProcess(ip=task.camera.uuid, params=[{"name":"id", "value":task.process.id}, {"name": "tmStop", "value": dt_stop}])
    va.close()
    del va
    return status    

def checkTasks():
        
    delay = datetime.timedelta(seconds=int(getParamFromBase(settings.CRON_DELAY_FOR_PROCESS)))
    
    now = datetime.datetime.now()
    
    stop_date = now
    stop_time = stop_date.time()
    
    start_date = now+delay
    start_time = start_date.time()
   
    weekday = str(datetime.date.today().weekday()+1)
    logging.info(weekday)
    
    query_params = {"stop_date": stop_date.strftime("%Y-%m-%d"), "start_date": start_date.strftime("%Y-%m-%d"), "stop_time": stop_time.strftime("%H:%M:%S"), 
                    "start_time": start_time.strftime("%H:%M:%S")}

    query  = "select * from videoarchive_tasks as tsk where "
    query += "(last_kill_process is NULL or last_kill_process < '%(start_date)s') and "
    query += "active=true and (start_date <= '%(start_date)s' and ((repeat_task and ((interval and stop_date >= '%(stop_date)s') or not interval)) or "
    query += "(not repeat_task and stop_date >= '%(stop_date)s'))) "
     
    query = query % query_params     
    logging.info(query)
    tasks = models.Tasks.objects.raw(query)
    logging.info("tasks time Interval: "+ str(len(list(tasks))))
         
    va_servers, va_ports, videoarchives = aUtils.getVideoArchives()
    if len(videoarchives)<1: return False

    processes, videoarchives = getActiveProceses(videoarchives)
    processes_tasks = getProcesesTasks(processes)
    logging.info("AllActiveProceses")
    logging.info(len(videoarchives))
    logging.info(processes)
    if len(videoarchives)<1: return False
    
    day_number = now.weekday()+1
    logging.info("day="+str(day_number))
    
    for task in tasks:
        logging.info("sssss!!!")
        logging.info(task)
        logging.info(task.repeat)
        logging.info(task.days)
        logging.info(processes_tasks)
        test = False        
        try:
            logging.info(task.idtask)
            if task.repeat_task:
                dt_start = getTaskProcessDateStart(task, start_date)
                if dt_start and (dt_start>=getTimestamp(task.start_date, task.start_time) or task.repeat == 6):
                    dt_stop = getTimestamp(dt_start + datetime.timedelta(hours=getDuration(task)), task.stop_time)
                    if dt_start <= start_date and stop_date < dt_stop:
                        if task.idtask in processes_tasks:
                            if task.process and processes.has_key(str(task.process.id)):                                
                                next_start = getTaskProcessDateStart(task, now, True)
                                next_stop = getTimestamp(next_start + datetime.timedelta(hours=getDuration(task)), task.stop_time)
                                if task.process.tm_stop>=stop_date and task.process.tm_stop<=start_date and task.process.tm_stop>=next_start and task.process.tm_stop<next_stop:
                                    ContinueTaskWork(task, next_stop)
                                elif task.process.tm_stop<stop_date: test = True
                        else: test = True
            else:
                dt_start = getTimestamp(task.start_date, task.start_time)
                dt_stop = getTimestamp(task.stop_date, task.stop_time)
                if task.all_day: dt_stop = dt_stop + datetime.timedelta(days=1)
                if dt_start<=start_date and stop_date<dt_stop:
                    if task.process and processes.has_key(str(task.process.id)):
                        if task.process.tm_stop>=stop_date and task.process.tm_stop<=start_date:
                            ContinueTaskWork(task, min(getTimestamp(task.stop_date, task.stop_time), dt_stop))
                        elif task.process.tm_stop<stop_date: test = True
                    else: test = True
            #test = (not task.process or not processes.has_key(str(task.process.id))) and not task.idtask in processes_tasks
        except:
            logging.error(sys.exc_info())
            test = True
        logging.info(test)
        
        if test:            
            va = getWorkingArchive(videoarchives)
            if not va: break
            process = startProcess(va, task, now, dt_start, dt_stop)
            va.close()
            del va            
    logging.info("checkTasks: ")
    
    
MONTH = dict ()
MONTH [1] = "Январь"
MONTH [2] = "Февраль"
MONTH [3] = "Март"
MONTH [4] = "Апрель"
MONTH [5] = "Май"
MONTH [6] = "Июнь"
MONTH [7] = "Июль"
MONTH [8] = "Август"
MONTH [9] = "Сентябрь"
MONTH [10] = "Октябрь"
MONTH [11] = "Ноябрь"
MONTH [12] = "Декабрь"
"""
MONTH [1] = "January"
MONTH [2] = "February"
MONTH [3] = "March"
MONTH [4] = "April"
MONTH [5] = "May"
MONTH [6] = "June"
MONTH [7] = "July"
MONTH [8] = "August"
MONTH [9] = "September"
MONTH [10] = "October"
MONTH [11] = "November"
MONTH [12] = "December"
"""
def getLastDay(year, month):
    try:
        dt = datetime.date(year=year, month=month, day=31)
    except:
        try:
            dt = datetime.date(year=year, month=month, day=30)
        except:
            try:
                dt = datetime.date(year=year, month=month, day=29)
            except:
                dt = datetime.date(year=year, month=month, day=28)
    return dt
    
@permission_required('user_perms.perm_videoarchive_calendar')
def getPageCalendar(request):
    data = dict()
    dt_now = datetime.datetime.now()
    data["now_year"] = dt_now.year
    data["now_month"] = dt_now.month
    data["now_day"] = dt_now.day
    fr_coeff = 0.42
    dtn = datetime.date(dt_now.year, dt_now.month, dt_now.day)
    form = forms.CheckCalendarForm(request.POST, request.FILES)
    dt = dt_now
    condition1 = []
    #condition2 = []
    #condition_stat = []
    camera = 0
    year = dt_now.year
    data["cameras"] = comModels.Camera.objects.filter(active=True)
    if form.is_valid():
        if form.cleaned_data['year'] and len(str(form.cleaned_data["year"]))>=4:
            dt = datetime.date(year=form.cleaned_data["year"], month=dt_now.month, day=1)
            year = dt.year        
        if form.cleaned_data['camera']:
            camera = form.cleaned_data["camera"]
            if form.cleaned_data['camera']>0: 
                #condition2.append("va_f.id_camera=%i" % (camera))
                condition1.append("id_camera=%i" % (camera))
                #condition_stat.append("id_camera_id=%i" % (camera))
        if form.cleaned_data["date_from"]:
            date_from = form.cleaned_data["date_from"]
            dt_from = date_from.strftime("%Y-%m-%d")
        else:
            #date_from = datetime.date(year, 1, 1)
            date_from = datetime.date.today() - datetime.timedelta(11*365/12)
            dt_from = date_from.strftime("%Y-%m-%d")        
        if form.cleaned_data["date_to"]:
            date_to = form.cleaned_data["date_to"]
            dt_to = date_to.strftime("%Y-%m-%d")
        else:
            #date_to = datetime.date(year, 12, 31)
            date_to = datetime.date.today()
            dt_to = date_to.strftime("%Y-%m-%d")            
        #condition_stat.append("(DATE(tm_start)>='%s' and DATE(tm_start)<='%s')" % (dt_from, dt_to))
    else:
        date_from = datetime.date.today() - datetime.timedelta(11*365/12)
        #datetime.datetime.date(year, 1, 1)
        dt_from = date_from.strftime("%Y-%m-%d")
        date_to = datetime.date.today() 
        #datetime.datetime.date(year, 12, 31)
        dt_to = date_to.strftime("%Y-%m-%d")

    condition1.append("(DATE(va_r.tm_start)>='%s' and DATE(va_r.tm_start)<='%s')" % (dt_from, dt_to))
    condition1.append("va_r.tm_stop is not NULL")

    data["year"] = year
    data["camera"] = camera
    data["date_from"] = date_from.strftime("%d.%m.%Y")
    data["date_to"] = date_to.strftime("%d.%m.%Y")
    
    arr = []
    last_day = getLastDay(year=dt.year-1, month=dt.month)

    cond1 = ""
    if len(condition1)>0: cond1 = "where %s" % (" and ".join(condition1))     
    
    row = None
    if cond1:        
        query = "select count(*), count(distinct(va_cr.id_camera)), DATE(va_r.tm_start) from va_rollers as va_r left join va_commands as va_cr on va_cr.id=va_r.id_command %s group by DATE(va_r.tm_start) order by DATE(va_r.tm_start);" % (cond1)
        logging.info(query)
        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchall()
    
    #frame_info = None
    #if cond2 and False:
    #    query = "select count(distinct(va_pf.id)) as count_face, count(distinct(if(va_pf.k_cs>%s,va_pf.id_cs, 0))) as count_person  from va_rollers as va_r  inner join va_frames_roller as va_fr on va_r.id=va_fr.id_roller right join va_frame as va_f  on va_f.id=va_fr.id_frame left join va_frame_info as va_pf on va_pf.id_frame=va_f.id %s;" % (fr_coeff, cond2)
    #    logging.info(query)
    #    db.query(query)
    #    frame_info = db.store_result()
    
    i_info = 0
    m_info = len(row)
    month_i = date_from.month
    year = date_from.year
    for i in range(1, 13):        
        info =  dict()
        info["month"] = _(MONTH[month_i])
        info["year"] = year
        info["month_num"] = month_i
        ds = []
        tm = datetime.date(year=dt.year, month=month_i, day=1)  
        wd = tm.weekday()        
        for j in range(0, wd):
            d = dict()
            d["noact"] = True
            d["id"] = last_day.day-wd+j+1
            d["week_num"] = tm.strftime("%U")
            ds.append(d)
        last_day = getLastDay(year=dt.year, month=month_i)
        num_wd = wd
        for j in range(last_day.day):
            d = dict()
            tm = datetime.date(year=dt.year, month=month_i, day=j+1)
            count_face = 0
            count_people = 0
            count_roller = 0
            count_camera = 0
            if row and len(row[i_info])>2 and str(tm) == str(row[i_info][2]):                
                count_roller = row[i_info][0]
                count_camera = row[i_info][1]
                if i_info+1<m_info:
                    i_info = i_info+1
                else: row = None    
            d["count_face"] = count_face
            d["count_camera"] = count_camera
            d["count_people"] = count_people
            d["count_roller"] = count_roller
            d["count"] = count_face+count_people+count_roller+count_camera > 0
            d["wday"] = num_wd
            d["week_num"] = tm.strftime("%U")
            d["id"] = j+1
            if dt_now.month == month_i and dt_now.day == j+1:
                d["current"] = True
            ds.append(d)
            num_wd += 1
            if num_wd == 7: num_wd = 0 
        for j in range(1, 43-wd-last_day.day):
            d = dict()
            d["noact"] = True
            d["id"] = j
            if month_i+1>12: d["week_num"] = datetime.date(year+1, 1, j).strftime("%U")
            else: d["week_num"] = datetime.date(year, month_i+1, j).strftime("%U")
            ds.append(d)            
        info["days"] = ds
        info["last_wday"] = range(6-last_day.weekday())
        arr.append(info)
        month_i += 1
        if month_i == 13: 
            month_i = 1
            year += 1
    #if dt.year == dt_now.year: arr[dt_now.month-1]["days"][dt_now.day+3]["current"] = True
    data["info"] = arr
    data["month"] = MONTH
#    db.close()
    return data

def getReParam(s, p):
    try:
        ss = '.*(,*%s=(?P<%s>[0-9|a-zA-Z]+),*).*' % (p, p)
        t = re.compile(ss)
        m = re.match(t, s)
        if m and m.group(p):
            return m.group(p)
    except: pass
    return None

def getCameraVideoInfo(cid, first_s, last_s):
    
    data = []
    
    return data

    signal = models.Signals.objects.all().order_by("-id")
    t = None
    date = datetime.datetime.now() # добавлена, т.к. не ясно откуда берется это значение 
    d = date+datetime.timedelta(days=1)
    try:
        for sig in signal:
            s = []
            t = vaModels.VaRoller.objects.filter(id_command__id_signal=sig.id, id_command__id_camera=cid, tm_start__gte=date.strftime("%Y-%m-%d"), tm_start__lte=d.strftime("%Y-%m-%d")) #.extra(where=["va_rollers.tm_stop != Null"]) #.extra(where=["DATE(va_rollers.tm_start)='2011-02-22'"])
            time_stat = {}
            fin = None
            for t1 in t:
                try:
                    if t1.params and t1.tm_stop:
                        s1 = dict()
                        s1["fps"] = getReParam(t1.params, "fps")
                        s1["w"] = getReParam(t1.params, "w")
                        s1["h"] = getReParam(t1.params, "h")
                        s1["fmt"] = getReParam(t1.params, "fmt")
                        sz = getReParam(t1.params, "sz")
                        try:                        
                            s1["sz"] = round((float(sz)/1024/1024 if sz else 0), 2)
                        except: s1["sz"] = 0
                        s1["count_people"] = getReParam(t1.params, "prs")
                        s1["count_face"] = getReParam(t1.params, "fcs")
                        s1["info"] = t1
                        s1["id_roller"] = t1.id
                        hour = t1.tm_start.hour
                        s1["hour"] = hour
                        minute = t1.tm_start.minute
                        s1["minute"] = minute
                        delta = t1.tm_stop-t1.tm_start
                        s1["delta"] = math.ceil(float(delta.seconds)/60)
                        s1["count"] = 1                 
                        if fin and t1.tm_start < fin: s1["count"] = 2
                        else:                            
                            if hour in time_stat:
                                if minute in time_stat[hour]: 
                                    time_stat[hour][minute] += 1
                                    s1["count"] = time_stat[hour][minute]
                                else: time_stat[hour][minute] = 1
                            else: time_stat[hour] = {}
                        fin = max(fin, t1.tm_stop) if fin else t1.tm_stop
                        s.append(s1)
                        
                except: logging.exception("getreparams "+str(sys.exc_info()))
            data.append({"id": sig.id, "info": s, "sig_name": sig.name})
    except:
        logging.exception("getCameraVideoInfo "+str(sys.exc_info()))
    return data

def StrToDate(s):
    try:
        m = re.match(r'^([0-9]{4}).([0-9]{1,2}).([0-9]{1,2})$', s)
        if m:
            if m.group(0) and m.group(1) and m.group(2) and m.group(3):
                return {"year": int(m.group(1)), 'month': int(m.group(2)), "day": int(m.group(3))}
    except: logging.exception("strTodate "+str(sys.exc_info()))
    return False

def deleteRoller(id):
    videoarchives = vaModels.VaRoller.objects.raw('select va_rollers.id as id, va_archives.ip as ip, va_archives.port from va_rollers join va_commands on va_rollers.id_command = va_commands.id join va_archives on va_commands.id_archive = va_archives.id where va_rollers.id = %s;' %id)
    status = False
    try:
        videoarchive = videoarchives[0]
        va = archive.Archive(videoarchive.ip, videoarchive.port)
        status = va.deleteRoller(id=id)
        va.close()
        del va
    except:
        logging.exception("deleteRoller: "+str(sys.exc_info()))
    return status

@permission_required('user_perms.perm_videoarchive_delete_video')
def getDeleteRollersData(request):
    try:
        rollers = request.REQUEST['rollers'].split(',')
        for roller in rollers:
            deleteRoller(roller)
        return {'status': True}
    except:
        logging.exception("getDeleteRollersData: "+str(sys.exc_info()))
    return {'status': False}

@permission_required('user_perms.perm_videoarchive_delete_video')
def deleteRollersForAllArchivesForCamera(archives, camera, date=datetime.datetime.now(), dateStop=None):
    if dateStop == None: dateStop = date
    for arch in archives:
        va = archive.Archive(arch.ip, arch.port)
        status = va.deleteRollers(tmStart=date.strftime("%Y%m%d000000"), tmStop=dateStop.strftime("%Y%m%d235959"), idCamera=camera)
        va.close()
        del va

"""
def getDeleteAllRollersData(request):
    try:
        date = getDateForPageVideo(request)
        form = forms.CheckCameraPageVideoForm(request.REQUEST)
        if not form.is_valid():
            return {'status': False, 'error': form.errors}
       
        archives = vaModels.VaArchive.objects.all()
        if request.REQUEST.has_key('camera'):
            deleteRollersForAllArchivesForCamera(archives, request.REQUEST['camera'], date)
        else:
            cameras = getCamerasForPageVideo(request, date)
            for camera in cameras:
                deleteRollersForAllArchivesForCamera(archives, camera.id_camera, date)

        return {'status': True}
    except:
        logging.exception("getDeleteAllRollersData: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False}
"""

@permission_required('user_perms.perm_videoarchive_delete_video')
def getDeleteAllRollersData(request):
    logging.info("getDeleteAllRollersData")
    try:
        now = datetime.datetime.now()
        date = getDateForPageVideo(request, now)
        rollers, params, cd, data = getFilterVideo(request, date, None, False)
        for roller in rollers:
            roller.delete()
        return {'status': True}
    except:
        logging.exception("getDeleteAllRollersData: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False}

@permission_required('user_perms.perm_videoarchive_delete_video')
def getDeleteAllRollersForPeriod(request):
    try:
        form = forms.CheckDatePeriodForm(request.POST)
        if not form.is_valid():
            return {'status': False, 'error': form.errors}
        
        if "dateBegin" in form.cleaned_data and form.cleaned_data["dateBegin"]: date_begin = form.cleaned_data["dateBegin"]
        if "dateEnd" in form.cleaned_data and form.cleaned_data["dateEnd"]: date_end = form.cleaned_data["dateEnd"]
        else: date_end = datetime.datetime.now()
        
        archives = vaModels.VaArchive.objects.all()
        if "source" in form.cleaned_data and form.cleaned_data["source"]>0:
            deleteRollersForAllArchivesForCamera(archives, form.cleaned_data["source"], date_begin, date_end)
        else:
            cameras = getCamerasForPeriod(request, date_begin, date_end)
            for camera in cameras:
                deleteRollersForAllArchivesForCamera(archives, camera.id, date_begin, date_end)

        return {'status': True}
    except:
        logging.exception("getDeleteAllRollersData: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False}

@permission_required('user_perms.perm_videoarchive_delete_task')
def getDeleteTasksData(request):
    try:
        tasks = request.REQUEST['tasks'].split(',')
        i = 0
        while i<len(tasks):
            tasks[i] = int(tasks[i])
            i+=1

        mTasks = models.Tasks.objects.filter(id__in = tasks)
        status = True
        for task in mTasks:
            kill = killPrecesses(task.process_id)
            logging.info('kill: '+str(kill))
        mTasks.update(active = False)
        return {'status': status}
    except:
        logging.exception("getDeleteTasksData: "+str(sys.exc_info()))
    return {'status': False}

def getAllCameras(ids=None):
    cameras = []
    if ids: coms = vcModels.Communicator.objects.filter(active = True, id__in=ids)
    else: coms = vcModels.Communicator.objects.filter(active = True)
    
#    for com in coms:
    try:
            #c = Communicator(com.host, com.port)
            c = Communicator()            
            cCameras = c.getCameras()["cameras"]
            """
            for cam in cCameras:
                cam["com_id"] = com.id
                cam["com_host"] = com.host
                cam["com_port"] = com.port
            """
            cameras.extend(cCameras)
            c.close()
            del c
    except:
            logging.exception("getAllCameras %s " %(str(sys.exc_info())))
    return cameras

def getPageCameras(request, all_cameras = True):
    data = dict()
    form = forms.CheckJournalSortForm(request.GET, request.FILES)
    if form.is_valid():         
        sort_arr = ["id", "ip", "type", "name", "commun__host"]
        sort_id = form.cleaned_data["sort"]
        order = 1 if form.cleaned_data["order"] == 1 else 0
        data["sort"] = sort_id
        data["order"] = order        
        if sort_id < len(sort_arr) and sort_id>=0:
            cameras = comModels.Camera.objects.all().order_by("%s%s" % ("" if order else "-", sort_arr[sort_id]))
        else: cameras = comModels.Camera.objects.all().order_by("name")
    else: cameras = comModels.Camera.objects.all().order_by("name")
    hashCam = dict()
    for camera in cameras:        
        hashCam["%s %s" %(camera.id_camera.ip, camera.id_camera.type)] = True
    cs = getAllCameras()
    addCameras = []
    for camera in cs:
        if not hashCam.has_key("%s %s" %(camera["ip"], camera["type"])):
            addCameras.append(camera)
    logging.info("hashCam: "+str(hashCam))
    if all_cameras:
        data['all_cameras'] = len(cameras)
        data['cameras'] = cameras
    data['addCameras'] = addCameras
    
    return data

def getAddCameras(request):
    try:
        cameras = request.REQUEST['cameras'].split(',')        
        status = False
        c = 0
        for camera in cameras:
            ip, type, com_id = camera.split(':')
            camera, create = comModels.Camera.objects.get_or_create(ip = ip, type = type)
            if create:
                camera.num = 0
                camera.name = "%s %s" %(camera.ip, camera.type)
                camera.save()
            if camera and com_id: # and comModels.vaCameraCommunicator.objects.filter(id_camera=camera).count() == 0:
#                comm = vcModels.Communicator.objects.get(id=com_id)
#                comModels.vaCameraCommunicator.objects.get_or_create(id_camera=camera, id_communicator=comm)
                c += 1
                status = True                
        return {'status': status, "count": c}
    except:
        logging.exception("getAddCameras: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False, "error": ""}

def getDeleteCameras(request):
    try:
        form = forms.TestDeleteCamerasForm(request.POST)
        if form.is_valid():
            ids = request.REQUEST['ids'].split(',')
            if len(ids) == 0: return HttpResponse("error")
            ids = ids[:-1]
            i = 0
            comms = comModels.Camera.objects.filter(id__in = ids).update(active=False)
            data = getPageCameras(request)
            return {'status': True, 'data': render_to_string("cameras_list.html", data)}
    except:
        logging.exception("getDeleteCameras: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False}

def getRenameCamera(request):
    try:
        form = forms.CheckRenameCameraForm(request.REQUEST)
        if not form.is_valid():
            return {'status': False, 'error': form.errors}
        camera = comModels.Camera.objects.get(id=form.cleaned_data["id"])
        camera.name = form.cleaned_data["name"]
        camera.save()
        return {'status': True}
    except:
        logging.exception("getRenameCamera: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False}

@permission_required('user_perms.perm_videoarchive_analysis')
def getInfoRollerImport(request):
    data = dict()
    va_servers, va_ports, videoarchives = aUtils.getVideoArchives()
    
    videoarchive = videoarchives[0]
    try:    
        va = archive.Archive(videoarchive["host"], videoarchive["port"])
        data.update(va.getInfo(request.REQUEST["url"]))
        va.close()
        del va
        data["dur"] = "%s:%s" %(int(data["dur"])/60, int(data["dur"])%60)
        data["info"] = render_to_string("info_roller.html", data)
        data["status"] = True
    except:
        logging.exception("getInfoRoller host: %s port: %s %s " %(videoarchive["host"], videoarchive["port"], str(sys.exc_info())))
        data["status"] = False
    return data

# Генерация уникальных UUID для камеры
def getUniqueUUID():
    try:
        t = True        
        while t:
            uuid = uuid.uuid1()
            t = comModels.Camera.objects.filter(uuid=uuid).count()>0
        return uuid
    except:
        return str(datetime.datetime.now())

@permission_required('user_perms.perm_videoarchive_analysis')
def getImportRoller(request):
    try:
        form = forms.CheckImportRollerForm(request.REQUEST)
        if not form.is_valid():
            s = ""
            for e in form.errors:
                s += "%s_error,%s," % (e, form.errors[e])
            return {'status': False, 'error': s}
        
        time = form.cleaned_data["date_imp"]+datetime.timedelta(hours = form.cleaned_data["hour_imp"])+ datetime.timedelta(minutes = form.cleaned_data["minute_imp"]) + datetime.timedelta( seconds = form.cleaned_data["second_imp"])
        now = datetime.datetime.now()
        if time > now:            
            if form.cleaned_data["date_imp"]>=now: return {'status': False, 'error': "error date"}
            else: return {'status': False, 'error': "error time"}
        
        va_servers, va_ports, videoarchives = aUtils.getVideoArchives()
        videoarchive = videoarchives[0]
        
        va = archive.Archive(videoarchive["host"], videoarchive["port"])
        source = form.cleaned_data["source"]
        
        params = []
        cameraUUID = ""        
        camera = None        
        if source == 0:
            new_name = form.cleaned_data["new_name_source"]            
            camera, create = comModels.Camera.objects.get_or_create(ip = new_name, type = settings.TYPE_IMPORT, active=True, uuid=getUniqueUUID())
            if create:
                camera.num = 0
                camera.name = "%s %s" %(new_name, settings.TYPE_IMPORT)
                camera.active = True
                camera.save()
        else: camera = comModels.Camera.objects.get(id=source)
        if camera:
            cameraUUID = camera.uuid 
            # Блок получения параметров управляющей системы
            cs = getControlSystem(camera)
            if cs:
                params = [{"name": "csIp", "value": cs.host},
                          {"name": "csPort", "value": cs.port},
                          {"name": "csLogin", "value": cs.login},
                          {"name": "csPassword", "value": cs.passwd},
                          {"name": "csUser", "value": cs.user},
                          {"name": "csVersion", "value": "2.22"}]
        mode = 0
        if form.cleaned_data["fd"]: mode = 1
        if form.cleaned_data["fr"]: mode = 2
        
        frames_proc = 0
        if form.cleaned_data["fps_imp"]: frames_proc = form.cleaned_data["enter_fps_imp"]
        
        interval = form.cleaned_data["interval"]
        interval = form.cleaned_data["time"] if interval == 0 and form.cleaned_data["time"] else interval
        # Разрешение        
        resol = form.cleaned_data["resol"]
        width = height = 0
        if resol.find("x") >= 0: width, height = form.cleaned_data["resol"].split('x')
        elif resol.find("*") >= 0: width, height = form.cleaned_data["resol"].split('*')
        if width and height: 
            params.append({"name": "width", "value": width})
            params.append({"name": "height", "value": height})
        # Кодек
        codec = form.cleaned_data.get("codec", 0)
        if codec:
            codecs = models.Codecs.objects.filter(id=codec)
            if codecs.count() > 0:
                params.append({"name": "codec", "value": codecs[0].number})
        # Частота ключевых кадров
        gop = form.cleaned_data.get("gop", 0)
        if gop: params.append({"name": "gopSize", "value": gop})
        # Отправка запроса на импорт
        answer, remark = va.importRoller(path=form.cleaned_data["path"], cameraUUID=cameraUUID, tmStart=time, mode=mode, diffFramesProc = frames_proc, convert = form.cleaned_data["convert"], interval = interval, params = params)
        va.close()
        del va
        
        return {'status': answer, 'error': remark}
    except:
        logging.exception("getImportRoller: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False}


def getInfoRoller(request):
    try:
        form = forms.CheckInfoRollerForm(request.REQUEST)
        if not form.is_valid():
            return {'status': False, 'error': form.errors}
        data = dict()
        
        #rollers = vaModels.VaRoller.objects.raw('select va_rollers.id as id, va_rollers.tm_start as tm_start, va_rollers.tm_stop as tm_stop, TIMESTAMPDIFF(SECOND, va_rollers.tm_start, va_rollers.tm_stop) as dt_time, location, params, signal_type, videoarchive_signals.name as signal_name, url, communicator_camera.ip as ip, communicator_camera.type as type from va_rollers, va_commands left join videoarchive_signals on va_commands.id_signal = videoarchive_signals.id join va_commands.id_archive = va_archives.id, communicator_camera  where va_rollers.id_command = va_commands.id and va_commands.id_camera = communicator_camera.id and va_rollers.tm_stop and va_rollers.id=%s;' %(form.cleaned_data["id"]))
        rollers = vaModels.VaRoller.objects.raw('select va_rollers.id as id, va_rollers.tm_start as tm_start, va_rollers.tm_stop as tm_stop, extract(epoch FROM cast(va_rollers.tm_stop AS timestamp)-cast(va_r.tm_start AS timestamp)) as dt_time, location, params, signal_type, videoarchive_signals.name as signal_name, url, communicator_camera.ip as ip, communicator_camera.type as type from va_rollers, va_commands left join videoarchive_signals on va_commands.id_signal = videoarchive_signals.id join va_commands.id_archive = va_archives.id, communicator_camera  where va_rollers.id_command = va_commands.id and va_commands.id_camera = communicator_camera.id and va_rollers.tm_stop and va_rollers.id=%s;' %(form.cleaned_data["id"]))
        
        info = loader.get_template('info_table_roller.html')  
        c = Context({
                 'rollers': rollers,
                 })
        data.update({'status': True, 'id': form.cleaned_data["id"], 'content': info.render(c)})
        return data
    except:
        logging.exception("getInfoRoller: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False}

@permission_required('user_perms.perm_videoarchive_export_video')
def getSaveRollers(request):
    errors = []
    try:
        form = forms.CheckSaveRollersForm(request.REQUEST)
        if not form.is_valid():
            return {'status': False, 'error': form.errors}

        rollers = form.cleaned_data["rollers"].split(',')
        fileno, short_name = tempfile.mkstemp(suffix="", prefix="video")
        if settings.USE_ZIP_FILE: 
            tarname = short_name+".zip"
            alias = "StoredVideo_%s.zip" % (datetime.datetime.now().strftime("%S%M%H%d%m%Y"))            
        else: 
            tarname = short_name+".tar.bz2"
            alias = "StoredVideo_%s.tar.bz2" % (datetime.datetime.now().strftime("%S%M%H%d%m%Y"))
        path = os.path.dirname(tarname)
        if not os.path.exists(path):
            os.makedirs(path)

        urltarname = "/gettmpfile/?name=%s&alias=%s" % (tarname, alias)
        if settings.ARCHIVE_URL != "":
            urltarname = '/%s%s' %(settings.ARCHIVE_URL,urltarname)
        
        if settings.USE_ZIP_FILE:
            zf = zipfile.ZipFile(tarname, mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
        else: tar = tarfile.open(tarname, "w:bz2")
        
        files = []
        raws = vaModels.VaRoller.objects.filter(id__in=rollers)
        for raw in raws:
            try:               
                url_prefix = raw.id_command.id_archive.url
                if not 'http:' in url_prefix:
                    url_prefix = "http://%s%s" %(request.get_host(), url_prefix)
                url = "%sfiles/video%s" %(url_prefix, raw.location)
                logging.info('getSaveRollers: url: '+str(url))
                ext = raw.location[-4:]
                f = urllib.urlopen(url)
                data_file = f.read()
                f.close()                
                if settings.USE_ZIP_FILE: zf.writestr(str(raw.id)+ext, data_file)
                else:
                    fileno, short_name = tempfile.mkstemp()
                    new_file = short_name+str(raw.id)+ext
                    f = open(new_file, "w+b")
                    f.write(data_file)
                    f.close()
                    tar.add(new_file, str(raw.id)+ext)
                    files.append(new_file)
            except:
                logging.exception("add_files: "+str(sys.exc_info()))
                errors.append("add_files: "+str(sys.exc_info()))
            
        #tar.close()
        if settings.USE_ZIP_FILE: zf.close()
        else: tar.close()        
        
        return {'status': len(errors) == 0, 'url': urltarname, 'errors': errors}
    except:
        logging.exception("getSaveRollers: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    finally:
        try:
            for file in files:
                os.unlink(file)
        except:
            logging.exception("export_unlink_tmp_file:"+str(sys.exc_info()))
            errors.append("export_unlink_tmp_file:"+str(sys.exc_info()))
    return {'status': False, 'errors': errors}

@permission_required('user_perms.perm_videoarchive_processes')
def getProcessRollerData(request):
    try:
        form = forms.CheckProcessRollerForm(request.REQUEST)
        if not form.is_valid():
            return {'status': False, 'error': form.errors}
        
        status = False
        videoarchives = vaModels.VaRoller.objects.raw('select va_rollers.id as id, va_archives.ip as ip, va_archives.port from va_rollers join va_commands on va_rollers.id_command = va_commands.id join va_archives on va_commands.id_archive = va_archives.id where va_rollers.id = %s;' %form.cleaned_data['id'])
        
        videoarchive = videoarchives[0]
        # Блок получения параметров управляющей системы
        params = []
        cs = getControlSystem(videoarchive.id_command.id_camera)
        if cs:
            params = [{"name": "csIp", "value": cs.host},
                      {"name": "csPort", "value": cs.port},
                      {"name": "csLogin", "value": cs.login},
                      {"name": "csPassword", "value": cs.passwd},
                      {"name": "csUser", "value": cs.user},
                      {"name": "csVersion", "value": "2.22"}]

        va = archive.Archive(videoarchive.ip, videoarchive.port)
        status = va.processRoller(id=form.cleaned_data['id'], mode=form.cleaned_data['mode'], diffFramesProc=form.cleaned_data['diffFramesProc'], params=params)
        va.close()
        del va
        
        return {'status': True}
    except:
        logging.exception("getProcessRollerData: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False}

@permission_required('user_perms.perm_videoarchive_settings')
def setResolutionInterface(request):
    try:
        form = forms.CheckSetResolutionInterfaceForm(request.REQUEST)
        if not form.is_valid():
            return {'status': False, 'error': form.errors}
        resol = form.cleaned_data["resol"]
        param, create = models.Settings.objects.get_or_create(name=settings.RES_INTERFACE)
        param.value = resol
        param.save()
        return {'status': True}
    except:
        logging.exception("setResolutionInterface: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False}

def getPageMonitor(request):
    space = settings.space
    raid_status = settings.raid_status
    data = dict()
    if space:    
        s = commands.getoutput(space)
        s = s.replace("\n", "")
        m = re.match(r".*G *([0-9]+)%.*", s)
        if m and m.group(1):
            data["space"] = 100-int(m.group(1))
    if raid_status:    
        s = commands.getoutput(raid_status)
        data["raid_status"] = s              
    return data

def getPageFaces(request, id):
    data = dict()
    roller = vaModels.VaRoller.objects.filter(id=id)
    if roller.count()>0:
        roller = roller[0]
        faces = vaModels.VaPersonsFrame.objects.raw("select va_frame_info.*, va_archives.url as url, va_archives.ip as ip from va_frame_info join va_archives on va_archives.id=va_frame_info.id_archive where id_archive=%s and id_camera=%s and tm_dt between '%s' and '%s';" % (roller.id_command.id_archive.id, roller.id_command.id_camera.id, roller.tm_start, roller.tm_stop))
        faces = list(faces)
        data["all_faces"] = len(faces)
        data.update(getNavigation(request, faces, 'faces', get_limits([[21, 28, 35, 42],[33, 44, 55, 66]]), navigation_title = _("Количество лиц на странице")))
    return data

def setFaceFio(raw_rollers):
    fio_cs = {}
    id_cs = {}
    if len(raw_rollers) > 0:
        balIds, balNames = getBalPersons()
        for raw_roller in raw_rollers:
            try:
                if raw_roller.fio_cs:
                    if not raw_roller.fio_cs in fio_cs: fio_cs[raw_roller.fio_cs] = getNamePersonByBalName(raw_roller.fio_cs)
                    setattr(raw_roller, "fio", fio_cs[raw_roller.fio_cs])
                elif raw_roller.id_cs:
                    if not raw_roller.id_cs in id_cs: id_cs[raw_roller.id_cs] = getNamePersonByBalIds(int(raw_roller.id_cs), balIds, balNames)
                    setattr(raw_roller, "fio", id_cs[raw_roller.id_cs])
            except:
                logging.exception(str(sys.exc_info()))
    return raw_rollers


def getPageRollerPersons(request, id):
    data = dict()
    logging.info(id)
    roller = vaModels.VaRoller.objects.filter(id=id)
    logging.info(roller)
    if roller.count()>0:
        roller = roller[0]
        k_cs = vcUtils.get_value_defaultparams(journalBoundCoeff)
        faces = vaModels.VaPersonsFrame.objects.raw("select va_frame_info.*, va_archives.url as url, va_archives.ip as ip from va_frame_info join va_archives on va_archives.id=va_frame_info.id_archive where id_archive=%s and id_camera=%s and tm_dt between '%s' and '%s' and id_cs is not null and k_cs>=%s;" % (roller.id_command.id_archive.id, roller.id_command.id_camera.id, roller.tm_start, roller.tm_stop, k_cs))
        faces = list(faces)
        data["all_faces"] = len(faces)
        data["oxion_url"] = settings.OXION_URL
        data.update(getNavigation(request, faces, 'faces', get_limits([[21, 28, 35, 42],[33, 44, 55, 66]]), navigation_title = _("Количество персон на странице")))
        data["faces"] = setFaceFio(data["faces"])
    return data

@permission_required('user_perms.perm_videoarchive_settings')
def setDaemonSettings(request):
    try:
        form = forms.SetSettingsForm(request.REQUEST)
        if not form.is_valid():
            return {'status': False, 'errors': form.errors}

        id = form.cleaned_data["id"]
        params = []
        params_name = {"thresholdDays": "delOlderDays", "thresholdAlerts": "thresholdFreeSpaceNotif", "thresholdRemove": "thresholdFreeSpaceDel",
                       "checkIntervalThresholds": "delIntervalHours", "rollerCapacity": "bitrate", "rollerBlur": "blur",
                       "rollerCompression": "compress", "rollerDistance": "gopSize", "rollerIdent": "identThreshold",
                       "timeout": "socketTimeout", "domen": "adminDomen", "domenAlert": "adminAlertUrl"}
        for p in params_name:
            val = form.cleaned_data.get(p, None)
            if val: params.append({'name': params_name[p], 'value': str(val).strip()})
        status = True
        
        if id:
            v_archives = vaModels.VaArchive.objects.filter(id=id)
            for v_archive in v_archives:
                #if form.cleaned_data['url'] != v_archive.url: v_archives.update(url=form.cleaned_data['url'])
                va = archive.Archive(v_archive.ip, v_archive.port)
                if not va.setDaemonSettings(params=params): status = False
                va.close()
                del va
        return {'status': status}
    except:
        logging.exception(str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False, 'errors': errors}

@permission_required('user_perms.perm_videoarchive_settings')
def setDefaultArchiveSettings(request):
    logging.info("setDefaultArchiveSettings")
    try:
        form = forms.SetDefaultArchiveSettingsForm(request.REQUEST)
        logging.info(form.is_valid())
        logging.info(form.errors)
        if not form.is_valid():
            return {'status': False, 'errors': form.errors}
        logging.info(form.cleaned_data)
        for cd in form.cleaned_data:
            vcUtils.update_value_defaultparams(cd, form.cleaned_data[cd])

        status = True
        return {'status': status}
    except:
        logging.exception(str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    return {'status': False, 'errors': errors}

def getCameraInfo(request):
    try:
        status = False
        msg = ""
        form = forms.CheckIdForm(request.POST)
        if form.is_valid(): 
            id = form.cleaned_data["id"]
            cam = comModels.Camera.objects.filter(id=id).exclude(type="IMPORT")
            if cam.count() > 0:
                #all_cameras = getAllCameras([cam[0].commun.id])
                #cameras = filter(lambda x: x.uuid==cam[0].uuid, all_cameras)
                #logging.info(cameras)
                #if len(cameras) > 0: 
                name = "%s %s" % (cam[0].ip, cam[0].type)
                if name != cam[0].name and cam[0].name: name = "%s (%s)" %(cam[0].name, name)
                msg = json.dumps({'info': name, 'uuid': cam[0].uuid, "ip": cam[0].ip, "type": cam[0].type})
                status = True
    except:
        logging.exception(str(sys.exc_info()))
    return {'status': status, 'msg': msg}

def checkTaskname(request):
    try:
        form = forms.CheckTaskNameForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get("id", 0)
            if id: task = models.Tasks.objects.filter(name=form.cleaned_data["name"], active=True).exclude(id=id)
            else: task = models.Tasks.objects.filter(name=form.cleaned_data["name"], active=True)
            if task.count() == 0: return {'status': True}
    except:
        logging.exception(str(sys.exc_info()))
    return {'status': False}

def addFileToZip(zf, url, path):               
                f = urllib.urlopen(url)
                data_file = f.read()
                f.close()
                if settings.USE_ZIP_FILE: zf.writestr(path, data_file)
                else:
                    fileno, short_name = tempfile.mkstemp()
                    new_file = short_name+path
                    f = open(new_file, "w+b")
                    f.write(data_file)
                    f.close()
                    tar.add(new_file, path)
                    files.append(new_file)   

@permission_required('user_perms.perm_videoarchive_export_video')
def getSaveRollerWithFace(request):
    errors = []
    try:
        form = forms.CheckIdForm(request.REQUEST)
        if not form.is_valid():
            return {'status': False, 'error': form.errors}

        roller_id = form.cleaned_data["id"]
        fileno, short_name = tempfile.mkstemp(suffix="", prefix="video")
        if settings.USE_ZIP_FILE: 
            tarname = short_name+".zip"
            alias = "StoredVideo_%s.zip" % (datetime.datetime.now().strftime("%S%M%H%d%m%Y"))            
        else: 
            tarname = short_name+".tar.bz2"
            alias = "StoredVideo_%s.tar.bz2" % (datetime.datetime.now().strftime("%S%M%H%d%m%Y"))
        path = os.path.dirname(tarname)
        if not os.path.exists(path):
            os.makedirs(path)

        urltarname = "/gettmpfile/?name=%s&alias=%s" % (tarname, alias)
        if settings.ARCHIVE_URL != "":
            urltarname = '/%s%s' %(settings.ARCHIVE_URL,urltarname)
        
        if settings.USE_ZIP_FILE:
            zf = zipfile.ZipFile(tarname, mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
        else: tar = tarfile.open(tarname, "w:bz2")
        
        files = []
        try:               
            raw = vaModels.VaRoller.objects.filter(id=roller_id)
            if raw.count() > 0:
                raw = raw[0]
                url_prefix = raw.id_command.id_archive.url
                if not 'http:' in url_prefix:
                    url_prefix = "http://%s%s" %(request.get_host(), url_prefix)
                
                url = "%sfiles/video%s" %(url_prefix, raw.location)
                ext = raw.location[-4:]
                addFileToZip(zf, url, str(roller_id)+ext)
                
                faces = vaModels.VaPersonsFrame.objects.filter(id_camera=raw.id_command.id_camera, id_archive=raw.id_command.id_archive, tm_dt__gte=raw.tm_start, tm_dt__lte=raw.tm_stop)
                for face in faces:
                    url = "%sfiles/video%s" %(url_prefix, face.location_photo)
                    ext = os.path.basename(face.location_photo)
                    addFileToZip(zf, url, "/faces/"+ext)
        except:
            logging.exception("add_files: "+str(sys.exc_info()))
            errors.append("add_files: "+str(sys.exc_info()))
            
        #tar.close()
        if settings.USE_ZIP_FILE: zf.close()
        else: tar.close()
        
        return {'status': len(errors) == 0, 'url': urltarname, 'errors': errors}
    except:
        logging.exception("getSaveRollers: "+str(sys.exc_info()))
        return {'status': False, 'error': str(sys.exc_info())}
    finally:
        try:
            for file in files:
                os.unlink(file)
        except:
            logging.exception("export_unlink_tmp_file:"+str(sys.exc_info()))
            errors.append("export_unlink_tmp_file:"+str(sys.exc_info()))
    return {'status': False, 'errors': errors}
