# coding=utf8
from django.http import *
from django.http import HttpResponse
from django.template import Context, loader
from django.http import HttpResponseRedirect, Http404
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
from django.shortcuts import *
import json
from django.template import RequestContext
from sim.models import *

def iframe(request):
    from operator import itemgetter
    from sim.util import get_absolute
    params = dict()

    if request.GET.has_key('post_id'):
        code = request.REQUEST['post_id']
        image = StoredImage.objects.get(code=code)
        
        return render_to_response( "post.html", 
            {'post_id': code,
             'app_url': 'http://ya.ru',
             'image_url': get_absolute(image.image.url)})

    for p in request.GET.iteritems():
        params[ p] = itemgetter(0)
    return render_to_response( "iframe.html", {'flashvars':params})
