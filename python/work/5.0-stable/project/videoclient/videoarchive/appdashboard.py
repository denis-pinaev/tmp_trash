# coding=utf-8

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

class DefaultAppIndexDashboard(AppIndexDashboard):
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)
        #self.columns = 3
        self.title = 'Видео архив'
        self.children.append(
            modules.ModelList(
                title = u'Переводы',
                models=(
                    'videoarchive.models.Language',
                    'videoarchive.models.Group',
                    'videoarchive.models.Translation',
                ),
            ),
        )
        self.children.append(
            modules.ModelList(
                title = u'Настройки',
                models=(
                    'videoarchive.models.Settings',
#                    'videoarchive.communicator.models.Communicator',
                    'videoarchive.va.models.VaArchive',
                    'videoarchive.va.models.VaCamera',
                    'videoarchive.models.Signals',
                    'videoarchive.models.Week',
                ),
            )
        )
        
        self.children.append(
            modules.ModelList(
                title = u'Временные',
                models=(
                    'videoarchive.persons.models.Person',
                    'videoarchive.persons.models.Document',
                ),
            )
        )
