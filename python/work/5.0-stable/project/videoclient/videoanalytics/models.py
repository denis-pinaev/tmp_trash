#coding=utf-8

from django.db import models
from videoclient.communicator import models as vcModels
from videoclient import settings
from django.utils.translation import ugettext as _

#def get_journal_upload_to(instance, filename):
#    from time import time
#    import datatime
#    now = datatime.datetime.now()
#    fname = "%s/%s/%s/%s/%s.jpg" %(now.year, now.month, now.day, now.hour, int(time()))
#    #fname = '%s.jpg' % int(time())
#    return settings.LOGDETECT_IMAGES + fname

def get_journal_upload_to(instance, filename):
    return getModelFileNameByFileName(filename)

def getDetectsFileNameByFileName(filename):
    return "detects%s" % (filename)

class Detector(models.Model):
    name = models.CharField( max_length = 250, null=False)
    dtype = models.CharField( max_length = 250, null=False, unique=True)

class DetectorLog(models.Model):
    #camera = models.ForeignKey(Camera, null=True, verbose_name=u'Камера')
    dt_detect = models.DateTimeField( auto_now=True, auto_now_add=True, verbose_name=u'Время детекта', db_index=True)
    camera = models.ForeignKey(vcModels.Camera, null=True, verbose_name=u'Камера')
    frame = models.ImageField( upload_to=get_journal_upload_to)
    preview = models.ImageField( upload_to=get_journal_upload_to)
    detector_type = models.ForeignKey(Detector, null=True, verbose_name=u'Детектор')
    description = models.TextField(blank=True, null=True)
    json_data = models.TextField(default=None, null=True)
    #camera_name = models.CharField( max_length = 250, null=False)
    #camera_type = models.CharField( max_length = 250, null=False)
    #detect_type = models.CharField( max_length = 250, null=False)
    orig_width = models.IntegerField(null=True)
    orig_height = models.IntegerField(null=True)

    def __unicode__(self):
        return self.camera.ip
