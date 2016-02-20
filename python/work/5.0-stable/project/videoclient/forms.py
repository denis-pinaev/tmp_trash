# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from videoclient.models import User, StatusUser, DivisionUser, PositionUser, Kpp, Person, Category, PersonId, Document, Article, ArticleItem, ArticlePart, GroupPerson, List, Distortion, Types
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import Group as AuthGroup
from django import forms
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
import logging
import sys
import re
import settings

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        
class UserUserChangeForm(UserChangeForm):
    class Meta:
        model = User        
        
class UserUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        
class UserAdminPasswordChangeForm(AdminPasswordChangeForm):
    class Meta:
        model = User

def validate_phone_number(value):
    phoneMatchRegex = re.compile(r"^[0-9\-\(\)\# \+]*$")
    if not phoneMatchRegex.match(value):
        raise ValidationError(_('Номер может состоять из цифр и символов +()-#'))
        
class UserChangeForm(forms.Form):
    id = forms.IntegerField(required=False)
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    #password = forms.CharField( max_length=128, label=u'Пароль')
    first_name = forms.CharField( max_length=30, label=u'Имя', required=True)
    last_name =  forms.CharField( max_length=30, label=u'Фамилия', required=True)
    middle_name = forms.CharField( max_length=30, label=u'Отчество', required=False)
    birthday = forms.DateField(required=False)
    passport_series = forms.IntegerField(label=u'Серия', required=False)
    passport_number = forms.IntegerField(label=u'Номер', required=False)
    passport_note = forms.CharField(required=False)
    passport_date = forms.DateField(label=u'Дата выдачи', required=False)
    address = forms.CharField(required=False)
    phone_work = forms.CharField( max_length=32, label=u'Служебный телефон', required=False)
    phone_home = forms.CharField( max_length=32, label=u'Домашний телефон', required=False)
    phone_mobile = forms.CharField( max_length=32, label=u'Мобильный телефон', required=False)
    note = forms.CharField(required=False)
    division = forms.IntegerField(required=False)
    position = forms.IntegerField(required=False)
    status = forms.IntegerField(required=False)
    kpp = forms.IntegerField(required=False)
    password1 = forms.CharField( max_length=128, label=u'Пароль1', required=False)
    password2 = forms.CharField( max_length=128, label=u'Пароль2', required=False)
    staff = forms.IntegerField(required=False)
    django_group = forms.IntegerField(required=True)
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        
        from videoclient import utils
        if (not self.cleaned_data.has_key(utils.CREATE)) and (user.id == self.cleaned_data["id"]):
            return username
        
        raise forms.ValidationError(_("A user with that username already exists."))
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
    
    def setValue(self, user):
        user.username = self.cleaned_data["username"]
        #user.password = self.cleaned_data["password"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.middle_name = self.cleaned_data["middle_name"]
        user.birthday = self.cleaned_data["birthday"]
        user.passport_series = self.cleaned_data["passport_series"]
        user.passport_number = self.cleaned_data["passport_number"]
        user.passport_note = self.cleaned_data["passport_note"]
        user.address = self.cleaned_data["address"]
        user.phone_work = self.cleaned_data["phone_work"]
        user.phone_home = self.cleaned_data["phone_home"]
        user.phone_mobile = self.cleaned_data["phone_mobile"]
        user.note = self.cleaned_data["note"]
        
        user.staff = self.cleaned_data["staff"]
        
        user.groups = list(AuthGroup.objects.filter(id = self.cleaned_data["django_group"]))
        
        #user.devision = self.cleaned_data["devision"]
        #user.position = self.cleaned_data["position"]
        user.status = StatusUser.objects.get(id = int(self.cleaned_data["status"]))
        user.division = DivisionUser.objects.get(id = int(self.cleaned_data["division"]))
        try:
            user.position = PositionUser.objects.get(id = int(self.cleaned_data["position"]))
        except:
            pass
        user.kpp = Kpp.objects.get(id = int(self.cleaned_data["kpp"]))
        
        user.is_staff = True
        user.is_active = True
        user.is_superuser= False
        
        
        password = self.cleaned_data["password1"]
        if password != "":
            user.set_password(password)
         
        return user
        
    def saveUser(self):
        user = User.objects.get(id = self.cleaned_data["id"])
        #try:
        user = self.setValue(user)
        user.save()
        #except:
        #    raise RuntimeError
        
    def addUser(self):
        user = User.objects.create(username = self.cleaned_data["username"])
        #try:
        user = self.setValue(user)
        user.save()
        #except:
        #    raise RuntimeError
        return user.id
    
    
