# coding=utf-8

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

from videoarchive import dashboard

class CustomIndexDashboard(Dashboard):
#class CustomIndexDashboard(dashboard.CustomIndexDashboard):

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
#        dashboard.CustomIndexDashboard.__init__(self, **kwargs)
        #self.columns = 3
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
