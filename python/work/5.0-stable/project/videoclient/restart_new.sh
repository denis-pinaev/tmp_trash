killall python -u oxion2.test.gale.ru
sleep 3
killall python -u oxion2.test.gale.ru

PYTHONPATH=/srv/www/vhosts/oxion2.test.gale.ru/project/:/srv/www/vhosts/oxion2.test.gale.ru/project/   /srv/www/vhosts/oxion2.test.gale.ru/project/videoclient/manage.py runfcgi method=prefork host=127.0.0.1 port=8994  maxrequests=1024 minspare=1 maxspare=3 maxchildren=50
