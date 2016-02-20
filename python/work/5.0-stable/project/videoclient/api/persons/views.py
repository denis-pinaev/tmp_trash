# coding=utf-8

from api.views import json_response, getDictFromListModel
from videoclient import models
from videoclient.communicator import Communicator
from videoclient.utils import updateBalId, getBalIdByName, DeletePerson
import logging
import sys

def getDictDataPersons(params=None, bal_id_update=True):
    m_persons = models.PersonId.objects.filter(active=True)
    if params is not None:
        if "group" in params and params["group"] is not None: m_persons = m_persons.filter(person__group__id = params["group"])
        if "id" in params and params["id"] is not None: m_persons = m_persons.filter(id = params["id"])
        if "bal_id" in params and params["bal_id"] is not None: m_persons = m_persons.filter(bal_id = params["bal_id"])
    d_persons = getDictFromListModel(m_persons, recurse_fields=['person'])
    
    if bal_id_update:
        updateBalId()
    for person in d_persons:
        try:
            if 'bal_id' not in person or 'bal_id' in person and person['bal_id'] is None:
                if 'id' in person:
                    person['bal_id'] = int(getBalIdByName(person['id'], bal_id_update=False))
        except:
            person["error"] = "bal_id not found"
    return d_persons

@json_response
def list(request):
    answer = dict()
    params = request.REQUEST
    answer["persons"] = getDictDataPersons(params)
    answer["status"] = True    
    return answer

@json_response
def manage(request):
    answer = dict()
    
    params = request.REQUEST
    if 'group' not in params:
        answer["error"] = "group in params not found"
        return answer
    if 'first_name' not in params:
        answer["error"] = "first_name in params not found"
        return answer
    if 'last_name' not in params:
        answer["error"] = "last_name in params not found"
        return answer
    if 'middle_name' not in params:
        answer["error"] = "middle_name in params not found"
        return answer
    
    id = params['id'] if 'id' in params else None
    
    res_id = None
    if id is not None:
        idPersons = models.PersonId.objects.filter(id = id)
        if idPersons.count() == 0:
            res_id = id
        
    if res_id is None:
        status = models.StatusUser.objects.raw("select videoclient_statususer.id as id from videoclient_list join videoclient_types on videoclient_list.type_id = videoclient_types.id join videoclient_statususer on videoclient_types.division_id = videoclient_statususer.division_id where group_id = %s limit 1;" %params["group"])
        
        person =  models.Person.objects.create(first_name=params["first_name"], last_name=params["last_name"], middle_name=params["middle_name"], group_id=params["group"], action=0, status_id = status[0].id)
        
        if id is not None:        
            idPerson = models.PersonId.objects.get(id = id)
            idPerson.person = person
            idPerson.save()
            person.action = 1
        else:
            idPerson = models.PersonId.objects.create(active=True, person=person)
                
        person.id_person=idPerson.id
        person.save()
        res_id = idPerson.id
    
    if res_id is None:
        answer["error"] = "person not found"
        return answer
    
    answer["persons"] = getDictDataPersons({"id": res_id})
    
    answer["status"] = True    
    return answer

@json_response
def delete(request):
    answer = dict()
    params = request.REQUEST
    if 'id' not in params:
        answer["error"] = "id in params not found"
        return answer
    try:
        DeletePerson(request, params['id'])
    except:
        logging.exception(str(sys.exc_info()))
        answer["exception"] = str(sys.exc_info())
        return answer
    answer["status"] = True
    return answer

@json_response
def delete_all(request):
    answer = dict()
    persons = models.PersonId.objects.filter(active=True)  # Удаляем только не удаленных персон из интерфейса
    try:
        for person in persons:
            try:
                DeletePerson(request, person.id)
            except:
                logging.exception("")
    except:
        logging.exception(str(sys.exc_info()))
        answer["exception"] = str(sys.exc_info())
        return answer
    answer["status"] = True
    return answer

