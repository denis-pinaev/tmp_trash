# coding=utf8

import urllib
import urllib2
import logging
from django.http import HttpResponse
import datetime
from settings import BILLING_URL, PRICE_COUNT, PROJECT_NAME 

def getParams(get):
    params = dict()
    for p in get:
        params[p] = get[p]
    params['project'] = PROJECT_NAME    
    return params

def sendUrl(url, params):
    url = "%s%s/?%s" %(BILLING_URL, url, urllib.urlencode(params))
    f = urllib.urlopen(url)
    return f.read()

def get_money(request):
    logging.info(getParams(request.REQUEST))
    return HttpResponse(sendUrl('get_money', getParams(request.REQUEST)))

def from_payment(request):
    return HttpResponse(sendUrl('from_payment', getParams(request.REQUEST)))

def isCorrectClientSIG(params):
    return str(sendUrl('is_correct_client_sig', getParams(params))) == 'True'
    
def isCorrectSession(vid, session_key):
    return str(sendUrl('is_correct_session', {'vid': vid, 'session_key': session_key, 'project': PROJECT_NAME})) == 'True'

def regSession(params):
    logging.info("reg_session")
    return sendUrl('reg_session', getParams(params))

def pay(viewer, Count):
    res = sendUrl('pay', {'uid': viewer, 'count': Count, 'project': PROJECT_NAME})
    return str(res).count('{"status": "1"}')>0
