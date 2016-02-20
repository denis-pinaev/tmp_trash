#!/usr/bin/env python
#coding=utf-8 

#* @changedby  $Author: belova.u.a $
#* @version    SVN: $Id: update.py 5539 2012-10-26 09:28:04Z belova.u.a $
#* @revision   SVN: $Revision: 5539 $
#* @link       $HeadURL: http://svn.smilart.com/websysadm/branches/5.0-stable/project/videoclient/update/update.py $
#* @date       $Date: 2012-10-26 12:28:04 +0300 (Пт, 26 окт 2012) $

import os
config_file_name = "../settings.py"
if (os.path.isfile(config_file_name)):
  execfile(config_file_name)

import logging
import sys
import os
import MySQLdb

s_finded = MEDIA_ROOT+"journal/finded/"
s_found = MEDIA_ROOT+"journal/found/"
db_host = DATABASES["default"]["HOST"]
db_base = DATABASES["default"]["NAME"]
db_user = DATABASES["default"]["USER"]
db_passwd = DATABASES["default"]["PASSWORD"]

try:
    db = MySQLdb.connect(host=db_host, db=db_base, user=db_user, passwd=db_passwd)
        
    if os.path.exists(s_finded):
        os.rename(s_finded, s_found)        
        query = "update videoclient_journal set finded=replace(finded, '/finded/', '/found/');"
        db.query(query)
        db.commit()

    query = "alter table videoclient_camera add column name varchar(128) null;"
    db.query(query)
    db.commit()

    db.close()     
except:
    print sys.exc_info()



