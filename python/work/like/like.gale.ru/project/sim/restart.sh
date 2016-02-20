killall python -u like.gale.ru
sleep 3
killall python -u like.gale.ru
su like.gale.ru -c "LD_LIBRARY_PATH=/opt/imagemagick/lib:/srv/www/vhosts/like.gale.ru/lib/ PYTHONPATH=/srv/www/vhosts/like.gale.ru/project/:/srv/www/vhosts/like.gale.ru/project/sim/   /srv/www/vhosts/like.gale.ru/project/sim/manage.py runfcgi method=prefork host=127.0.0.1 port=8885  maxrequests=1024 minspare=10 maxspare=30    outlog=/var/log/python/like.gale.ru.out  errlog=/var/log/python/like.gale.ru.err --verbosity=2 debug=true"
ps aux | grep 8885 | wc -l
