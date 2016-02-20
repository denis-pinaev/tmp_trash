#coding=utf-8
from django.shortcuts import render_to_response
from videoclient import utils as vUtils
from monitoring import utils
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from videoclient.views import initBalancer, initCommunicators, tester, render_to_response_ex, video, getAllActiveCameras, getActiveSystemCameras
from videoclient.utils import get_value_defaultparams, VERSION
from videoclient.monitoring import models as mModels
from videoclient.communicator import Communicator
import settings
import commands
import logging
import json
import sys
import re
from django.template.loader import render_to_string
import os
from django.utils.safestring import mark_safe
import zipfile
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
import videoclient
import math
from videoclient.utils import getDefaultParams
from videoclient.communicator.models import Camera
from django.contrib.auth.decorators import permission_required, login_required
from videoclient.monitoring import forms
from django.db.models import Max
from videoclient.monitoring.systemlog import views as syslogViews 


@tester
@permission_required('user_perms.perm_monitoring')
def events(request):

    data = dict()
    data.update(vUtils.getDefaultParams(request, 'monitoring_events', None))
    data.update(utils.getEventsData(request))
    data.update(vUtils.dataGet(request))
    
    return render_to_response_ex(request, 'monitoring_events.html', data, context_instance=RequestContext(request))

@tester
@permission_required('user_perms.perm_monitoring')
def system(request, uuid=None):
    
    from videoclient import views as vViews
    
    data = dict()
    data.update(getDefaultParams(request, 'monitoring_system'))
    
    res_get_all_active_cameras = getActiveSystemCameras(uuid, 'monitoring_system2')
    data["all_active_cameras"] = res_get_all_active_cameras["all_active_cameras"]
    data["selected_camera"] = res_get_all_active_cameras["camera"]
    data["communicator_errors_info"] = res_get_all_active_cameras["communicator_errors_info"]

    data["show_js"] = False
    data["show_flash"] = True
    if int(get_value_defaultparams("use_js")) == 1:
        data["show_js"] = True
        data["show_flash"] = False
        
    data.update(utils.getSystemData(request))
    
    return render_to_response_ex(request, "monitoring_system.html", data)

@tester
@permission_required('user_perms.perm_monitoring')    
def videoanalytics(request, uuid=None):
        
    from videoclient import views as vViews
    
    data = dict()
    data.update(getDefaultParams(request, 'monitoring_videoanalytics'))
    
    res_get_all_active_cameras = getActiveSystemCameras(uuid, 'monitoring_videoanalytics2')
    data["all_active_cameras"] = res_get_all_active_cameras["all_active_cameras"]
    data["selected_camera"] = res_get_all_active_cameras["camera"]
    data["communicator_errors_info"] = res_get_all_active_cameras["communicator_errors_info"]
    
    data["show_js"] = False
    data["show_flash"] = True
    if int(get_value_defaultparams("use_js")) == 1:
        data["show_js"] = True
        data["show_flash"] = False
        
    data.update(utils.getSystemData(request))
    
    return render_to_response_ex(request, "monitoring_videoanalytics.html", data)

@tester
@permission_required('user_perms.perm_monitoring')
def get_camera_frames_statistics_js(request):
    try:
        c = Communicator()
        res_frame_answer = c.getCameraFramesStat(request.REQUEST["uuid"])
        c.close()
        del c
        if res_frame_answer["success"]:
            colors = ['CC3300', '0066CC', '00CC00', 'FF9900', '33CC00', '00CC66', '99FF00', 'FF0099']
            return JsonResponse({'status': 'success', 'data': res_frame_answer['answer'], 'colors':colors})
        else:
            return JsonResponse({'status': 'error'})
    except:
        return JsonResponse({'status': 'error'})

@tester
@permission_required('user_perms.perm_monitoring')
def get_camera_va_statistics_js(request):
    try:
        c = Communicator()
        res_frame_answer = c.getCameraVaStat(request.REQUEST["uuid"])
        c.close()
        del c
        
        if res_frame_answer["success"]:
            frame_answer = res_frame_answer["answer"]
            colors = ['CC3300', '0066CC', '00CC00', 'FF9900', '33CC00', '00CC66', '99FF00', 'FF0099']
            return JsonResponse({'status': 'success', 'data': frame_answer, 'colors':colors})
        else:
            return JsonResponse({'status': 'error'})
    except:
        return JsonResponse({'status': 'error'})    

