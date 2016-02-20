set @dt = curdate();
#set @dt = '2011-02-22';
set @dt = date (adddate(@dt, interval -5 day));

delete from videoarchive_calendarstatistic where tm_start = @dt;
insert into videoarchive_calendarstatistic(tm_start , count_face, count_people, count_roller, count_camera, id_camera_id)
    select @dt, t2.count_face, t2.count_person, t1.count_roller, 1, t2.id_camera from
        (select id_camera, count(*) as count_roller from va_roller as va_r left join va_command_roller as va_cr on va_cr.id=va_r.id_command where date(va_r.tm_start)=@dt group by id_camera) as t1
        join (select va_cr.id_camera as id_camera, count(distinct(va_pf.id)) as count_face, count(distinct(if(va_pf.k_cs>0.3,va_pf.id_cs, 0))) as count_person  from va_roller as va_r
                inner join va_frames_roller as va_fr on va_r.id=va_fr.id_roller right join va_frame as va_f  on va_f.id=va_fr.id_frame
                left join va_persons_frame as va_pf on va_pf.id_frame=va_f.id inner join va_command_roller as va_cr on va_cr.id=va_r.id_command
                where date(va_r.tm_start)=@dt group by va_cr.id_camera) as t2
                on t1.id_camera=t2.id_camera
    ;
