#coding=utf-8

import models
import utils
import updates 
from videoclient.settings import log_videoarchive as logging
import sys
from django.core.management.commands import syncdb
from videoarchive.management.commands import archive_initbase as initbase

NO_UPDATE_FOUND = "No update found"

def run_syncdb():
    print "syncdb"
    command = syncdb.Command()
    command.handle_noargs()
    
def run_initbase():
    print "initbase"
    command = initbase.Command()
    command.handle()
    

def update(v, b, r):
    try:
        if not (v is not None and b is not None and r is not None):
            print NO_UPDATE_FOUND
            return False
        
        print "version: %s.%s.%s" %(v, b, r)
        v, b, r = eval("updates._%s_%s_%s()" %(v, b, r))
        models.Version.objects.create(version = v, branch = b, revision = r)
        return True
    except AttributeError:
        print "No update found"
    except:
        print "Error: "+str(sys.exc_info())
    return False

def check_version(v=None, b=None, r=None):
    try:
        versions = models.Version.objects.all().order_by('-id')
        if versions.count() == 0:
            models.Version.objects.create(version = v, branch = b, revision = r)
            versions = models.Version.objects.all().order_by('-id')
            
        version = versions[0]
        
        try:
            v = version.version if v == None else v
            b = version.branch if b == None else b
            r = version.revision if r == None else r
        except:
            print "Incorrect version"        
        
    except:
        pass
    
    if (str(v) == str(utils.VERSION_PREFIX) and str(b) == str(utils.BRANCH) and str(r) == str(utils.REVISION)):
        print "No update found"
        return 0
    
    run_syncdb()
    
    while not (str(v) == str(utils.VERSION_PREFIX) and str(b) == str(utils.BRANCH) and str(r) == str(utils.REVISION)):
        if update(v, b, r):
            versions = models.Version.objects.all().order_by('-id')
            version = versions[0]
            v = version.version
            b = version.branch
            r = version.revision
        else:
            break
        
    run_initbase()