class PersonChangeForm(forms.Form):
    id = forms.IntegerField(required=False)
    #username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
    #    help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
    #    error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    #password = forms.CharField( max_length=128, label=u'Пароль')
    first_name = forms.CharField( max_length=30, label=u'Имя', required=False)
    last_name =  forms.CharField( max_length=30, label=u'Фамилия', required=False)
    middle_name = forms.CharField( max_length=30, label=u'Отчество', required=False)
    birthday = forms.DateField(required=False, input_formats=('%d.%m.%Y',))
    passport_series = forms.CharField(max_length=8, label=u'Серия', required=False)
    passport_number = forms.IntegerField(label=u'Номер', required=False)
    passport_note = forms.CharField(required=False, max_length=256)
    passport_date = forms.DateField(label=u'Дата выдачи', required=False, input_formats=('%d.%m.%Y',))
    address = forms.CharField(required=False, max_length=256)
    phone_work = forms.CharField( max_length=32, label=u'Служебный телефон', required=False, validators=[validate_phone_number])
    phone_home = forms.CharField( max_length=32, label=u'Домашний телефон', required=False, validators=[validate_phone_number])
    phone_mobile = forms.CharField( max_length=32, label=u'Мобильный телефон', required=False, validators=[validate_phone_number])
    note = forms.CharField(required=False)
    division = forms.IntegerField(required=False)
    position = forms.IntegerField(required=False)
    status = forms.IntegerField(required=False)
    kpp = forms.IntegerField(required=False)
    
    
    id_person = forms.IntegerField(required=False)
    #date = models.DateField(auto_now=True, auto_now_add=True)
    user = forms.IntegerField(required=False)
    action = forms.IntegerField(required=False)
    
    note = forms.CharField(required=False, max_length=256)
    group = forms.IntegerField(required=False)
    status = forms.IntegerField(required=False)
    goto = forms.IntegerField(required=False)
    #person = models.ForeignKey(Person, null=True, verbose_name=u'Персона')
    document = forms.IntegerField(required=False)
    passport_code = forms.CharField( max_length=8, required=False)
    address_temp = forms.CharField(required=False, max_length=256) 
    category = forms.IntegerField(required=False)
    number = forms.CharField( max_length=32, required=False)
    article = forms.IntegerField(required=False)
    article_part = forms.IntegerField(required=False)
    article_item = forms.IntegerField(required=False)
    room_facility = forms.CharField(required=False, max_length=32)
    
    def getValueByName(self, model, name, try_check = True):
        if try_check:
            try:
                return model.objects.get(id = int(self.cleaned_data[name]))
            except:
                pass
        else:
            return model.objects.get(id = int(self.cleaned_data[name]))
    
    def setValue(self, user):
        #user.username = self.cleaned_data["username"]
        #user.password = self.cleaned_data["password"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.middle_name = self.cleaned_data["middle_name"]
        user.birthday = self.cleaned_data["birthday"]
        user.passport_series = self.cleaned_data["passport_series"]
        user.passport_date = self.cleaned_data["passport_date"]
        user.passport_number = self.cleaned_data["passport_number"]
        user.passport_note = self.cleaned_data["passport_note"]
        user.address = self.cleaned_data["address"]
        user.phone_work = self.cleaned_data["phone_work"]
        user.phone_home = self.cleaned_data["phone_home"]
        user.phone_mobile = self.cleaned_data["phone_mobile"]
        user.note = self.cleaned_data["note"]
        
        #user.status = StatusUser.objects.get(id = int(self.cleaned_data["status"]))
        user.division = DivisionUser.objects.get(id = int(self.cleaned_data["division"]))
        try:
            user.position = PositionUser.objects.get(id = int(self.cleaned_data["position"]))
        except:
            pass
        try:
            group = GroupPerson.objects.get(id = int(self.cleaned_data["group"]))
            user.group = group 
        except:
            pass
        try:
            user.kpp = Kpp.objects.get(id = int(self.cleaned_data["kpp"]))
        except:
            pass
        try:
            user.user = User.objects.get(id = int(self.cleaned_data["user"]))
        except:
            pass
        
        try:
            user.category = Category.objects.get(id = int(self.cleaned_data["category"]))
        except:
            pass
        
        try:
            user.id_person = PersonId.objects.get(id = int(self.cleaned_data["id_person"]))
        except:
            pass
        
        try:
            user.article = Article.objects.get(id = int(self.cleaned_data["article"]))
        except:
            logging.info(sys.exc_info())
                
        try:
            user.article_item = ArticleItem.objects.get(id = int(self.cleaned_data["article_item"]))
        except:
            logging.info(sys.exc_info())
                
        try:
            user.article_part = ArticlePart.objects.get(id = int(self.cleaned_data["article_part"]))
        except:
            logging.info(sys.exc_info())
        #group = forms.IntegerField(required=False)
        #goto = forms.IntegerField(required=False)
        #person = models.ForeignKey(Person, null=True, verbose_name=u'Персона')
        
        user.document = self.getValueByName(Document, "document")
        #try:
        #    user.document = Document.objects.get(id = int(self.cleaned_data["document"]))
        #except:
        #    pass
        
        user.passport_code = self.cleaned_data["passport_code"]
        user.address_temp = self.cleaned_data["address_temp"]
        user.address_temp = self.cleaned_data["address_temp"]
        user.number = self.cleaned_data["number"]
        #user.article = self.cleaned_data["article"]
        #user.article_part = self.cleaned_data["article_part"]
        #user.article_item = self.cleaned_data["article_item"]
        user.room_facility = self.cleaned_data["room_facility"]
        
        #password = self.cleaned_data["password1"]
        #if password != "":
        #    user.set_password(password)
         
        return user
        
    def saveUser(self):
        user = Person.objects.create()
        user = self.setValue(user)
        idPerson = PersonId.objects.get(id = user.id_person.id)
        oldUser = idPerson.person
        idPerson.person = user
        idPerson.save()
        from videoclient.utils import renameFR
        user.action = 1
        user.save()
        renameFR(oldUser.id, user.id)
        return user.id
        
        
    def addUser(self):
        user = Person.objects.create()
        user = self.setValue(user)
        idPerson = PersonId.objects.create(person = user)
        user.id_person = idPerson.id
        user.action = 0
        user.save()
        return user.id

