#coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from videoarchive import updates

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args)>0:
            try:
                v, b, r = args[0].split('.')
            except:
                v, b, r = None, None, None 
                logging.exception("command update: "+str(sys.exc_info()))
            updates.check_version(v, b, r)
        else:
            updates.check_version()
