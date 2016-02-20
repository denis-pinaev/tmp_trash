from django.db import models
from django.conf import settings
from django.db.models import ImageField, signals
from django.dispatch import dispatcher
from sim import settings

def get_upload_to( instance, filename):
    from sim.util import get_store_path
    return "%s%s%s/%s" % (settings.STORED_IMG, settings.STORE_PHOTO_PATH, get_store_path(filename), filename)

def get_upload_to_tmp( instance, filename):
    from sim.util import get_store_path
    return "%s%s%s/%s" % (settings.TMP_IMG, settings.TMP_PHOTO_PATH, get_store_path(filename), filename)


UPLOAD_URL = settings.UPLOAD_URL
UPLOAD_COMP = settings.UPLOAD_COMP
UPLOAD_CAM = settings.UPLOAD_CAM

class StoredImage( models.Model):
    user = models.PositiveIntegerField( default=0)
    dt_open = models.DateTimeField( auto_now=True, auto_now_add=True)
    image = ImageField( upload_to=get_upload_to)
    code = models.CharField( max_length=64, unique=True)
    mark = models.IntegerField( default=0)
    def __unicode__(self):
        return u'%s' % (self.user)

class TmpImage( models.Model):
    user = models.PositiveIntegerField( default=0)
    dt_open = models.DateTimeField(auto_now=True, auto_now_add=True)
    image = ImageField( upload_to=get_upload_to_tmp)
    code = models.CharField( max_length=64, unique=True)
    def code_exists(self):
        code = gen_code() 
    def __unicode__(self):
        return u'%s' % (self.user)

def gen_code():
    import random, hashlib, time
    return hashlib.sha1(
	str(time.time()) + 
	str(random.random())
	).hexdigest()

def gen_tmp_code():
    code = gen_code()
    while TmpImage.objects.filter(code = code).count() > 0:
        code = gen_code()

    return code

def gen_image_code():
    code = gen_code()
    while StoredImage.objects.filter(code = code).count() > 0:
        code = gen_code()

    return code

class Archive( models.Model):
    id_user = models.IntegerField()
    file_name = models.CharField( max_length=128, null=True)
    result_detect = models.TextField( null = True)
    comment = models.TextField( null = True)
    count_face = models.IntegerField()
    count_not_face = models.IntegerField()
    date_work = models.DateTimeField()
    time_work = models.FloatField()
    permit_photo = models.CharField( max_length=128)
    format_photo = models.CharField( max_length=128)
    system_id = models.CharField( max_length=128)
    video_id = models.CharField( max_length=128, null=True)
    op_id = models.CharField( max_length=128, null=True)
