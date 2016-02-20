#coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from videoclient.updates import updates as updates_sql
from videoclient import updates
from optparse import make_option
import settings
import sys
import os

def clear_dir(path):
    try:
        command = 'rm %s* -f -R' %path
        print command
        os.system(command)
    except:
        print "Error: "+str(sys.exc_info()) 

class Command(BaseCommand):
    args = "[all|journal]"

    def handle(self, *args, **options):
        if len(args) == 0:
            return
        first_parameter = args[0]
        if first_parameter == "journal":
            updates_sql.execute_sql("drop table videoclient_journal;\ndrop table videoclient_journalagregate;");
            clear_dir(os.path.join(settings.WWW_ROOT, 'files/journal/'))
            updates.run_syncdb()
        elif first_parameter == "all":
            from django.contrib.auth.models import User as AuthUser
            is_cash = True
            try:
                user = AuthUser.objects.get(id=1)
                username = user.username
                password = user.password
            except AuthUser.DoesNotExist:
                is_cash = False
                username = 'admin'
                password = 'eghfdkz.ofz cbcntvf'
                
            updates_sql.execute_sql("drop database sa;\ncreate database sa;");
            clear_dir(settings.TEMPORARY_FOLDER)
            clear_dir(settings.VIDEO_CLIP_PATH)
            clear_dir(settings.PERMANENT_FILES)
            clear_dir(settings.LEARNING_IMAGES)
            clear_dir(settings.LOGDETECT_IMAGES)
            clear_dir(settings.MAP_IMAGES)
            
            clear_dir(settings.EVENTS_EXPORT_JOURNAL_PATH)
            clear_dir(settings.EXPORT_PATH)
            clear_dir(os.path.join(settings.PROJECT_ROOT, 'log/'))
            clear_dir(os.path.join(settings.WWW_ROOT, 'files/journal/'))
            
            updates.check_version()
            from videoclient import initbase as videoclient_initbase
            videoclient_initbase.InitBase()
            from videoclient.videoarchive import initbase as videoarchive_initbase
            videoarchive_initbase.InitBase()
            
            try:
                from django.contrib.auth.models import User as AuthUser
                user, create = AuthUser.objects.get_or_create(username=username)
                if create:
                    user.is_staff = True
                    user.is_active = True
                    user.is_superuser = True
                    if is_cash:
                        user.password = password
                        print "is_cash"
                    else:
                        print "is_not_cash"
                        user.set_password(password)
                    print password
                    user.save()
                print "User was add"
            except:
                print "User Error: %s" %str(sys.exc_info())
