# coding:utf-8
import os
import logging
# Django settings for VideoClient project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

LOGIN_URL = '/'

VERSION_PREFIX = 5
BRANCH = 0
REVISION = 1

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

PROJECT_ROOT = os.path.join( os.path.dirname(__file__), '../../')
SRC_ROOT = PROJECT_ROOT + 'project/videoclient/'
VERSION_FILE = os.path.join(PROJECT_ROOT, SRC_ROOT, 'version.txt')
WWW_ROOT = PROJECT_ROOT + 'www/'

VIDEO_CLIP_FOLDER = 'records/'

""" Задание правил логирования """
import loggers
all_loggers = loggers.LoggingConfig(PROJECT_ROOT, DEBUG)
log_communicator = all_loggers.getCommunicatorLogger()
log_balancer = all_loggers.getBalancerLogger()
log_videoarchive = all_loggers.getArchiveLogger()
log_person_journal = all_loggers.getPersonJournalLogger()
log_self_test = all_loggers.getSelfTestLogger()

if PROJECT_ROOT.startswith('/'):
    PATH_SMILART = "/opt/smilart/"
else:
    PATH_SMILART = "c:/smilart/"
#logging.info('PATH_SMILART %s' %PATH_SMILART) 


TEMPORARY_FOLDER = PATH_SMILART + 'data/sa/temporary_folder/'
PERMANENT_FILES = PATH_SMILART + 'data/sa/permanent_files/'
   
VIDEO_CLIP_PATH = PATH_SMILART+'data/communicator/savevideo/'#TEMPORARY_FOLDER + VIDEO_CLIP_FOLDER

LEARNING_IMAGES = PERMANENT_FILES+'learning_images/'#PERMANENT_FILES + 'learning_images/'
LOGDETECT_IMAGES = PERMANENT_FILES +'logdetect_images/'

MAP_IMAGES = PERMANENT_FILES +'map_images/'

EVENTS_EXPORT_JOURNAL_PATH = TEMPORARY_FOLDER+'events_journal_export/'#Don't forget to set chmod i.e. 777

EVENTS_ON_PAGE = 400 #lines on page
EVENTS_EXPORT_FILENAME = 'events_journal.zip'
VERSION_COMPONENTS_FILENAME = 'versions.zip'

#режим отображения графиков: можно показать обе версии сразу
MONITORING_SYSTEM_GRAPH_JS = True
MONITORING_SYSTEM_GRAPH_FLASH = False

MAX_JS_VIDEO_SCREEN = 670

# Настройки поумолчанию для тестирования скорости идентификации
FACES_PATH = os.path.join( os.path.dirname(__file__), 'self_test/faces/')
FACES_3_PATH = os.path.join(FACES_PATH, '3/')
FACES_5_PATH = os.path.join(FACES_PATH, '5/')
FACES_RESAULT = os.path.join(FACES_PATH, 'resault.json')

# Настройки поумолчанию для самотестирования
# Запуск самотестирования при старте системы, параметр self_test в настройках по умолчанию
# SELF_TEST_DEFAULT_FD_PHOTOS = os.path.join( os.path.dirname(__file__), '/self-test/FD_photos/') # Путь к набору фотографий для тестирования FaceDetect
# SELF_TEST_DEFAULT_EXT = ['.jpg', '.png'] # разрешения на картинки поумолчанию
# SELF_TEST_DEFAULT_INFO_TEMPERATURE = 90 # Порог предупреждения о возможной перегрузке тумпературы
# SELF_TEST_DEFAULT_WARNING_TEMPERATURE = 97 # Порог перегрузки температуры
# SELF_TEST_DEFAULT_DELAY_CRON_FOR_TEMPERATURE_TESTING = 1800 # Периодичнось выполнение тестирования температуры, доступности управляющей системы и доступности демонов.
# SELF_TEST_DAYS_LIMIT_FOR_LICENSE = 30 # Количество дней, если осталось меньше до завершения то будут писаться сообщения в журнал событий с информационными окнами. 

S_COMMAND = 'sudo '#'sudo ' # 'sudo '
SCRIPTS_ROOT =  PATH_SMILART+'scripts/'
S_BACKUP = 'restart.sh'
S_RESTORE = 'restart.sh'
S_RESTART = 'restart.sh'
S_REBOOT = 'restart.sh'
S_COMPLITE = 'complite'

S_RESTART_CS = 'cb.sh'
RESTART_CS_CMD = S_COMMAND+SCRIPTS_ROOT+S_RESTART_CS