def get_training_group_choices():
    choices = ()
    exclude_dict = [settings.SELF_LEARNING, settings.noise_learning]
    try:
        choices = []
        for list in List.objects.exclude(group__id__in=exclude_dict).filter(active=True):
            id = list.group.id
            name = list.group.name
            if len(name)>40:
                name = '%s...'%(name[:38])
            choices.append((id, name))
    except:
        logging.exception(sys.exc_info())
        #pass
    return choices

class TrainingPersonGroup(forms.Form):
    person_group = forms.ChoiceField(widget=forms.Select(attrs={'class':'selector'}), choices=())
    
    def __init__(self, *args, **kwargs):
        super(TrainingPersonGroup, self).__init__(*args, **kwargs)
        choices = get_training_group_choices()
        #choices.extend(EXTRA_CHOICES)
        self.fields['person_group'].choices = choices
    
        
class TestClearDataJournal(forms.Form):
    dataClear = forms.DateField(required=False, input_formats=('%d.%m.%Y',),)
    period = forms.IntegerField(required = True) 


class TestExportData(forms.Form):
    fr = forms.BooleanField(required=False)
    journal = forms.BooleanField(required=False)
    admin = forms.BooleanField(required=False)
    db = forms.BooleanField(required=False)
    version = forms.BooleanField(required=False)
    
class ExportPersonForm(forms.Form):
    persons = forms.CharField(required=True)
    
class SaveDistortionForm(forms.ModelForm):
    class Meta:
        model = Distortion
        
class DeleteDistortionForm(forms.Form):
    id = forms.IntegerField(required=True)            
    
class TestRebootDaemon(forms.Form):
    balancerIp = forms.CharField(max_length=15, required=True)
    balancerPort = forms.IntegerField(required=True)
    daemonType = forms.CharField(max_length=128, required=True)
    daemonIp = forms.CharField(max_length=15, required=True)
    daemonPort = forms.IntegerField(required=True)

class TestSetBalancerState(forms.Form):
    balancerIp = forms.CharField(max_length=15, required=True)
    balancerPort = forms.IntegerField(required=True)
    stateUsed = forms.BooleanField(required=False)    
    daemonip = forms.CharField(max_length=64, required=False)
    daemonport = forms.CharField(max_length=64, required=False)
    type = forms.CharField(max_length=64, required=False)
    
class TestGetDaemonsStatistics(forms.Form):
    ip = forms.CharField(max_length=256, required=True)
    port = forms.CharField(max_length=256, required=True)
    colors = forms.CharField(max_length=256, required=False)
    
class TestGetStatistics(forms.Form):
    ip = forms.CharField(max_length=256, required=True)
    port = forms.CharField(max_length=256, required=True)
    index = forms.CharField(max_length=64, required=False)
    colors = forms.CharField(max_length=256, required=False)
    
