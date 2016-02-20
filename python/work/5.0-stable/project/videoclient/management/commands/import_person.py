#coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from videoclient.updates import updates as updates_sql
from videoclient import updates
from optparse import make_option
import settings
import sys
import os
import json
import logging
import datetime
from videoclient.views import learning,initBalancer
from videoclient.models import User
from videoclient.balancer import Balancer  
from django.utils.translation import ugettext as _
from status_thread.models import Status
from django.db import connection, transaction


def get_keys_values(data, group_id=None):
    keys = ''
    values = ''
    
    i = 0
    for d in data:
        if d == "id" or d == "bal_id" or d == "user_id" or data[d] == None:
            continue
        if group_id and d == "group_id":
            data[d] = group_id
        if i>0:
            keys=keys+','
            values=values+','
        i = i+1
        keys = keys+d
        values = values+"'"+str(data[d])+"'"
    
    return '('+keys+')', '('+values+')'

def getStatusId(cursor, group_id):
    sql = "select videoclient_statususer.id as status_id from videoclient_list join videoclient_types on videoclient_list.type_id = videoclient_types.id join videoclient_statususer on videoclient_types.division_id = videoclient_statususer.division_id where group_id = %s limit 1;" %(group_id)
    logging.info("sql: %s" %sql)
    cursor.execute(sql)
    cursor_data =  cursor.fetchall()
    return cursor_data[0][0] if len(cursor_data)>0 and len(cursor_data[0])>0 else None

