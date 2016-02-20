# coding=utf-8

from django.db import models
from django.utils import translation
from videoclient.settings import *
from django.contrib import auth
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import pre_save
from videoclient.settings import last_journal_update, wait_unidentified_person, status_notdefined, journalBoundCoeff, reaction_time, count_time_test, time_span_time_test
from videoclient.communicator.models import Kpp, Camera, Communicator
import logging
import json
import sys

class Alerts(models.Model):
    name = models.CharField(max_length=1024, verbose_name=u'Адрес')
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Адрес"
        verbose_name_plural='Адреса оповещений'

class Article(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'Имя статьи')
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Статью"
        verbose_name_plural='Статьи'

class ArticlePart(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'Часть статьи')
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Часть статьи"
        verbose_name_plural='Части статей'
        
class ArticleItem(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'Пункт статьи')
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Пункт статьи"
        verbose_name_plural='Пункты статей'        

class DivisionUser(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'Отдел')
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Отдел"
        verbose_name_plural='Отделы'
        
class PositionUser(models.Model):
    division = models.ForeignKey(DivisionUser, null=True, verbose_name=u'Отдел')
    name = models.CharField(max_length=32, verbose_name=u'Должность')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name="Должность"
        verbose_name_plural='Должности'
        
class StatusUser(models.Model):
    division = models.ForeignKey(DivisionUser, null=True, verbose_name=u'Отдел')
    name = models.CharField(max_length=32, verbose_name=u'Статус')
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Статус"
        verbose_name_plural='Статусы'   
        
#class Kpp(models.Model):
#    name = models.CharField(max_length = 32, null = False, verbose_name=u'Имя КПП')
#    location = models.CharField(max_length = 128, blank=True, null=True, verbose_name=u'Расположение КПП')
    
#    def __unicode__(self):
#        return "%s" %(self.name if self.name is not None else "")
#    class Meta:
#        verbose_name="КПП"
#        verbose_name_plural="КПП"
        
class Document(models.Model):
    name = models.CharField(max_length = 32, null = False, verbose_name=u'Имя документа')
    def __unicode__(self):
        return "%s" %(self.name if self.name is not None else "")
    class Meta:
        verbose_name="Вид документа"
        verbose_name_plural="Виды документов"
        
class Category(models.Model):
    name = models.CharField(max_length = 32, null = False, verbose_name=u'Имя категории')
    def __unicode__(self):
        return "%s" %(self.name if self.name is not None else "")
    class Meta:
        verbose_name="Категорию"
        verbose_name_plural="Категории"
 

class User(AuthUser):
    middle_name = models.CharField( max_length=30, verbose_name=u'Отчество', blank=True)
    birthday = models.DateField(null=True)
    passport_series = models.CharField(max_length = 8, verbose_name=u'Серия', null=True)
    passport_number = models.CharField(max_length = 16, verbose_name=u'Номер', null=True)
    passport_note = models.TextField(verbose_name=u'Выдан', null=True)
    passport_date = models.DateField(verbose_name=u'Дата выдачи', null=True)
    address = models.TextField(verbose_name=u'Адрес', null=True)
    phone_work = models.CharField( max_length=32, verbose_name=u'Служебный телефон')
    phone_home = models.CharField( max_length=32, verbose_name=u'Домашний телефон')
    phone_mobile = models.CharField( max_length=32, verbose_name=u'Мобильный телефон')
    note = models.TextField(verbose_name=u'Примечание')
    division = models.ForeignKey(DivisionUser , null=True, verbose_name=u'Отдел')
    position = models.ForeignKey(PositionUser , null=True, verbose_name=u'Должность')
    status = models.ForeignKey(StatusUser , null=True, verbose_name=u'Статус')
    kpp = models.ForeignKey(Kpp , null=True, verbose_name=u'КПП')
    staff = models.IntegerField(null=True, verbose_name=u'Сотрудник')
    last_access = models.DateTimeField(auto_now=True, auto_now_add=True)
    #groups = models.ManyToManyField(UserGroup, verbose_name=_('groups'), blank=True,
    #    help_text=_("In addition to the permissions manually assigned, this user will also get all permissions granted to each group he/she is in."))
    
    def get_fio(self):
        fio = ""
        try:
            fio = "%s %s %s" %(self.first_name, self.last_name, self.middle_name)
            fio = fio.split()
            fio = ' '.join(fio)
        except:
            logging.exception(str(sys.exc_info()))
        return fio    
    
    def getDict(self):
        data = dict()
        
        data['id'] = self.id
        
        data['pk_django_groups'] = [group.pk for group in self.groups.all()]
        data['self'] = self
        
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['middle_name'] = self.middle_name
        data['get_fio'] = self.get_fio()
        
        data['birthday'] = self.birthday
        
        data['passport_series'] = self.passport_series
        data['passport_number'] = self.passport_number
        data['passport_note'] = self.passport_note
        data['passport_date'] = self.passport_date
        
        data['address'] = self.address
        
        data['phone_work'] = self.phone_work
        data['phone_home'] = self.phone_home
        data['phone_mobile'] = self.phone_mobile
        
        data['note'] = self.note
        
        data['username'] = self.username
        data['password'] = self.password
        data['last_login'] = self.last_login
        data['date_joined'] = self.date_joined
        
        data['division'] = self.division.name if self.division else ''
        data['position'] = self.position.name if self.position else ''
        data['status'] = self.status.name if self.status else ''
        data['status_trans'] = self.status
        data['kpp'] = self.kpp.name if self.kpp else ''
        data['kpp_location'] = self.kpp.location if self.kpp and self.kpp.location else ''
        data['staff'] = self.staff
        if hasattr(self, "staff_name"): data['staff_name'] = self.staff_name
        
        for d in data:
            if data[d] == None:
                data[d] = ''
        return data
        
    class Meta:
        verbose_name="Пользователя"
        verbose_name_plural="Пользователи"
        