HTTP_HOST = '/'

MEDIA_ROOT = WWW_ROOT +'files/'

MEDIA_URL = HTTP_HOST+'files/'

EXPORT_PATH = TEMPORARY_FOLDER
USE_ZIP_FILE = True # if USE_ZIP_FILE then *.zip file else *.tar.bz2

ICON_EYES = MEDIA_ROOT+ 'images/icon-eyes.png'
ICON_REC = MEDIA_ROOT+ 'images/icon-rec.png'

#MACHINE_IP_ADDRESS = '192.168.0.55'#for logperson

MEDIA_ADMIN = WWW_ROOT+'admin/media/'
MEDIA_ADMIN_TOOLS = WWW_ROOT+'admin_tools/'

TEST_JAR = SRC_ROOT+'scripts/test.jar' 
TEST_CONFIG = SRC_ROOT+'scripts/test.properties'

TEST_OUTPUT_BASE = 'files/test/result.log'
TEST_OUTPUT = WWW_ROOT+TEST_OUTPUT_BASE
TEST_OUTPUT_URL = HTTP_HOST+TEST_OUTPUT_BASE 
TEST_TMP_FILE = os.path.dirname(__file__)+'test_tmp.log'

MODULE_TASK_LIST = 'tasks'

USE_ARCHIVE = True

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2', #'sqlite3', #'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sa', #SRC_ROOT+'sqlite3.db',#'vc_test_gale_ru',                      # Or path to database file if using sqlite3.
        'USER': 'sa',                       # Not used with sqlite3.
        'PASSWORD': 'sa',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.    
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'autocommit': True,
        },
    },
    'systemlog':{
        'ENGINE': 'postgresql_psycopg2', #'sqlite3', #'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'syslog', #SRC_ROOT+'sqlite3.db',#'vc_test_gale_ru',                      # Or path to database file if using sqlite3.
        'USER': 'syslog',                       # Not used with sqlite3.
        'PASSWORD': 'syslog',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.    
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# MySql - options
#DATABASE_OPTIONS = {
#   "init_command": "SET storage_engine=INNODB",
#}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'Asia/Dubai' # Установлено для того что бы избезать ошибки с переходом на летнее/зимнее вермя.
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

division_visitor = 2
division_person = 3
division_employee = 4
division_auto = 5
status_enter = 1
status_exit = 2
status_notdefined = 3
camera_enter = 0
camera_exit = 1
camera_all = 2
action_delete = 3

self_learning = -1
noise_learning = -2

is_active_self_learning = False
SELF_LEARNING = self_learning

reaction_time = "reaction_time"
last_journal_update = "last_journal_update"
wait_unidentified_person = "wait_unidentified_person"
journalBoundCoeff = "journalBoundCoeff"
count_time_test = "count_time_test"
time_span_time_test = "time_span_time_test"
add_not_ident_person = "add_not_ident_person"
transfer_alerts = "transfer_alerts"
transfer_alerts_url = "transfer_alerts_url"
show_ident_window = "show_ident_window"
show_ident_window_recogn_only = "show_ident_window_recogn_only"
permit_control_system_params = "permit_control_system_params"
self_test = "self_test"
local_host_name = "local_host_name"
delay_for_create_new_group = "delay_for_create_new_group"

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
"django.core.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.request",
"videoclient.context_processors.global_vars"
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "videoarchive/archive_settings/templates")
)

ADMIN_TOOLS_INDEX_DASHBOARD = 'videoclient.dashboard.CustomIndexDashboard'
#ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'admin_tools.dashboard.DefaultAppIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'videoclient.appdashboard.DefaultAppIndexDashboard'
ADMIN_TOOLS_MENU = 'videoclient.menu.CustomMenu'


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
 #   'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'middleware.StreamSmilartMiddleware',
    'sessions.middleware.SessionIdleTimeout',
)

