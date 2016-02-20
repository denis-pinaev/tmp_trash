from django.db import models
from django.conf import settings
from django.db.models import ImageField, signals
from django.dispatch import dispatcher
import settings
from sim.fb.models import gen_code, get_store_path

"""
def get_upload_to( instance, filename):
    from sim.util import get_store_path
    return "%sstore/%s/%s" % (settings.STORE_IMG, get_store_path(filename), filename)
"""
def get_upload_to_tmp( instance, filename):
    #from sim.util import get_store_path
    return "%stmp/%s/%s" % (settings.TMP_IMG, get_store_path(filename), filename)


UPLOAD_URL = 0
UPLOAD_COMP = 1
UPLOAD_CAM = 2


class StoredImage( models.Model):
    user = models.CharField(max_length = 30,  default=0)
    dt_open = models.DateTimeField( auto_now=True, auto_now_add=True)
    image = ImageField( upload_to=get_upload_to_tmp)
    code = models.CharField( max_length=64, unique=True)
    mark = models.IntegerField( default=0)
    def __unicode__(self):
        return u'%s' % (self.user)

class TmpImage( models.Model):
    user = models.CharField(max_length = 30, default=0)
    dt_open = models.DateTimeField( auto_now=True, auto_now_add=True)
    image = ImageField( upload_to=get_upload_to_tmp, max_length=128)
    code = models.CharField( max_length = 64, unique=True)
    def code_exists(self):
        code = gen_code() 
    def __unicode__(self):
        return u'%s' % (self.user)

"""
def gen_code(format=".jpg"):
    import random, hashlib, time
    return hashlib.sha1(
	str(time.time()) + 
	str(random.random())
	).hexdigest()+format
"""

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

