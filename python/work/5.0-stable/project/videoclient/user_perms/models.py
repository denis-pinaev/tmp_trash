#coding=utf-8

from django.db import models
import user_perms

# Please don't use this model.
# This is only for create permissions
class PermissionsList(models.Model):
    class Meta:
        managed = False
        permissions = user_perms.PERMISSIONS
        
        