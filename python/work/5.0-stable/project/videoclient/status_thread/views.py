from api.views import json_response, getDictFromListModel, getDictFromItemModel
from status_thread import models as stModels
import datetime

TIME_OUT_UPDATE_MINUTE = 10

@json_response
def list(request):
    answer = dict()
    params = request.REQUEST
    active = False
    if 'active' in params:
        if params['active'] == "true":
            active = True
        elif params['active'] == "false":
            active = False
        else:
            answer["error"] = "active mast be true or false"
            return answer
    if active:
        m_items = stModels.Status.objects.filter(state__lt = 2)
    else:
        m_items = stModels.Status.objects.all()
    if 'id' in params:
        id = params['id']
        m_items = m_items.filter(id = int(id))
    
    now = datetime.datetime.now() 
    time_delta = datetime.timedelta(minutes=TIME_OUT_UPDATE_MINUTE)
    m_items = m_items.filter(dt_update__gte = now - time_delta)
    d_items = getDictFromListModel(m_items, json_parse=['answer']) 
    answer["threads"] = d_items
    answer["status"] = True    
    return answer