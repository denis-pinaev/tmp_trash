from django.http import *
from django.shortcuts import *
from django import forms

import json
from sim.models import *

from sim import util
from sim import settings
import logging
import sys

from vkontakte.forms import VKontakteForm
from smilart.similarity import Similarity

SUCCESS = settings.SUCCESS
ERROR_FORM = settings.ERROR_FORM

UPLOAD_VK = settings.UPLOAD_VK
UPLOAD_COMP = settings.UPLOAD_COMP

PREVIEW_ROOT = settings.PREVIEW_ROOT
STAR_PHOTO_PATH=settings.STAR_PHOTO_PATH

def get_preview( root, path, size, out_path = '', stored=True):
    if stored: 
        path = path[len(settings.STORED_IMG)+len(settings.MEDIA_ROOT):]
        dir_img = settings.STORED_IMG
    else: 
        path = path[len(settings.TMP_IMG)+len(settings.MEDIA_ROOT):]
        dir_img = settings.TMP_IMG
        
    preview_path = PREVIEW_ROOT + root + path
    try:
        import magick_effect
        if out_path == '':
            preview_path = PREVIEW_ROOT + root + path
#        full_preview_path = settings.WWW_ROOT + preview_path
        else:
            preview_path = PREVIEW_ROOT + root + out_path.replace('.jpg', '_%dx%d.jpg' % size)
        full_preview_path = settings.MEDIA_ROOT + settings.TMP_IMG +  preview_path
        #if not os.path.lexists( settings.MEDIA_ROOT + preview_path):
        if not os.path.exists( full_preview_path):
            original_path = settings.MEDIA_ROOT + dir_img + root + path
            if not os.path.exists( original_path): return preview_path
            res = magick_effect.initEffect(original_path)
            w, h = size
            res = magick_effect.execEffect('thumbnail', w , h)
            #full_preview_path = settings.WWW_ROOT + preview_path
            preview_dir = os.path.dirname( full_preview_path)
            if not os.path.exists( preview_dir):
                os.makedirs( preview_dir)

            if res == 1:
                magick_effect.writeEffect(full_preview_path)

    except:
        logging.error("fb.preview "+str(sys.exc_info()))
    return settings.MEDIA_URL + settings.TMP_IMG + preview_path
    

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
    try:
        form = ImageUploadForm( request.REQUEST, request.FILES)
        if not form.is_valid():
            return json_response( {"status": ERROR_FORM, "message": str( form.errors)})

        code = gen_tmp_code()
        viewer = form.cleaned_data['viewer']
        uploadedImage = form.cleaned_data['image']
        itype = form.cleaned_data['itype']
    
        img = TmpImage( code = code, user = viewer)
        stored = False
        if itype:
            stored = True
            img = StoredImage( code = code, user = viewer, mark = UPLOAD_VK)

        img.image.save( code, uploadedImage)
        img.save()

        f = Similarity()
        return json_response(
            {
                "status": SUCCESS,
                "url": util.get_absolute(img.image.url, stored),
                "url_small": util.get_absolute(get_preview( "", img.image.path, (120, 160), stored=stored ), False),
                "code": code,
                "faces": f.face_detect( img.image.path, viewer, uploadedImage)
            }
        )
    except:
        logging.error("fb.upload "+str(sys.exc_info()))
        return json_response({})

class UploadFromUrlForm( VKontakteForm):
    url = forms.URLField( required=True)
    itype = forms.IntegerField( required=False)

def upload_url (request):
    try:
        form = UploadFromUrlForm( request.REQUEST, request.FILES)
        if not form.is_valid():
            return json_response( {"status": ERROR_FORM, "message": str( form.errors)})

        viewer = form.cleaned_data['viewer']
        url =  form.cleaned_data['url']
        itype = form.cleaned_data['itype']
        
        loader = util.FileLoader(url)
        code = gen_image_code()
    
        img = TmpImage( code = code, user = viewer)
        stored = False
        if itype:
            stored = True
            img = StoredImage( code = code, user = viewer, mark = UPLOAD_VK)
        img.image.save( code, loader.File)
        img.save()

        f = Similarity()
        data = {
            "status": SUCCESS,
            "url": util.get_absolute( img.image.url, stored),
            "url_small":  util.get_absolute(get_preview( "", img.image.path, (120, 160), stored=stored ), False),
            "code": code,
            #"faces": f.face_detect( util.get_absolute(img.image.url), viewer, None)
            "faces": f.face_detect( img.image.path, viewer, None)
        }

        return json_response(data)
    except:
        logging.error("fb.upload_url "+str(sys.exc_info()))
        return json_response({})

