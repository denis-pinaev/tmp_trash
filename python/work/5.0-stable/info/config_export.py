#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from export_funcs import tar_fr, tar_journal, tar_admin, tar_db_dump, tar_version

### Обязательные параметры ###

media_root = "/home/smirnova.u.a/workspace/wspe3/websysadm/brunches/oxion-passive/websysadm_update/www/"
media_url = "/files/tar/"
tar_dir = media_root+media_url
http_host = ""

fname = tar_dir+"all_info.txt" # Файл с информацией о системе (камеры, балансировщик, демоны)
command_fname = tar_dir+"command.txt" # Файл с информацией собранной из следующих команд 
commands_list = ["netstat -anp | grep 8000"]
# Дириктории и файлы обязательных параметров для упаковки в архив
required_paths = [fname, command_fname]
tar_name = tar_dir+"info.tar" # Имя архива обязательных параметров


### Опции ###

# fr - упаковка в архив папки с fr-ом
# journal - упаковка в архив журнала
# admin - упаковка всей админки
# db_dump - упаковка баз данных
# version  - получение версий

# Список опций 
options_functions = {"fr": tar_fr, "journal": tar_journal, "admin": tar_admin, "db_dump": tar_db_dump, "version": tar_version}

admin_dir = "/home/smirnova.u.a/workspace/wspse1/websysadm/brunches/oxion-passive/project/" # Дириктория всей админки - для упаковки а архив
admin_tar_name = tar_dir+"admin.tar" # Имя этого архива
journal_dir = "/home/smirnova.u.a/workspace/wspse1/websysadm/brunches/oxion-passive/www/files/journal/" # Дириктория журнала - для упаковки а архив
journal_tar_name =  tar_dir+"journal.tar" # Имя этого архива
fr_dir = "/home/smirnova.u.a/workspace/wspse1/websysadm/brunches/oxion-passive/www/files/journal/" # Дириктория fr-a - для упаковки а архив
fr_tar_name = tar_dir+"fr.tar" # Имя этого архива
dump_tar_name = tar_dir+"dump.tar"  # Имя архива с дампами баз данных админки и управляющей системы
version_tar_name = tar_dir+"version.tar"

# Список баз данных, дамп которых нужно делать
#db_list = [{"host": '' , "port": '', "login": '', "password": '', "name": ''}]
db_list = [{"host": '127.0.0.1' , "port": 0, "login": 'oxion_p_gale_ru', "password": 'oxion_p_gale_ru', "name": 'oxion_p_gale_ru'}]
admin_db_index = 0 # Индекс базы админки
# Список команд для получения версии (tar_version)
version_list = ["netstat -anp | grep 8000"]


info_value = {"info.tar": "Общая информация",
              "admin.tar": "Админка",
              "version.tar": "Версии ПО",
              "dump.tar": "Базы данных",
              "journal.tar": "Журнал",
              "fr.tar": "База идентифицируемых личностей"}