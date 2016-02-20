#coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from videoclient import updates
import logging
import sys

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args)>0:
            try:
                versions = args[0].split('.')
                if len(versions) == 3:
                    r = versions[2]
                elif len(versions) == 1:
                    r = versions[0]
                else:
                    r = 0 
            except:
                r = 0
                logging.exception("command update: "+str(sys.exc_info()))
            updates.check_version(r)
        else:
            updates.check_version()
