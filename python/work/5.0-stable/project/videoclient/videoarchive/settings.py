# coding=utf-8
import os
import glob
import re

# Django settings for VideoClient project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SVN_REVISION = '$Revision: 4167 $' 
VERSION_PREFIX = 3
BRANCH = 3
REVISION = 1

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

LOGGING_PATH = os.path.join( os.path.dirname(__file__), '../../../')+'log/'

PROJECT_ROOT = os.path.join( os.path.dirname(__file__), '../../../')
SRC_ROOT = PROJECT_ROOT + 'project/videoarchive/'
WWW_ROOT = PROJECT_ROOT + 'www/'

MEDIA_ROOT = WWW_ROOT +'files/'
MEDIA_URL = '/files/'


ARCHIVE_URL = 'archive' #
if ARCHIVE_URL:
    from videoclient import settings as vcSettings
    VERSION_PREFIX = vcSettings.VERSION_PREFIX
    BRANCH = vcSettings.BRANCH
    REVISION = vcSettings.REVISION

#HTTP_HOST = "http://archive.test.gale.ru"
HTTP_HOST = ""

DATABASES = {
    'default': {
        'ENGINE': 'mysql',#'sqlite3', #'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sa',#SRC_ROOT+'sqlite3.db',#'vc_test_gale_ru',                      # Or path to database file if using sqlite3.
        'USER': 'sa',                      # Not used with sqlite3.
        'PASSWORD': 'sa',                  # Not used with sqlite3.
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
LANGUAGE_CODE = 'ru'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


#DEFAULT VIDEOARCHIVE PARAMS

RES_INTERFACE = "res_interface"
TYPE_IMPORT = "IMPORT"
from videoclient.settings import CRON_DELAY_FOR_PROCESS as videoclient_CRON_DELAY_FOR_PROCESS
CRON_DELAY_FOR_PROCESS = videoclient_CRON_DELAY_FOR_PROCESS

DEFAULT_VIDEOARCHIVE_VIDEO_CODEC = 0 # 0-h264, 1-flv, 2-mjpeg, 3-mpeg4
DEFAULT_VIDEOARCHIVE_GOP_SIZE = 5

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x4x3yk2r*$zv37te43s2x1&+8+s-dv=n51d-n&c4d*r(z0x=j)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    "django.core.context_processors.i18n",
)

ADMIN_TOOLS_INDEX_DASHBOARD = 'videoarchive.dashboard.CustomIndexDashboard'
#ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'admin_tools.dashboard.DefaultAppIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'videoachive.appdashboard.DefaultAppIndexDashboard'
ADMIN_TOOLS_MENU = 'videoarchive.menu.CustomMenu'


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', 
 #   'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',   
)

ROOT_URLCONF = 'videoarchive.urls'

TEMPLATE_DIRS = (
    #os.path.join( os.path.dirname(__file__), 'templates'),                 
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

ADMIN_TOOLS_INDEX_DASHBOARD = 'videoarchive.dashboard.CustomIndexDashboard'
#ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'admin_tools.dashboard.DefaultAppIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'videoarchive.appdashboard.DefaultAppIndexDashboard'
ADMIN_TOOLS_MENU = 'videoarchive.menu.CustomMenu'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'videoarchive',
    'archive',
    'django_cron',
    'videoarchive.va',
    'videoarchive.person',
    'videoarchive.balancer',
    'videoarchive.communicator',
    'videoarchive.upload',
    'videoarchive.updates',
    'videoarchive.archive_settings',    
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
)

LOCALE_PATHS = (
    '/locale/<language>/LC_M    ESSAGES/django.(po|mo)',
#    PROJECT_ROOT + '/project/videoclient/locale/ru/LC_MESSAGES/django.mo',
#    PROJECT_ROOT + '/project/videoclient/locale/',
#    PROJECT_ROOT + '/project/videoclient/',
 #   PROJECT_ROOT + '/project/videoclient/locale/ru/LC_MESSAGES/django.mo',
 #   PROJECT_ROOT + '/project/videoclient/locale/ru/LC_MESSAGES/django.mo',
)


space = "df -h /opt"
raid_status = "echo"
USE_ZIP_FILE = True # (True - use zip, False - use tar)

OXION_URL = "/"
