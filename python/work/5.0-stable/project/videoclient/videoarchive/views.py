# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

from django.contrib import auth
from videoclient.settings import log_videoarchive as logging
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from videoarchive import utils
from videoclient import utils as cUtils
from videoclient import settings
import json
from videoclient.views import tester
from django.contrib.auth.decorators import permission_required

SVN_REVISION = '$Revision: 5539 $'#
#REVISION = max([utils.getRevision(SVN_REVISION), utils.getRevision(utils.REVISION)])
REVISION = utils.REVISION
VERSION_PREFIX = settings.VERSION_PREFIX
BRANCH = settings.BRANCH
VERSION = '%s.%s.%s' %(VERSION_PREFIX, BRANCH, REVISION)
def check_version():
    from updates import models as uModels
    versions = uModels.Version.objects.all().order_by('-id')
    if versions.count() == 0:
        uModels.Version.objects.create(version = VERSION_PREFIX, branch = BRANCH, revision = REVISION)
        
check_version()

import os
import sys
import codecs
import locale, codecs; locale.setlocale(locale.LC_ALL, '')
encoding = locale.getlocale()[1]
encoding = "utf-8"
reload(sys);
sys.setdefaultencoding(encoding)
sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

class LoginForm(forms.Form):
    login = forms.CharField(required=True) #max_length=30, 
    password = forms.CharField(required=True)
    
@tester
def start_processes(request):
    utils.checkTasks()
    
    return HttpResponse('start_processes');

@tester
@permission_required('user_perms.perm_videoarchive')
def pages(request, path=None):

    params = path.split('/')
    params.extend([None, None, None, None, None])
    page = params[0].replace("page_", "")
    data = dict()
    data.update(utils.getDefaultParams(request, "page_%s" %page))
    data.update({'version': VERSION})
    if page == "task": data.update(utils.getPageTask(request, params[1]))
    if page == "task_cameras": data.update(utils.getPageTaskCameras(request, params[1]))
    elif page == "tasks": data.update(utils.getPageTasks(request))
    elif page == "camera_resolution": data.update(utils.getCameraResolutions(request))
    elif page == "copy_task": 
        data.update(utils.getPageCopyTask(request, params[1]))
        data['action'] = utils.ACTION_CREATE
        data["copy"] = True
        page = "task"
    elif page == "user": data.update(utils.getPageUser(request, params[1]))
    elif page == "video_faces": data.update(utils.getPageFaces(request, params[1]))
    elif page == "video_persons": data.update(utils.getPageRollerPersons(request, params[1]))
    elif page == "users": data.update(utils.getPageUsers(request))
    elif page == "persons": data.update(utils.getPagePersons(request, params[1]))
    elif page == "records": data.update(utils.getPageRecords(request))
    elif page == "calendar": data.update(utils.getPageCalendar(request))
    elif page == "tables_video": data.update(utils.getPageTablesVideo(request, params[1]))
    elif page == "journal": data.update(utils.getPageJournal(request))
    elif page == "video": data.update(utils.getPageVideo(request))
    elif page == "analysis": data.update(utils.getPageAnalysis(request))
    elif page == "view_video": data.update(utils.getPageViewVideo(request, params[1]))
    elif page == "view_detail_video": data.update(utils.getPageViewDetailVideo(request, params[1]))
    elif page == "cameras": return HttpResponseRedirect(reverse("archive_page", args=["page_interface/"]))
    elif page == "monitor": data.update(utils.getPageMonitor(request))    

    if data.has_key('redirect'):
        return HttpResponseRedirect(data['redirect'])
    else:
        return render_to_response('page_%s.html' %page, data, context_instance=RequestContext(request))
    
def JsonResponse(data):
    return HttpResponse(json.dumps(data), mimetype="application/json")