@tester
@permission_required('user_perms.perm_monitoring')
def communicator(request, uuid=None):
    
    data = dict()
    data["show_js"] = settings.MONITORING_SYSTEM_GRAPH_JS
    data["show_flash"] = settings.MONITORING_SYSTEM_GRAPH_FLASH
    
    res_get_all_active_cameras = getActiveSystemCameras(uuid, 'monitoring_communicator2')
    data["all_active_cameras"] = res_get_all_active_cameras["all_active_cameras"]
    data["selected_camera"] = res_get_all_active_cameras["camera"]
    data["communicator_errors_info"] = res_get_all_active_cameras["communicator_errors_info"]

    try:
        data.update(vUtils.getDefaultParams(request, 'monitoring_communicator', None))
        SERVERC, PORTC, COMMUNICATORS = initCommunicators()
        data['communicators'] = COMMUNICATORS
    except:
        logging.exception("monitoring_communicator "+str(sys.exc_info()))
    return render_to_response_ex(request, "monitoring_communicator.html", data)

@tester
@permission_required('user_perms.perm_monitoring')
def versions(request):
    
    data = dict()
    status = False
    try:
        data.update(vUtils.getDefaultParams(request, 'monitoring_versions', None))
        SERVERC, PORTC, COMMUNICATORS = initCommunicators()
        components = []
        
        # Получение списка коммуникаторов
        c = Communicator()
        res_version = c.getVersion()
        versions = []
        if res_version["success"]:
            for info in res_version["versions"]:
                cams = []
                v = ''
                a = ''
                if  info["version"]:
                    v = info["version"]
                    a = True
                else:
                    v = _('Недоступен')
                    a = False
                    
                try:
                    cameras_res = c.getCameras(True)
                    if cameras_res["success"]:
                        cameras = cameras_res["cameras"]
                        for camera in cameras:
                                success, version = c.getVAVersion(camera.uuid)
                                if 'Smilart Videoanalytics Daemon ' in version: version = version.split('Smilart Videoanalytics Daemon ')[1]
                                if success and not version in versions:
                                    versions.append(version)
                                    cams.append({'name':camera.name,'info':camera.ip+' '+camera.type,'port':camera.port,'ip':camera.ip,'type':camera.type,'version':version})
                except:
                    logging.exception(str(sys.exc_info()))
                if len(cams)<1: cams = False
                components.append({'name': _('Коммуникатор'), 'ip': info["host"], 'port': info["port"], 'version': v, 'active': a, 'cameras':cams})
        c.close()
                
        # Получение списка видеоархивов
        try:
            from videoclient.videoarchive.archive import archive
            from videoclient.videoarchive.archive import utils as aUtils 
            va_servers, va_ports, videoarchives = aUtils.getVideoArchives()        
            for videoarchive in videoarchives:
                component = {'name': _('Видеоархив'), 'ip': videoarchive["host"], 'port': videoarchive["port"], 'version': _('Недоступен'), 'active': False}
                try:
                    va = archive.Archive(videoarchive["host"], videoarchive["port"])
                    va.open()
                    data_version = None
                    if va.connect:
                        data_version = va.getVersion()
                    va.close()
                    del va
                    if data_version is not None and 'version' in data_version:
                        component['version'] = data_version["version"]
                        component['active'] = True
                except:
                    logging.exception(str(sys.exc_info()))
                components.append(component)
        except:
            logging.exception(str(sys.exc_info()))
        
        balancers = None
        
        try:
            from videoclient.balancer import Balancer
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            balancers, csV = b.getSystemInfo("SDKBalancer", True)
            b.close()
            del b
            component = {'name': _('Управляющая система'), 'ip': str(HOST), 'port': str(PORT), 'version': _('Недоступен'), 'active': False}
            logging.info("get_extended_video_info_version: " + str(csV))
            if csV:
                component["version"] = csV
                component["active"] = True 
            components.append(component)
        except:
            logging.info("get_extended_video_info: b.getSystemInfo failed: " + str(sys.exc_info()))
        
        if balancers and balancers.has_key("balancer"):
            for balancer in balancers["balancer"]:
                if balancer.has_key("daemons"):
                    for daemons in balancer["daemons"]:
                        if not isinstance(daemons, dict):
                            continue
                        for daemon in daemons["daemon"]:
                            if daemon.has_key("address") and daemon.has_key("type") and daemon.has_key("port"):
                                component = {'name': _(daemon["type"]), 'ip': daemon["address"], 'port': daemon["port"], 'version': _('Недоступен'), 'active': False}
                                if daemon.has_key("version"):
                                    component["version"] = daemon["version"]
                                if daemon.has_key("active") and daemon["active"] == "true":
                                    component["active"] = True
                                if daemon.has_key("license_days"):
                                    component["license_days"] = daemon["license_days"]
                                components.append(component)
        
        
        data['components'] = components
        status = True
    except:
        logging.exception("monitoring_versions "+str(sys.exc_info()))
        
    if 'export' in request.REQUEST:
        result = { 'status': 'success' }
        error = False
        data['version']=VERSION
        try:
            wrapper = render_to_string("monitoring_versions_export.html", data)

            #create zip file
            fname = settings.VERSION_COMPONENTS_FILENAME
            path = os.path.dirname(settings.EVENTS_EXPORT_JOURNAL_PATH)
            if not os.path.exists(path):
                os.makedirs(path)
            zip_file = settings.EVENTS_EXPORT_JOURNAL_PATH + fname
            zf = zipfile.ZipFile(zip_file, mode='w', compression=zipfile.ZIP_DEFLATED,)        
            try:
                zf.writestr('versions.html', wrapper)
            except:
                error = True
                logging.exception('add file to archive error: ' + str(sys.exc_info()))
            try:
                zf.close()
            except:
                error = True
                logging.exception('close archive error: ' + str(sys.exc_info()))
        except:
            error = True
            logging.exception('export version error: ' + str(sys.exc_info()))
        if error:
            result['status']='error' 
        return JsonResponse(result)
    elif 'download' in request.REQUEST:
        try:
            fname = settings.VERSION_COMPONENTS_FILENAME
            zip_file = settings.EVENTS_EXPORT_JOURNAL_PATH + fname
            f = open(zip_file, 'r+b')
            wrapper = f.read()
            f.close()
            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Length'] = len(wrapper)
            response['Content-Disposition'] = 'attachment;filename=%s' % fname
            return response
        except:
            logging.exception('download zip error: ' + str(sys.exc_info()))
            return HttpResponseRedirect('/monitoring/versions/')

    else:
        return render_to_response_ex(request, "monitoring_versions.html", data)

