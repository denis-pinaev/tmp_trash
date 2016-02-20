from django.db import models
from django.conf import settings
from django.db.models import ImageField, signals
from django.dispatch import dispatcher

class Visit(models.Model):
    viewer = models.PositiveIntegerField( default=0)
    user = models.PositiveIntegerField( default=0)
    dt_open = models.DateTimeField( auto_now=True, auto_now_add=True)
    def __unicode__(self):
        return u'%s' % (self.viewer)




