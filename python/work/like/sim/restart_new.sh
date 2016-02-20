killall python -u like.gale.ru
sleep 3
killall python -u like.gale.ru

PYTHONPATH=/srv/www/vhosts/like.gale.ru/project/:/srv/www/vhosts/like.gale.ru/project/   /srv/www/vhosts/like.gale.ru/project/sim/manage.py runfcgi method=prefork host=127.0.0.1 port=8885  maxrequests=1024 minspare=10 maxspare=30 maxchildren=50
