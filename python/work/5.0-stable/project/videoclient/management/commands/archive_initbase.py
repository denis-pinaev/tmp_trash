#coding=utf-8

from django.core.management.base import BaseCommand
from videoarchive import initbase

class Command(BaseCommand):

    def handle(self, *args, **options):
        initbase.InitBase()
        