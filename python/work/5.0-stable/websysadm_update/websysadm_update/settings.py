# Django settings for websysadm_update project.
# coding=utf-8
import logging
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': '', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

PROJECT_ROOT = os.path.join( os.path.dirname(__file__), '../')
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT+'/www/files/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bl4vu!^hjtqd$nehbail^%!v2d83ojziham817v+j-7e&y5mdr'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'websysadm_update.urls'

TEMPLATE_DIRS = (
    PROJECT_ROOT+'/websysadm_update/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
)


# Папка для складывания туда обновлений
dir_updates = "/home/smirnova.u.a/workspace/wspse1/websysadm_update/server_dir/" 

# Лог обновлений
log_updates_file = ""

command_after_load = "ps -ayx | grep %s"

# Список серверов
#server_list = [{"name": "Имя сервера", "check_dir": "Проверяемая дирриктория"}]
server_list = [{"name": "Сервер1", "check_dir": "/home/smirnova.u.a/workspace/wspse1/websysadm_update/server_dir/dir1/"},
               {"name": "Сервер2", "check_dir": "/home/smirnova.u.a/workspace/wspse1/websysadm_update/server_dir/dir2/"},
               {"name": "Сервер3", "check_dir": "/home/smirnova.u.a/workspace/wspse1/websysadm_update/server_dir/dir3/"},
               {"name": "Сервер4", "check_dir": "/home/smirnova.u.a/workspace/wspse1/websysadm_update/server_dir/dir4/"},
              ]

result_val = {1: "Обновление произойдет после перезагрузки", 0: "Нет обновлений", -1: "Ошибка проверки папки"}

script_export_info = "/home/smirnova.u.a/workspace/wspe3/websysadm/brunches/oxion-passive/info/export_info.py"
REBOOT_SYSTEM = ""

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(message)s', filename = os.path.dirname(__file__)+'log.log', filemode = 'a')