class LoginJournal(models.Model):
    user = models.ForeignKey(User, null=False, verbose_name=u'Пользователь')
    login = models.DateTimeField()
    logout = models.DateTimeField(null = True)
    
    def getDict(self):
        from time import strftime
        
        j_id = self.id
        data = self.user.getDict()
        data['j_id'] = j_id
        data['login'] = self.login
        data['logint_time'] = self.login.strftime("%H:%M:%S") if self.login else ""
        data['logout'] = self.logout
        data['logout_time'] = self.logout.strftime("%H:%M:%S") if self.logout else ""
        data['fio'] = "%s %s %s" %(self.user.first_name, self.user.last_name, self.user.middle_name)
        return data
    
def getDictUsers(users = None, model = User):
    data = []
    
    if users == None:
        users = model.objects.all()
        
    for user in users:
        data.append(user.getDict())
    return data    

class GroupPerson(models.Model):
    name = models.CharField( max_length=128, verbose_name=u'Группа')
    def __unicode__(self):
        return "%s" %(self.name if self.name is not None else "")
    class Meta:
        verbose_name="Группу персон"
        verbose_name_plural="Группы персон"
        
ACTIONS = (
    (0, "Создание"),
    (1, "Редактирование"),
    (2, "Добавление фотографий"),
    (3, "Удаление"),
)

GOTO = (
    (0, "Персона"),
    (1, "Сотрудник"),
)        

