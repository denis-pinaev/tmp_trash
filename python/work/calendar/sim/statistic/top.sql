set @dt = curdate();
#set @dt = date (adddate(@dt, interval -5 day));
set @dt_next = date (adddate(@dt, interval 1 day));

#alter table faces_storedframe modify wizer_code varchar(64)CHARACTER SET utf8 COLLATE utf8_unicode_ci;
#alter table faces_storedframe MODIFY wizser_code CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';
#alter table faces_wizer modify code CHARACTER SET utf8 COLLATE 'utf8_unicode_ci';

#delete from statistic_contesttop where date = @dt;
insert into fb_contesttop(dt_date , count_vote, user, contest_id)
    select
	@dt,
	count_vote,
	user,
	id
    from fb_contestimage
    where id=(select max(id) from fb_contestimage as ci
              join (select max(count_vote) as count_vote, dt_date from fb_contestimage where dt_date=@dt group by dt_date) as mx
              using(count_vote, dt_date) group by count_vote)
    ;
