#coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import sys
import os
import httplib
from urllib import urlencode
import time
import datetime

LOGIN = 'admin'
PASSWORD = 'eghfdkz.ofz cbcntvf'

def init_connection(host, port):
    try:
        return httplib.HTTPConnection(host, port)
    except Exception as http_exception:
        print 'error init_connection'

def get_login_token(connection, login, password):
    # Формируем url для входа
    url = '/'
    parameters = urlencode({
                            'login': login,
                            'password': password,
                            })    
    # Отправляем запрос
    connection.request('POST', url, parameters)
    response = connection.getresponse()
    
    if response.status == 200:
        print 'Login fault. Password rejected'
    
    if response.status <> 302:
        print 'Login fault. Unsupported request.status'
    
    # Вычитываем переданные данные, чтобы освободить сокет
    response.read()
    
    # Получаем и обрабатываем cookies
    if 'set-cookie' not in response.msg:
        print 'Login fault. No set-cookie in response header'
        
    set_cookie = response.msg['set-cookie']
    
    cookies_list = [cookie.lstrip().rstrip().split('=') for cookie in set_cookie.split(';')]
    
    cookies = {}
    for cookie in cookies_list:
        cookies[cookie[0]] = cookie[1]
    
    # Получаем id сессии
    if 'sessionid' not in cookies:
        print 'Login fault. No sessionid in cookies'
    
    # Формируем токен
    sessionid = '%s=%s' % ('sessionid', cookies['sessionid'])
    return sessionid
    
    
def http_send(connection, url, parameters, auth_token):
    try:
        # Формируем header с id сессии
        headers = {
                   'Cookie': auth_token,
                   }
        # Формируем строку параметров
        params_url = urlencode(parameters)
        
        # Для GET запроса все параметры передаются в url
        if len(params_url) > 0:
            full_url = '%s?%s' % (url, params_url)
        else:
            full_url = url
        
        # Отправляем запрос
        connection.request('GET', full_url, '', headers)
        
    except Exception as http_exception:
        print 'error http_send'


def http_recv(connection):
    try:
        # Получаем статус и данные
        response = connection.getresponse()
        response_data = response.read()
         
        # Возвращаем кортеж
        return response.status, response_data 
    
    except Exception as http_exception:
        print 'http_recv'
    

class Command(BaseCommand):
    help = 'Измерение времени отлика системы.'
    requires_model_validation = True

    def handle(self, *args, **options):
        if len(args) < 1:
            print 'Необходимо указать файл для записи результатов'
            return
        try:
            f = open(args[0], 'a')
        except:
            print 'Неверно указан файл'
            return
        page = 'ident/'
        if len(args) > 1:
            page = args[1]
        request_url = 'http://127.0.0.1/' + page 
        conn = init_connection('127.0.0.1', 80)
        auth_token = get_login_token(conn, LOGIN, PASSWORD)
        t1 = time.time()
        http_send(conn, request_url, '', auth_token)
        status, json = http_recv(conn)
        t2 = time.time()
        f.write(str(datetime.datetime.now()) + ' ' + str(t2 - t1) + '\n')
        f.close
        print str(datetime.datetime.now()) + ' ' + str(t2 - t1)