class Person(models.Model):
    id_person = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
    user = models.ForeignKey(User, null=True)
    action = models.PositiveIntegerField(verbose_name="Действие", choices = ACTIONS, default=0)
    
    first_name = models.CharField( max_length=30, verbose_name=u'Фамилия')
    last_name = models.CharField( max_length=30, verbose_name=u'Имя')
    middle_name = models.CharField( max_length=30, verbose_name=u'Отчество')
    birthday = models.DateField(null=True)
    passport_series = models.CharField(max_length = 8, verbose_name=u'Серия', null=True)
    passport_number = models.CharField(max_length = 16, verbose_name=u'Номер', null=True)
    passport_note = models.TextField(verbose_name=u'Выдан', null=True)
    passport_date = models.DateField(verbose_name=u'Дата выдачи', null=True)
    address = models.TextField(verbose_name=u'Адрес', null=True)
    phone_work = models.CharField( max_length=32, verbose_name=u'Служебный телефон', null=True)
    phone_home = models.CharField( max_length=32, verbose_name=u'Домашний телефон', null=True)
    phone_mobile = models.CharField( max_length=32, verbose_name=u'Мобильный телефон', null=True)
    note = models.TextField(verbose_name=u'Примечание', null=True)
    group = models.ForeignKey( GroupPerson, null=True, verbose_name=u'')
    
    status = models.ForeignKey(StatusUser , null=True, verbose_name=u'Статус')
    goto = models.PositiveIntegerField(default = False, verbose_name="К кому", choices = GOTO)
    #person = models.ForeignKey(Person, null=True, verbose_name=u'Персона')
    document = models.ForeignKey(Document, null=True, verbose_name=u'Персона')
    passport_code = models.CharField( max_length=8, null=True, verbose_name=u'Код подразделения')
    address_temp = models.TextField(verbose_name=u'Временная регистрация', null=True) 
    category = models.ForeignKey(Category, null=True, verbose_name=u'Категория')
    number = models.CharField( max_length=32, null=True, verbose_name=u'Номер дела')
    article = models.ForeignKey(Article, null=True, verbose_name=u'Статья')
    article_part = models.ForeignKey(ArticlePart, null=True, verbose_name=u'Часть')
    article_item = models.ForeignKey(ArticleItem, null=True, verbose_name=u'Пункт')
    room_facility = models.CharField( max_length=32, null=True, verbose_name=u'Номер изолятора')
    
    def get_fio(self):
        fio = ""
        try:
            fio = "%s %s %s" %(self.first_name, self.last_name, self.middle_name)
            fio = fio.split()
            fio = ' '.join(fio)
        except:
            logging.exception(str(sys.exc_info()))
        return fio
            
    def getDict(self):
        data = dict()
        
        data['id'] = self.id
        data['date'] = self.date
        try:            
            if self.user: data['user'] = self.user.getDict()
            else: data["user"] = None
            
        except:
            logging.info(sys.exc_info())
        data['action'] = self.action
        
        try:
            data['id_person'] = self.id_person
        except:
            pass
        
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['middle_name'] = self.middle_name
        data['fio'] = self.get_fio()
        data['get_fio'] = self.get_fio()
         
        data['birthday'] = self.birthday
        
        data['passport_series'] = self.passport_series
        data['passport_number'] = self.passport_number
        data['passport_note'] = self.passport_note
        data['passport_date'] = self.passport_date
        
        data['address'] = self.address
        
        data['phone_work'] = self.phone_work
        data['phone_home'] = self.phone_home
        data['phone_mobile'] = self.phone_mobile
        
        data['note'] = self.note
        
        data['status'] = self.status.name if self.status else ''
        data['status_trans'] = self.status
        data['goto'] = str(GOTO[self.goto][1])
        data['document'] = self.document.name if self.document else ''
        data['passport_code'] = self.passport_code
        data['address_temp'] = self.address_temp
        data['category'] = self.category.name if self.category else ''
        data['action'] = self.action
        data['number'] = self.number
        data['article'] = self.article
        data['article_part'] = self.article_part
        data['article_item'] = self.article_item
        data['room_facility'] = self.room_facility
        data['for_trans'] = self
        try:
            data['group'] = self.group
        except:
            data['group'] = ""
        if hasattr(self, "staff_name"):
            try: 
                data['staff_name'] = self.staff_name
            except:
                pass
        try:
            data['division'] = self.status.division.name
        except:
            pass
        
        #data['division'] = str(self.division)
        #data['position'] = str(self.position)
        
        #data['kpp'] = str(self.kpp)
        
        for d in data:
            if data[d] == None:
                data[d] = ''
        return data
    
    def searchString(self):
        return "%s %s %s" % (self.first_name.lower() if self.first_name is not None else "", self.last_name.lower() if self.last_name is not None else "", self.middle_name.lower() if self.middle_name is not None else "")
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(Person,self).formfield_for_dbfield(db_field,**kwargs)

        if db_field.name == 'birthday' or db_field.name == 'passport_date':
            return forms.DateField(required=False, input_formats=('%d.%m.%Y',), widget=SelectDateWidget(input_format='%d.%m.%Y', null=True))
        return field

    def __unicode__(self):
        return "%s %s %s" %(self.first_name if self.first_name is not None else "", self.last_name if self.last_name is not None else "", self.middle_name if self.middle_name is not None else "")

    class Meta:
        verbose_name="Персону"
        verbose_name_plural="Персоны"
        
