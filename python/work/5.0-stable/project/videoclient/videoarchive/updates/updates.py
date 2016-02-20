#coding=utf-8

def execute_sql(sql):
    print sql
    import settings
    import MySQLdb
    db_host = settings.DATABASES["default"]["HOST"]
    db_base = settings.DATABASES["default"]["NAME"]
    db_user = settings.DATABASES["default"]["USER"]
    db_passwd = settings.DATABASES["default"]["PASSWORD"]                   
    db = MySQLdb.connect(host=db_host, db=db_base, user=db_user, passwd=db_passwd)
    db.query(sql)
    db.commit()
    db.close()
    
# Используйте videoclient/updates/updates.py    

def _1_1_214():
    execute_sql("alter table videoarchive_tasks add column duration double default NULL;")
    return 1, 1, 235

def _1_1_235():
    execute_sql("update videoarchive_codecs set name='mpeg4' where number=3;")
    
    from videoclient import utils
    return 4, 1, 1495

def _4_1_1495():
    execute_sql("alter table videoarchive_tasks add column gop int(11) default 1;")
    
    from videoclient import utils
    return 4, 1, 1531

def _4_1_1531():
    execute_sql("alter table videoarchive_tasks add column compress double default Null;")
    
    from videoclient import utils
    return 4, 1, 1575

def _4_1_1575():
    execute_sql("alter table videoarchive_tasks add column bitrate int(11) default Null;")
    execute_sql("alter table videoarchive_tasks add column blur double default Null;")
    return 4, 1, 1664

# Используйте videoclient/updates/updates.py

