from django import forms
from django.template import Context, loader
from django.http import *
import json
from django.db.models import Avg, Max, Min, Count

from vkontakte.models import *
from vkontakte.forms import *

class VisitForm(VKontakteForm):
    user = forms.IntegerField( required=True)

def visit(request):
    from datetime import datetime, timedelta

    form = VisitForm( request.REQUEST, request.FILES)
    if not form.is_valid():
	data = {"status": "error", "message": str(form.errors)}
	return HttpResponse(  json.dumps( data))

    user = form.cleaned_data['user']
    viewer = form.cleaned_data['viewer']
    last_visit = None
    interval = timedelta(hours = 1)

    try:
        last_visit = Visit.objects.filter(viewer=viewer).latest('dt_open')
    except Visit.DoesNotExist:
	None

    if last_visit == None or (last_visit != None and last_visit.dt_open > datetime.today() + interval):
	visit = Visit( user = user, viewer = viewer)
	visit.save()

    data = {"status": "success"}
    return HttpResponse(  json.dumps( data))