class PersonId(models.Model):
    date = models.DateField(auto_now=True, auto_now_add=True)
    person = models.ForeignKey(Person, null=True)
    active = models.BooleanField(default=1, null=False, verbose_name=u'Активированность пользователя')
    bal_id = models.IntegerField(null=True, unique=True)
    
    def get_fio(self):
        return self.person.get_fio() if self.person else ""
    
    def getDict(self):
        data = dict()
        data["id"] = self.id
        data["active"] = self.active
        data["person"] = self.person.getDict()
        data['get_fio'] = self.get_fio()
        return data

class PhotoExifData(models.Model):
    personid = models.ForeignKey(PersonId, null=True)
    person_id = models.IntegerField(null=True, unique=False)
    photo_id = models.IntegerField(null=True, unique=False)
    learning_date = models.DateField(auto_now=True, auto_now_add=True)
    exif = models.TextField(verbose_name=u'Exif данные', null=True)
        
#class Rule(models.Model):
#    name = models.CharField(max_length = 32, verbose_name=u'Имя')
#    def __unicode__(self):
#        return self.name if self.name is not None else ""
#    class Meta:
#        verbose_name="Роль"
#        verbose_name_plural="Роли"
#        
#class RuleGroup(models.Model):
#    group = models.ForeignKey( auth.models.Group, null=False, verbose_name=u'Группа')
#    rule = models.ForeignKey( Rule, null=False, verbose_name=u'Роль')
#    active = models.BigIntegerField(default = False)
#    def __unicode__(self):
#        return "%s -> %s" %(self.group if self.group is not None else "", self.rule if self.rule is not None else "")
#    class Meta:
#        verbose_name="Назначение права группе"
#        verbose_name_plural="Назначение прав группам"                
 
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
       
        
#POSITIONS = (
#    (0, "Вход"),
#    (1, "Выход"),
#    (2, "Вход/Выход"),
#)           
        
#class Camera(models.Model):
#    ip = models.CharField(max_length = 255, null = False, verbose_name=u'IP')
#    type = models.CharField(max_length = 64, null = False, verbose_name=u'Тип')
#    kpp = models.ForeignKey( Kpp, null = True, verbose_name=u'КПП', help_text=u'Контрольно пропускной пункт')
#    position = models.PositiveIntegerField(default = 2, verbose_name="Размещение", choices = POSITIONS)
#    name = models.CharField(max_length = 128, null = True, verbose_name=u'Название камеры', blank=True)
#    commun = models.ForeignKey(Communicator, null=True, verbose_name=u'Коммуникатор')
#    active = models.BooleanField(default=True, verbose_name=u'Активность')
#    uuid = models.CharField(max_length = 255, unique=True, verbose_name=u'Uid камеры')
    
#    def __unicode__(self):
#        return "%s %s %s %s" %(self.ip if self.ip is not None else "", self.type if self.type is not None else "", "("+self.name+")" if self.name is not None else "", self.kpp if self.kpp is not None else "")

#    class Meta:
#        verbose_name="Камеру"
#        verbose_name_plural="Камеры"
        

def pre_save_camera(sender, **kwargs):
    try:
        if not kwargs['instance'].kpp:           
            kpp = Kpp.objects.all().order_by("id")[:1]
            if kpp.count() > 0:
                kwargs['instance'].kpp = kpp[0]
    except:
        logging.error(sys.exc_info())         
        
pre_save.connect(pre_save_camera, sender=Camera)        
        
class Balancer(models.Model):
    host = models.CharField( max_length = 255, null=False, verbose_name=u'Хост') 
    port = models.IntegerField(null=True, verbose_name=u'Порт')
    login = models.CharField( max_length = 32, verbose_name = u'Логин')
    passwd = models.CharField( max_length = 32, verbose_name = u'Пароль')
    user = models.CharField( max_length = 32, verbose_name = u'Пользователь')
    active = models.BooleanField(default = True, verbose_name=u'Активность')
    
    def __unicode__(self):
        return "%s:%s %s %s %s" %(self.host if self.host is not None else "", self.port if self.port is not None else "", self.login if self.login is not None else "", self.passwd if self.passwd is not None else "", self.user if self.user is not None else "")
    class Meta:
        verbose_name="Управляющую систему"
        verbose_name_plural="Управляющая система"