def JsonResponse(data):
    return HttpResponse(json.dumps(data), mimetype="application/json")

@tester
# @permission_required('user_perms.perm_monitoring')
# Проверка на права пользователей убрана т.к. используется видеоархивом без авторизации,
# Необходимо предусмотреть авторизацию на демоне видеоархиве  
def alert(request):
    from videoclient import forms
    
    data = dict()
    data["status"] = False 
    try:
        import monitoring
        from monitoring.utils import saveMonitoringMessage
        form = forms.CheckVideoarchiveAlertForm(request.REQUEST)
        if form.is_valid():
            app = form.cleaned_data["app"]
            info = form.cleaned_data["type"]
            type = "%s_%s" %(app, info)
            description = ""
            logging.info(type)
            logging.info(type in mModels.MONITORING_TYPE_CHOICES)
            if len(filter(lambda x: x[0] == type, mModels.MONITORING_TYPE_CHOICES)) > 0:
                isArchive = False
                isFree = False
                isImport = False
                isCritical = False
                params = dict()
                if app=="va":
                    logging.info("va")
                    if form.cleaned_data.get("id", None):
                        id = form.cleaned_data["id"]
                        from django.shortcuts import get_object_or_404
                        from videoarchive.va import models as vaModels
                        archive = get_object_or_404(vaModels.VaArchive, id = int(id))
                        description = "Видеоархив: %s:%s" %(archive.ip, archive.port)
                        params["host"] = archive.ip
                        params["port"] = archive.port
                        isArchive = True
                    if form.cleaned_data.get("space", None):
                        space = form.cleaned_data["space"]
                        if description != "":
                            description = description + " "
                        description = description + 'Свободного места на диске: %s%%' %(space)
                        params["free"] = space
                        isFree = True
                    
                        if info=="critical":
                            description = description + ", некоторые ролики будут удалены"
                            isCritical = True
                    elif form.cleaned_data.get("command", None):
                        isImport = True
                #monitoring.warning(type=type, description=description, show=True)
                ''' del ->'''
                if isArchive:
                    if isFree:
                        if isCritical:
                            saveMonitoringMessage(id = 'space_info_videoarchive_critical', params = params, type=type, description=_("Видеоархив: %(host)s:%(port)s. Свободного места на диске: %(free)s%%, некоторые ролики будут удалены.")%params, show=True)
                        else:
                            saveMonitoringMessage(id = 'space_info_videoarchive', params = params, type=type, description=_("Видеоархив: %(host)s:%(port)s. Свободного места на диске: %(free)s%%.")%params, show=True)
                    elif isImport:
                        saveMonitoringMessage(id = 'import_error_videoarchive', params = params, type=type, description=_("Видеоархив: %(host)s:%(port)s. Ошибка импорта.")%params, show=True)
                else:
                    if isFree:
                        if isCritical:
                            saveMonitoringMessage(id = 'space_info_critical', params = params, type=type, description=_("Свободного места на диске: %(free)s%%, некоторые ролики будут удалены.")%params, show=True)
                        else:
                            saveMonitoringMessage(id = 'space_info', params = params, type=type, description=_("Свободного места на диске: %(free)s%%")%params, show=True)
                    elif isImport:
                        saveMonitoringMessage(id = 'import_error', params = params, type=type, description=_("Ошибка импорта.")%params, show=True)
                ''' del ->'''
                data["status"] = True
    except:
        logging.exception('monitoring_alert: '+str(sys.exc_info()))
    return JsonResponse(data)

