#coding=utf-8
import os


delay_update = "delay_update"
delayed_removal = "delayed_removal"
upload_dir = "upload_dir"

default_settings = [
                    {"name": delay_update,      "value": 500,           "info": "мс. Задержка для обновления полосы загрузки."},
                    {"name": delayed_removal,   "value": 1,             "info": "дней. Задержка удаления старых файлов."},
                    {"name": upload_dir,        "value": "upload_dir/", "info": "директория загрузки файлов."},
                    ]                    
                    