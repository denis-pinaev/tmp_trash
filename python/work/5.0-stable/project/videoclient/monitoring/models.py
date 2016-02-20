#coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _

MONITORING_STATUS_CHOICES =  (
    ('warning', _('Аварийная ситуация')),
    ('info', _('Информационное сообщение')),
    ('action', _('Действия с системой')),
)

MONITORING_TYPE_CHOICES =  (
    ('overload_temperatures', _('Перегрузки температур')),
    ('overload_queues', _('Перегрузки по очередям')),
    ('finding_objects', _('Нахождение объектов')),
    ('accident_components', _('Авария компонентов')),
    ('successful_boot', _('Успешная загрузка системы')),
    ('activating', _('Включение системы')),
    ('deactivating', _('Выключение системы')),
    ('update', _('Обновление системы')),
    ('testing', _('Тестирование системы')),
    ('license_testing', _('Проверка лицензий')),
    ('system_crash', _('Аварийное выключение системы')),
    ('va_info', _('Заканчивается свободное место')),
    ('va_critical', _('Закончилось свободное место')),
    ('va_error', _('Ошибка в работе')),
    ('exception', _('Неизвестная ошибка')),
)

def get_time_path():
    import datetime
    now = datetime.datetime.now()
    return "%s/%s/%s/%s" % (now.year, now.month, now.day, now.hour)

def get_upload_to_error(instance, filename):
    return "errors/%s/%s_%s" % (get_time_path(), instance.id, filename)

from django.contrib.sessions.models import Session
from videoclient.monitoring.utils import getMonitoringMessage
class Events(models.Model):
    date = models.DateField(auto_now=True, auto_now_add=True)
    time = models.TimeField(auto_now=True, auto_now_add=True)
    status = models.CharField(max_length=32, choices=MONITORING_STATUS_CHOICES)
    type = models.CharField(max_length=32, choices=MONITORING_TYPE_CHOICES)
    description = models.TextField()
    json_description = models.TextField()
    show = models.BooleanField(default=True)
    sessions = models.ManyToManyField(Session, through='Events_Sessions')
    error_file = models.FileField(upload_to=get_upload_to_error)
    error_level = models.IntegerField(default=3)
    message_id = models.CharField(max_length=64)
    
    def getDict(self):
        data = dict()
        data["id"] = self.id
        data["date"] = self.date
        data["time"] = self.time
        data["status"] = self.status
        data["type"] = self.type
        data["show"] = self.show
        data["sessions"] = self.sessions
        data["error_level"] = self.error_level
        data["message_id"] = self.message_id
        data["error_file"] = self.error_file
        data["get_status_display"] = self.get_status_display()
        data["get_type_display"] = self.get_type_display()
        data["description"] = getMonitoringMessage(self.description, self.json_description)
        return data
    
    def save_error(self, data):
        #fileno, path = tempfile.mkstemp()
        #f = open(path, 'w+b')
        #f.write(data)
        #f.close()
        
        #f = open(path, 'r+b')
        from django.core.files.base import ContentFile
        self.error_file.save('error.err', ContentFile(str(data)))
        self.save()
        
        #os.remove(path)
      
    
class Events_Sessions(models.Model):
    event = models.ForeignKey(Events)
    session = models.ForeignKey(Session)