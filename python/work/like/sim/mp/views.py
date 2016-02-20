from django import forms
from django.http import *
from django.shortcuts import *
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django import forms
from django.conf import settings
from django.db.models import Avg, Max, Min, Count
from django.core import serializers
from django.utils.html import strip_tags, escape
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os.path, os
import json
from django.template import RequestContext
from sim.models import *
from smilart.fanstudio import FanStudio

def iframe(request):
    from operator import itemgetter
    from sim.util import get_absolute
    params = dict()
    if request.GET.has_key('post_id'):
	code = request.REQUEST['post_id']
        image = StoredImage.objects.get(code=code)
        return render_to_response( "post.html", {'post_id': code,
    	    'app_url': 'http://ya.ru', 'image_url': get_absolute(image.image.url)})
    for p in request.GET.iteritems():
	params[ p] = itemgetter(0)
	return render_to_response( "iframe.html", {'flashvars':params})


from sim import util
from sim import settings

from vkontakte.forms import VKontakteForm
SUCCESS = settings.SUCCESS
ERROR_FORM = settings.ERROR_FORM

UPLOAD_VK = settings.UPLOAD_VK
UPLOAD_COMP = settings.UPLOAD_COMP

PREVIEW_ROOT=settings.PREVIEW_ROOT
STAR_PHOTO_PATH=settings.PHOTOS_FULL_PATH

def get_preview( root, path, size):    
    import magick_effect
    
    preview_path = settings.MEDIA_URL + PREVIEW_ROOT + path
    if not os.path.lexists( settings.MEDIA_ROOT + preview_path):
        original_path = settings.WWW_ROOT + root + path
        res = magick_effect.initEffect(original_path)
        w, h = size
        res = magick_effect.execEffect('thumbnail', w , h)
        full_preview_path = settings.WWW_ROOT + preview_path
        preview_dir = os.path.dirname( full_preview_path)
        if not os.path.lexists( preview_dir):
    	    os.makedirs( preview_dir)

    	if res == 1:
    	    magick_effect.writeEffect(full_preview_path)

    return preview_path

def json_response( data):
    return HttpResponse( json.dumps( data))
    
class ImageUploadForm( VKontakteForm):
    image = forms.ImageField()
    itype = forms.IntegerField( required=False)
    def clean_image(self):
        max_size = 8 * 2**20 #8Mb
        image = self.cleaned_data.get('image')
        if len(image) > max_size:
            raise forms.ValidationError( 'too large image')
        else:
            return image

def upload(request):
    from smilart import fanstudio
    form = ImageUploadForm( request.REQUEST, request.FILES)
    if not form.is_valid():
        return json_response( {"status": ERROR_FORM, "message": str( form.errors)})

    code = gen_tmp_code()
    viewer = form.cleaned_data['viewer']
    uploadedImage = form.cleaned_data['image']
    itype = form.cleaned_data['itype']
    
    img = TmpImage( code = code, user = viewer)
    if itype:
	img = StoredImage( code = code, user = viewer, mark = UPLOAD_VK)
	
    img.image.save( code, uploadedImage)
    img.save()
    
    f=FanStudio()
    return json_response( 
	{
	"status": SUCCESS, 
	"url": util.get_absolute( img.image.url),
	"url_small": util.get_absolute(get_preview( "", img.image.url, (120, 160) )),
	"code": code,
    "faces": f.face_detect(util.get_absolute(img.image.url))
	}
    )

class UploadFromUrlForm( VKontakteForm):
    url = forms.URLField( required=True)
    itype = forms.IntegerField( required=False)

def upload_url (request):
    from smilart import fanstudio
    import os,sys, urllib2
    from sim import settings
    from django.core.files import File

    form = UploadFromUrlForm( request.REQUEST, request.FILES)
    if not form.is_valid():
        return json_response( {"status": ERROR_FORM, "message": str( form.errors)})

    viewer = form.cleaned_data['viewer']
    url =  form.cleaned_data['url']
    itype = form.cleaned_data['itype']
        
    loader = util.FileLoader(url)
    code = gen_image_code()
    
    img = TmpImage( code = code, user = viewer)
    if itype:
	img = StoredImage( code = code, user = viewer, mark = UPLOAD_VK)
    img.image.save( code, loader.File)
    img.save()

    f=FanStudio()
    data = {
	"status": SUCCESS,
	"url": util.get_absolute( img.image.url),
	"url_small":  util.get_absolute(get_preview( "", img.image.url, (120, 160) )),
	"code": code,
    "faces": f.face_detect( util.get_absolute(img.image.url))
    }

    return json_response(  json.dumps( data))

class ProcessForm( VKontakteForm):
    code = forms.CharField(required=True)
    itype = forms.IntegerField( required=False)

def process( request):
    from smilart import fanstudio

    form = ProcessForm( request.REQUEST, request.FILES)
    if not form.is_valid():
        return json_response( {"status": ERROR_FORM, "message": str( form.errors)})
    code = form.cleaned_data['code']
    itype = form.cleaned_data['itype']

    img = get_object_or_404( TmpImage, code = code)

    if itype:
        img = get_object_or_404( StoredImage, code = code)
    f = FanStudio()    
    result_str = f.recognize( img.image.path)
    result = result_str.split(' ')
    l = []
    i = 0
#    while i < len(result)-1:
#        try:
#            e = {}
#            name = result[i]
#            e['name'] = name.replace( '_', ' ').strip()
#            e['coeff'] = int(100*float(result[i+2]))
#            e['url'] = util.get_absolute( settings.MEDIA_URL + STAR_PHOTO_PATH + result[i+1])
#            e['url_small'] = util.get_absolute(get_preview( settings.MEDIA_URL + STAR_PHOTO_PATH, result[i+1], (60, 80) ))
#            l.append(e)
#        except:
#            None
#        i = i + 3

    data = {"result": l, "status": SUCCESS}

    return json_response( data)

