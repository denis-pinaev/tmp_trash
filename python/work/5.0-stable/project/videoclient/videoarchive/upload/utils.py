#coding=utf-8

import sys
from videoclient.settings import log_videoarchive as logging
import models
import archive

def getVideoArchives(va = None):
    try:
        videoarchives = []
        if va:
            va = [va]
        else:
            va = models.VideoArchives.objects.filter(active = True)
            
        va_servers = ''
        va_ports = ''
        
        for v in va:
            videoarchives.append({'host': v.ip, 'port': v.port})
            va_servers = va_servers + str(v.ip)+'*'
            va_ports = va_ports + str(v.port)+'*'
    
        if len(va_servers)>0:
            va_servers = va_servers[0:len(va_servers)-1]
        if len(va_ports)>0:
            va_ports = va_ports[0:len(va_ports)-1]
        return va_servers, va_ports, videoarchives
    except:
        logging.exception("getVideoArchives: "+str(sys.exc_info()))
        
    return None, None, None

