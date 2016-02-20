# coding=utf-8
from django.template.defaultfilters import slugify
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from admin_tools.dashboard import modules
from admin_tools.dashboard.dashboards import AppIndexDashboard

from videoarchive import appdashboard         
        
class DefaultAppIndexDashboard(AppIndexDashboard):
#class DefaultAppIndexDashboard(appdashboard.DefaultAppIndexDashboard):
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)
        #appdashboard.DefaultAppIndexDashboard.__init__(self, *args, **kwargs)
        #app = appdashboard.DefaultAppIndexDashboard(*args, **kwargs)
        #self.children.extend(app.children)

        # we disable title because its redundant with the model list module
        self.title = 'Администрирование ОКСИОН'
        self.children.append(
            modules.ModelList(
                title = u'Системные',
                models=(
                    'videoclient.models.Balancer',
                    'videoclient.communicator.models.Communicator',
                    'videoarchive.va.models.VaArchive',
                ),
            ),
        )
        self.children.append(
            modules.ModelList(
                title = u'Настройки',
                models=(
                    'videoclient.models.DefaultParams',
                    'videoclient.videoarchive.models.Week',
                ),
            )
        )
        self.children.append(
            modules.ModelList(
                title = u'Переводы',
                models=(
                    'videoclient.models.Translation',
                    'videoclient.models.Language',
                    'videoclient.models.Group',
                ),
            )
        )
