killall python -u like.gale.ru
su like.gale.ru -c "PYTHONPATH=/srv/www/vhosts/like.gale.ru/project/:/srv/www/vhosts/like.gale.ru/project/sim/   /srv/www/vhosts/like.gale.ru/project/sim/manage.py runfcgi method=prefork host=127.0.0.1 port=8885  maxrequests=1024 minspare=10 maxspare=30  --verbosity=2 debug=true"

