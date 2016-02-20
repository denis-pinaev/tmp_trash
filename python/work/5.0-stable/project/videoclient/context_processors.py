# -*- coding: utf-8 -*-
from videoclient.utils import getVersion, getCurrentTime, getDataAllDefaultParams
import settings

def global_vars(request):
    data = {}
    data.update(getVersion())
    data.update(getCurrentTime())
    data['login_user'] = request.user.username
    data['LANGUAGES'] = settings.LANGUAGES
    data.update(getDataAllDefaultParams())
    return data