def getModelFileNameByFileName(filename):
    return "journal%s" % (filename)

def get_journal_upload_to(instance, filename):
    return getModelFileNameByFileName(filename)   
   
class PositionsStatus(models.Model):
    name = models.CharField( max_length = 32, null=False, verbose_name=u'Имя')
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Событие на кпп"
        verbose_name_plural="Событие на кпп"
   
def get_image_info(image):
    try:
        if image:
            from PIL import Image
            img = Image.open(image)
            width, height = img.size
            return {'resol': "%sx%s" %(width, height)}
    except:
        logging.exception(sys.exc_info())
    return None

    
def distCalculation(face):
    import math
    return math.sqrt(math.pow(float(face[9])-float(face[12]), 2) + math.pow(float(face[10])-float(face[13]), 2))

class ParamAggregator(models.Model):
    data = models.TextField()
    
    PARAM_JOURNAL_COUNT = "journal_count"
    PARAM_JOURNAL_IDENT_COUNT = "journal_ident_count"
    PARAM_JOURNAL_FIRST_ID = "journal_first_id"  # При выборках условие должно быть >
    PARAM_JOURNAL_LAST_ID = "journal_last_id" # При выборках условие должно быть  <=
    
    def getParam(self, name):
        answer = None
        try:
            data = json.loads(self.data)
            if name in data:
                answer = data[name]
        except:
            logging.exception("")
        return answer
    
    def setParam(self, name, value):
        answer = False
        try:
            data = json.loads(self.data)
            
            data[name] = value
            self.data = json.dumps(data)
            
            self.save()
        except:
            logging.exception("")
        return answer
    
    @staticmethod
    def getRecord():
        j = ParamAggregator.objects.filter(id=1)
        if len(j) == 0:
            default_data = {ParamAggregator.PARAM_JOURNAL_COUNT:0, ParamAggregator.PARAM_JOURNAL_IDENT_COUNT:0, ParamAggregator.PARAM_JOURNAL_FIRST_ID: 0, ParamAggregator.PARAM_JOURNAL_LAST_ID: 0}
            j = ParamAggregator.objects.create(id=1, data=json.dumps(default_data))
        else:
            j = j[0]
        return j
   
