#coding=utf-8

from django.core.management.base import BaseCommand
import utils

class Command(BaseCommand):

    def handle(self, *args, **options):
        print utils.VERSION