class TestSetSelfLearning(forms.Form):
    source = forms.CharField(max_length=64, required=True)
    type = forms.CharField(max_length=64, required=True)
    param = forms.BooleanField(required=False)

class TestCameraDelete(forms.Form):
    uuid = forms.CharField(max_length = 255, required=False)
    id = forms.IntegerField(required=False)
    

class TestSelfLearning(forms.Form):
    id = forms.IntegerField(required=True)

class TestAddAlerts(forms.Form):
    new_address = forms.CharField(max_length=1024, required=True) 

class TestDelAlerts(forms.Form):
    delo = forms.IntegerField(required=True)
    
class TestFRForm(forms.Form):
    coeff = forms.FloatField(required=True)    
    
class TestCameraAlias(forms.Form):
    cid = forms.IntegerField(required=True)
    name = forms.CharField(required=False)
    
class CheckSaveRollersForm(forms.Form):
    rollers = forms.CharField(required=True)
    
class CheckStartRollerForm(forms.Form):
    uuid = forms.CharField(max_length = 255, required=True)

class CheckVideoarchiveAlertForm(forms.Form):
    app = forms.CharField(max_length=16, required=True)
    type = forms.CharField(max_length=32, required=True)
    id = forms.IntegerField(required=False)
    space = forms.IntegerField(required=False)
    command = forms.IntegerField(required=False) 

class CheckSimilarCameraForm(forms.Form):
    ip = forms.CharField(max_length=256, required=False)
    url = forms.CharField(max_length=256, required=False)
    port = forms.IntegerField(required=False)


class CkechDetectCoefficients(forms.Form):
    id = forms.IntegerField(required=True)
    numcamera = forms.IntegerField(required=False)

#from videoclient.models import TestModel
#import exwidgets as exWidgets

#COMPUTERS = (
#('0', 'ZX Spectrum'),
#('1', 'Amstrad'),
#('2', 'Atari'),
#('3', 'Commodore 64'),
#)

#LANGUAGES = (
#('0', 'Python'),
#('1', 'C++'),
#('2', 'C#'),
#('3', 'Java'),
#)

#G_ENGINES = (
#('0', 'HGE'),
#('1', 'Ogre 3D'),
#('2', 'Другой'),
#)

#class TestModelForm(forms.ModelForm):
#    password2 = forms.CharField(widget=exWidgets.PasswordInput(label=u'Подтвердите пароль', minlength='4', minlength_txt=u'Минимум 4 символа', required_txt=u'Введите пароль', required=True, equalTo='password', equalTo_txt=u'Пароли не совпадают', help_txt=u'например, 123456'))
  
#    class Meta:
#        model = TestModel
#        fields = ('name', 'description', 'level', 'password', 'password2', 'agree', 'letters', 'computers', 'money', 'money2', 'languages', 'languages1')
#        widgets = {
#            'name': exWidgets.TextInput(label=u'Название', minlength='3', minlength_txt=u'Пиши еще!', required_txt=u'Введите название', required=True),
#            'level': exWidgets.TextInput(help_txt=u'например, Level0', label=u'Уровень угрозы'),
#            'description': exWidgets.Textarea(label=u'Описание', required=True, required_txt=u'Введите описание', help_txt=u'например: пыщ пыщ'),
#            'password': exWidgets.PasswordInput(label=u'Пароль', minlength='4', minlength_txt=u'Минимум 4 символа', required_txt=u'Введите пароль', required=True),
#            'agree': exWidgets.CheckboxInput(label='Я согласен', required=True, required_txt='Подтвердите свое согласие'),
#            'letters': exWidgets.CheckboxInput(label='Подписаться на рассылку', checked=True),
#            'computers': exWidgets.Select(choices=COMPUTERS, label=u'Компьютер', help_txt=u'например: Amstrad', required=True, required_txt=u'Выберите модель', blank_choice=u'Пожалуйста выберите'),
#            'money': exWidgets.SpinBox(label=u'Счет', help_txt=u'например: 123', w=50, default=9, min=2, max=17, step=0.5),
#            'money2': exWidgets.SpinBox(label=u'Счет2'),
#            'languages': exWidgets.RadioSelect(choices=LANGUAGES, label=u'Язык программирования', help_txt=u'например: python'),
#            'languages1': exWidgets.RadioSelect(choices=G_ENGINES, label=u'Движок', help_txt=u'например: HGE', vertical=False),
#        }