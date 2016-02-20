killall python -u vc.test.gale.ru
sleep 3
killall python -u vc.test.gale.ru

PYTHONPATH=/srv/www/vhosts/vc.test.gale.ru/project/:/srv/www/vhosts/vc.test.gale.ru/project/   /srv/www/vhosts/vc.test.gale.ru/project/videoclient/manage.py runfcgi method=prefork host=127.0.0.1 port=8891  maxrequests=1024 minspare=10 maxspare=30 maxchildren=50
