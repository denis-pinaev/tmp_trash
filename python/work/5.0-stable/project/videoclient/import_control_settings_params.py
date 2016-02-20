#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

# Импорт настроек управляющей системы
# @revision   SVN: $Revision: 1977 $
# @date       $Date: 2012-02-16 15:07:04 +0300 (Чт, 16 фев 2012) $

#############   НАСТРОЙКА ПАРАМЕТРОВ ДЛЯ ИМПОРТА  ##################

# данные управляющей состемы
HOST = "192.168.0.55"
PORT = 16544
LOGIN = "catcher"
PASSWORD = "cather"
USER = "communicator"

import_filename = "" # файл с импортируемыми данными

PRINT_MESSAGE = True # выводить сообщения на экран об успешности операций
ACCOUNT_PERMISSIONS = 0 # Разрешить редактировать все параметры управляющей системы 
                           # (1 - разрешить,
                           # 0 - запретить редактировать параметры из списка "Не редактируемые параметры УС")
# база данных, где имеется список запрещенных к изменению параметров
DATABASES = {
    'default': {
        'ENGINE': 'mysql', #'sqlite3', #'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'oxion2', #SRC_ROOT+'sqlite3.db',#'vc_test_gale_ru',                      # Or path to database file if using sqlite3.
        'USER': 'oxion2',                       # Not used with sqlite3.
        'PASSWORD': 'oxion2',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

####################################################################

from balancer import Balancer
import os
import sys
import MySQLdb

def message(msg):
    if PRINT_MESSAGE: print msg

def get_notEditable():
    try:
        if ACCOUNT_PERMISSIONS: return []
        dbinfo = DATABASES["default"]
        db = MySQLdb.connect(host=dbinfo["HOST"], db=dbinfo["NAME"], user=dbinfo["USER"], passwd=dbinfo["PASSWORD"])
        db.query("set character_set_client=utf8")
        db.query("set character_set_connection=utf8")
        db.query("set character_set_results=utf8")
        db.query("select code from control_settings_noteditableparams where permit=false")
        rows = db.store_result()
        row = rows.fetch_row(0)
        params = map(lambda x: x[0], row)
        db.close()
        return params
    except:
        message(sys.exc_info())
        return []

def import_settings(filename=""):
    try:
        from xml.dom.minidom import parseString
        if filename:
            img = open(filename, "r")
            data = img.read()
            img.close()
            if data:
                b = Balancer(HOST, PORT, LOGIN, PASSWORD, USER)
                data = b.splitXmlParams(parseString(data))
                params = b.getAllParameters()
                notEditable = get_notEditable()
                for base in data:
                    for param in base["params"]:
                        if not param["name"] in notEditable:
                            if b.setParameter(value=param["val"], param = param["name"], toBase=base["name"]): message("%s set" % (param["name"]))
                            else: message("%s not set" % (param["name"]))
                        else: message("%s permit to set" % (param["name"]))
                for base in params:
                    f = filter(lambda x: x["name"] == base["name"], data)
                    del_param = len(f) == 0
                    for param in base["params"]:
                        if not param["name"] in notEditable:
                            if not del_param:
                                del_param = len(filter(lambda x: x["name"] == param["name"], f[0]["params"])) == 0
                            if del_param:
                                if b.deleteParameter(param=param["name"], toBase=base["name"]): message("%s delete" % (param["name"]))
                        else: message("%s permit to delete" % (param["name"]))
                return True
        return False
    except:
        message(sys.exc_info())
    finally:
        try:
            if b:
                b.close()
                del b
        except: pass
    return False


if len(sys.argv) > 1 or import_filename:
    if not import_filename: import_filename = sys.argv[1]
    if os.path.exists(import_filename):
        if import_settings(import_filename): message("Импорт завершен")
        else: message("Ошибка импорта")
    else: message("Нет указанного файла")
else: message("Не хватает параметров! Ожидается имя файла!")
