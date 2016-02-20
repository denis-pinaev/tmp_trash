#coding=utf-8

from django.core.management.base import BaseCommand
from videoarchive import utils

class Command(BaseCommand):

    def handle(self, *args, **options):
        print utils.VERSION
        #models.Version.objects.create(version = utils.VERSION_PREFIX, branch = utils.BRANCH, revision = utils.REVISION)