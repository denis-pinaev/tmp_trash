#coding=utf-8
import sys
import settings

def execute_item(cursor, sql):
    if isinstance(sql, str):
        cursor.execute(sql)

def execute_sql(items):
    answer = False
    try:
        from django.db import connection, transaction
        cursor = connection.cursor()
        if isinstance(items, list):
            for item in items:
                cursor.execute(item)
        else:
            execute_item(cursor, items)
        
        transaction.commit_unless_managed()
        answer = True
    except:
        transaction.rollback_unless_managed()
        print str(sys.exc_info())
    answer = True # Предполагается что не зависимо от ошибок обновление выполнено успешно
    return answer

def update_from_revision_2190():
    sql = []
    sql.append('alter table videoarchive_tasks add column idtask character varying(16);')
    return execute_sql(sql)

def update_from_revision_2238():
    # 1, Добавдение номера камеры в таблицу камер и в уникальный ключ
    # 2. Связка камеры и коммуникатора
    from videoarchive.va import models as vaModels
    from videoarchive.communicator import models as comModels
    from videoclient import models as vcModels
    from videoarchive import utils as vaUtils
    try:
        cameras = vaModels.VaCamera.objects.all()
        cs = vaUtils.getAllCameras()
        for camera in cameras:
            c = filter(lambda x: x['ip']==camera.ip and x['type']==camera.type, cs)
            if len(c)>0:
                comm = vcModels.Communicator.objects.get(id=c[0]["com_id"])
                comModels.vaCameraCommunicator.objects.get_or_create(id_camera=camera, id_communicator=comm)            
            else: vaModels.VaCamera.objects.filter(id=camera.id).delete()
    except:
        print sys.exc_info()
    return True

def update_from_revision_2319():
    from videoarchive import models as vaModels
    sql = []
    sql.append('alter table videoarchive_resolutions add column width integer default 0;')
    sql.append('alter table videoarchive_resolutions add column height integer default 0;')
    if (execute_sql(sql)):
        try:
            resolutions = vaModels.Resolutions.objects.all()
            for resol in resolutions:
                width, height = resol.name.split("*")
                vaModels.Resolutions.objects.filter(id=resol.id).update(width=width, height=height)
            return True
        except:
            print sys.exc_info()
    return False

def update_from_revision_2441():
    from videoarchive.communicator import models as comModels
    cam_comm = comModels.vaCameraCommunicator.objects.all();
    clist = []
    for c in cam_comm:
        if c.id_communicator.active:
            if c.id_camera.id not in clist: clist.append(c.id_camera.id)
            else: comModels.vaCameraCommunicator.objects.filter(id=c.id).delete()
        else: comModels.vaCameraCommunicator.objects.filter(id=c.id).delete()
    return True

def update_from_revision_2477():
    sql = []
    sql.append('alter table web_api_users_webapisetting add column users_url character varying(250);')
    sql.append('alter table web_api_users_webapisetting add column stat_url character varying(250);')
    return execute_sql(sql)

def update_from_revision_2593():
    sql = []
    sql.append('ALTER TABLE maps_mapcamera ALTER COLUMN angle TYPE double precision;')
    sql.append('ALTER TABLE maps_mapcamera ALTER COLUMN angle SET NOT NULL;')
    return execute_sql(sql)

def update_from_revision_2734():
    sql = []
    sql.append("alter table videoclient_journal add column info text not null default '{}';")
    return execute_sql(sql)

def update_from_revision_2818():
    sql = []
    sql.append('alter table videoarchive_tasks add column repeat_task boolean not null default false;')
    sql.append('alter table videoarchive_tasks add column duration_type integer not null default 1;')
    sql.append('alter table videoarchive_tasks add column resolution character varying(16);')
    sql.append('alter table videoarchive_tasks add column all_day boolean not null default false;')
    sql.append('alter table videoarchive_tasks alter column resol_id drop not null;')
    from videoarchive import models as vaModels
    if (execute_sql(sql)):
        try:
            tasks = vaModels.Tasks.objects.all()
            for task in tasks:                
                vaModels.Tasks.objects.filter(id=task.id).update(resolution=task.resol.name, repeat_task=True)
            return True
        except:
            print sys.exc_info()
    return False 

def update_from_revision_2875():
    sql = []
    sql.append('alter table videoclient_kpp add column location character varying(128);')
    return execute_sql(sql)

def update_from_revision_2929():
    sql = []
    sql.append('ALTER TABLE videoarchive_tasks DROP CONSTRAINT "videoarchive_tasks_user_id_fkey";')
    sql.append('ALTER TABLE videoarchive_tasks ADD CONSTRAINT "videoarchive_tasks_user_id_fkey" FOREIGN KEY (user_id) REFERENCES videoclient_user(user_ptr_id) DEFERRABLE INITIALLY DEFERRED;')
    return execute_sql(sql)

