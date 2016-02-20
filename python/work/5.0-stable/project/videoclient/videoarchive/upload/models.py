#coding=utf-8

from django.db import models
import config
import os

class Settings(models.Model):
    name = models.CharField(max_length=64, null=True, verbose_name=u'Имя параметра')
    value = models.CharField(max_length=256, null=False, verbose_name=u'Значение параметра')
    info = models.TextField(null=False, verbose_name=u'Комментарий')
    
    def __unicode__(self):
        if len(self.info)>99:
            return "%s = %s (%s...)" %(self.name if self.name else "", self.value if self.value else "", self.info[:97] if self.info else "")
        else:
            return "%s = %s (%s)" %(self.name if self.name else "", self.value if self.value else "", self.info if self.info else "")
        
    @staticmethod
    def getValue(name):
        values = Settings.objects.filter(name=name)
        if values.count() > 0:
            return values[0].value
        return None
    
    class Meta:
        verbose_name="Настройку"
        verbose_name_plural="Настройки"
        
def get_format_file(fname):                                                                                                                                                                                               
    try:        
        import re
        ref = re.compile(".*\.([^.]+)$")
        m = ref.match(fname)
        if (m and m.group(1)):
            return "."+m.group(1).lower()
        return ""
    except:
        return ""
        
def get_tmp_name():
    import time
    return str(int(time.time()))

def get_files_upload_to(instance, filename):
    upload_dir = Settings.getValue(config.upload_dir)
    return os.path.join(upload_dir, "%s_%s%s" %(instance.id, get_tmp_name(), get_format_file(filename)))

class Files(models.Model):
    file = models.FileField(upload_to=get_files_upload_to)
    size = models.IntegerField(blank = True)
    dt_open = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    class Meta:
        verbose_name="Файл"
        verbose_name_plural="Файлы"
        
    @staticmethod
    def getNewId():
        file = Files.objects.create(size = 0)
        return file.id       