class Command(BaseCommand):
    args = "[all|journal]"
    
    def getUTF8Name(self, name):
        return unicode(name, 'utf-8')[:30]

    def handle(self, *args, **options):
        if len(args) < 2:
            return
        file_name = args[0]    
        if not args[1].isdigit():            
            return
        group_id = args[1]

        thread_id = ''
        thread = '' 
        if len(args) > 2 and args[2].isdigit():
            thread_id = args[2]
            try:
                thread = Status.objects.get(id=thread_id)
            except: 
                thread = ''   
        if thread:
            thread.setRunning()
        user_id = False
        if len(args) > 3 and args[3].isdigit():
            user_id = args[3]
        data=dict()  
        data["status"] = False 
        cursor = connection.cursor()
        HOST, PORT, LOGIN, PASSWORD, USER, Error = initBalancer(True)
      
        try:     
            import zipfile
            zf = zipfile.ZipFile(file_name, 'r')    
            files = zf.namelist()
            persons = []
            ids = dict()
            for file in files:
                try:
                    file = file.decode('UTF-8').encode('UTF-8')
                except:
                    file = file.decode('cp866').encode('UTF-8') 
                ids[file.split('/')[0]] = True
            id_num = 0
            percent = 0
            for id in ids:
                filename = id+'/'+'person.json'
                if filename in files:
                    text = zf.read(filename)
                    person_json = json.loads(text)
                else:
                    logging.info('id: '+str(id))
                    flm = id.split('.')[0].split()
                    logging.info(str(flm))
                    first_name = flm[0] if len(flm)>0 else ' ' 
                    last_name = flm[1] if len(flm)>1 else ' '
                    middle_name = flm[2] if len(flm)>2 else ' '
                    status_id = getStatusId(cursor, group_id)
                    
                    #информация об урезаниях имён должна использоваться для отчёта
                    person_json = {'first_name': self.getUTF8Name(first_name), 'last_name': self.getUTF8Name(last_name), 'middle_name': self.getUTF8Name(middle_name), 'group_id': group_id, 'status_id': status_id, 'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'category_id': '1', 'goto':'1'}
                    
                person_json["action"] = 0
                
                #sql = "select s1.division_id = s2.division_id as equal from (select division_id from videoclient_list join videoclient_types on videoclient_list.type_id = videoclient_types.id where group_id = %s) s1, (select division_id from videoclient_statususer where videoclient_statususer.id = %s) s2;" %(group_id, person_json["status_id"])
                sql = "select videoclient_statususer.id from videoclient_list join videoclient_types on videoclient_list.type_id = videoclient_types.id join videoclient_statususer on videoclient_types.division_id = videoclient_statususer.division_id where group_id=%s order by videoclient_statususer.id;" %(group_id)
                logging.info("sql: %s" %sql)
                cursor.execute(sql)
     
                # получаем результат выполнения запроса
                cursor_data =  cursor.fetchall()
                if len(cursor_data) == 0 or len(cursor_data[0]) ==0 or not cursor_data[0][0]:
                    persons.append({"person":id, "error": "error type", 'photos_json': {}})
                    res = False
                    continue
                else:
                    person_json["status_id"] = cursor_data[0][0]
                
                keys, values = get_keys_values(person_json, group_id)          
                
                sql = "INSERT into videoclient_person %s values %s RETURNING id;" %(keys, values)
                logging.info("sql: %s" %sql)
                cursor.execute(sql)
                id_person=cursor.fetchone()[0]
                
                if user_id:
                    users = User.objects.filter(id=user_id)
                    if len(users)>0:
                        try:
                            sql = "UPDATE videoclient_person set user_id=%s where id = %s" %(users[0].id, id_person)
                            logging.info("sql: %s" %sql)
                            cursor.execute(sql)
                        except:
                            logging.exception('import_person (%s) = ' + str(sys.exc_info()))
                filename = id+'/'+'personid.json'
                if filename in files:
                    text = zf.read(filename)
                    personid_json = json.loads(text)
                else:
                    personid_json = {'date': datetime.datetime.now().strftime('%Y-%m-%d'), 'active': 1}
                personid_json["person_id"] = id_person
                keys, values = get_keys_values(personid_json, group_id)
                
                sql = "INSERT into videoclient_personid %s values %s RETURNING id;" %(keys, values)
                logging.info("sql: %s" %sql)
                cursor.execute(sql)
                id_person_id=cursor.fetchone()[0]
                
                sql = "UPDATE videoclient_person set id_person=%s where id = %s" %(id_person_id, id_person)
                logging.info("sql: %s" %sql)
                cursor.execute(sql)
                
                id_num+=1
                filename = id+'/'+'photos.json'
                if filename not in files:
                    for file in files:
                        try:
                            n_file = file.decode('UTF-8').encode('UTF-8')
                        except:
                            n_file = file.decode('cp866').encode('UTF-8')
                        if n_file.startswith(id+'/') or (n_file == id and '.' in id):
                            text = zf.read(file)
                            if len(text)>0:
                                learning(text, str(id_person_id))
                        
                    persons.append({"person":id_person, "personid": id_person_id, 'photos_json': {}})
                    
                    current_percent = id_num*100/len(ids)
                    if thread:
                        if current_percent != percent:
                            percent = current_percent
                            thread.setPercent(percent)
                    continue
                text = zf.read(filename)
                photos_json = json.loads(text)
                
                
                b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
                
                try:
                    minBoundCoeffForLearn = b.getParameter('minBoundCoeffForLearn')
                    maxBoundCoeffForLearn = b.getParameter('maxBoundCoeffForLearn')
                    b.setParameter(param="minBoundCoeffForLearn", value="0")
                    b.setParameter(param="maxBoundCoeffForLearn", value="1")
                except:
                    transaction.rollback_unless_managed()
                    data["exception"] = str(sys.exc_info())
                    data["message"] = _("Неизвестная ошибка при инициализации управляющей системы")
                    logging.exception(str(sys.exc_info()))
                    if thread:
                        thread.setFinished()
                        thread.setAnswer(data)
                    return
            
                count = 0
                for photo_json in photos_json:
                    filename = id+'/'+photo_json["name"]
                    eyes = None
                    try:
                        if len(photo_json["params"]["response"])>0:
                            if photo_json["params"]["response"][0].has_key('info'):
                                info = photo_json["params"]["response"][0]["info"]
                                if len(info)>0:
                                    eyes = info[0]["eyes"]
                    except:
                        pass   
                    data_file = zf.read(filename)
                    if learning(data_file, str(id_person_id), add_original_photo=False, eyes = eyes):
                        count=count+1
                    
                    try:    
                        if len(photo_json["base_name"]) > 0:
                            filename_base = id + '/' + photo_json["base_name"]
                            write_f = settings.LEARNING_IMAGES + '%s/%04d.jpg' % (str(id_person_id), int(photo_json["params"]["response"][0]["name_photo"][0]))
                            data_file = zf.read(filename_base)
                            if len(data_file) > 0:
                                path = os.path.dirname(write_f)
                                if not os.path.exists(path):
                                    os.makedirs(path)
                                f = open(write_f, 'w+b')
                                f.write(data_file)
                                f.close()
                    except:
                        logging.exception("imp_exp import base photo person: "+str(sys.exc_info()))
    
                    try:
                        if len(photo_json["meta"]) > 0:
                            photoexif = models.PhotoExifData(personid_id=int(id_person_id), person_id=int(id_person_id), photo_id=int(photo_json["params"]["response"][0]["name_photo"][0]), exif=photo_json["meta"])
                            photoexif.save()
                    except:
                        logging.exception("imp_exp import zip metadata: "+str(sys.exc_info()))
    
                #persons.append({"person":id_person, "personid": id_person_id, 'photos_json': photos_json})
    
                try:
                    b.setParameter(param="minBoundCoeffForLearn", value=minBoundCoeffForLearn)
                    b.setParameter(param="maxBoundCoeffForLearn", value=maxBoundCoeffForLearn)
                except:
                    transaction.rollback_unless_managed()
                    data["exception"] = str(sys.exc_info())
                    data["message"] = _("Неизвестная ошибка при инициализации управляющей системы")
                    logging.exception(str(sys.exc_info()))
                    if thread:
                        thread.setFinished()
                        thread.setAnswer(data)
                    return
                b.close()
                del b
                if thread:
                    current_percent = id_num*100/len(ids)
                    if current_percent != percent:
                        percent = current_percent
                        thread.setPercent(percent)
                        
            zf.close()
            
            data['persons'] = persons
            data["status"] = True
            
        except:
            print 'except',str(sys.exc_info())
            data["exception"] = str(sys.exc_info())
            data["message"] = _("Неизвестная ошибка при импорте персон")
            logging.exception(str(sys.exc_info()))
            
        if data["status"]:
            transaction.commit_unless_managed()
        else:
            transaction.rollback_unless_managed()
        if thread:
            os.remove(file_name)
            thread.setAnswer(data)
            thread.setFinished()
            
         
        
           
    
