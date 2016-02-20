# coding=utf-8
from django.db import models
from videoclient import models as vcModels
from videoclient.communicator import models as comModels
from videoclient import settings
from videoarchive.archive import models as archiveModels
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import pre_save
import datetime
import random
from videoclient.settings import log_videoarchive as logging

class AccessUser(models.Model):
    str_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length = 128)
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Доступ для пользователей"
        verbose_name_plural='Доступ для пользователей'
        
class PositionUser(models.Model):
    name = models.CharField(max_length = 128)
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Должность"
        verbose_name_plural='Должности'            
    
class Users(AuthUser):
    middle_name = models.CharField( max_length=32, verbose_name=u'Отчество', blank=True)
    position = models.ForeignKey(PositionUser)
    access = models.ForeignKey(AccessUser)
    #birthday = models.DateField(null=True)
    #passport_series = models.CharField(max_length = 8, verbose_name=u'Серия', null=True)
    #passport_number = models.CharField(max_length = 16, verbose_name=u'Номер', null=True)
    #passport_note = models.TextField(verbose_name=u'Выдан', null=True)
    #passport_date = models.DateField(verbose_name=u'Дата выдачи', null=True)
    #address = models.TextField(verbose_name=u'Адрес', null=True)
    #phone_work = models.CharField( max_length=32, verbose_name=u'Служебный телефон', null=True)
    #phone_home = models.CharField( max_length=32, verbose_name=u'Домашний телефон', null=True)
    #phone_mobile = models.CharField( max_length=32, verbose_name=u'Мобильный телефон', null=True)
    #note = models.TextField(verbose_name=u'Примечание', null=True)
        
class Signals(models.Model):
    str_id = models.CharField(max_length=16, unique=True)
    short_name = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    #params = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Запуск задачи"
        verbose_name_plural='Сигналы'

class Resolutions(models.Model):
    name = models.CharField(max_length=16)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Разрешение"
        verbose_name_plural='Разрешения'

def pre_save_resolutions(sender, **kwargs):
    resol = kwargs['instance']
    if resol:
        import sys
        try:
            resol.width, resol.height = resol.name.split("*")
        except: logging.error(sys.exc_info())
        
pre_save.connect(pre_save_resolutions, sender=Resolutions)
        
class Codecs(models.Model):
    name = models.CharField(max_length=16)
    number = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Кодек"
        verbose_name_plural='Кодеки'

REPEAT_DICT = dict()
REPEAT_DICT['one'] = 0
REPEAT_DICT['every'] = 1
REPEAT_DICT['work'] = 2
REPEAT_DICT['week_end'] = 3
REPEAT_DICT['days'] = 4
REPEAT_DICT['weeks'] = 5
REPEAT_DICT['always'] = 6

REPEATS = (
    (REPEAT_DICT['one'], "one"),
    (REPEAT_DICT['every'], "every"),
    (REPEAT_DICT['work'], "work"),
    (REPEAT_DICT['week_end'], "week_end"),
    (REPEAT_DICT['days'], "days"),
    (REPEAT_DICT['weeks'], "weeks"),
    (REPEAT_DICT['always'], "always"),
)

DURATION_TYPE_DICT = dict()
DURATION_TYPE_DICT['min'] = 0
DURATION_TYPE_DICT['hour'] = 1
DURATION_TYPE_DICT['day'] = 2

DURATIONS_TYPE = (
    (DURATION_TYPE_DICT['min'], "min"),
    (DURATION_TYPE_DICT['hour'], "hour"),
    (DURATION_TYPE_DICT['day'], "day"),
)

def generate_task_code():
    randoms = [(97, 122), (48, 57)]
    code = ""
    for i in xrange(0,6):
        r= randoms[random.randint(0, 1)]
        code = "%s%s" % (code, chr(random.randint(r[0], r[1])))
    return code

def get_task_code():
    code = generate_task_code()
    while Tasks.objects.filter(idtask=code).count()>0:
        code = generate_task_code()
    return code

def pre_save_tasks(sender, **kwargs):
    task = kwargs['instance']
    if task:
        tasks = Tasks.objects.filter(id=task.id)
        task.idtask = tasks[0].idtask if tasks.count() > 0 and tasks[0].idtask else get_task_code() 
        if not task.start_date or task.repeat_task and task.repeat == 6: task.start_date = datetime.datetime.date(datetime.datetime.now())
        max_duration = 24
        if task.repeat in (1, 6): task.days = "1234567"            
        elif task.repeat == 2: task.days = "12345"
        elif task.repeat == 3: task.days = "67"
