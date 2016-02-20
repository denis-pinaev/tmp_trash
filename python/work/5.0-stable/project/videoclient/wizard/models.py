#coding=utf-8

from django.db import models

class Settings(models.Model):
    value = models.TextField()
    active = models.BooleanField(default=False)