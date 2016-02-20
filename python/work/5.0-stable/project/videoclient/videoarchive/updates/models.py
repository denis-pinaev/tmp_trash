#codion=utf-8

from django.db import models

class Version(models.Model):
    version = models.IntegerField(null = False)
    branch = models.IntegerField(null = False)
    revision = models.IntegerField(null = False)
    dt_change = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    class Meta: 
        db_table = u'videoarchive_updates_version'