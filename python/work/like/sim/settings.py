# -*- coding: utf-8 -*-.. 
# -*- encoding: utf-8 -*-
import os;

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'      # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'like_gale_ru'   # Or path to database file if using sqlite3.
DATABASE_USER = 'like_gale_ru'   # Not used with sqlite3.
DATABASE_PASSWORD = 'gbplbrkzec'         # Not used with sqlite3.
DATABASE_HOST = '127.0.0.1' # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


#sys.path.append('/srv/www/vhosts/like.gale.ru/project/')


TIME_ZONE = 'Russia/Moscow'
LANGUAGE_CODE = 'en-en'

USE_I18N = True

PROJECT_ROOT = "/srv/www/vhosts/like.gale.ru/"
WWW_ROOT = PROJECT_ROOT + 'www/'

MEDIA_URL = '/files/media/'
HTTP_HOST = 'http://like.test.gale.ru/'
MEDIA_ROOT = '/srv/www/vhosts/like.gale.ru/filedir/'

STORED_IMG = 'files/media/' # путь к постоянно хранимым файлам. Относительно MEDIA_ROOT
TMP_IMG = 'files/media/'    # путь к временным файлам. Относительно MEDIA_ROOT 

LOG_DIR = "/home/srv/www/vhosts/like.gale.ru/tmpfiledir/"

ADMIN_MEDIA_PREFIX = '/admin/media/'
SECRET_KEY = 'u3h92fgh&nme)y)%o16o=y1-z526i6ht(=vt7!furxr=p8-guw7!'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'sim.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
    '/srv/www/vhosts/like.test.gale.ru/project/sim/fb/templates/',
#    "/usr/local/lib64/python2.6/site-packages/django/contrib/admin/templates/"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
#    'registration',
    'vkontakte',
    'sim',
    'sim.vk',
    'sim.fb',
    'sim.mp'
)

DEFAULT_FROM_EMAIL = 'hjtgdrfyt@gmail.com'
ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hjtgdrfyt@gmail.com'
EMAIL_HOST_PASSWORD = 'django registration'
EMAIL_USE_TLS = True

LOGIN_REDIRECT_URL = '/'

HOST = '192.168.0.61'#234'#61'#237'
PORT = 16544

FS_HOST = '192.168.0.61'
FS_PORT = 16544
FS_LOGIN = 'lLogin'
FS_PASSWD = 'pPassword'
FS_USER = 'similarity'

SUCCESS = 0
ERROR_FORM = 1

UPLOAD_VK = 0
UPLOAD_COMP = 1
UPLOAD_URL = 0
UPLOAD_CAM = 2

PREVIEW_ROOT = "preview/"
STAR_PHOTO_PATH = "photos.like/"
PHOTOS_FULL_PATH = "photos/full"
TMP_PHOTO_PATH = "tmp/"
STORE_PHOTO_PATH = "store/"


import logging
logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(message)s', filename = LOG_DIR+'like_log.log', filemode = 'a')
