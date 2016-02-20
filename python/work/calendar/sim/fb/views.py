#coding:utf8
from django.http import Http404
from django.shortcuts import HttpResponse, render_to_response
from django import forms
import logging
import datetime
import json
from sim import billing
from sim.fb.models import CalendarMeeting, CalendarUser,CalendarUserMeeting, CalendarLog
from sim import settings
from sim import config

SUCCESS = config.SUCCESS
ERROR_FORM = config.ERROR_FORM

UPLOAD_VK = config.UPLOAD_VK
UPLOAD_COMP = config.UPLOAD_COMP

PREVIEW_ROOT= config.PREVIEW_ROOT
STAR_PHOTO_PATH=config.STAR_PHOTO_PATH

face_size_small = 75, 100
face_size_big = 120, 160
collage_size_small = 120, 90
collage_size_big = 500, 375


class GetMeetingForm(forms.Form):
    viewer = forms.CharField(max_length=30, required=True)

def getMeetingFriends(meeting_id):
    friends = []
    req = CalendarUserMeeting.objects.all().filter(mid__id = meeting_id)
    for p in req:
        friends.append(p.uid.vid)
    return friends

def getStringDate(date):
    return date;
    string = ''
    return string

def getDateString(string):
    return string
    date = datetime.datetime.utcnow()
    return date
    
def logEvent(vid, to_vid, operation, mid, muid):
    logging.info("user: %s, operation: %s, to_user: %s, event: %s, user_event: %s" % (str(vid),str(operation),str(to_vid),str(mid),str(muid)))
    log = CalendarLog(vid=vid, to_vid=to_vid, operation=operation, mid=mid, muid=muid)
    log.save()
    
def delMeeting(request):
    try:
        form = GetMeetingForm(request.REQUEST, request.FILES)
        if not form.is_valid():
            return json_response( {"status": ERROR_FORM, "message": str( form.errors)})
        data = json.loads(request.REQUEST["meeting"])
        vid = form.cleaned_data['viewer']
        try:
            usermeet = CalendarUserMeeting.objects.get(id = data['id'])
        except:
            return json_response( {"status": 1, "message": "no such event "+str(data["id"])})
        if vid == usermeet.mid.owner:
            meet = usermeet.mid
            req = CalendarUserMeeting.objects.all().filter(mid = meet)
            for p in req:
                logEvent(vid, p.uid.vid, "uninvite", meet.id, p.id)
                p.delete()
            logEvent(vid, vid, "delete", meet.id, 0)
            meet.delete()
        else:
            if vid == usermeet.uid.vid:
                logEvent(vid, vid, "uninvite", usermeet.mid.id, usermeet.id)
                usermeet.delete()
            else:
                return json_response( {"status": 1, "message": "not your meeting "+str(data["id"])})
        return json_response( {"status": 0, "message": "deleted", "data":{"id":data['id']}})
    except:
        return json_response({"status":1, "message":"del meeting error"})
    
def getMeetings(request):
    try:
        form = GetMeetingForm(request.REQUEST, request.FILES)
        if not form.is_valid():
            return json_response( {"status": ERROR_FORM, "message": str( form.errors)})
        
        vid = form.cleaned_data['viewer']
        updateUser(vid)
        meetings = []
        req = CalendarUserMeeting.objects.all().filter(uid__vid = vid)
        for p in req:
            o = {}
            o["id"] = p.id
            o["name"] = p.mid.name
            o["description"] = p.mid.description
            o["partyDay"] = p.mid.party
            o["color"] = p.color
            o["notificationMail"] = p.mail_time
            o["mail"] = p.mail
            o["notificationWall"] = p.wall_time
            o["wall"] = p.wall
            o["notificationNote"] = p.note_time
            o["note"] = p.note
            o["email"] = p.email
            o["friendsAccess"] = p.mid.access
            o["repeat"] = p.mid.repeat
            o["owner"] = p.mid.owner
            o["friends"] = getMeetingFriends(p.mid.id)
            o["dateStart"] = getStringDate(p.mid.date_start)
            o["dateEnd"] = getStringDate(p.mid.date_end)
            o["invited"] = p.invited
            meetings.append(o)
            logEvent(vid, vid, "get", p.mid.id, p.id)
            
            
        return json_response({"status":0, "data":meetings})
    except:
        return json_response({"status":1, "message":"get meeting error"})