class Journal(models.Model):
    person = models.ForeignKey(PersonId, null=True, verbose_name=u"ID персоны", db_index=True, related_name="person_found")
    person_not_found = models.ForeignKey(PersonId, null=True, verbose_name=u"ID персоны для не распознанных записей", db_index=True, related_name="person_not_found")
    camera = models.ForeignKey(Camera, null=True, verbose_name=u'Камера')
    coeff = models.FloatField(verbose_name=u'Процент похожести')
    bound_coeff = models.FloatField(verbose_name=u'Граничный коэффициент')
    dt_first_fixed = models.DateTimeField(null=False, verbose_name=u'Дата первой фиксации персоны камерой', db_index=True)
    dt_last_fixed = models.DateTimeField(null=False, verbose_name=u'Дата последней фиксации персоны камерой', db_index=True)
    
    t_first_fixed = models.TimeField(null=False, verbose_name=u'Время первой фиксации персоны камерой', db_index=True)
    t_last_fixed = models.TimeField(null=False, verbose_name=u'Время последней фиксации персоны камерой', db_index=True)
    photos_count = models.IntegerField(default=1)
    
    dt_continue = models.DateTimeField(null=True, verbose_name=u'Дата ожидания', db_index=True)
    original = models.ImageField( upload_to=get_journal_upload_to)
    finded = models.ImageField( upload_to=get_journal_upload_to, db_column = 'found')
    positions_status = models.ForeignKey(PositionsStatus, default = status_notdefined, verbose_name="Статус", null=True)
    operator = models.ForeignKey(User, null=True, verbose_name=u'Оператор')
    show_info = models.IntegerField(default=None, null=True, verbose_name=u'Показали информацию оператору', db_index=True)
    dt_open = models.DateTimeField( auto_now=True, auto_now_add=True)
    transfer = models.IntegerField(default=None, null=True, verbose_name=u'Показали информацию оператору', db_index=True)
    original_face = models.TextField(default=None, null=True)
    found_face = models.TextField(default=None, null=True)
    agregate  = models.ForeignKey('self', null=True)
    training = models.NullBooleanField(null=True, default=False, verbose_name=u'Было проведено обучение')
    info = models.TextField()
    
        
    def save(self, *args, **kwargs):
        import datetime
        now = datetime.datetime.now()
        idPk = self.pk
        super(Journal, self).save(*args, **kwargs)
        if not idPk:
            if self.person is None:
                 self.agregate = self
            else:
                date_filter = now - datetime.timedelta(seconds=60)
                journal = Journal.objects.filter(person = self.person, camera=self.camera, dt_last_fixed__gte = date_filter).exclude(id = self.id).order_by('-id')[:1]
                if journal.count()>0:
                    journal = journal[0] 
                    self.agregate = journal.agregate if journal.agregate is not None else self  
                else:
                    self.agregate = self
            self.save()

    def get_original_photo(self, width=None, height=None):
        from videoclient import settings
        from PIL import Image
        import base64
        from cStringIO import StringIO as StringIO
        
        objWidth = 0
        objHeight = 0
        COLOR = (255, 153, 0)
        
        try:
            #frame = settings.WWW_ROOT[:-1] + "/files/detects/test.jpg"
            frame = settings.MEDIA_ROOT + str(self.original)
            image_file = open(frame , "rb")
            object_frame = Image.open(image_file)
            #fWidth, fHeight = object_frame.size
            
            if width and height:
                object_frame.thumbnail((width, height), Image.ANTIALIAS)
                #objWidth, objHeight = object_frame.size
            
            #objWidth, objHeight = object_frame.size
            #factor = float(objWidth)/float(fWidth) if float(objWidth)/float(fWidth) < float(objHeight)/float(fHeight) else float(objHeight)/float(fHeight)
            #draw = ImageDraw.Draw(object_frame)
            #draw_face_on_image(draw, eye1=eye1, eye2=eye2, nose=nose, chin=chin, quad=quad, factor=factor, color=COLOR)  
            #del draw

            output = StringIO()
            object_frame.save(output, format="JPEG", quality=100)
            obj_content = output.getvalue()
            output.close()
            return base64.b64encode(obj_content)
        except:
            return None
        return None
    
    def get_original_photo_120x120(self):
        return self.get_original_photo(width=120, height=120)

    def get_original_info(self):
        return get_image_info(self.original.path)
    
    def get_found_info(self):
        return get_image_info(self.finded.path)
    
    def get_original_image_url(self):
        from videoclient import settings
        return settings.MEDIA_URL + str(self.original)
        
    def get_distance(self):
        try:
            if self.original_face:
                str = self.original_face
                face = str.split(',')
                return distCalculation(face)
            else:
                return None
        except:
            logging.exception(str(sys.exc_info()))
        return None
    
    def get_found_distance(self):
        try:
            if self.found_face:
                str = self.found_face
                face = str.split(',')
                return distCalculation(face)
            else:
                return None
        except:
            logging.exception(str(sys.exc_info()))
        return None
    
    def getDict(self, filter=""):
        data = dict()
        
        data['id'] = self.id
        if self.person: 
            data['person'] = self.person.getDict()
            data['division'] = self.person.person.status.division
        else: data['person'] = None
        if self.operator: 
            data['operator'] = self.operator.getDict()
        else: data['operator'] = None
        data['camera'] = self.camera
        if self.camera and self.camera.kpp: data['kpp_name'] = self.camera.kpp.name
        else: data['kpp_name'] = ""
        data['dt_first_fixed'] = self.dt_first_fixed
        data['dt_last_fixed'] = self.dt_last_fixed
        data['original'] = self.original
        data['finded'] = self.finded
        data['positions_status'] = self.positions_status
        data['positions_status_name'] = self.positions_status.name
        data['dt_open'] = self.dt_open        

        for d in data:
            if data[d] == None:
                data[d] = ''
            #if filter!="" and not searchData(data[d], filter): return None
        return data    
    
    class Meta:
        verbose_name="Запись в журнале"        
        verbose_name_plural="Журнал"
        
class LastIdent(models.Model):
    person = models.ForeignKey(PersonId)
    camera = models.ForeignKey(Camera)
    time = models.DateTimeField()
    agregate = models.ForeignKey(Journal)
    
    class Meta:
        unique_together = ("person", "camera")