def update_from_revision_3070():
    sql = []
    sql.append('alter table videoclient_communicator add column mjpeg_port integer default %s;' %settings.DEFAULT_COMMUNICATOR_MJPEG_PORT)
    return execute_sql(sql)

def update_from_revision_3093():
    sql = []
    sql.append('ALTER TABLE monitoring_events ADD column json_description text;')
    return execute_sql(sql)

def update_from_revision_3432():
    sql = []
    sql.append('alter table videoclient_journalupdater rename to videoclient_paramaggregator;')
    sql.append('delete from videoclient_paramaggregator;')
    return execute_sql(sql)

#def update_from_revision_3312():
#    from videoclient import models as vcModels
#    import uuid
#    answer = True
#    sql = []
#    sql.append('ALTER TABLE videoclient_camera DROP COLUMN num;')
#    sql.append('ALTER TABLE videoclient_camera ADD COLUMN uuid character varying(255);')
#    if not execute_sql(sql): answer = False
    
    # TODO script
#    sys.stdout.write("START UUID UPDATE")
    
#    i = 0
#    cameras = vcModels.Camera.objects.all()
#    for cam in cameras:
#        cam.uuid = str(uuid.uuid1())
#        if cam.name:
#            cam.name = "%s deprecated" % str(cam.name)
#        else:
#            cam.name = "%s %s deprecated" % (str(cam.ip), str(cam.type))
#        cam.save()
#        i += 1
    
#    sql = []
#    sql.append('ALTER TABLE videoclient_camera ALTER COLUMN "uuid" SET NOT NULL;')
#    sql.append("ALTER TABLE videoclient_camera ADD CONSTRAINT videoclient_camera_uuid_key UNIQUE(uuid);")
#    if not execute_sql(sql): answer = False
    
#    return answer

def update_from_revision_3337():
    sql = []
    
    answer = True
    
    if not execute_sql("alter table videoclient_journal add column t_first_fixed time without time zone not null default  '00:00:00';"): answer = False
    if not execute_sql("update videoclient_journal set t_first_fixed = dt_first_fixed;"): answer = False
    if not execute_sql("alter table videoclient_journal alter t_first_fixed drop default;"): answer = False
    if not execute_sql("create index videoclient_journal_t_first_fixed on videoclient_journal using btree (t_first_fixed);"): answer = False
    
    if not execute_sql("alter table videoclient_journal add column t_last_fixed time without time zone not null default  '00:00:00';"): answer = False
    if not execute_sql("update videoclient_journal set t_last_fixed = dt_last_fixed;"): answer = False
    if not execute_sql("alter table videoclient_journal alter t_last_fixed drop default;"): answer = False
    if not execute_sql("create index videoclient_journal_t_last_fixed on videoclient_journal using btree (t_last_fixed);"): answer = False
    
    if not execute_sql("alter table videoclient_journal add column photos_count integer not null default 1;"): answer = False
    
    return answer

def update_from_revision_3356():
    sql = []
    sql.append("alter table videoclient_journalupdater add column data text not null default '{}';")
    sql.append("alter table videoclient_journalupdater drop column journal_id;")
    sql.append("delete from videoclient_journalupdater;")
    return execute_sql(sql)

def update_from_revision_3455():
    sql = []
    #sql.append('alter table va_archive rename to va_archives;')
    #sql.append('alter table va_command_roller rename to va_commands;')
    #sql.append('alter table va_roller rename to va_rollers;')
    #sql.append('alter table va_persons_frame rename to va_frame_info;') 
    sql.append('ALTER TABLE va_archives ADD column active boolean not null default true;')    
    #sql.append('ALTER TABLE va_commands DROP CONSTRAINT "va_commands_id_camera_fkey";')
    #sql.append('ALTER TABLE va_commands ADD CONSTRAINT "va_commands_id_camera_fkey" FOREIGN KEY (id_camera) REFERENCES communicator_camera(id) DEFERRABLE INITIALLY DEFERRED;')
    sql.append('ALTER TABLE videoarchive_tasks DROP CONSTRAINT "videoarchive_tasks_camera_id_fkey";')
    sql.append('ALTER TABLE videoarchive_tasks ADD CONSTRAINT "videoarchive_tasks_camera_id_fkey" FOREIGN KEY (camera_id) REFERENCES communicator_camera(id) DEFERRABLE INITIALLY DEFERRED;')
    sql.append('ALTER TABLE videoarchive_calendarstatistic DROP CONSTRAINT "videoarchive_calendarstatistic_id_camera_fkey";')
    sql.append('ALTER TABLE videoarchive_calendarstatistic ADD CONSTRAINT "videoarchive_calendarstatistic_id_camera_fkey" FOREIGN KEY (id_camera) REFERENCES communicator_camera(id) DEFERRABLE INITIALLY DEFERRED;')        
    
    sql.append('ALTER TABLE va_archive_params DROP CONSTRAINT "va_archive_params_id_archive_fkey";')
    sql.append('ALTER TABLE va_archive_params ADD CONSTRAINT "va_archive_params_id_archive_fkey" FOREIGN KEY (id_archive) REFERENCES va_archives(id) DEFERRABLE INITIALLY DEFERRED;')
    sql.append('ALTER TABLE va_frame_info DROP CONSTRAINT "va_frames_info_id_archive_fkey";')
    sql.append('ALTER TABLE va_frame_info ADD CONSTRAINT "va_frames_info_id_archive_fkey" FOREIGN KEY (id_archive) REFERENCES va_archives(id) DEFERRABLE INITIALLY DEFERRED;')
    sql.append('ALTER TABLE va_frame_info ADD CONSTRAINT "va_frames_info_id_camera_fkey" FOREIGN KEY (id_camera) REFERENCES communicator_camera(id) DEFERRABLE INITIALLY DEFERRED;')
    sql.append('ALTER TABLE va_commands ADD CONSTRAINT "va_commands_id_signal_fkey" FOREIGN KEY (id_signal) REFERENCES videoarchive_signals(id) DEFERRABLE INITIALLY DEFERRED;')
    
    return execute_sql(sql)

