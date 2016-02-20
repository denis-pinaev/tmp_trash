# coding=utf8

from django import forms

from django.http import *
from django.template import loader
from wizer.faces.models import *
from wizer.faces.util import *
from wizer.faces.wizers import *
from django.http import *
import json
from django.db.models import Avg, Max, Min, Count


from sim import settings
#from wizer.vkontakte import vsecure
from django.shortcuts import *
from django.contrib.auth.decorators import login_required


class DispatchForm( forms.Form):
    message = forms.CharField( required=True)
    users = forms.IntegerField( required=False)

@login_required
def dispatch(request):
    from wizer.vkontakte import vkontakte
    message=u'Мы рады объявить, что теперь Вы можете разместить ссылку на наше приложение - http://vkontakte.ru/app1510688 прямо на своей странице – слева в общем списке ссылок. Для этого в Настройках приложения надо поставить галочку напротив фразы - Выводить ссылку на приложение в меню слева! Желаем приятных часов проведённых с приложением.'
#    vkontakte.sendAll( message)
    return HttpResponse( message)
