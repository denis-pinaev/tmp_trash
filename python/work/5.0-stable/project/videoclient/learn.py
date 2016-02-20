#!/usr/bin/env python2.6
#coding=utf-8
from django.core.management import setup_environ
import settings
setup_environ(settings)

from videoclient.models import Person, DivisionUser, PersonId, StatusUser, GroupPerson
from videoclient.utils import idToName
from videoclient.views import learning
import os
import sys

CONST_PATH = '/home/dmitry/50persons'
CONST_DIVISION = 'Персона'
CONST_STATUS = 'Осужденный'

def createPerson(first_name, last_name, middle_name, division, status):
    user = Person.objects.create()
    user.first_name = first_name
    user.last_name = last_name
    user.middle_name = middle_name
    user.division = DivisionUser.objects.get(name = division)
    user.status = StatusUser.objects.get(name = status, division=user.division)
    user.group = GroupPerson.objects.get(id = 3)
    
    user.action = 0
    idPerson = PersonId.objects.create(person = user)
    user.id_person = idPerson.id
    user.save()
    return idPerson.id
    
def learnPhoto(personId, path):
    name_person = idToName(personId)
    #print "Добавление фотографий для персоны: " + name_person
    count = 0
    all_count = 0
    for f in os.listdir(path):
        if f[-4:] != '.jpg':
            continue
        
        filename = "%s/%s" % (path, f)
        if os.path.isdir(filename):
            continue
         
        f = open(filename, 'r+b')
        data_file = f.read()
        all_count = all_count + 1
        #print "Добавление фотографии: " + str(f)
        if learning(data_file, name_person):
            count = count +1
        #print "Фотография обработана"
        f.close()
    
    return (count, all_count)

def allLearn(path):
    #print "Обучение всех фотографий"
    for f in os.listdir(path):
        filename = "%s/%s" % (path, f)
        if os.path.isdir(filename):
            #print "Обучение из папки: "+f
            res = f.split(' ')
            personId = createPerson(res[0], res[1], '', CONST_DIVISION, CONST_STATUS)
            stat = (0,0)
            try:
                stat = learnPhoto(personId, filename)
                print "%s %s создан, добавлено фотографий %s из %s" %(res[0], res[1], stat[0], stat[1])
            except:
                print "%s %s создан. Ошибка добавления фотографий: %s" %(res[0], res[1], str(sys.exc_info()))
        else:
            continue

allLearn(CONST_PATH)