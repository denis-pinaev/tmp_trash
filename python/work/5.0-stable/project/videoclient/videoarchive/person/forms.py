#coding:utf-8
from django import forms
from videoarchive.person import models
from videoclient.settings import log_videoarchive as logging

class PersonChangeForm(forms.Form):
    id = forms.IntegerField(required=False)
    #username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$', 
    #    help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."), 
    #    error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")}) 
    #password = forms.CharField( max_length=128, label=u'Пароль') 
    first_name = forms.CharField( max_length=30, label=u'Имя')
    last_name =  forms.CharField( max_length=30, label=u'Фамилия')
    middle_name = forms.CharField( max_length=32, label=u'Отчество')
    birthday = forms.DateField(required=False, input_formats=('%d.%m.%Y',))
    passport_series = forms.IntegerField(label=u'Серия', required=False)
    passport_number = forms.IntegerField(label=u'Номер', required=False)
    passport_note = forms.CharField(required=False)
    passport_date = forms.DateField(label=u'Дата выдачи', required=False, input_formats=('%d.%m.%Y',))
    address = forms.CharField(required=False)
    phone_work = forms.CharField( max_length=32, label=u'Служебный телефон', required=False)
    phone_home = forms.CharField( max_length=32, label=u'Домашний телефон', required=False)
    phone_mobile = forms.CharField( max_length=32, label=u'Мобильный телефон', required=False)
    note = forms.CharField(required=False)
#    division = forms.IntegerField(required=False)
#    position = forms.IntegerField(required=False)
    status = forms.IntegerField(required=False)
#    kpp = forms.IntegerField(required=False)

#    id_person = forms.IntegerField(required=False)
    #date = models.DateField(auto_now=True, auto_now_add=True) 
#    user = forms.IntegerField(required=False)
    action = forms.IntegerField(required=False)

#    note = forms.CharField(required=False)
#    group = forms.IntegerField(required=False)
#    status = forms.IntegerField(required=False)
#    goto = forms.IntegerField(required=False)
    #person = models.ForeignKey(Person, null=True, verbose_name=u'Персона') 
    document = forms.IntegerField(required=False)
    passport_code = forms.CharField(required=False)
    address_temp = forms.CharField(required=False)
    category = forms.IntegerField(required=False)
    number = forms.CharField(required=False)
#    article = forms.IntegerField(required=False)
#    article_part = forms.IntegerField(required=False)
#    article_item = forms.IntegerField(required=False)
#    room_facility = forms.CharField(required=False)

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

#        user.status = StatusUser.objects.get(id = int(self.cleaned_data["status"]))
#        user.division = DivisionUser.objects.get(id = int(self.cleaned_data["division"]))
#        try:
#            user.position = PositionUser.objects.get(id = int(self.cleaned_data["position"]))
#        except:
#            pass
#        try:
#            group = GroupPerson.objects.get(id = int(self.cleaned_data["group"]))
#            user.group = group.
#        except:
#            pass
#        try:
#            user.kpp = Kpp.objects.get(id = int(self.cleaned_data["kpp"]))
#        except:
#            pass
#        try:
#            user.user = User.objects.get(id = int(self.cleaned_data["user"]))
#        except:
#            pass

#        try:
#            user.category = Category.objects.get(id = int(self.cleaned_data["category"]))
#        except:
#            pass

#        try:
#            user.id_person = PersonId.objects.get(id = int(self.cleaned_data["id_person"]))
#        except:
#            pass

#        try:
#            user.article = Article.objects.get(id = int(self.cleaned_data["article"]))
#        except:
#            logging.info(sys.exc_info())

#        try:
#            user.article_item = ArticleItem.objects.get(id = int(self.cleaned_data["article_item"]))
#        except:
#            logging.info(sys.exc_info())

#        try:
#            user.article_part = ArticlePart.objects.get(id = int(self.cleaned_data["article_part"]))
#        except:
#            logging.info(sys.exc_info())
        #group = forms.IntegerField(required=False) 
        #goto = forms.IntegerField(required=False) 
        #person = models.ForeignKey(Person, null=True, verbose_name=u'Персона') 

        user.document = self.getValueByName(models.Document, "document")
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
#        user.room_facility = self.cleaned_data["room_facility"]

        #password = self.cleaned_data["password1"] 
        #if password != "": 
        #    user.set_password(password) 

        return user

    def saveUser(self, id=None):
        from videoarchive.person.views import idToNameForPerson, renameFR
        if id:
            user = models.Person.objects.filter(id=id)
            if user.count()==0: return None;      
            oldname = idToNameForPerson(id)
            user = self.setValue(user[0])
            """
            user = self.setValue(user)
            idPerson = Person.objects.get(id = user.id_person.id)
            oldUser = idPerson.person
            idPerson.person = user
            idPerson.save()
            from videoclient.utils import renameFR
            """
            user.action = 1        
            user.save()
            newname = idToNameForPerson(user.id)
            renameFR(oldname, newname)
            return user.id
        return None

    def addUser(self):
        user = models.Person.objects.create()
        user = self.setValue(user)
        user.action = 0
        user.save()
        return user.id
    
class ChangePersonNameForm(forms.Form):
    person = forms.IntegerField(required=True)
    name = forms.CharField( max_length=128, required=True)
