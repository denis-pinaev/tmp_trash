#!/bin/bash
exit
DESTDIR=$2
CREATEFILE=/backup/complete
DB_NAME="balancer"
DB_USER="balancer"
DB_PASS="balancer"
FR_BASE="/opt/daemons/rec/1/"
FR_RESTART="/opt/scripts/fr.sh"
CB_RESTART="/opt/scripts/cb.sh"
JOURNAL="/srv/www/vhosts/vc.test.gale.ru/www/files/journal/"
MANAGEPY="/srv/www/vhosts/vc.test.gale.ru/project/videoclient/manage.py"

case $1 in
    backup)
        mysqldump -u$DB_USER -p$DB_PASS $DB_NAME > /tmp/control.sql
        python $MANAGEPY dumpdata > /tmp/sa.json
        tar -cPf $DESTDIR $FR_BASE $JOURNAL /tmp/sa.json /tmp/control.sql 
    ;;
    restore)
        rm -rf $JOURNAL
        rm -rf $FR_BASE
        tar -C /-xvf $DESTDIR
        mysql -u$DB_USER -p$DB_PASS $DB_NAME < /tmp/control.sql
        python $MANAGEPY loaddata /tmp/sa.json
        $FR_RESTART
        $CB_RESTART
    ;;
esac

rm /tmp/control.sql
rm /tmp/sa.json
touch $CREATEFILE