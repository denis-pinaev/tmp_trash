#!/bin/bash

root="/srv/www/vhosts/newyear.gale.ru/project/sim/statistic"
"$root/database.sh" < "$root/top.sql"

