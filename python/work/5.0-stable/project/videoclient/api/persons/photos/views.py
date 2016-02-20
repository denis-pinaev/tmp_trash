from api.views import json_response, getDictFromListModel
from videoclient import models
from videoclient.communicator import Communicator
from videoclient.utils import getAllPhotosByName, getAllPhotosByBalId
from videoclient.views import getLeftPhotosCount

@json_response
def list(request):
    answer = dict()
    
    params = request.REQUEST
    if 'id' not in params and 'bal_id' not in params:
        answer["error"] = "id or bal_id in params not found"
        return answer
    
    get_base64 = False
    if 'get_base64' in params:
        if params['get_base64'] == "true":
            get_base64 = True
        elif params['get_base64'] != "false":
            answer["error"] = "get_base64 mast be true or false"
            return answer
    
    
    id = params['id'] if 'id' in params else None
    bal_id = params['bal_id'] if 'bal_id' in params else None
    photo_number = params['photo_number'] if 'photo_number' in params else None
     
    photos_num = None
    if bal_id is not None:
        photos_num = getAllPhotosByBalId(bal_id, get_base64 = get_base64, photo_number=photo_number)
    else:
        photos_num = getAllPhotosByName(id, get_base64 = get_base64, photo_number=photo_number)
    answer['photos_num'] = photos_num
    answer["status"] = True    
    return answer


@json_response
def left(request):
    answer = dict()
    params = request.REQUEST
    
    answer.update(getLeftPhotosCount())
    
    answer["status"] = True    
    return answer