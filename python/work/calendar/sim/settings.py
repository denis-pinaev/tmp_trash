import os
import logging

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

PROJECT_ROOT = os.path.join( os.path.dirname(__file__), '../')

DATABASE_ENGINE = 'sqlite3'      # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = PROJECT_ROOT+'web_api.db'   # Or path to database file if using sqlite3.
DATABASE_USER = ''   # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = '' # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'en-en'

USE_I18N = True

WWW_ROOT = PROJECT_ROOT + 'www/'

HTTP_HOST = 'http://calendar.test.gale.ru/'
MEDIA_ROOT = '/srv/'

STORE_IMG = 'project_data/calendar.gale.ru/'
TMP_IMG = 'project_tmp/calendar.gale.ru/'

MEDIA_URL = '/files/media/'

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
    PROJECT_ROOT+'sim/fb/templates/',
#    "/usr/local/lib64/python2.6/site-packages/django/contrib/admin/templates/"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'sim',
    'sim.fb',
    'sim.smilart',
    'sim.statistic'
)

DEFAULT_FROM_EMAIL = 'hjtgdrfyt@gmail.com'
ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hjtgdrfyt@gmail.com'
EMAIL_HOST_PASSWORD = 'django registration'
EMAIL_USE_TLS = True

BILLING_URL = 'http://billing.test.gale.ru/'
#BILLING_URL = 'http://192.168.0.55:8890/'
PRICE_COUNT = {1:1, 10:1, 20:2, 30:3}
PROJECT_NAME = 'calendartest'

FS_HOST = '192.168.0.55'
FS_PORT = 16544
FS_LOGIN = 'lLogin'
FS_PASSWD = 'pPassword'
FS_USER = 'calendar'

face_size = 120, 160
DeletePassword = "gaga_smilart"

LOGIN_REDIRECT_URL = '/'

redirect_url = "http://cdn9.appsmail.ru/hosting/585573/lady1911040211/index.html"

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(message)s', filename = MEDIA_ROOT+TMP_IMG+'/calendar_log.log', filemode = 'a')

