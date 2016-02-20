
import sys
from django.db.models import signals
from videoarchive.upload import config
        
def default_settings(app, created_models, verbosity, **kwargs):
    from videoarchive.upload import models
    from django.core.management import call_command
    if models.Settings in created_models and kwargs.get('interactive', True):
        for param in config.default_settings:
            try:
                if models.Settings.objects.filter(name = param["name"]).count() == 0:
                    models.Settings.objects.create(name = param["name"], value=param["value"], info=param["info"])
                    print "Creating param %s" %param["name"]
            except:
                print "ERROR %s %s" %( param["name"], str(sys.exc_info()))

signals.post_syncdb.connect(default_settings, 
    dispatch_uid = "upload.management.default_settings")
