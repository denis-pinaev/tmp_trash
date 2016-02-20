#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging
import commands

from balancer import Balancer
from xml.etree.ElementTree import ElementTree, Element
from StringIO import StringIO
import config_export
import MySQLdb

def get_url(url, name=""):
    url = url.replace(config_export.media_root, '')
    return "<li><a href='%s'>%s</a></li>" % (url, name if name else url)

def get_info(name=""):
    try:
        b = config_export.db_list[config_export.admin_db_index]
        db = MySQLdb.connect(host = b["host"], db = b["name"],user = b["login"],passwd = b["password"], port=int(b["port"]))
        c = db.cursor(MySQLdb.cursors.DictCursor)
        c.execute("SELECT * FROM %s" % (name))
        row = c.fetchall()
        c.close()
        return row
    except:
        logging.error("get info "+str(sys.exc_info()))
        return []

def get_all_params(obj, s):
    e = Element("%s_list" % (s))
    for c in obj:
        e1 = Element(s)
        for k in c:
            try:
                e11 = Element(k)
                e11.text = str(c[k])
                e1.append(e11)
            except: pass
        e.append(e1)
    return e

def get_balancer_params(obj, s):
    e = Element("%s_list" % (s))
    for c in obj:
        e1 = Element(s)
        for k in c:
            try:
                e11 = Element(k)
                e11.text = str(c[k])
                e1.append(e11)
            except: pass
        try:
            b = Balancer(c["host"], c["port"], c["login"], c["passwd"], c["user"])
            e11 = Element("demons_list")
            t = b.getSystemInfo()
            e11.text = str(t)
            e1.append(e11)
            e1.append(get_parameter(b, ['eyes_distance', 'journalBoundCoeff', 'minBoundCoeffForLearn', 'maxBoundCoeffForLearn'], "configuration_recognizers"))
            b.close()
        except: logging.info(sys.exc_info())

        e.append(e1)
    return e

def get_parameter(b, d, s):
    e = Element(s)
    for di in d:
        try:
            txt = b.getParameter(di)
        except:
            txt = 0
        e1 = Element(di)
        e1.text = txt
        e.append(e1)
    return e

def tar_objects(tname, d):
    try:
        os.system("tar -czf %s %s" % (tname, d))
    except:
        logging.info("tar_objects "+str(sys.exc_info()))

def tar_fr():
    tar_objects(config_export.fr_tar_name, config_export.fr_dir)
    print get_url(config_export.fr_tar_name, config_export.info_value["fr.tar"])
    

def tar_journal():
    tar_objects(config_export.journal_tar_name, config_export.journal_dir)
    print get_url(config_export.journal_tar_name, config_export.info_value["journal.tar"])


def tar_admin():
    tar_objects(config_export.admin_tar_name, config_export.admin_dir)
    print get_url(config_export.admin_tar_name, config_export.info_value["admin.tar"])


def tar_db_dump():
    try:
        s = []
        for i, item in enumerate(config_export.db_list):
            dump_admin_name = "%sdump_name%s.dump" % (config_export.tar_dir, i)
            os.system("mysqldump --host=%s --port=%s -u%s -p%s %s > %s" % (item["host"], item["port"], item["login"], item["password"], item["name"], dump_admin_name))
            s.append(dump_admin_name)
        if len(s)>0: 
            tar_objects(config_export.dump_tar_name, " ".join(s))
            print get_url(config_export.dump_tar_name, config_export.info_value["dump.tar"])
        return True
    except:
        logging.error("tar db dump "+str(sys.exc_info()))
        return False

def get_commands(command, fname):
    try:
        s = []
        root = Element("commands_list")
        for c in command:
            e = Element("item")
            data = commands.getoutput(c)
            e11 = Element("command")
            e11.text = c
            e.append(e11)
            e12 = Element("value")
            e12.text = str(data)
            e.append(e12)
            root.append(e)
        tree = ElementTree(root)
        f = StringIO()
        tree.write(f, 'UTF-8')
        fl = open(fname, "w")
        fl.write(str(f.getvalue()))
        fl.close()
        return True
    except:
        logging.error("get commands "+str(sys.exc_info()))
        return False

def tar_version():
    try:
        fname = "%sversion.txt" % (config_export.tar_dir)
        if get_commands(config_export.version_list, fname):
            tar_objects(config_export.version_tar_name, fname)
            print get_url(config_export.version_tar_name, config_export.info_value["version.tar"])
            return True
    except:
        logging.error("tar version "+str(sys.exc_info()))
        return False