@tester
@permission_required('user_perms.perm_videoarchive')
def command(request, path=None):
    
    logging.info(path)
    params = path.split('/')
    params.extend([None, None, None, None, None])
    command = params[0]

    data = dict()
    if command == "roller_data": data.update(utils.getRollerData(request))
    elif command == "rollers_data": data.update(utils.getRollersData(request))
    elif command == "roller_url": data.update(utils.getRollerUrl(request))    
    elif command == "kill_processes": data.update(utils.getKillProcessesData(request, params[1]))
    elif command == "is_active_processes": return HttpResponse(utils.chackActiveProcesses(request, params[1]))
    elif command == "delete_rollers": data.update(utils.getDeleteRollersData(request))
    elif command == "delete_all_rollers": data.update(utils.getDeleteAllRollersData(request))
    elif command == "delete_rollers_for_period": data.update(utils.getDeleteAllRollersForPeriod(request))    
    #elif command == "delete_users": data.update(utils.getDeleteUsersData(request))
#    elif command == "add_cameras": data.update(utils.getAddCameras(request))
#    elif command == "delete_cameras": data.update(utils.getDeleteCameras(request))
    #elif command == "tables_data": data.update(utils.getTablesData(request))
    #elif command == "page_cameras": data.update(utils.getPageCameras(request, all_cameras = False))
    #elif command == "rename_camera": data.update(utils.getRenameCamera(request))
    elif command == "import_roller": data.update(utils.getImportRoller(request))
    elif command == "info_roller": data.update(utils.getInfoRoller(request))
    elif command == "set_daemon_settings": data.update(utils.setDaemonSettings(request))
    elif command == "set_default_archive_settings": data.update(utils.setDefaultArchiveSettings(request))
    elif command == "save_rollers": data.update(utils.getSaveRollers(request))
    elif command == "save_video_with_face": data.update(utils.getSaveRollerWithFace(request))
    elif command == "delete_tasks": data.update(utils.getDeleteTasksData(request))
    elif command == "process_roller": data.update(utils.getProcessRollerData(request))
    elif command == "set_rosolution_interface": data.update(utils.setResolutionInterface(request))
    elif command == "get_camera_info": data.update(utils.getCameraInfo(request))
    elif command == "check_task_name": data.update(utils.checkTaskname(request))
    elif command == "info_roller_import": data.update(utils.getInfoRollerImport(request))
    elif command == "get_video_faces_count": data.update(utils.getVideoCountFace(request, params[1]))
    elif command == "start_task": data.update(utils.startTask(request, params[1]))
   
    return JsonResponse(data)



#class FileWrapper(object):
#    def __init__(self, wrapper):
#        self.fileno, self.path = tempfile.mkstemp()
#        f = open(self.path, 'w+b')
#        f.write(wrapper)
#        f.close()
#        f = open(self.path, 'rb')
#        self.File = File(f)
#    def __del__(self):
#        os.remove(self.path)

@tester
def gettmpfile(request):
    try:
        if not request.REQUEST.has_key('name'):
            logging.info('has_key(name)')
            raise Http404
                   
        tarname = request.REQUEST['name']
        alias = tarname
        if request.REQUEST.has_key('alias') and request.REQUEST['alias']:
            alias = request.REQUEST['alias']
        
        if not os.path.isfile(tarname):
            logging.info('not os.path.isfile(tarname)')
            raise Http404
        
        ftar = open(tarname, 'r+b')
        datatar = ftar.read()
        ftar.close()
        response = HttpResponse(datatar, content_type='application/x-tar') # 
        response['Content-Length'] = len(datatar)
        response['Content-Disposition'] = 'attachment;filename=%s' % (alias)
        response['Content-Encoding'] = 'x-bzip2'
        
        os.unlink(tarname)
        
        return response
    except:
        logging.exception("exportfile: "+str(sys.exc_info()))
        raise Http404
    
@tester
def DownloadVideo(request, id=None):
    try:
        from videoarchive.va import models as vaModels
        import urllib
           
        if not id: return Http404       
        roller = get_object_or_404(vaModels.VaRoller, pk=int(id))

        url_prefix = roller.id_command.id_archive.url
        if not 'http:' in url_prefix:
            url_prefix = "http://%s%s" %(roller.id_command.id_archive.ip, url_prefix)
        url = "%sfiles/video%s" %(url_prefix, roller.location)
        
        f = urllib.urlopen(url)
        wrapper = f.read()
        f.close()
        response = HttpResponse(wrapper, content_type='video/x-msvideo')
        response['Content-Length'] = len(wrapper)
        response['Content-Disposition'] = 'attachment;filename=%s' % (os.path.basename(roller.location))
        return response
    except:
        logging.exception(sys.exc_info())
    return Http404
