killall python -u babyboom.gale.ru
sleep 3
killall python -u babyboom.gale.ru

PYTHONPATH=/srv/www/vhosts/babyboom.gale.ru/project/:/srv/www/vhosts/babyboom.gale.ru/project/   /srv/www/vhosts/babyboom.gale.ru/project/sim/manage.py runfcgi method=prefork host=127.0.0.1 port=9001  maxrequests=1024 minspare=10 maxspare=30 maxchildren=50