@tester
@login_required
def checkmessage(request):
    #from django.db import connections, transaction
    #cursor = connections['systemlog'].cursor()

    data = dict()
    data["status"] = False
    try:
        form = forms.CheckForm(request.GET)
        messages = []
        if form.is_valid():
            if form.cleaned_data.get("check", None):
                events = mModels.Events.objects.filter(id__gt=int(form.cleaned_data["check"]), error_level=0)
                for event in events:
                    content = "%s. %s" %(event.get_type_display(), utils.getMonitoringMessage(event.description, event.json_description))
                    date = "%s %s" %(event.time.strftime("%H:%M:%S"), event.date.strftime("%d.%m.%Y")) #'13:00:00 20.07.2011'
                    message = {'date': date, 'content': content}
                    messages.append(message)
            if form.cleaned_data.get("syscheck", None):
                events = syslogViews.getSyslogEvents(form.cleaned_data["syscheck"])
                for event in events:
                    date, content = syslogViews.getSyslogEventsContent(event)
                    message = {'date': date, 'content': content}
                    messages.append(message)
        else:
            data["error"] = form.errors
            logging.error(form.errors)
        max_check = mModels.Events.objects.filter(show=False).aggregate(Max('id'))
        if "id__max" in max_check: data["check"] = max_check["id__max"]
        data["syscheck"] = syslogViews.getMaxSyslogId()
        #events.update(show=True)
        data["status"] = True
        data["messages"] = messages
    except:
        logging.exception('monitoring_checkmessage: '+str(sys.exc_info()))
    return JsonResponse(data)

