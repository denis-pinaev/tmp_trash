#coding=utf-8
from django.db import models
from videoclient.communicator import models as comModels

class VaArchive(models.Model):
    #id = models.IntegerField(primary_key=True)
    ip = models.CharField(max_length=60)
    port = models.IntegerField()
    url = models.CharField(max_length=150)
    save_dir = models.CharField(max_length=150)
    active = models.BooleanField(default=1, null=False)
    
    def __unicode__(self):
        return "%s %s" %(self.ip, self.port) if self.ip and self.port is not None else ""
    
    class Meta:
        db_table = u'va_archives'
        verbose_name="Видеоархив"
        verbose_name_plural='Видеоархивы' 

class VaCamera(models.Model):
    #id = models.IntegerField(primary_key=True)
    ip = models.CharField(max_length=128)
    num = models.IntegerField(null=True, blank=True, default=0)
    type = models.CharField(max_length=60, blank=True)
    mac = models.CharField(max_length=60, blank=True)
    name = models.CharField(max_length=128, blank=True)
    
    def __unicode__(self):
        return "%s %s" %(self.ip, self.type) if self.ip and self.type is not None else ""
    
    class Meta:
        unique_together = ("ip", "type")
        db_table = u'va_cameras'
        verbose_name="Источник"
        verbose_name_plural='Источники'        

class VaCommandRoller(models.Model):
    #id = models.IntegerField(primary_key=True)
    source = models.CharField(max_length=75, blank=True)
    signal_type = models.CharField(max_length=75, blank=True)
    interval_roller = models.IntegerField(null=True, blank=True)
    tm_start = models.DateTimeField(null=True, blank=True)
    tm_stop = models.DateTimeField(null=True, blank=True)
    id_camera = models.ForeignKey(comModels.Camera, db_column = 'id_camera')
    id_signal = models.IntegerField(db_column = 'id_signal')
    id_archive = models.ForeignKey(VaArchive, db_column = 'id_archive')
    signal_params = models.CharField(max_length=300, blank=True)
    
    class Meta:
        db_table = u'va_commands'

class VaRoller(models.Model):
    #id = models.IntegerField(primary_key=True)
    tm_start = models.DateTimeField()
    tm_stop = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=450, blank=True)
    id_command = models.ForeignKey(VaCommandRoller, db_column='id_command')
    params = models.CharField(max_length=300)
    ms_start = models.IntegerField(default = 0)
    
    class Meta:
        db_table = u'va_rollers'

class VaPersonsFrame(models.Model):
    #id = models.IntegerField(primary_key=True)
    #id_frame = models.ForeignKey(VaFrame, db_column = 'id_frame')
    location_photo = models.CharField(max_length=300)
    id_cs = models.CharField(max_length=30, null=True, blank=True)
    fio_cs = models.CharField(max_length=180, blank=True)
    photo_cs = models.CharField(max_length=36, blank=True)
    k_cs = models.FloatField(null=True, blank=True)
    face = models.CharField(max_length=600)
    id_like = models.IntegerField(null=True, blank=True)
    tm_dt = models.DateTimeField()
    tm_ms = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    id_camera = models.ForeignKey(comModels.Camera, db_column = 'id_camera')
    id_archive = models.ForeignKey(VaArchive, db_column = 'id_archive')
    
    class Meta:
        db_table = u'va_frame_info'

class VaArchiveParams(models.Model):
    id_archive = models.ForeignKey(VaArchive, db_column = 'id_archive')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    
    class Meta:
        db_table = u'va_archive_params'
