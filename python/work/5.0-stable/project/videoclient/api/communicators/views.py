from api.views import json_response, getDictFromListModel
from videoclient import models
from videoclient.communicator import Communicator

@json_response
def list(request):
    answer = dict()
    m_lists = models.Communicator.objects.filter(active=True)
    d_lists = getDictFromListModel(m_lists) 
    answer["communicators"] = d_lists
    answer["status"] = True    
    return answer