@tester
@permission_required('user_perms.perm_monitoring')
def export_events_journal(request):
    data = dict()
    
    result = { 'status': 'success' }
    error = False
    
    try:
        
        # events = mModels.Events.objects.filter(show=True)  был установлен фильт, считаю что это не правильно, 
        # т.к. поле show предназначено не для фильтрации по журналу а для вывода сообщений.
        # Шилов Дмитрий
        
        events_b = mModels.Events.objects.filter()
        events = []
        for event in events_b:
            events.append(event.getDict())  
        
        pages = int(len(events) / settings.EVENTS_ON_PAGE)
        if (len(events) % settings.EVENTS_ON_PAGE) > 0:
            pages += 1

        #create zip file
        fname = settings.EVENTS_EXPORT_FILENAME
        path = os.path.dirname(settings.EVENTS_EXPORT_JOURNAL_PATH)
        if not os.path.exists(path):
            os.makedirs(path)
        zip_file = settings.EVENTS_EXPORT_JOURNAL_PATH + fname
        zf = zipfile.ZipFile(zip_file, mode='w', compression=zipfile.ZIP_DEFLATED,)
        
        for p in range(pages):
            f_begin = (p * settings.EVENTS_ON_PAGE)
            f_end = (settings.EVENTS_ON_PAGE * p) + settings.EVENTS_ON_PAGE
            if p == pages:
                data["events"] = events[f_begin:len(events)]
            else:
                data["events"] = events[f_begin:f_end]
            path = os.path.dirname(zip_file)
            if not os.path.exists(path):
                os.makedirs(path)
            
            #pagination
            data["pages"] = True
            data["pagination"] = ''
            for i in range(pages):
                data["page"] = i
                data["sel_page"] = p
                data["p_name"] = i + 1
                data["pagination"] += u'%s' % render_to_string("export_events_journal.html", data)
            data["pages"] = False
            data["pagination"] = mark_safe(data["pagination"])
            
            #html
            data["journal"] = True
            data['version']=VERSION
            try:
                zf.writestr('%d.html' % p, render_to_string("export_events_journal.html", data))
            except:
                error = True
                logging.exception('add file to archive error: ' + str(sys.exc_info()))
            data["journal"] = False
    
        try:
            zf.close()
        except:
            error = True
            logging.exception('close archive error: ' + str(sys.exc_info()))
    except:
        logging.exception('export error: ' + str(sys.exc_info()))
    
    if error:
        result = { 'status': 'error' }
        
    return JsonResponse(result)
    
@tester
@permission_required('user_perms.perm_monitoring')
def download_events_journal_zip(request):
    try:
        fname = settings.EVENTS_EXPORT_FILENAME
        zip_file = settings.EVENTS_EXPORT_JOURNAL_PATH + fname
        f = open(zip_file, 'r+b')
        wrapper = f.read()
        f.close()
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Length'] = len(wrapper)
        response['Content-Disposition'] = 'attachment;filename=%s' % fname
        return response
    except:
        logging.exception('download zip error: ' + str(sys.exc_info()))
        return HttpResponseRedirect('/monitoring/')
    
from threading import Thread
class TestThread(Thread):
    max_thread = 0
    max_iteration = 0

    def __init__( self, max_thread, max_iteration):
        Thread.__init__(self)
        self.max_thread = max_thread
        self.max_iteration = max_iteration

    def run(self):
        import settings
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        command = 'python %s %s %s %s %s %s' %(os.path.join(settings.SRC_ROOT, 'self_test/thread_test_frident.py'), 
                                         os.path.join(settings.SRC_ROOT, 'self_test/'), 
                                         self.max_thread, 
                                         self.max_iteration, 
                                         HOST, 
                                         PORT) 
        logging.info(command)
        os.system(command);
        #test_dir(self.dr, self.fls, self.ti, max_thread = self.max_thread, max_iteration = self.max_iteration)


@tester
@permission_required('user_perms.perm_monitoring')
def testfr(request):
        
    if request.REQUEST.has_key('command') and not request.REQUEST.has_key('resault'): 
        if request.REQUEST['command'] == 'run':
            import self_test
            self_test.testing()
            return HttpResponse(True)
        
            path = os.path.dirname(TEST_OUTPUT)
            if not os.path.exists(path):
                os.makedirs(path)
            os.system("java -jar %s --config=%s --output=%s --tempfile=%s --coeff=%s" %(TEST_JAR, TEST_CONFIG, TEST_OUTPUT, TEST_TMP_FILE, request.REQUEST['coeff']))
        elif request.REQUEST['command'] == 'ping':
            size = request.REQUEST['size'] 
            if os.path.isfile(TEST_OUTPUT):
                size2 = os.path.getsize(TEST_OUTPUT)
                if size != 0 and size == size2:
                    return HttpResponse('True')
                return HttpResponse(size2)
        return HttpResponse('False')
    data = dict()
    data.update(vUtils.getDefaultParams(request, 'monitoring_testfr', None))
    from videoclient import settings
    coeff = vUtils.get_value_defaultparams(settings.journalBoundCoeff)