#        elif task.repeat == 0: max_duration = 365*60*24
        date_delta = float((task.stop_date - task.start_date).seconds)/3600+24
        #logging.info("max_duration = %s" % (max_duration))
        #duration = task.duration
        """
        if task.duration<=24 and task.start_time<task.stop_time :
            time_delta = (task.stop_date-task.start_date).seconds
        else:
            year = datetime.datetime.year
            month = datetime.datetime.month
            day = datetime.datetime.day 
            time_delta = (datetime.datetime.date(year, month, day, 23, 59, 59)-datetime.datetime.date(task.start_date.year, task.start_date.month, task.start_date.day, task.start_time.hour, task.start_time.minute, task.start_time.second)).seconds
            time_delta += (datetime.datetime.date(task.start_date.year, task.start_date.month, task.start_date.day, task.stop_time.hour, task.stop_time.minute, task.stop_time.second)-datetime.datetime.date(year, month, day, 0, 0, 0)).seconds1
        """
        #task.duration = duration
        #if duration > date_delta or (task.interval == 0 and task.repeat == 0): 
            #task.stop_date = datetime.datetime.date(datetime.datetime.combine(task.start_date, datetime.time(0,0,0)) + datetime.timedelta(hours=duration))
        if not task.start_time: task.start_time = "00:00:00"
        if not task.stop_time: task.stop_time = "00:00:00"      

class Tasks(models.Model):
    from videoarchive.va.models import VaCommandRoller
    name = models.CharField(max_length=128)
    camera = models.ForeignKey(comModels.Camera)
    signal = models.ForeignKey(Signals)
    process = models.ForeignKey(VaCommandRoller, null = True, blank=True)
    last_kill_process = models.DateField(null = True, default=None, blank=True)
    repeat_task = models.BooleanField(default=False)
    repeat = models.PositiveIntegerField(verbose_name="Повтор", choices = REPEATS)
    days = models.CharField(max_length=7, default="", blank=True)
    interval = models.BooleanField(default=False)
    start_date = models.DateField(null=True, default=None, blank=True, db_index=True)
    stop_date = models.DateField(null=True, default=None, blank=True, db_index=True)
    start_time = models.TimeField(null=True, default=None, blank=True, db_index=True)
    stop_time = models.TimeField(null=True, default=None, blank=True, db_index=True)
    duration = models.FloatField(null = True, default=None, blank=True)
    duration_type = models.PositiveIntegerField(verbose_name="Тип повторения", choices = DURATIONS_TYPE)
    all_day = models.BooleanField(default=False)
    video_delimiter = models.IntegerField()
    resol = models.ForeignKey(Resolutions, null=True, blank=True)
    resolution = models.CharField(max_length=16)
    fps = models.IntegerField(null = True)
    codec = models.ForeignKey(Codecs)
    gop = models.IntegerField(null = True, default=None, blank=True)
    compress = models.FloatField(null = True, default=None, blank=True)
    bitrate = models.IntegerField(null = True, default=None, blank=True)
    blur = models.FloatField(null = True, default=None, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(vcModels.User, null=True, blank=True)
    last_run = models.DateTimeField(null = True, default=None, blank=True)
    last_error = models.DateTimeField(null = True, default=None, blank=True)
    error = models.IntegerField(null = True, default=0, blank=True)
    idtask = models.CharField(max_length=16, unique=True, null=True, blank=True)
    dt_create = models.DateTimeField(auto_now_add=True)
    
    def get_fields(self):
        data = dict()    
        data["name"] = self.name
        data["camera"] = self.camera
        data["signal"] = self.signal
        data["repeat"] = self.repeat
        data["days"] = self.days
        data["repeat_task"] = self.repeat_task
        data["interval"] = self.interval
        data["start_date"] = self.start_date
        data["stop_date"] = self.stop_date
        data["start_time"] = self.start_time
        data["stop_time"] = self.stop_time
        data["duration"] = self.duration
        data["duration_type"] = self.duration_type
        data["all_day"] = self.all_day
        data["video_delimiter"] = self.video_delimiter
        data["resolution"] = self.resolution
        data["fps"] = self.fps
        data["codec"] = self.codec
        data["gop"] = self.gop
        data["compress"] = self.compress
        data["bitrate"] = self.bitrate
        data["blur"] = self.blur
        data["idtask"] = self.idtask
        return data
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Задача"
        verbose_name_plural='Задачи'    
    
pre_save.connect(pre_save_tasks, sender=Tasks)
    
class TasksCommandRoller(models.Model):
    from videoarchive.va.models import VaCommandRoller
    id_task = models.ForeignKey(Tasks)
    id_command = models.ForeignKey(VaCommandRoller)
    def __unicode__(self):
        return "%s - %s" % (self.id_task.name, self.id_command.id)
    class Meta:
        verbose_name="Связь: задача - процесс"
        verbose_name_plural='Таблица связка: задача - процесс'             
        
class Week(models.Model):
    str_id = models.CharField(max_length=16, unique=True)
    number = models.IntegerField(null = True)
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=16)
    is_work = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="День недели"
        verbose_name_plural='Дни недели'