def createUserMeeting(vid, invited, meet_id):
    user, created = CalendarUser.objects.get_or_create(vid = vid)
    if created:
        logging.info(str(vid)+" new user")
    if meet_id == 0:
        meet = CalendarMeeting.objects.create(owner = vid)
        meet.save()
    else:
        meet = CalendarMeeting.objects.get(id = meet_id)
    usermeet = CalendarUserMeeting.objects.create(mid = meet, uid = user, invited = invited)
    usermeet.save()
    return usermeet

def compareMeetingFriends(friends, meet_id, vid, umid):
    req = CalendarUserMeeting.objects.all().filter(mid__id = meet_id)
    for p in req:
        was = False
        for i in range(len(friends)):
            if friends[i] == p.uid.vid:# and not vid == p.uid.vid:
                was = True
                friends[i] = ''
                break
        if (not was) and (not p.id == umid) and (vid == p.mid.owner or vid == p.uid.vid or CalendarLog.objects.all().filter(vid=vid, to_vid=p.uid.vid, mid=p.mid.id).count()>0):
            logEvent(vid, p.uid.vid, "uninvite", p.mid.id, p.id)
            p.delete()
    #req.save()
    for fr in friends:
        if fr != '' and (vid == p.mid.owner or p.mid.access):
            usermeet = createUserMeeting(fr, True, meet_id)
            logEvent(vid, fr, "invite", usermeet.mid.id, usermeet.id)

def createSaveMeeting(request):
    try:
        form = GetMeetingForm(request.REQUEST, request.FILES)
        if not form.is_valid():
            return json_response( {"status": ERROR_FORM, "message": str( form.errors)})
        data = json.loads(request.REQUEST["meeting"])
        vid = form.cleaned_data['viewer']
        user, created = CalendarUser.objects.get_or_create(vid = vid)
        if created:
            logging.info(str(vid)+" new user")
        if data['id'] == 0 or data['id'] == '0' or data['id'] == '':
            usermeet = createUserMeeting(vid, False, 0)
            logEvent(vid, vid, "create", usermeet.mid.id, usermeet.id)
        else:
            try:
                usermeet = CalendarUserMeeting.objects.get(id = data['id'])
            except:
                return json_response( {"status": 1, "message": "no such event "+str(data["id"])})
        meet = usermeet.mid
        if meet.owner == '' or vid == meet.owner:
            meet.owner = vid
            if 'name' in data:
                meet.name = data['name'] 
            if 'description' in data:
                meet.description = data['description'] 
            if 'dateStart' in data:
                meet.date_start = data['dateStart'] 
            if 'dateEnd' in data:
                meet.date_end = data['dateEnd'] 
            if 'partyDay' in data:
                meet.party = data['partyDay'] 
            if 'friendsAccess' in data:
                meet.access = data['friendsAccess']
            if 'repeat' in data:
                meet.repeat = data['repeat']
        if 'friends' in data:
            compareMeetingFriends(data['friends'], meet.id, vid, usermeet.id)
        if 'color' in data: 
            usermeet.color = data['color']
        if 'mail' in data: 
            usermeet.mail = data['mail']
        if 'wall' in data: 
            usermeet.wall = data['wall']
        if 'note' in data: 
            usermeet.note = data['note']
        if 'notificationMail' in data: 
            usermeet.mail_time = data['notificationMail']
        if 'notificationWall' in data: 
            usermeet.wall_time = data['notificationWall']
        if 'notificationNote' in data: 
            usermeet.note_time = data['notificationNote']
        if 'invited' in data: 
            usermeet.invited = data['invited']
        if 'email' in data: 
            usermeet.email = data['email']
            user.email = data['email']
            user.save()
        meet.save()
        usermeet.save()
        data = {}
        data["id"] = usermeet.id
        data["name"] = usermeet.mid.name
        data["description"] = usermeet.mid.description
        data["partyDay"] = usermeet.mid.party
        data["color"] = usermeet.color
        data["notificationMail"] = usermeet.mail_time
        data["mail"] = usermeet.mail
        data["notificationWall"] = usermeet.wall_time
        data["wall"] = usermeet.wall
        data["notificationNote"] = usermeet.note_time
        data["note"] = usermeet.note
        data["email"] = usermeet.email
        data["friendsAccess"] = usermeet.mid.access
        data["repeat"] = usermeet.mid.repeat
        data["owner"] = usermeet.mid.owner
        data["friends"] = getMeetingFriends(usermeet.mid.id)
        data["dateStart"] = getStringDate(usermeet.mid.date_start)
        data["dateEnd"] = getStringDate(usermeet.mid.date_end)
        data["invited"] = 0
        return json_response({"status":0, "data":data})
    except:
        return json_response({"status":1, "message":"set meeting error"})