#    form = VcForms.TestFRForm(request.POST, request.FILES)
#    if form.is_valid():
#        coeff = form.cleaned_data["coeff"]
#        os.system("java -jar %s --config=%s --output=%s --tempfile=%s --coeff=%s" %(TEST_JAR, TEST_CONFIG, TEST_OUTPUT, TEST_TMP_FILE, coeff))
#        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()    
#        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
#        result = b.correlationTest(coeff)
#        logging.info(result)
#        data["result"] = result 
#    else: logging.info(form.errors)
    data["coeff"] = coeff
    data['test_output_url']= settings.TEST_OUTPUT_URL
    data.update(utils.getEventsData(request, last=True))
    #for p in data["events"]:
        #s1 = str(p["status"])
        #s1 = _(s1)
        #p["status"] = s1
        #p["get_type_display"] = s1
        #p["description"] = s1
    data.update(vUtils.dataGet(request))
    from django.template import RequestContext
    
    filename = os.path.join(settings.SRC_ROOT, 'self_test/resault.json')
    try:
        if os.path.exists(filename) :
            data["values_exists"] = True            
            f = open(filename, 'r+b')
            reads = f.read()
            logging.info(reads)
            values = json.loads(reads)
            f.close()
        else:
            values = []
    except:
        values = []
    data["values"] = values
    #if not ('all_time' in values): 
    #tr = TestThread(2, 2)
    #tr.start()
    if request.REQUEST.has_key('resault'):
        return render_to_response_ex(request, "monitoring_testfr_resault.html", data, context_instance=RequestContext(request))
    else:
        return render_to_response_ex(request, "monitoring_testfr.html", data, context_instance=RequestContext(request))


@tester
@permission_required('user_perms.perm_monitoring')
def get_upload_file(request, path):
    from videoclient.monitoring.models import Events
    
    absolute_path = 'none'
    events = Events.objects.filter(id=path)
    if events.count()>0 and events[0].error_file:
        absolute_path = events[0].error_file.path
        
    if not os.path.isfile(absolute_path):
        raise Http404
    
    f = open(absolute_path, 'r+b')
    wrapper = f.read()
    f.close()
    response = HttpResponse(wrapper, content_type='application/x-force-download')
    response['Content-Length'] = len(wrapper)
    response['Content-Disposition'] = 'attachment;filename=error.html'
    return response


@tester
@permission_required('user_perms.perm_monitoring')
def start_test(request):
    
    filename = os.path.join(settings.SRC_ROOT, 'self_test/resault.json')
    f = open(filename, 'w+b')
    f.write('{}')
    f.close()
    max_thread = request.REQUEST["max_thread"]
    max_iteration = request.REQUEST["max_iteration"]
    logging.info("start_test")
    tr = TestThread(int(max_thread), int(max_iteration))
    tr.start()
    return HttpResponse('True')


@tester
@permission_required('user_perms.perm_monitoring')
def upload_recognition(request):
    
    data = dict()
    data.update(vUtils.getDefaultParams(request, 'monitoring_identification', None))
    res = get_value_defaultparams("res_interface")
    data["res_interface"] = 0
    size = 7
    if res:
        data["res_interface"] = res
        if not data["res_interface"] == '0':
             data["res_interface"] = 11
    faces = []
    files_count = 0
    ident_count = 0
    for files_name in request.FILES:
        for file in request.FILES.getlist(files_name):
            files_count+=1
            faces.extend(save_upload_file(file.read(), str(file), size))
    data["faces"] = faces
    data["select_page"] = "monitoring_identification"
    data["was_files"] = files_count > 0
    data["files_count"] = files_count
    data["faces_count"] = len(faces)
    data["coeff"] = int(round(float(videoclient.utils.get_value_defaultparams("journalBoundCoeff"))*100))
    for face in faces:
        try:
            if face[1][0]["k"]>=data["coeff"]:
                ident_count+=1
        except: None
    data["ident_count"] = ident_count
    logging.info(data)
    
    return render_to_response_ex(request, "monitoring_upload_recognition.html", data)

