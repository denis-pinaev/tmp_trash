from django.core.urlresolvers import reverse
from admin_tools.menu.models import *

class CustomMenu(Menu):
    def __init__(self, **kwargs):
        super(CustomMenu, self).__init__(**kwargs)
#        self.children.append(
#            MenuItem(title='Home', url=reverse('admin:index'))
#        )
#        self.children.append(
#            AppListMenuItem(title='Applications')
#        )
#        self.children.append(
#            MenuItem(
#                title='Multi level menu item',
#                children=[
#                    MenuItem('Child 1'),
#                    MenuItem('Child 2'),
#                ]
#            ),
#        )