#class JournalExtended(models.Model):
#    person = models.ForeignKey(PersonId, null=True, verbose_name=u'ID персоны')

#class JournalExtendedPhoto(models.Model):
#    journal = models.ForeignKey(Journal, null=True, verbose_name=u'Журнал')
#    journal_extended = models.ForeignKey(JournalExtended, null=True, verbose_name=u'Расширенный журнал')

class DefaultParams(models.Model):
    name = models.CharField(max_length=32, null=True, verbose_name=u'Имя параметра')
    value = models.CharField(max_length=32, null=False, verbose_name=u'Значение параметра')
    info = models.TextField(null=False, verbose_name=u'Комментарий')
    dt_create = models.DateTimeField(auto_now=False, auto_now_add=True)
    dt_update = models.DateTimeField(auto_now=True, auto_now_add=True)
    def __unicode__(self):
        return "%s = %s (%s...)" %(self.name if self.name is not None else "", self.value if self.value is not None else "", self.info[:96] if self.info is not None else "")
    class Meta:
        verbose_name="Настройку"
        verbose_name_plural="Настройки"

class Ground(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'Основание')
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Основание для посещения"
        verbose_name_plural='Основания для посещения'

class VisitingCard(models.Model):
    active = models.BooleanField(null=False, default=True, verbose_name=u'Активность')
    visitor = models.ForeignKey(PersonId, null=False, verbose_name=u'Id посетителя', related_name='person_who')
    person = models.ForeignKey(PersonId, null=False, verbose_name=u'Id персоны к кому', related_name='person_whom')
    ground = models.ForeignKey(Ground, null=False, verbose_name=u'Основание посещения')
    dt_enter = models.DateTimeField(null=False, verbose_name=u'Дата входа')
    dt_exit = models.DateTimeField(null=False, verbose_name=u'Дата выхода')
    dt_open = models.DateTimeField( auto_now=True, auto_now_add=True)
    
    class Meta:
        verbose_name="Карточку посещения"
        verbose_name_plural="Карточки посещений"
        
def get_sound_upload_to(instance, filename):   
    return "sounds/%s" % (filename)        
        
class Sound(models.Model):
    name = models.CharField(max_length=32, null=True)
    sound = models.FileField( upload_to=get_sound_upload_to)
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
    
    class Meta:
        verbose_name="Звук"
        verbose_name_plural="Звуки"
        
class Signal(models.Model):
    name_id = models.CharField(max_length=32, null=False, verbose_name=u'Строковый идентификатор')
    name = models.CharField(max_length=32, null=False, verbose_name=u'Название')
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
    
    class Meta:
        verbose_name="Внешнее событие"
        verbose_name_plural="Внешнии события"
        
class ProfileEvent(models.Model):
    name_id = models.CharField(max_length=32, null=False, verbose_name=u'Строковый идентификатор')
    name = models.CharField(max_length=32, null=False, verbose_name=u'Название')
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Провиль"
        verbose_name_plural="Провили"
        
class Event(models.Model):
    name_id = models.CharField(max_length=32, null=False, verbose_name=u'Строковый идентификатор')
    name = models.CharField(max_length=32, null=False, verbose_name=u'Название')
    sound = models.ForeignKey(Sound, null=True, verbose_name=u'Звук')
    signal = models.ForeignKey(Signal, null=True, verbose_name=u'Внешний сигнал')
    active = models.BooleanField(default=False)
    profile = models.ForeignKey(ProfileEvent, null=True, verbose_name=u'Профиль')
    
    def __init__(self, *args, **kwargs):
        if kwargs.has_key('object'):
            object = kwargs['object']
            del kwargs['object']
            if object is not None:
                kwargs['name_id'] = object.name_id
                kwargs['name'] = object.name
                kwargs['sound'] = object.sound
                kwargs['signal'] = object.signal
                kwargs['active'] = object.active
                kwargs['profile'] = object.profile
            
        models.Model.__init__(self, *args, **kwargs)
                
    def __unicode__(self):
        return self.name if self.name is not None else ""
    
    class Meta:
        verbose_name="Событие"
        verbose_name_plural="События"