def update_from_revision_3449():
    from videoclient import models as vcModels
    try:
        statusesOfusers = vcModels.StatusUser.objects.all()
        security_exists = False
        for su in statusesOfusers:
            if su.name == 'Охранник':
                security_exists = True
    
        if not security_exists:
            su = vcModels.StatusUser(division_id=1, name="Охранник")
            su.save()
    except:
        print sys.exc_info()

    return True

def update_from_revision_3668():
    sql = []
    sql.append('ALTER TABLE va_archives alter column active set default true;')
    return execute_sql(sql)
    
    
def update_from_revision_3707():
    sql = []
    sql.append("alter table videoclient_groupperson alter column name type varchar(128);")
    return execute_sql(sql)
    
def update_from_revision_3731():
    sql = []
    sql.append("update videoarchive_signals set name='По расписанию' where str_id='simple';")
    return execute_sql(sql)

def update_from_revision_3739():
    sql = []
    sql.append("ALTER TABLE communicator_camera add column available boolean null default true;")
    sql.append("ALTER TABLE communicator_camera add column port integer default 0;")
    sql.append("ALTER TABLE communicator_camera add column url varchar(255);")
    return execute_sql(sql)

def update_from_revision_3781():
    sql = []
    sql.append("ALTER TABLE communicator_camera add column delete boolean null default false;")
    return execute_sql(sql)

def update_from_revision_3831():
    sql = []
    sql.append("alter table videoclient_journal alter column coeff type double precision;")
    sql.append("alter table videoclient_journal alter column bound_coeff type double precision;")
    return execute_sql(sql)

def update_from_revision_4095():
    sql = []
    sql.append("drop table videoclient_lastident;")
    answer = execute_sql(sql)
    from videoclient.updates import run_syncdb
    run_syncdb()
    return answer

def update_from_revision_4969():
    sql = []
    sql.append('alter table videoclient_visitingcard add column active boolean default true;')
    return execute_sql(sql)

def update_from_revision_5045():
    sql = []
    
    answer = True
    
    if not execute_sql("alter table videoclient_journal add column person_not_found_id integer default NULL;"): answer = False
    if not execute_sql("create index videoclient_journal_person_not_found_id on videoclient_journal using btree (person_not_found_id);"): answer = False
   
    return answer

def update_from_revision_5381():
    sql = []
    if not execute_sql("alter table monitoring_events add column error_level integer default 0;"): return False
    if not execute_sql("alter table monitoring_events add column message_id varchar(64);"): return False
    return True

def update_from_revision_5450():
    sql = []
    if not execute_sql("alter table videoclient_journal add column training boolean default null;"): return False
    if not execute_sql("update videoclient_journal set training=(coeff=100); "): return False
    return True

def update_from_revision_5480():
    from videoclient import models as vcModels
    kpp = vcModels.Kpp.objects.all().order_by("id")[:1]
    if kpp:
        if not  execute_sql("update communicator_camera set kpp_id=%s; " %kpp[0].id): return False
    return True
    

# Указывается последняя ревизия без изменений.
# Например в ревизии 2113 у меня появится новая колонка в журнале,
# то название функции должно быть: update_from_revision_2112
# в случае успешного обновления должна вернуть True, в случае аварийного завершения Falst

# функция приведена для примера
 
#def update_from_revision_2112():
#    sql = []
#    sql.append('select * from videoclient_list')
#    return execute_sql(sql)
