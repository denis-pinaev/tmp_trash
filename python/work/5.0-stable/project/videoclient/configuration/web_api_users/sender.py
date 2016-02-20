# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

import logging
import urllib
import urllib2
import httplib
import json
import sys
import os
from urllib2 import URLError, HTTPError
import hashlib, time, datetime

SUCCESS = 0
ERROR_FORM = 1

class Sender():
    host = ''
    port = 0
    url = ''

    
    def __init__(self, host, port, url):
        self.host = host
        self.port = port
        self.url = url


    def __postData(self, kwargs):#POST  - запрос
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        try:
            params = urllib.urlencode(kwargs)    
            if self.port: 
                conn = httplib.HTTPConnection(str(self.host) + ':' + str(self.port))
            else:
                conn = httplib.HTTPConnection(str(self.host))
            conn.request("POST", self.url, params, headers)
            response = conn.getresponse()
            body = response.read()
        except:
            logging.error("sender.__postData " + str(sys.exc_info())) 
            return ('', ERROR_FORM, '')
        finally:
            conn.close()
            del conn
            print 
        return (body, response.status, response.reason)  
    
      
    def sendData(self, kwargs):
        resp, status, reason = self.__postData(kwargs)
        return (status, reason, resp)