# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

import socket
import sys
import datetime
from struct import pack, unpack
from videoclient import settings
from cStringIO import StringIO
from xml.dom.minidom import parseString
from django.utils.translation import ugettext as _
from videoclient.settings import log_videoarchive as logging

DEFAULT_ID_COMMAND = 'SDKArchive'
XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>'
MAX_READ_DATA = 10
TIME_OUT = 5.0

class Archive():
    
    host = ''
    port = 0
    time_out = TIME_OUT
    max_read_data = MAX_READ_DATA
        
    sock = socket.SocketType
    connect = False
    
    def __init__(self, host, port, time_out = TIME_OUT, max_read_data= MAX_READ_DATA):
        try:
            self.host = host
            self.port = port
            self.time_out = time_out
            self.max_read_data = max_read_data
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __init__: "+str(sys.exc_info()))
    
    def __del__(self):
        self.__disconnect()
        
    def __connect(self):
        try:
            if not self.connect:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                self.connect = True
        except:
            from videoclient import monitoring
            from monitoring.utils import saveMonitoringMessage
            params = {'host':self.host, 'port':self.port}
            #monitoring.warning(type='accident_components', description=_("Ошибка подключения к демону видеоархива, демон %(host)s:%(port)s") % params, show=True )
            saveMonitoringMessage(id = 'videoarchive_error', params = params, type='accident_components', description=_("Ошибка подключения к демону видеоархива, демон %(host)s:%(port)s") % params, show=True )
            logging.exception(DEFAULT_ID_COMMAND+" __connect: "+str(sys.exc_info()))
            
    def __disconnect(self):
        try:
            self.sock.close()
            self.connect = False    
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __disconnect: "+str(sys.exc_info()))


    def close(self):
        self.__disconnect()
        
    def open(self):
        self.__connect()
        
    def __readBytes(self, bytes):
        try:
            if bytes == 0:
                return ''
            buffer = StringIO()
            df = bytes
            self.sock.settimeout(self.time_out)
            while df > 0:
                if (df > 1024):
                    s = self.sock.recv(1024)
                else :
                    s = self.sock.recv(df)
                if len(s) == 0:
                    return ''
                df = df - len(s)
                buffer.write(s)
                
            res=buffer.getvalue()
            buffer.close()
            return res
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __readBytes: "+str(sys.exc_info()))
            return ''
    
    def __sendSize(self, size):
        try:
            spack = pack('<I', size)
            self.sock.send(spack)    
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __sendSize: "+str(sys.exc_info()))
          
    def __sendData(self, data):
        try:
            logging.info("__sendData: "+str(data)+"   size: "+str(len(data)))
            spack = pack('<I', len(data)) + pack('<%ss' %len(data), str(data))
            self.sock.send(spack)
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __sendData: "+str(sys.exc_info()))
            
    def __sendXml(self, data):
        try:
            data = data.encode("utf-8")
            data = bytearray(data)
            self.__sendData(data)
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __sendXML: "+str(sys.exc_info()))            
        
    def __readSize(self):
        try:
            self.sock.settimeout(self.time_out)
            b4 = self.sock.recv(4)
            size = unpack('<I', b4)[0]
            logging.info("__readSize: "+str(size))
            return size
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __readSize: "+str(sys.exc_info()))
        return 0
    
    def __readData(self):
        try:
            size = self.__readSize();
            return self.__readBytes(size)
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __readData: "+str(sys.exc_info()))
    
    def __readXml(self):
        try:
            data = self.__readData()
            if not data: return None 
            data = data.strip(" \t\n")
            logging.info("__readXml: "+str(data))
            res = parseString(data)
            return res
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __readXml: "+str(sys.exc_info()))
            return None
    
    def __answerIsTrue(self, xml_node):
        try:
            xml_text = xml_node.toxml()
            return xml_node.getElementsByTagName('exec')[0].firstChild.toxml() == 'ok'
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __answerIsTrue: "+str(sys.exc_info()))
            return None


    def __sendCommandXml(self, method, params=[], params2=[], id_command = DEFAULT_ID_COMMAND, receive = True):
        try:
            self.__connect()
            xml_text = XML_HEADER+'<methodCall><methodName>%s</methodName><params></params><idСommand>%s</idСommand></methodCall>' %(method, id_command)
            xml_node = parseString(xml_text)
            xml_params = xml_node.getElementsByTagName("params")[0]
            if params:
                for param in params:
                    if param['value'] is not None:
                        node_str = '<%s>%s</%s>' % (param['name'], param['value'], param['name'])
                        xml_params.appendChild(parseString(node_str).firstChild)
            if params2:
                for param in params2:
                    if param['value'] is not None:
                        logging.info(str(param))
                        node_str = '<%s>%s</%s>' % (param['name'], param['value'], param['name'])
                        xml_params.appendChild(parseString(node_str).firstChild)
            xml_text = xml_node.toxml()
            self.__sendXml(xml_text)
            if receive:
                xml_node = self.__readXml()
                return xml_node
            else:
                return None
        except:
            logging.exception(DEFAULT_ID_COMMAND+" __sendCommandXml: "+str(sys.exc_info()))
            return None
        
    # params num=None, signal_params=None, interval=None, tm_start=None, tm_stop=None, fps=None, width=None, height=None,        
    def startProcess(self, uuid, signal, signal_id, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            xml_node = self.__sendCommandXml(method='start_process', params=[{'name':'cameraUUID', 'value': uuid}, {'name':'signalType', 'value': signal}, {'name':'idSignal', 'value':signal_id}], params2=params, id_command="startProcess%s" %id_command)
            if not xml_node:
                return 0
            if xml_node.getElementsByTagName('exec')[0].firstChild.toxml() == "ok":
                return int(xml_node.getElementsByTagName('id')[0].firstChild.toxml())
            else:
                try:
                    logging.error(str(xml_node.getElementsByTagName('remark')[0].firstChild.toxml()))
                except:
                    logging.error(sys.exc_info())
                return -1
        except:
            logging.exception(DEFAULT_ID_COMMAND+" startProcess: "+str(sys.exc_info()))
            return -1
        
    def stopProcess(self, uuid, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            xml_node = self.__sendCommandXml(method='stop_process', params=[{'name':'cameraUUID', 'value': uuid}], params2=params, id_command="stopProcess%s" %id_command)
            return self.__answerIsTrue(xml_node)
        except:
            logging.exception(DEFAULT_ID_COMMAND+" stopProcess: "+str(sys.exc_info()))
            return False
        
    def deleteRoller(self, id, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            xml_node = self.__sendCommandXml(method='delete_roller', params=[{'name':'id', 'value': id}], params2=params, id_command="deleteRoller%s" %id_command)
            return self.__answerIsTrue(xml_node)
        except:
            logging.exception(DEFAULT_ID_COMMAND+" deleteRoller: "+str(sys.exc_info()))
            return False
        
    def deleteRollers(self, tmStart, tmStop, idCamera, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            xml_node = self.__sendCommandXml(method='delete_rollers', params=[{'name':'tmStart', 'value': tmStart}, {'name':'tmStop', 'value': tmStop}, {'name':'idCamera', 'value': idCamera}], params2=params, id_command="deleteRollers%s" %id_command)
            return self.__answerIsTrue(xml_node)
        except:
            logging.exception(DEFAULT_ID_COMMAND+" deleteRollers: "+str(sys.exc_info()))
            return False   
        
        
    def processRoller(self, id, mode, diffFramesProc = None, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            p = [{'name':'id', 'value': id}, {'name':'mode', 'value': mode}]
            if diffFramesProc is not None:
                p.append({'name':'diffFramesProc', 'value': diffFramesProc})
            xml_node = self.__sendCommandXml(method='process_roller', params=p, params2=params, id_command="processRoller%s" %id_command)
            return self.__answerIsTrue(xml_node)
        except:
            logging.exception(DEFAULT_ID_COMMAND+" processRoller: "+str(sys.exc_info()))
            return False        
                     
        
    def activeProcesses(self, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            xml_node = self.__sendCommandXml(method='active_processes', params2=params, id_command="activeProcesses%s" %id_command)
            if not xml_node: return False
            processes = xml_node.getElementsByTagName('process')
            res_processes=dict()
            for process in processes:
                res_process = dict()
                id = process.getElementsByTagName("id")[0].firstChild.toxml()
                res_process["state"] = process.getElementsByTagName("state")[0].firstChild.toxml()
                #res_process["value"] = process.getElementsByTagName("value")[0].firstChild.toxml()
                try:
                    if len(process.getElementsByTagName("idTask"))>0:
                        res_process["idTask"] = process.getElementsByTagName("idTask")[0].firstChild.toxml()
                except: pass
                res_processes[id] = res_process
            return res_processes
        except:
            logging.exception(DEFAULT_ID_COMMAND+" activeProcesses: "+str(sys.exc_info()))
            return False
        
    def flv(self, id, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            xml_node = self.__sendCommandXml(method='flv', params=[{'name':'id', 'value': id}], params2=params, id_command="flv%s" %id_command)
            import time
            time.sleep(0.5)
            return self.__answerIsTrue(xml_node)
        except:
            logging.exception(DEFAULT_ID_COMMAND+" flv: "+str(sys.exc_info()))
            return False
        
    def getParam(self, node, name):
        try:
            return node.getElementsByTagName(name)[0].firstChild.toxml()
        except:
            logging.exception("getParam %s: %s" %(name, str(sys.exc_info())))
        return None
    
    def getInfo(self, path, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            xml_node = self.__sendCommandXml(method='info', params=[{'name': 'path', 'value': path}], params2=params, id_command="info%s" %id_command)
            is_ok = self.getParam(xml_node, 'exec')
            if is_ok and is_ok != 'ok':
                return None
            data = dict()
            data["width"]   = self.getParam(xml_node, 'width')
            data["height"]  = self.getParam(xml_node, 'height')
            data["ext"]     = self.getParam(xml_node, 'ext')
            data["codec"]   = self.getParam(xml_node, 'codec')
            data["fps"]     = self.getParam(xml_node, 'fps')
            data["dur"]     = self.getParam(xml_node, 'dur')
    
            return data            
        except:
            logging.exception(DEFAULT_ID_COMMAND+" getInfo: "+str(sys.exc_info()))
            return None

    def dataUpdater(self, xml_node, str):
        data = dict()
        data[str] = self.getParam(xml_node, str)
        return data

    def getSettings(self, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            xml_node = self.__sendCommandXml(method='getSettings', params=[], params2=params, id_command="getSettings%s" %id_command)
            if not xml_node: return None
            is_ok = self.getParam(xml_node, 'exec')
            if is_ok and is_ok != 'ok':
                return None
            data = dict()
            
            data.update(self.dataUpdater(xml_node, 'delOlderDays'))
            data.update(self.dataUpdater(xml_node, 'delIntervalHours'))
            data.update(self.dataUpdater(xml_node, 'thresholdFreeSpaceNotif'))
            data.update(self.dataUpdater(xml_node, 'thresholdFreeSpaceDel'))
            
            data.update(self.dataUpdater(xml_node, 'bitrate'))
            data.update(self.dataUpdater(xml_node, 'blur'))
            data.update(self.dataUpdater(xml_node, 'compress'))
            data.update(self.dataUpdater(xml_node, 'gopSize'))
            data.update(self.dataUpdater(xml_node, 'identThreshold'))
            
            data.update(self.dataUpdater(xml_node, 'socketTimeout'))
            data.update(self.dataUpdater(xml_node, 'adminDomen'))
            data.update(self.dataUpdater(xml_node, 'adminAlertUrl'))
    
            return data            
        except:
            logging.exception(DEFAULT_ID_COMMAND+" getSettings: "+str(sys.exc_info()))
            return None
        
    def getVersion(self, params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            xml_node = self.__sendCommandXml(method='version', params=[], params2=params, id_command="getVersion%s" %id_command)
            # В API не предусмотренно возвращать состояние ответа
            #is_ok = self.getParam(xml_node, 'exec') 
            #if is_ok and is_ok != 'ok':
            #    return None
            data = dict()
            
            data.update(self.dataUpdater(xml_node, 'version'))
            return data            
        except:
            logging.exception(DEFAULT_ID_COMMAND+" getSettings: "+str(sys.exc_info()))
            return None 
        
    def getRemark(self, xml_node):                                                                                                                                                                                              
        try:                                                                                                                                                                                                              
            return xml_node.getElementsByTagName('remark')[0].firstChild.toxml()                                                                                                                                          
        except:                                                                                                                                                                                                           
            return ""        
        
    def importRoller(self, path, cameraUUID, tmStart=datetime.datetime.now(), mode=0, diffFramesProc=None, convert=0, interval=None, idSignal = 6, signalType='import', params=[], id_command = DEFAULT_ID_COMMAND):
        try:
            p = [{'name': 'path', 'value': path},
                 {'name': 'cameraUUID', 'value': cameraUUID},
                 {'name': 'tmStart', 'value': tmStart.strftime("%Y%m%d%H%M%S")},
                 {'name': 'mode', 'value': mode},
                 {'name': 'convert', 'value': convert},
                 ]
            if diffFramesProc is not None: p.append({'name': 'diffFramesProc', 'value': diffFramesProc})
            if interval is not None: p.append({'name': 'interval', 'value': interval})
            if idSignal is not None: p.append({'name': 'idSignal', 'value': idSignal})
            if signalType is not None: p.append({'name': 'signalType', 'value': signalType})
            
            xml_node = self.__sendCommandXml(method='import_video', params=p, params2=params, id_command="import%s" %id_command)
            
            return self.__answerIsTrue(xml_node), self.getRemark(xml_node)
        except:
            logging.exception(DEFAULT_ID_COMMAND+" importRoller: "+str(sys.exc_info()))
            return False, "error import"
    
    def setDaemonSettings(self, params=[], id_command = DEFAULT_ID_COMMAND):
   
        xml_node = self.__sendCommandXml(method='setSettings', params=params, params2=[], id_command="setSettings%s" %id_command)  
        return self.__answerIsTrue(xml_node)
   