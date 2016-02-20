from django import forms
from django.http import *
from django.shortcuts import *
import json
from sim.models import *
from sim import util
from sim import settings
from vkontakte.forms import VKontakteForm
SUCCESS = 0
ERROR_FORM = 1

UPLOAD_VK = 0
UPLOAD_COMP = 1

PREVIEW_ROOT="preview/"
STAR_PHOTO_PATH="photos/full"
#import logging

def get_preview( root, path, size):
    import os.path, os
    #import Image
    import magick_effect
    
    preview_path = settings.MEDIA_URL + PREVIEW_ROOT + path
    if not os.path.lexists( settings.MEDIA_ROOT + preview_path):
        original_path = settings.WWW_ROOT + root + path
        res = magick_effect.initEffect(original_path)
        #logging.debug(original_path)
        w, h = size
        res = magick_effect.execEffect('thumbnail', w , h)
        #logging.debug(res)
            
        #image = Image.open( original_path)
        #image.thumbnail( size, Image.BICUBIC)
        full_preview_path = settings.WWW_ROOT + preview_path
        preview_dir = os.path.dirname( full_preview_path)
        if not os.path.lexists( preview_dir):
    	    os.makedirs( preview_dir)

    	if res == 1:
    	    magick_effect.writeEffect(full_preview_path)
    	    #logging.debug(full_preview_path)
    	    

        #image.save( full_preview_path, "JPEG")
    return preview_path
    
def thumb_image(path, w, h):
    import magick_effect
    res = magick_effect.initEffect(path)
    res = magick_effect.execEffect('thumbnail', w , h)
    if res == 1:
	magick_effect.writeEffect(path)



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
    url_r = util.get_absolute(img.image.url)
    if itype:
	w, h = 360, 760
	thumb_image(settings.WWW_ROOT + img.image.url, w, h)
        

    return json_response(
	{
	"status": SUCCESS, 
	"url": util.get_absolute(img.image.url),
	"url_small": util.get_absolute(get_preview( "", img.image.url, (120, 160) )),
	"code": code
	}
    )

class UploadFromUrlForm( VKontakteForm):
    url = forms.URLField( required=True)
    itype = forms.IntegerField( required=False)

def upload_url (request):
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
    

    data = {
	"status": SUCCESS,
	"url": util.get_absolute( img.image.url),
	"url_small":  util.get_absolute(get_preview( "", img.image.url, (120, 160) )),
	"code": code}

    return json_response(  json.dumps( data))

class ProcessForm( VKontakteForm):
    code = forms.CharField(required=True)
    itype = forms.IntegerField( required=False)

def process( request):
    from smilart import similarity

    form = ProcessForm( request.REQUEST, request.FILES)
    if not form.is_valid():
        return json_response( {"status": ERROR_FORM, "message": str( form.errors)})
    code = form.cleaned_data['code']
    itype = form.cleaned_data['itype']

    img = get_object_or_404( TmpImage, code = code)

    if itype:
        img = get_object_or_404( StoredImage, code = code)
    result_str = similarity.get_similar( img.image.path)
    result = result_str.split(' ')
    l = []
    i = 0
    while i < len(result)-1:
#        try:
        e = {}
        name = result[i]
        e['name'] = name.replace( '_', ' ').strip()
        e['coeff'] = int(100*float(result[i+2]))
        e['url'] = util.get_absolute( settings.MEDIA_URL + STAR_PHOTO_PATH + result[i+1])
        e['url_small'] = util.get_absolute(get_preview( settings.MEDIA_URL + STAR_PHOTO_PATH, result[i+1], (60, 80) ))
        l.append(e)
#        except:
#            None
        i = i + 3

    data = {"result": l, "status": SUCCESS}

    return json_response( data)