def updateUser(vid):
    req, created = CalendarUser.objects.get_or_create(vid = vid)
    if created:
        logging.info(str(vid)+" new user")
    req.counter = req.counter + 1
    req.save()

def json_response( data):
    return HttpResponse( json.dumps( data))
"""
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

class UploadFromUrlForm( VKontakteForm):
    url = forms.URLField( required=True)
    itype = forms.IntegerField( required=False)

class ProcessForm( VKontakteForm):
    code = forms.CharField(required=True)
    wizer = forms.CharField(required=True)
    viewer = forms.CharField(required=True)
    itype = forms.IntegerField( required=False)
"""
def facebook(request):
    from operator import itemgetter
    from sim.util import get_absolute
    from django.shortcuts import redirect
    import urllib
    params = dict()

    for p in request.GET.iteritems():
        params[ p] = itemgetter(0)

    fv_str = ''
    for p in request.REQUEST:
        fv_str+=p+"="+request.REQUEST[p]+"%26"
        
#    billing.regSession(request.REQUEST)
    
    if (request.REQUEST.has_key("fb_sig_session_key") and request.REQUEST.has_key("fb_sig_ext_perms") and request.REQUEST["fb_sig_ext_perms"].find("publish_stream")>=0 and request.REQUEST["fb_sig_ext_perms"].find("friends_photos")>=0): 
#        return render_to_response( "iframe.html", {'flashvars':params, 'curr_host':settings.HTTP_HOST, 'flashvars_string':fv_str})
#    elif request.REQUEST.has_key("fb_sig_session_key"):
        data = urllib.urlopen("https://graph.facebook.com/oauth/exchange_sessions","client_id=329296052509&client_secret=aac2eef10e0417b30557bbffd2361f50&sessions="+request.REQUEST["fb_sig_session_key"]).read()
        access_token = json.loads(data)[0]["access_token"]
        fv_str+="access_token="+access_token
        return render_to_response( "iframe.html", {'flashvars':params, 'curr_host':settings.HTTP_HOST, 'flashvars_string':fv_str})
    elif request.REQUEST.has_key("code"):
        data = urllib.urlopen("https://graph.facebook.com/oauth/access_token?client_id=329296052509&client_secret=aac2eef10e0417b30557bbffd2361f50&redirect_uri=http://apps.facebook.com/likeness_test_app/&code="+request.REQUEST["code"]).read()
        return redirect("http://apps.facebook.com/likeness_test_app/?"+data)
    else:
        return redirect("https://graph.facebook.com/oauth/authorize?client_id=329296052509&scope=user_photos,friends_photos,publish_stream&redirect_uri=http://apps.facebook.com/likeness_test_app/")#?"+fv_str)

def mymail(request):
    from operator import itemgetter
    from sim.util import get_absolute
    import urllib
    params = dict()

    for p in request.GET.iteritems():
        params[ p] = itemgetter(0)

    fv_str = ''
    for p in request.REQUEST:
        fv_str+=p+"="+request.REQUEST[p]+"%26"
        
    logging.info(billing.regSession(request.REQUEST))

    url = "%s?%s" % (settings.redirect_url, urllib.urlencode(request.REQUEST))
    return render_to_response( "index.html", {'flashvars':params, 'curr_host':settings.HTTP_HOST, 'flashvars_string':fv_str, 'url': settings.redirect_url})
#    return render_to_response( "index.html", {'flashvars':params, 'curr_host':settings.HTTP_HOST, 'flashvars_string':fv_str})

def from_payment(request):
    return billing.from_payment(request)

def get_money(request):
    return billing.get_money(request)

def iframe():
    None