class ProcessForm( VKontakteForm):
    code = forms.CharField(required=True)
    itype = forms.IntegerField( required=False)

def process( request):
    try:
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
        #from smilart.balancer import Balancer
        #import smilart.similarity

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
            e['url'] = util.get_absolute(settings.MEDIA_URL + settings.STORED_IMG + STAR_PHOTO_PATH + path)
            e['coeff'] = coeff
            e['photoes'] = getAllImagesId(name)
            ind = path.rindex("/")
            if path[ind+1:] in e['photoes']:
                e['url_small'] = util.get_absolute( get_preview( STAR_PHOTO_PATH, settings.MEDIA_ROOT + settings.TMP_IMG + path, (60, 80), stored = False ), False)
            elif len(e['photoes'])>0:
                path = path[:ind+1]+e['photoes'][0]
                e['url_small'] = util.get_absolute( get_preview( STAR_PHOTO_PATH, settings.MEDIA_ROOT + settings.TMP_IMG + path, (60, 80), stored = False ), False)
            else: e['url_small'] = ''
            l.append(e)
        
            i = i + 1
        l = sorted(l, key = lambda name: name["name"])
        data = {"result": l, "status": SUCCESS, "res_len":len(res)}
    
        return json_response( data)
    except:
        logging.error("fb.process "+str(sys.exc_info()))
        return json_response({})

def getAllImagesId(idName):
    imageFiles = []
    path = settings.MEDIA_ROOT + settings.STORED_IMG + STAR_PHOTO_PATH + idName
    for f in os.listdir(path):
        filename = "%s/%s" % (path, f)
        if os.path.isdir(filename):
            continue
        size = (60, 80)
        if re.search("_%sx%s.jpg" % size, filename):
            continue
        if re.search(".jpg", filename):
            preview = "%s/%s" % (idName, f)
            get_preview( STAR_PHOTO_PATH, settings.MEDIA_ROOT + settings.STORED_IMG + preview, size, preview)
            imageFiles.append(f)
    return imageFiles


def iframe(request):
    from operator import itemgetter
    from sim.util import get_absolute
    import urllib
    params = dict()

    if request.REQUEST.has_key('post_id'):
        code = request.REQUEST['post_id']
        try:
            image = StoredImage.objects.get(code=code)
        except:
            raise Http404

        return render_to_response( "post.html",
            {'post_id': code,
             'image_url': get_absolute( image.image.url)})

    curr_host = settings.HTTP_HOST
    flashvars_string = ''
    app_id = '109252122447689'
    secret_key ='3446fbdc1905cca54a426a93fcbe7d28'
    app_path = 'http://apps.facebook.com/like_you/'
    
    for i in request.REQUEST:
        flashvars_string+=i+'='+request.REQUEST[i]+'%26'
        
    for p in request.REQUEST.iteritems():
        params[ p] = itemgetter(0)
        
    if(request.REQUEST.has_key('fb_sig_ext_perms') and not request.REQUEST.has_key('code')):
        perms = request.REQUEST['fb_sig_ext_perms']
        has_all = perms.find('publish_stream')>=0 and perms.find('user_photos')>=0 and perms.find('friends_photos')>=0
        if not has_all:
            return redirect('https://graph.facebook.com/oauth/authorize?client_id='+app_id+'&redirect_uri='+app_path+'&scope=user_photos,publish_stream,friends_photos')
    if(request.REQUEST.has_key('fb_sig_session_key')):
        resp = urllib.urlopen('https://graph.facebook.com/oauth/exchange_sessions?client_id='+app_id+'&client_secret='+secret_key+'&sessions='+request.REQUEST['fb_sig_session_key']+'&redirect_uri='+curr_host+'fb/iframe/').read()
        token = json.loads(resp)[0]['access_token']
        flashvars_string+='access_token='+token+'%26token='+token
        return render_to_response( "facebook.html", {'flashvars':params, 'flashvars_string':flashvars_string, 'curr_host':curr_host})
    else:
        return redirect('https://graph.facebook.com/oauth/authorize?client_id='+app_id+'&redirect_uri='+app_path+'&scope=user_photos,publish_stream,friends_photos')

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