def save_upload_file(data, name="", size = 7):
    from videoclient.views import TMP_DIR_FOR_UPLOAD
    from videoclient.balancer import Balancer
    import tempfile
    from PIL import Image
    
    if not os.path.isdir(TMP_DIR_FOR_UPLOAD):
        os.makedirs(TMP_DIR_FOR_UPLOAD)
        
    res = []
    images = []
    
    HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
    b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
    try:
        #res, images = b.faceDetect(data, api_version="2.0")
        res, images = b.recognize(data, size, {"answerType":"1"})
    except:
        logging.exception(str(sys.exc_info()))
        return res
    
    logging.info('res: '+str(res))
    
    if len(res)>=1:
        fileno, path = tempfile.mkstemp(dir=TMP_DIR_FOR_UPLOAD)
        f = open(path, 'w+b')
        f.write(data)
        f.close()
        
        #from django.core.urlresolvers import reverse
        filename = os.path.basename(path)
        
        import StringIO
        data_image = StringIO.StringIO(data)
        image = Image.open(data_image)
        size_x, size_y = image.size
        list = []
        for rr in res:
            r = rr[0]
            if 'face_string' not in r:
                continue
            face = r['face_string']
            i = 0
            while i < len(face): 
                face[i] = float(face[i])
                i = i+1
                
            x_min = int(min((face[0], face[2], face[4], face[6])))
            y_min = int(min((face[1], face[3], face[5], face[7])))
            x_max = int(max((face[0], face[2], face[4], face[6])))
            y_max = int(max((face[1], face[3], face[5], face[7])))
            i = i+1
            
            x_min_new = x_min - (x_max-x_min)/2 #Увеличиваем захват, берем больше фона
            if x_min_new<0:
                x_min_new=0
            x_max = x_max+x_min-x_min_new
            if x_max>size_x:
                x_max=size_x
            x_min=x_min_new                
            x_max = x_min+(x_max-x_min)/3*3
                                   
            if float(x_max-x_min)/3 > float(y_max-y_min)/4:
                add_len = (float(x_max-x_min)/3*4-(y_max-y_min))
                y_min = y_min-add_len/2
                y_max = y_max+add_len/2
               
                if y_min<0:
                    y_max = y_max-y_min
                    y_min=0
               
                if y_max>size_y:
                    y_max=size_y                    
                     
            img1 = image.crop((int(x_min), int(y_min), int(x_max), int(y_max)))
            face_string = r["face_string"]
            
            face_string[0] = float(face_string[0])-int(x_min)
            face_string[1] = float(face_string[1])-int(y_min)
            
            face_string[2] = float(face_string[2])-int(x_min)
            face_string[3] = float(face_string[3])-int(y_min)
            
            face_string[4] = float(face_string[4])-int(x_min)
            face_string[5] = float(face_string[5])-int(y_min)
            
            face_string[6] = float(face_string[6])-int(x_min)
            face_string[7] = float(face_string[7])-int(y_min)
            
             
            face_string[9] = float(face_string[9])-int(x_min)
            face_string[10] = float(face_string[10])-int(y_min)
            
            
            face_string[12] = float(face_string[12])-int(x_min)
            face_string[13] = float(face_string[13])-int(y_min)
            
            
            face_string[15] = float(face_string[15])-int(x_min)
            face_string[16] = float(face_string[16])-int(y_min)
            
            
            face_string[18] = float(face_string[18])-int(x_min)
            face_string[19] = float(face_string[19])-int(y_min)
            
            i = 0
            while i<len(face_string):
                face_string[i] = str(face_string[i])
                i = i + 1
            
            r["face_string"] = face_string
            r["full_face"] = ','.join(face_string)
            #img1.thumbnail((120,120))
            
            fileno, path_face = tempfile.mkstemp(dir=TMP_DIR_FOR_UPLOAD)
            img1.save(path_face, 'PNG')
            
            face_width, face_height = img1.size
            
            filename_face = os.path.basename(path_face)
            r["filename"] = filename
            r["url_photo"] = reverse('get_upload_image', args=[filename])
            r["filename_face"] = filename_face
            r["url_photo_face"] = reverse('get_upload_image', args=[filename_face])
            r["face_width"] = face_width
            r["face_height"] = face_height
            if(float(face_string[9])<1 and float(face_string[10])<1 and float(face_string[12])<1 and float(face_string[13])<1):
                r["face_dist"] = int(round(getPointsDistance(face_string[9],face_string[10],face_string[12],face_string[13])*getPointsDistance(face_string[0],face_string[1],face_string[2],face_string[3])))
            else:
                r["face_dist"] = int(round(getPointsDistance(face_string[9],face_string[10],face_string[12],face_string[13])))
            if face_width>face_height :
                r["size_width"] = "120px"
                r["size_height"] = ""
            else:
                r["size_width"] = ""
                r["size_height"] = "120px"
                
            persons = rr[1]
            
            from videoclient.models import PersonId
            for r2 in persons:
                images = []
                r2["k"] = ((float(r2["rang"])*100))
                try:
                    images, params = b.getPersonPhotoWithParams(r2["id"], str(int(r2["image"])))
                    imageP = images[0]
                    img = Image.open(StringIO.StringIO(imageP))
                    fileno, path_face = tempfile.mkstemp(dir=TMP_DIR_FOR_UPLOAD)
                    face_width, face_height = img.size
                    img.save(path_face, 'PNG')
                    filename_face = os.path.basename(path_face)
                    eyes = params["response"][0]["info"][0]["eyes"].split(',')
                    dist = int(round(getPointsDistance(eyes[0],eyes[1],eyes[2],eyes[3])))
                    try:
                        r2["face_string"] = params["response"][0]["info"][0]["quad"]+',0,'
                    except:
                        r2["face_string"] = '0,0,0,0,0,0,0,0,0,'
                    try:
                        r2["face_string"] += str(eyes[0])+','+str(eyes[1])+',0,'+str(eyes[2])+','+str(eyes[3])+',0,'
                    except:
                        r2["face_string"] += '1,1,0,1,1,0,'
                    try:
                        r2["face_string"] += params["response"][0]["info"][0]["nose"]+',0'#+params["response"][0]["info"][0]["chin"]+',0'
                    except: None
                    try:
                        r2["face_string"] += ',' + params["response"][0]["info"][0]["chin"]
                    except: None
                    r2["face_dist"] = dist
                    r2["filename_face"] = filename_face
                    r2["face_width"] = face_width
                    r2["face_height"] = face_height
                    r2["url_photo_face"] = reverse('get_upload_image', args=[filename_face])
                except:
                    r2["url_photo_face"] = ""
                    images = []
                    logging.exception("upload_recognition get photo "+str(sys.exc_info()))
                try:
                    person = PersonId.objects.get(bal_id = int(r2["id"]))
                    try:
                        division = person.person.status.division.id
                        if division == settings.division_visitor: division = "/anketavisitor/"+str(person.person.id)+"/"
                        if division == settings.division_employee: division = "/anketastaff/"+str(person.person.id)+"/"
                        if division == settings.division_person: division = "/anketaperson/"+str(person.person.id)+"/"
                        if division == settings.division_auto: division = "/anketaauto/"+str(person.person.id)+"/"
                        division += "?group="+str(person.person.group.id)
                    except:
                        logging.exception("upload_recognition get division info "+str(sys.exc_info()))
                        division = '#'
                    #info = person.person.getDict()
                    info = {"fio": person.get_fio()}
                    if info.has_key("id_person"):
                        r2['person_info'] = {"fio":info["fio"], "fio_small":info["fio"], "person_id":division}
                    else:
                        r2['person_info'] = {"fio":info["fio"], "fio_small":info["fio"], "person_id":division}
                    if len(info["fio"])>18:
                        r2['person_info']["fio_small"] = '%s...' % info["fio"][:15]
                except:
                    logging.exception("upload_recognition get person info "+str(sys.exc_info()))
                    r2['person_info'] = {"fio":r2["id"], "fio_small":"", "person_id":"#"}
    b.close()
    del b
    return res

def getPointsDistance(x1,y1,x2,y2):
    return math.sqrt((float(x1)-float(x2))*(float(x1)-float(x2))+(float(y1)-float(y2))*(float(y1)-float(y2)))
#for uploading & recognition   ---- END