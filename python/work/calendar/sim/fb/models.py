from django.db import models
from django.db.models import ImageField
import hashlib, time, datetime
from sim import settings
import os
from django.template.defaultfilters import default

def gen_code():
    filename = hashlib.sha1(str(time.time())).hexdigest()
    datenow = datetime.datetime.today()
    year = str(datenow.year)
    month = str(datenow.month)
    day = str(datenow.day)
    hour = str(datenow.hour)
    minute = str(datenow.minute)
    if (len(month)<2):
        month = "0%s" % month
    if (len(day)<2):
        day = "0%s" % day
    if (len(hour)<2):
        hour = "0%s" % hour
    if (len(minute)<2):
        minute = "0%s" % minute
    return "%s%s%s%s%s%s.jpg" % (year, month, day, hour, minute, filename)

def gen_filename():
    code = gen_code()
    #while ContestImage.objects.filter(code = code).count() > 0:
#        code = gen_code()
    return code

def get_store_path(filename):
    return "%s/%s/%s/%s/%s" % (filename[:4], filename[4:6], filename[6:8], filename[8:10], filename[10:12])


def get_upload_to( instance, filename):
    return "%sstore/%s/%s" % (settings.STORE_IMG, get_store_path(filename), filename)

def get_previewupload_to( instance, filename):
    return "%sstore/%s/small_%s" % (settings.STORE_IMG, get_store_path(filename), filename)

class CalendarMeeting(models.Model):
    name = models.CharField(max_length = 64,  default='')
    description = models.CharField(max_length = 255,  default='')
    date_start = models.CharField(max_length = 20,  default='')#models.DateTimeField( auto_now=False, auto_now_add=True)
    date_end = models.CharField(max_length = 20,  default='')#models.DateTimeField( auto_now=False, auto_now_add=True)
    date_create = models.DateField( auto_now=False, auto_now_add=True)
    party = models.BooleanField(default = False) 
    access = models.BooleanField(default = True)
    owner = models.CharField(max_length = 64,  default='')
    repeat = models.IntegerField(default = 0)
#    preview = ImageField( upload_to=get_previewupload_to, blank=True, null=True)
    def __unicode__(self):
        return u'%s' % (self.name)
    
class CalendarUser(models.Model):
    vid = models.CharField(max_length = 64,  default='')
    description = models.CharField(max_length = 255,  default='')
    date_first = models.DateField( auto_now=False, auto_now_add=True)
    date_last = models.DateField( auto_now=True, auto_now_add=True)
    email = models.CharField(max_length = 64,  default='')
    counter = models.IntegerField(default = 0)
#    preview = ImageField( upload_to=get_previewupload_to, blank=True, null=True)
    def __unicode__(self):
        return u'%s' % (self.vid)
    
class CalendarUserMeeting(models.Model):
    uid = models.ForeignKey('CalendarUser')
    mid = models.ForeignKey('CalendarMeeting')
    email = models.CharField(max_length = 64,  default='')
    color = models.CharField(max_length = 12, default='0xcccccc')
    mail_time = models.IntegerField(default = 0)
    wall_time = models.IntegerField(default = 0)
    note_time = models.IntegerField(default = 0)
    mail = models.BooleanField(default = False)
    wall = models.BooleanField(default = False)
    note = models.BooleanField(default = False)
    invited = models.BooleanField(default = False)
#    preview = ImageField( upload_to=get_previewupload_to, blank=True, null=True)
    def __unicode__(self):
        return u'%s' % (self.vid)
    
class CalendarLog(models.Model):
    vid = models.CharField(max_length = 64,  default='')
    operation = models.CharField(max_length = 10,  default='')
    date_log = models.DateField( auto_now=False, auto_now_add=True)
    to_vid = models.CharField(max_length = 64,  default='')
    mid = models.IntegerField(default = 0)
    muid = models.IntegerField(default = 0)
#    preview = ImageField( upload_to=get_previewupload_to, blank=True, null=True)
    def __unicode__(self):
        return u'%s' % (self.vid)
    
'''
        o.dateStart = date.date + "." + sm + "." + date.fullYear + "." + int(hour) + ".00";
        o.dateEnd = date.date + "." + sm + "." + date.fullYear + "." + int(hour + 1) + ".00";
        o.name = "";
            //o.wholeDay = false;
        o.partyDay = false;
        o.color = 0xcccccc;
        o.notificationMail = 0;
        o.notificationWall = 0;
        o.notificationNote = 0;
        o.id = String(Math.round(Math.random() * 99999999))+"_"+String(GClass.GetTimer());
        o.friendsAccess = 1;
        o.friends = [GClass.params.vid, int(Math.random()*99999)];
        o.description = '';
        o.note = false;
        o.mail = false;
        o.email = "";
        o.wall = false;
        o.repeat = 0;
        o.owner = GClass.params.vid;
class ContestImage( models.Model):
    user = models.CharField(max_length = 64,  default='')
    date = models.DateTimeField( auto_now=False, auto_now_add=True)
    dt_date = models.DateField( auto_now=False, auto_now_add=True)
    image = ImageField(max_length=128, upload_to=get_upload_to)
#    preview = ImageField( upload_to=get_previewupload_to, blank=True, null=True)
    code = models.CharField( max_length=64, unique=True)
    coeff = models.FloatField(null=True)
    name = models.CharField(max_length = 64,  default='')
    count_vote = models.IntegerField(default=0)
    last_pay = models.TimeField(null=True, default=None)
    def __unicode__(self):
        return u'%s' % (self.user)


class ContestTop( models.Model):
    user = models.CharField(max_length = 64,  default='')
    dt_date = models.DateField(auto_now=False, auto_now_add=True)
    contest = models.ForeignKey(ContestImage)
    count_vote = models.IntegerField(default=0)
    def __unicode__(self):
        return u'%s' % (self.user)

STATUS_BUY = (
    (0, "buy content"),
    (1, "vote 10"),
    (2, "vote 20"),
    (3, "vote 30")
)

class ContestBuy( models.Model):
    user = models.CharField(max_length = 64,  default='')
    date = models.DateTimeField( auto_now=True, auto_now_add=True)
    contest = models.ForeignKey(ContestImage, null=False)
    price = models.IntegerField(default=0)
    status = models.CharField(max_length=128, null=True)
    status_pay = models.PositiveIntegerField(null=True, choices=STATUS_BUY)
    def __unicode__(self):
        return u'%s' % (self.user)
    
class CollageBuy( models.Model):
    user = models.CharField(max_length = 64, null=False)
    date = models.DateTimeField( auto_now=True, auto_now_add=True)
    code = models.CharField(max_length=256, null=False)
    def __unicode__(self):
        return u'%s' % (self.user)

class VoteImage( models.Model):
    user = models.CharField(max_length = 64,  default='')
    date = models.DateTimeField( auto_now=True, auto_now_add=True)
    code = models.CharField( max_length=64, default = '')
    vote = models.IntegerField(default = 0)
    def __unicode__(self):
        return u'%s' % (self.user)
'''