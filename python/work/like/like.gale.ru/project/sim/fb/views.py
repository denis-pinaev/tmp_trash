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

import json
from django.template import RequestContext
from sim.models import *

from sim import util
from sim import settings

from vkontakte.forms import VKontakteForm
from smilart.similarity import Similarity
SUCCESS = 0
ERROR_FORM = 1

UPLOAD_VK = 0
UPLOAD_COMP = 1

PREVIEW_ROOT="preview/"
STAR_PHOTO_PATH="photos.like/"

def get_preview( root, path, size, out_path = ''):
    import os.path, os
    import magick_effect
    
    if out_path == '':
        preview_path = settings.MEDIA_URL + PREVIEW_ROOT + path
        full_preview_path = settings.WWW_ROOT + preview_path
    else:
        preview_path = out_path.replace('.jpg', '_%dx%d.jpg' % size);
        full_preview_path = settings.WWW_ROOT + root + preview_path
    #if not os.path.lexists( settings.MEDIA_ROOT + preview_path):
    if not os.path.lexists( full_preview_path):
        original_path = settings.WWW_ROOT + root + path
        res = magick_effect.initEffect(original_path)
        w, h = size
        res = magick_effect.execEffect('thumbnail', w , h)
        #full_preview_path = settings.WWW_ROOT + preview_path
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

    f = Similarity()
    return json_response( 
	{
	"status": SUCCESS, 
	"url": util.get_absolute( img.image.url),
	"url_small": util.get_absolute(get_preview( "", img.image.url, (120, 160) )),
	"code": code,
	"faces": f.face_detect( img.image.path, viewer, uploadedImage)
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

    f = Similarity()
    import settings
    data = {
	"status": SUCCESS,
	"url": util.get_absolute( img.image.url),
	"url_small":  util.get_absolute(get_preview( "", img.image.url, (120, 160) )),
	"code": code,
	#"faces": f.face_detect( util.get_absolute(img.image.url), viewer, None)
    "faces": f.face_detect( settings.WWW_ROOT + img.image.url, viewer, None)
    }

    return json_response(data)

class ProcessForm( VKontakteForm):
    code = forms.CharField(required=True)
    itype = forms.IntegerField( required=False)

def process( request):
    form = ProcessForm( request.REQUEST, request.FILES)
    if not form.is_valid():
        return json_response( {"status": ERROR_FORM, "message": str( form.errors)})
    code = form.cleaned_data['code']
    itype = form.cleaned_data['itype']
    
    img = get_object_or_404( TmpImage, code = code)

    if itype:
        img = get_object_or_404( StoredImage, code = code)
    
    f = Similarity()
    res = f.recognize(img.image.path)
        
    from smilart.balancer import Balancer
    import smilart.similarity
    
    #return HttpResponse('OK')

    #b = Balancer(smilart.similarity.FS_HOST, smilart.similarity.FS_PORT, smilart.similarity.FS_LOGIN, smilart.similarity.FS_PASSWD, smilart.similarity.FS_USER)
            
    l = []
    i = 0
    res_count = 0
    res_max = 10
#    return json_response(res)
    while i < len(res):
        e = {}
        id = str(res[i]['id'])
        image = str(res[i]['image'])
        name = str(res[i]['name']) 
        path = name+'/'+image+'.jpg'
        coeff = res[i]['rang']*100
        
        insert = True
        for item in range(len(l)):
            if name == l[item]['name']:
                if coeff>l[item]['coeff']:
                    insert = True
                    l.pop(item)
                else:
                    insert = False
                break

        if not insert:
            i+=1
            continue
        
        res_count+=1
        if res_count>res_max:
            break
        
        e['id'] = id
        e['name'] = name
        e['url'] = util.get_absolute( settings.MEDIA_URL + STAR_PHOTO_PATH + path)
        e['coeff'] = coeff
        e['url_small'] = util.get_absolute( get_preview( settings.MEDIA_URL + STAR_PHOTO_PATH, path, (60, 80) ))
        e['photoes'] = getAllImagesId(name)
        l.append(e)
        
        i = i + 1
    l = sorted(l, key = lambda name: name["name"])
    data = {"result": l, "status": SUCCESS, "res_len":len(res)}
    
    return json_response( data)

def getAllImagesId(idName):
    imageFiles = []
    path = settings.MEDIA_ROOT + STAR_PHOTO_PATH + idName
    for f in os.listdir(path):
        filename = "%s/%s" % (path, f)
        if os.path.isdir(filename):
            continue
        size = (60, 80)
        if re.search("_%sx%s.jpg" % size, filename):
            continue
        if re.search(".jpg", filename):
            preview = "%s/%s" % (idName, f)
            get_preview( settings.MEDIA_URL + STAR_PHOTO_PATH, preview, size, preview)
            imageFiles.append(f)
    return imageFiles


def iframe(request):
    from operator import itemgetter
    from sim.util import get_absolute
    import urllib
    from django.shortcuts import redirect

    params = dict()

    if request.GET.has_key('post_id'):
        code = request.REQUEST['post_id']
        try:
            image = StoredImage.objects.get(code=code)
        except:
            raise Http404

        return render_to_response( "post.html",
            {'post_id': code,
             'image_url': get_absolute( image.image.url)})

    vars_string = ''
    curr_host = settings.HTTP_HOST
    for p in request.GET:
        vars_string+=p+"="+request.GET[p]+"%26"
    for p in request.GET.iteritems():
        params[ p] = itemgetter(0)
    return render_to_response( "iframe.html", {'flashvars':params, 'flashvars_string':vars_string, 'curr_host':curr_host})

def test(request):
    from operator import itemgetter
    from sim.util import get_absolute
    params = dict()
    if request.GET.has_key('post_id'):
        code = request.REQUEST['post_id']
	try:
	    image = StoredImage.objects.get(code=code)
	except:
	    raise Http404
	return render_to_response( "post.html",
	{'post_id': code,
	     'image_url': get_absolute( image.image.url)})
	
    for p in request.GET.iteritems():
	params[ p] = itemgetter(0)
    return render_to_response( "iframe.html", {'flashvars':params})
	
	
	
def invite(request):
    return render_to_response( "invite.html")

def learn(request):
    from sim.fb.teach import learnPerson, learnAllPersons
    if(request.GET.has_key('id')):
        str = learnPerson(request.REQUEST['id'])
        return HttpResponse(str)
    else:
        str = learnAllPersons()
        return HttpResponse(str)