ROOT_URLCONF = 'videoclient.urls'

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
    #'videoclient.localeurl',
    'videoclient',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'videoclient.po1',
    'videoclient.po2',
    'videoclient.po3',
    'videoclient.po4',
    'videoclient.wizard',
    'videoclient.control_settings',
    'videoclient.distortion',
    'videoclient.profile',
    'pagination',
    'videoclient.monitoring',
    'videoclient.monitoring.systemlog',
    'videoclient.maps',
    'videoclient.person_training',
    'videoclient.videoanalytics',
    'videoclient.imp_exp',
    'videoclient.updates',
    'sessions',
    'self_test',
    'videoclient.configuration',
    'videoclient.configuration.integration',
    'videoclient.configuration.web_api_users',
    'videoclient.configuration.turnstiles',
    'videoclient.configuration.setup',
    'videoclient.configuration.kpp',
    'videoclient.rosetta',
    'videoclient.api.cameras',
    'videoclient.api.communicators',
    'videoclient.api.log',
    'videoclient.api.lists',
    'videoclient.api.persons',
    'videoclient.api.persons.photos',
    'videoclient.status_thread',
    'videoclient.communicator',
    'videoclient.security',
    'videoclient.user_perms',
    'videoclient.smilart_cron',
)

if USE_ARCHIVE:
    ARCHIVE_URL = 'archive'
    INSTALLED_APPS += (
            'videoclient.videoarchive',
            'videoclient.videoarchive.archive',
            #'videoclient.videoarchive.django_cron',
            'videoclient.videoarchive.va',
            #'videoclient.videoarchive.person',
            'videoclient.videoarchive.balancer',
            #'videoclient.videoarchive.communicator',
            'videoclient.videoarchive.upload',
            'videoclient.videoarchive.archive_settings',
            #'videoclient.videoarchive.updates',    
        )


LOCALE_PATHS = (
    '/locale/<language>/LC_MESSAGES/django.(po|mo)',
    PROJECT_ROOT + '/project/videoclient/locale/ru/LC_MESSAGES/django.mo',
    PROJECT_ROOT + '/project/videoclient/locale/',
    PROJECT_ROOT + '/project/videoclient/',
    PROJECT_ROOT + '/project/videoclient/locale/ru/LC_MESSAGES/django.mo',
    PROJECT_ROOT + '/project/videoclient/locale/ru/LC_MESSAGES/django.mo',
)

CRON_POLLING_FREQUENCY = 1
FILE_SERVER_ADDR = 'files.smilart.com'
moderator = "Модератор"
script_export_info = "/home/smirnova.u.a/workspace/wspse1/websysadm/brunches/oxion-passive/info/export_info.py"

CONFIG_IDENT_SWF = WWW_ROOT+"/files/swf/ident/xml/config.xml"

JOURNAL_FOUND = "/found/"
JOURNAL_ORIGINAL = '/original/'


TMP_DISTORSION_DIR = "/tmpdist/"

#videoarchive
CRON_DELAY_FOR_PROCESS = "cron_delay_for_process"


#DEFAULT PARAMS
DEFAULT_BALANCER_HOST = ''
DEFAULT_BALANCER_PORT = 16544
DEFAULT_BALANCER_USER = "oxion"
DEFAULT_BALANCER_PASSWORD = "oxion"
DEFAULT_BALANCER_LOGIN = "oxion"
#DEFAULT_COMMUNICATOR_HOST = '127.0.0.1'
DEFAULT_COMMUNICATOR_PORT = 12600
DEFAULT_COMMUNICATOR_MJPEG_PORT = 13600
DEFAULT_VIDEOARCHIVE_PORT = 12700                                                                                                                                                                                                                      
DEFAULT_VIDEOARCHIVE_SAVE_DIR = "/srv/www/vhosts/sa/www/files/archive/files/video/"   
DEFAULT_COMMUNICATOR_VIDEO_CODEC = 2 # 1-flv,2-mjpeg,3-mpeg
DEFAULT_CONTROL_CLIENTS_COUNT = 1
DEFAULT_CONTROL_CLIENT_0_TYPE = "communicator"
DEFAULT_CONTROL_CLIENT_0_PORT = DEFAULT_COMMUNICATOR_PORT
DEFAULT_CONTROL_CLIENT_0_USER = "oxion"

PAGINATION_DEFAULT_PAGINATION = 15
PAGINATION_DEFAULT_WINDOW = 3
PAGINATION_DEFAULT_ORPHANS = 0
INVALID_PAGE_RAISES_404 = True

SAVE_CAMERA_BALANCER_TIMEOUT = 1100.0

FORCE_SCRIPT_NAME = '' # Настройка для запустка оксиона на nginx

# Получение свободного места на диске
space = "df -h /opt"
raid_status = "echo"
# Раскомментировать если используется Рэйд
#raid_status = "dmraid -s | grep status"

#LANGUAGE_CODE = 'ru'

gettext = lambda s: s

LANGUAGES = (
      ('ru', gettext('Русский')),
      ('en', gettext('Английский')),
)