class Settings(models.Model):
    name = models.CharField(max_length=64, null=True, verbose_name=u'Имя параметра')
    value = models.CharField(max_length=64, null=False, verbose_name=u'Значение параметра')
    info = models.TextField(null=False, verbose_name=u'Комментарий')
    def __unicode__(self):
        if len(self.info)>99:
            return "%s = %s (%s...)" %(self.name if self.name else "", self.value if self.value else "", self.info[:97] if self.info else "")
        else:
            return "%s = %s (%s)" %(self.name if self.name else "", self.value if self.value else "", self.info if self.info else "")
    class Meta:
        verbose_name="Настройку по умолчанию"
        verbose_name_plural="Настройки по умолчанию"
        
class CalendarStatistic(models.Model):
    dt = models.DateField(null=False)
    tm_start = models.DateField(null=False)
    id_camera = models.ForeignKey(comModels.Camera, null=False)
    signal_type = models.CharField(max_length=75, null=False)
    count_people = models.IntegerField()
    count_face = models.IntegerField()
    count_roller = models.IntegerField()
    count_camera = models.IntegerField()
        
class Language(models.Model):
    name = models.CharField( max_length=8, unique=True, verbose_name=u'Имя', help_text=u'Короткое имя языка. Например: Russian(Русский) - ru')
    title = models.CharField( max_length=32, unique=True, verbose_name=u'Полное имя', help_text=u'Полное имя языка. Например: Russian')
    def __unicode__(self):
        return "%s:%s" %(self.name if self.name is not None else "", self.title if self.title is not None else "")
    class Meta:
        verbose_name="Язык"
        verbose_name_plural="Языки"
    
class Group(models.Model):
    title = models.CharField( max_length=32, unique = True, null=False, verbose_name=u'Имя группы', help_text=u'Название группы')
    def __unicode__(self):
        return "%s" % self.title if self.title is not None else ""
    class Meta:
        verbose_name="Группу переводов"
        verbose_name_plural="Группы переводов"
    
class Translation(models.Model):
    group = models.ForeignKey( Group, null=False, verbose_name=u'Группа', help_text=u'Группа переводимой фразы')
    phrase = models.TextField(max_length=4096, null=False, verbose_name=u'Фраза', help_text=u'переводимая фраза')
    language = models.ForeignKey( Language, null=False, verbose_name=u'Язык', help_text=u'На кокой язык будет переведена фраза')
    translate = models.TextField(max_length=4096, default="", verbose_name=u'Перевод', help_text=u'Перевод фразы')
    active = models.BooleanField(default = False, verbose_name=u'Активность', help_text=u'В активном состоянии фраза участвует в переводе')
    def __unicode__(self):
        if self.active:
            return "V %s:%s -%s-> %s" %(self.group if self.group is not None else "", self.phrase if self.phrase is not None else "", self.language if self.language is not None else "", self.translate if self.translate is not None else "")
        else:
            return "X %s:%s -%s-> %s" %(self.group if self.group is not None else "", self.phrase if self.phrase is not None else "", self.language if self.language is not None else "", self.translate if self.translate is not None else "")
    class Meta:
        verbose_name="Перевод"
        verbose_name_plural="Переводы"
