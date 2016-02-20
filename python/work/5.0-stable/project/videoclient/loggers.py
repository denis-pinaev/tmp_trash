# coding:utf-8
import os
import sys
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler

# Свойства для ротация файлов логов
MAX_BYTES = 10240000
BACKUP_COUNT = 5

class LoggingConfig():
    """ Задание правил логирования для блоков системы. """

    FORMAT = '%(asctime)s %(levelname)s %(filename)s %(funcName)s %(message)s'
    DEBUG = False
    
    def __init__(self, PROJECT_ROOT, DEBUG):
        """ Инициализация данных """
        self.DEBUG = DEBUG
        self.__getLogsFileName(PROJECT_ROOT)
        self.__setLogDefaultParams()
        
    def __setLogDefaultParams(self):
        """ Задание дефолтных значений логирования. """
        self.formatter = logging.Formatter(self.FORMAT)
        logging.basicConfig(format = self.FORMAT,
                            level = logging.DEBUG
                            )
        self.getKppLogger()
        #log_communicator.addHandler(logging.StreamHandler(sys.stderr))
    
    def __getLogsFileName(self, PROJECT_ROOT):
        """ Формирование имяни файлов для логов. """
        self.LOGGING_NAME = os.path.join(PROJECT_ROOT, 'log/', 'videoclient.log')
        self.VIDEOCLIENT_LOGPERSON_LOGS = os.path.join(PROJECT_ROOT, 'log/', 'recognitiion_journal.log')
        self.VIDEOARCHIVE_LOGS = os.path.join(PROJECT_ROOT, 'log/', 'videoarchive.log')
        self.COMMUNICATOR_INFO_LOGS = os.path.join(PROJECT_ROOT, 'log/', 'communicator_info.log')
        self.COMMUNICATOR_ERROR_LOGS = os.path.join(PROJECT_ROOT, 'log/', 'communicator_error.log')
        self.BALANCER_INFO_LOGS = os.path.join(PROJECT_ROOT, 'log/', 'balancer_info.log')
        self.BALANCER_ERROR_LOGS = os.path.join(PROJECT_ROOT, 'log/', 'balancer_error.log')
        self.VIDEOCLIENT_SELF_TEST = os.path.join(PROJECT_ROOT, 'log/', 'self_test.log')

        LOG_FILES_LIST = [self.LOGGING_NAME, 
                  self.VIDEOARCHIVE_LOGS,
                  self.VIDEOCLIENT_SELF_TEST, 
                  self.VIDEOCLIENT_LOGPERSON_LOGS,
                  self.BALANCER_INFO_LOGS, 
                  self.BALANCER_ERROR_LOGS, 
                  self.COMMUNICATOR_INFO_LOGS, 
                  self.COMMUNICATOR_ERROR_LOGS
                  ]
        self.__createLogsFile(LOG_FILES_LIST)

    def __createLogsFile(self, LOG_FILES_LIST):
        """ Проверка наличия лог файлов
        и их создание в случае отсутствия
        """
        for log_file in LOG_FILES_LIST:
            dir_logging_name = os.path.dirname(log_file)
            if not os.path.isdir(dir_logging_name):
                os.mkdir(dir_logging_name)
        
    def getKppLogger(self):
        """ Логирование для основного блока """
        log_kpp = logging.getLogger()
        if not hasattr(log_kpp, 'vFHandle'):
            handler = RotatingFileHandler(self.LOGGING_NAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
            handler.setFormatter(self.formatter)
            if self.DEBUG:
                log_kpp.setLevel(logging.INFO)
                handler.setLevel(logging.INFO)
            else:
                log_kpp.propagate = False
                log_kpp.setLevel(logging.ERROR)
                handler.setLevel(logging.ERROR)                
            log_kpp.addHandler(handler)
            #logger_kpp.vFHandle = handler
        return log_kpp

    def getCommunicatorLogger(self):
        """ Логирование для блока коммуникатор """
        log_communicator_error = logging.getLogger('log_communicator')
        if not hasattr(log_communicator_error, 'vFHandle'):
            log_communicator_error.setLevel(logging.ERROR)    
            handler = RotatingFileHandler(self.COMMUNICATOR_ERROR_LOGS, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
            handler.setLevel(logging.ERROR)
            handler.setFormatter(self.formatter)
            log_communicator_error.addHandler(handler)
            log_communicator_error.vFHandle = handler
            if not self.DEBUG:
                log_communicator_error.propagate = False

        log_communicator = logging.getLogger('log_communicator.info')
        if not hasattr(log_communicator, 'vFHandle'):
            log_communicator.setLevel(logging.INFO)
            handler = RotatingFileHandler(self.COMMUNICATOR_INFO_LOGS, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
            handler.setLevel(logging.INFO)
            handler.setFormatter(self.formatter)
            log_communicator.addHandler(handler)
            log_communicator.vFHandle = handler
        
        return log_communicator

    def getBalancerLogger(self):
        """ Логирование для блока коммуникатор """
        log_balancer_error = logging.getLogger('log_balancer')
        if not hasattr(log_balancer_error, 'vFHandle'):
            log_balancer_error.setLevel(logging.ERROR)    
            handler = RotatingFileHandler(self.BALANCER_ERROR_LOGS, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
            handler.setLevel(logging.ERROR)
            handler.setFormatter(self.formatter)
            log_balancer_error.addHandler(handler)
            log_balancer_error.vFHandle = handler
            if not self.DEBUG:
                log_balancer_error.propagate = False

        log_balancer = logging.getLogger('log_balancer.info')
        if not hasattr(log_balancer, 'vFHandle'):
            log_balancer.setLevel(logging.INFO)
            handler = RotatingFileHandler(self.BALANCER_INFO_LOGS, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
            handler.setLevel(logging.INFO)
            handler.setFormatter(self.formatter)
            log_balancer.addHandler(handler)
            log_balancer.vFHandle = handler
            
        return log_balancer

    def getArchiveLogger(self):
        """ Логирование для блока видеоархив """
        log_videoarchive = logging.getLogger('kpp.log_videoarchive')        
        if not hasattr(log_videoarchive, 'vFHandle'):
            handler = RotatingFileHandler(self.VIDEOARCHIVE_LOGS, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
            handler.setFormatter(self.formatter)
            if self.DEBUG:
                log_videoarchive.setLevel(logging.INFO)
                handler.setLevel(logging.INFO)
            else:
                log_videoarchive.propagate = False
                log_videoarchive.setLevel(logging.ERROR)
                handler.setLevel(logging.ERROR)
            log_videoarchive.addHandler(handler)
            log_videoarchive.vFHandle = handler
        
        return log_videoarchive

    def getPersonJournalLogger(self):
        """ Логирование занесения данных в журнал идентификаций """
        log_person_journal = logging.getLogger('kpp.log_person')
        if not hasattr(log_person_journal, 'vFHandle'):
            handler = RotatingFileHandler(self.VIDEOCLIENT_LOGPERSON_LOGS, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
            handler.setFormatter(self.formatter)
            if self.DEBUG:
                log_person_journal.setLevel(logging.INFO)
                handler.setLevel(logging.INFO)
            else:
                log_person_journal.setLevel(logging.ERROR)
                handler.setLevel(logging.ERROR)
            log_person_journal.addHandler(handler)
            log_person_journal.vFHandle = handler
            log_person_journal.propagate = False
            
        return log_person_journal 

    def getSelfTestLogger(self):
        """ Логирование самотетирования """
        log_self_test = logging.getLogger('kpp.slog_self_test')
        if not hasattr(log_self_test, 'vFHandle'):
            handler = RotatingFileHandler(self.VIDEOCLIENT_SELF_TEST, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
            handler.setFormatter(self.formatter)
            if self.DEBUG:
                log_self_test.setLevel(logging.INFO)
                handler.setLevel(logging.INFO)
            else:
                log_self_test.setLevel(logging.ERROR)
                handler.setLevel(logging.ERROR)
            log_self_test.addHandler(handler)
            log_self_test.vFHandle = handler
            log_self_test.propagate = False                
            
        return log_self_test
