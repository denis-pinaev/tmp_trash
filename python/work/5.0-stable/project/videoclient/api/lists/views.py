from api.views import json_response, getDictFromListModel
from videoclient import models
from videoclient import views as vcViews
from videoclient.communicator import Communicator
import logging
import sys

@json_response
def list(request):
    answer = dict()
    import settings
    
    params = request.REQUEST
    if 'id' not in params:
        m_lists = models.List.objects.filter(active=True).exclude(group__id__in=[settings.noise_learning, settings.self_learning])
    else:
        id = int(params["id"])
        m_lists = models.List.objects.filter(id = id)
    
    d_lists = getDictFromListModel(m_lists)
    
    get_photos_count = False
    if 'get_photos_count' in params:
        if params["get_photos_count"] == "true":
            get_photos_count = True 
        elif params["get_photos_count"] != "false":
            answer["error"] = "get_photos_count mast be true or false"
            return answer
        
    bal_id_update = False
    if 'bal_id_update' in params:
        if params["bal_id_update"] == "true":
            bal_id_update = True 
        elif params["bal_id_update"] != "false":
            answer["error"] = "bal_id_update mast be true or false"
            return answer
    
    for d_list in d_lists:
        personIds = models.PersonId.objects.filter(active=1, person__group__id=d_list["group"])
        d_list["person_count"] = personIds.count()
        
        if get_photos_count:
            count_person_photos = vcViews.getCountPersonPhotosOfObject(request, personIds, mainlist=True, bal_id_update=bal_id_update)
            d_list["person_photos_count"] = count_person_photos

    answer["lists"] = d_lists
    answer["status"] = True    
    return answer

@json_response
def add_list(request):
    answer = dict()
    status = False
    
    params = request.REQUEST    
    if 'name' not in params:
        answer["error"] = "name_was_not_found"
        return answer
    if "type" not in params:
        answer["error"] = "type_was_not_found"
        return answer
    if "group" in params: del(params["group"])
    
    result = vcViews.addList(params)
    answer.update(result)
    return answer

@json_response
def delete_list(request):
    answer = dict()
    params = request.REQUEST
    if 'id' not in params:
        answer["error"] = "id_was_not_found"
        return answer
    try:
        delete, error = vcViews.DeleteList(users=[params['id']])
        if not delete: answer["error"] = error 
        answer["status"] = delete
    except:
        logging.exception(str(sys.exc_info()))
        answer["error"] = "exception"
        answer["exception"] = str(sys.exc_info())
        answer["status"] = False
    return answer