class Types(models.Model):
    url = models.CharField(max_length=128, null=False, verbose_name=u'Путь')
    name = models.CharField(max_length=128, null=True, verbose_name=u'Название')
    division = models.ForeignKey(DivisionUser, null=True, verbose_name=u'Группа', blank=True)
    def __unicode__(self):
        return self.name if self.name is not None else ""
    class Meta:
        verbose_name="Тип"
        verbose_name_plural="Типы"
        
class List(models.Model):
    name = models.CharField(max_length=128, null=True, unique=True, verbose_name=u'Название')
    discription = models.TextField(null=True, blank=True, verbose_name=u'Описание')
    group = models.ForeignKey(GroupPerson, null=True, verbose_name=u'Группа', blank=True)
    type = models.ForeignKey(Types, null=True, verbose_name=u'Тип')
    level = models.CharField(max_length = 64, null=False, blank=True, verbose_name=u'Уровень угрозы', default="")
    active = models.BooleanField(default=True, blank=True)
    
    def __unicode__(self):
        return self.name if self.name is not None else ""
     
    class Meta:
        verbose_name="Список"
        verbose_name_plural="Списки"
        
class TimeTest(models.Model):
    person = models.ForeignKey(PersonId, null=True)
    camera = models.ForeignKey(Camera, null=True)
    count = models.IntegerField(null=False, default=0)
    dt_fixed = models.DateTimeField(null=True)
    
    #def __unicode__(self):
    #    return "%s %s" %(self.count if self.count is not None else "", self.dt_fized  if self.dt_fixed is not None else "")
    
class Roller(models.Model):
    com = models.ForeignKey(Communicator, null=False)
    camera = models.ForeignKey(Camera, null=True)
    dt_start = models.DateField(null=False)
    tm_start = models.TimeField(null=False)
    dt_stop = models.DateField(null=True)
    tm_stop = models.TimeField(null=True)
    filename = models.CharField(max_length=256, null=False)
     
    def __unicode__(self):
        #return "%s => %s (%s %s - %s)" %(self.com, self.camera, self.dt_start, self.tm_start, self.tm_stop)
        return "roller %s" % self.pk

    class Meta:
        verbose_name="Ролик"
        verbose_name_plural="Ролики"    

class Distortion(models.Model):
    name = models.CharField(max_length=256, null=False)
    count = models.IntegerField(null = False, default=3)
    v = models.FloatField(null=False, default=0)
    i = models.FloatField(null=False, default=0)
    x = models.FloatField(null=False, default=0.5)
    y = models.FloatField(null=False, default=0.5)
    def __unicode__(self):
        return self.name 
    class Meta:
        verbose_name="Ролик"
        verbose_name_plural="Ролики"  
        
def get_time_path():
    import datetime
    now = datetime.datetime.now()
    return "%s/%s/%s/%s" % (now.year, now.month, now.day, now.hour)
        
def get_upload_to_tmp(instance, filename):
    return "tmp/%s/%s_%s" % (get_time_path(), instance.id, filename)
        
class TmpImage(models.Model):
    image = models.ImageField(upload_to=get_upload_to_tmp)
    parent = models.ForeignKey('self', null=True)
    dt_open = models.DateTimeField( auto_now=True, auto_now_add=True)
    
    def delete(self):
        logging.info(self.image.path)
        if os.path.exists(self.image.path):
            os.remove(self.image.path)
        super(TmpImage, self).delete()

class Lens(models.Model):
    name = models.CharField(max_length=250, null=False)
    v = models.FloatField(null=False, default=0)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name="Объектив"
        verbose_name_plural="Объектвы"

import string
class LogingHash(models.Model):
    hash = models.CharField(max_length=32)
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    dt_open = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    @staticmethod
    def get_hash(length=32, chars=string.letters + string.digits):
        import md5
        import random
        return md5.md5(''.join([random.choice(chars) for i in range(length)])).hexdigest()
    
    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        if not self.hash:
            self.hash = LogingHash.get_hash() 
            self.save()
    
    @staticmethod
    def get_loging_by_hash(hash):
        import datetime
        time = datetime.datetime.now()
        first_time = datetime.datetime.now() - datetime.timedelta(minutes=1)
        list = LogingHash.objects.filter(hash=hash, dt_open__lte=time, dt_open__gte=first_time)
        if list.count()==0:
            return None
        else:
            return list[0]
        
        
    def __unicode__(self):
        return self.hash       
