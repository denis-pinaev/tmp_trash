# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

import socket
from struct import pack, unpack
from cStringIO import StringIO
from xml.dom.minidom import parseString
from django.db.models import Q
import urllib
from videoclient.settings import log_communicator as logging
import sys
import datetime

DEFAULT_ID_COMMAND = 'SDKCommunicator'
XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>'
TIME_OUT = 15

class ConnectUnit():
    host = ''
    port = 0
    com_id = 0
    time_out = TIME_OUT
    socket_timeout = False
    sock = socket.SocketType
    status_connect = False
    
    def __init__(self, host, port, com_id, time_out = TIME_OUT):
        self.host = host
        self.port = port
        self.com_id = com_id
        self.time_out = time_out
    
    def connect(self):
        if self.socket_timeout:
            logging.error("timeout")
            raise self.socket.timeout
        if not self.status_connect:
            from django.utils.translation import ugettext as _
            from videoclient.monitoring.utils import saveMonitoringMessage
            params = {'host':self.host, 'port':self.port}
            try:
                #print 'connecting to %s:%s' %(self.host, self.port)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(self.time_out)
                self.sock.connect((self.host, self.port))
                self.sock.settimeout(None)
                self.status_connect = True
            except socket.timeout:
                self.socket_timeout = True
                saveMonitoringMessage(id = 'communicator_timeout', params = params, type='accident_components', description=_("Превышено время ожидания соединения с Коммуникатором %(host)s:%(port)s") % params, show=True)
            except:
                saveMonitoringMessage(id = 'communicator_connect_error', params = params, type='accident_components', description=_("Ошибка подключения к Коммуникатору %(host)s:%(port)s") % params, show=True)
                logging.exception("Communicator __connect: "+str(sys.exc_info()))                
            
    def disconnect(self):
        if self.status_connect:
            self.sock.close()
            self.status_connect = False    


    def close(self):
        self.disconnect()
        
    def open(self):
        self.connect()
        
    def readBytes(self, bytes):
        if bytes == 0:
            return ''
        buffer = StringIO()
        df = bytes
        self.sock.settimeout(self.time_out)
        try:
            while df > 0:
                if (df > 1024):
                    s = self.sock.recv(1024)
                else :
                    s = self.sock.recv(df)
                if len(s) == 0:
                    return None
                    break
                    #raise RuntimeError
                df = df - len(s)
                buffer.write(s)
        except socket.timeout:
            self.socket_timeout = True
            
        res=buffer.getvalue()
        buffer.close()
        #    print 'res:', res
        return res
    
    def sendSize(self, size):
        spack = pack('<I', size)
        self.sock.send(spack)
          
    def sendXML(self, data):
        logging.info("Communicator __sendData: "+str(data))
        spack = pack('<I', len(data)) + pack('<%ss' %len(data), str(data))
        self.sock.send(spack)
        
    def sendData(self, xml_text):
        try:
            xml_node = parseString(xml_text)
            id_commands = xml_node.getElementsByTagName("id_command")
            if id_commands:
                id_command = id_commands[0].firstChild.toxml()
                new_id_command = "".join([id_command, datetime.datetime.now().isoformat()])
                xml_text = xml_text.replace("<id_command>%s</id_command>" % id_command, 
                                            "<id_command>%s</id_command>" % new_id_command)
        except:
            logging.exception(sys.exc_info())
        self.sendXML(xml_text)
        
        
    def readSize(self):
        #b4 = self.__readBytes(4)
        self.sock.settimeout(self.time_out)
        size = 0
        try:
            b4 = self.sock.recv(4)
            #logging.info("__readSize: b4="+str(b4))
            size = unpack('<I', b4)[0]
        except socket.timeout:
            self.socket_timeout = True
        return size
    
    def readData(self):
        size = self.readSize();
        return self.readBytes(size)
    
    def readXml(self):
        self.sock.settimeout(self.time_out)
        data = self.readData()
        data = data.strip(" \t\n")
        logging.info("Communicator __readData: "+str(data))
        if self.socket_timeout:
            return None
        return parseString(data)
    
    def answerIsTrue(self, xml_node):
        try:
            xml_text = xml_node.toxml()
            answer = xml_node.getElementsByTagName('exec')[0].firstChild.toxml() == 'ok'
            return answer
        except: 
            logging.exception("answerIsTrue: "+str(sys.exc_info()))
        return False
    
    def answerIsTrueLogless(self, xml_node):
        try:
            xml_text = xml_node.toxml()
            answer = xml_node.getElementsByTagName('exec')[0].firstChild.toxml() == 'ok'
            return answer
        except: 
            pass
        return False
    
    def answerIsActive(self, xml_node):
        try:
            xml_text = xml_node.toxml()
            answer = xml_node.getElementsByTagName('active')[0].firstChild.toxml() == 'true'
            logging.info("__answerIsActive: "+str(xml_text)+str(answer))
            return answer
        except: 
            logging.exception("__answerIsActive: "+str(sys.exc_info()))
        return False
    
    def answerIsActiveLogless(self, xml_node):
        try:
            xml_text = xml_node.toxml()
            answer = xml_node.getElementsByTagName('active')[0].firstChild.toxml() == 'true'
            return answer
        except: 
            pass
        return False
    
    def toFloat(self, param):
        i = 0
        while i<len(param):
            param[i] = float(param[i])
            i=i+1
        return param
    
    def parsRes(self, text):
        res = dict()
        
        params = self.toFloat(text.split(','));
        
        res['face'] = (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
        res['is_face'] = int(params[8])
                
        res['eye1'] = (params[9], params[10])
        res['is_eye1'] = int(params[11])
        
        res['eye2'] = (params[12], params[13])
        res['is_eye2'] = int(params[14])
        
        res['nouse'] = (params[15], params[16])
        res['is_nouse'] = int(params[17])
        
        res['chin'] = (params[18], params[19])
        res['is_chin'] = int(params[20])
        return res

    def _del(self):
        self.disconnect()

class Communicator():
    host = ''
    port = 0
    time_out = TIME_OUT
    socket_timeout = False
    
    CONNECT_UNITS = []
    UUIDS_CONNECT_INFO = []
        
    #sock = socket.SocketType
    connect = False
    
    def __init__(self):
        self.__del__
        self.CONNECT_UNITS = []
        self.UUIDS_CONNECT_INFO = []
    
    def deleteAllConnectUnits(self):
        for cUnit in self.CONNECT_UNITS:
            try:
                cUnit["connect"]._del()
                del cUnit["connect"]
            except:
                pass

        self.CONNECT_UNITS = []
        self.UUIDS_CONNECT_INFO = []
        return True

    def close(self):
        self.deleteAllConnectUnits()
        
    def getCommunicatorByUUID(self, uuid=None, host=None, port=None, mjpeg_port=None):
        c = {'success': False, 'reason': ''}
        try:
            if uuid:
                c = models.Camera.objects.filter(active=True, uuid=uuid)[0]
                c = {'success': True, 'host': c.commun.host, 'port': str(c.commun.port), 'mjpeg_port': str(c.commun.mjpeg_port), 'id': c.commun.pk}
            if host and port and mjpeg_port:
                c = models.Communicator.objects.filter(active=True, host=host, port=port, mjpeg_port=mjpeg_port)[0]
                c = {'success': True, 'host': c.host, 'port': str(c.port), 'mjpeg_port': str(c.mjpeg_port), 'id': c.pk}
        except:
            c = {'success': False, 'reason': str(sys.exc_info())}
        
        return c

    def getListOfCommunicators(self):
        COMMUNICATORS = []
        try:
            comms = models.Communicator.objects.filter(active = True)
            for comm in comms:
                COMMUNICATORS.append({'host': comm.host, 'port': comm.port, 'mjpeg_port': comm.mjpeg_port, 'id': comm.id, 'commun': comm})
        except:
            logging.info("Class communicator getListOfCommunicators: %s", str(sys.exc_info()))
        
        return COMMUNICATORS
    
    def __del__(self):
        self.deleteAllConnectUnits()
        logging.info("ALL CONNECTIONS ARE CLOSED")
    
    def selectSocketUnit(self, uuid=None, host=None, port=None, mjpeg_port=None):
        try:
            if uuid or (host and port and mjpeg_port):
                #check for current connections in CONNECT_UNITS
                cHost = ''
                cPort = ''
                cMjPort = ''
                connection_exist = False
                
                if uuid:
                    for uuid_data in self.UUIDS_CONNECT_INFO:
                        if str(uuid) == str(uuid_data['uuid']):
                            cHost = uuid_data['host']
                            cPort = uuid_data['port']
                            cMjPort = uuid_data['mjpeg_port']
                            connection_exist = True

                if host and port and mjpeg_port:
                    for cUnit in self.CONNECT_UNITS:
                        logging.info("CONNECTION ALREADY EXISTS")
                        if str(host) == cUnit["host"] and str(port) == str(cUnit["port"]) and str(mjpeg_port) == str(cUnit["mjpeg_port"]):
                            return {'success': True, 'connect': cUnit["connect"]}
                
                if connection_exist:
                    logging.info("CONNECTION ALREADY EXISTS")
                    #get current connection unit
                    for cUnit in self.CONNECT_UNITS:
                        if str(cHost) == cUnit["host"] and str(cPort) == str(cUnit["port"]) and str(cMjPort) == str(cUnit["mjpeg_port"]):
                            return {'success': True, 'connect': cUnit["connect"]}
                else:
                    #create connection unit
                    communicator = self.getCommunicatorByUUID(uuid=uuid, host=host, port=port, mjpeg_port=mjpeg_port)
                    if communicator["success"]:
                        #check for connections wich was created without uuid
                        for cUnit in self.CONNECT_UNITS:
                            if str(communicator["host"]) == str(cUnit["host"]) and str(communicator["port"]) == str(cUnit["port"]) and str(communicator["mjpeg_port"]) == str(cUnit["mjpeg_port"]):
                                logging.info("CONNECTION ALREADY EXISTS")
                                self.UUIDS_CONNECT_INFO.append({'uuid': uuid, 'host': communicator["host"], 'port': communicator["port"], 'mjpeg_port': communicator["mjpeg_port"]})
                                return {'success': True, 'connect': cUnit["connect"]}
                        
                        logging.info("ESTABLISHMENT OF A CONNECTION")
                        connectUnit = ConnectUnit(communicator["host"], int(communicator["port"]), communicator["id"])
                        self.CONNECT_UNITS.append({'host': communicator["host"], 'port': communicator["port"], 'mjpeg_port': communicator["mjpeg_port"], 'connect': connectUnit})
                        self.UUIDS_CONNECT_INFO.append({'uuid': uuid, 'host': communicator["host"], 'port': communicator["port"], 'mjpeg_port': communicator["mjpeg_port"]})
                        return {'success': True, 'connect': connectUnit}
    
                    else:
                        logging.info("Comminicator is not found for UUID: %s" % uuid)
                
                return {'success': False}
            else:
                #UUIDS_CONNECT_INFO.append({'mjpeg_port': '13600', 'host': u'oxion2.test.gale.ru', 'uuid': '400d468a-9519-11e1-b595-20cf30bac9ca', 'port': '12600'})
                #CONNECT_UNITS.append({'mjpeg_port': '13600', 'host': u'192.168.0.125', 'port': '12600', 'connectUnit': ConnectUnit('oxion2.test.gale.ru', '12600')})
                
                listOfConnectUnits = []
                listOfCommunicators = self.getListOfCommunicators()
    
                for comm in listOfCommunicators:
                    #check for available connectionUnit, use it or create new one
                    isExists = False
                    for cUnit in self.CONNECT_UNITS:
                        if str(comm["host"]) == cUnit["host"] and str(comm["port"]) == str(cUnit["port"]) and str(comm["mjpeg_port"]) == str(cUnit["mjpeg_port"]):
                            listOfConnectUnits.append(cUnit["connect"])
                            isExists = True
                            logging.info("CONNECTION ALREADY EXISTS")
    
                    if not isExists:
                        logging.info("ESTABLISHMENT OF A CONNECTION")
                        connectUnit = ConnectUnit(comm["host"], int(comm["port"]), comm["id"])
                        self.CONNECT_UNITS.append({'host': comm["host"], 'port': comm["port"], 'mjpeg_port': comm["mjpeg_port"], 'connect': connectUnit})
                        listOfConnectUnits.append(connectUnit)
    
                return {'success': True, 'listOfConnectUnits': listOfConnectUnits}
        except:
            return {'success': False, 'reason': str(sys.exc_info())}

        return {'success': False, 'reason': ''}             
    
    def getFrame(self, num, mode, w, h, id_command = DEFAULT_ID_COMMAND):
        
        self.__connect()
        
        xml_text = XML_HEADER+'<methodCall><methodName>getFrame</methodName><params><numcamera>%s</numcamera><mode>%s</mode><w>%s</w><h>%s</h></params><id_command>getFrame%s</id_command></methodCall>' % (num, mode, w, h, id_command)
        
        self.__sendData(xml_text)
        xml_node = self.__readXml()
        
        xml_persons = xml_file.getElementsByTagName("person")
        
        out = []
        for xml_person in xml_persons:
            
            xml_face = xml_person.getElementsByTagName("face")[0]
            res_face = self.__parsRes(xml_face.firstChild.toxml())
            
            xml_k = xml_person.getElementsByTagName("k")
            xml_person_id = xml_person.getElementsByTagName("person_id")
            xml_person_name = xml_person.getElementsByTagName("person_name")
            xml_name_photo = xml_person.getElementsByTagName("name_photo")
            
            
            i=0
            res_sim = []
            while i<len(xml_person_id):
                res_sim.append({'person_id': xml_person_id[i].firstChild.toxml(),
                                'person_name': xml_person_id[i].firstChild.toxml(), 
                                'name_photo': xml_name_photo[i].firstChild.toxml(), 
                                'k': float(xml_k[i].firstChild.toxml()), }) 
                i = i+1
           
            out.append((res_face, res_sim))

        return out
    
    def va_detector(self, d_name, xml_node, detector):
        try:
            xml_obj = xml_node.getElementsByTagName(d_name)[0]
        except:
            xml_obj = None

        objErrors = False
        if xml_obj:
            try:
                xml_objects = xml_obj.getElementsByTagName("objects")[0]
            except:
                objErrors = True
                logging.info("getVideoFrame: Can't get %s data" % d_name)
            try:
                detect_objects = xml_objects.getElementsByTagName("object")
            except:
                objErrors = True
                logging.info("getVideoFrame: Can't get %s objects array" % d_name)
                
            objects_data = []
            try:
                for xml_obj in detect_objects:
                    try:
                        obj_id = xml_obj.getElementsByTagName("id")[0].firstChild.toxml()
                    except:
                        objErrors = True
                        logging.info("getVideoFrame: Can't get %s objects id" % d_name)
                    
                    try:
                        obj_points = xml_obj.getElementsByTagName("points")[0].firstChild.toxml()
                        obj_points = obj_points.split(',')
                    except:
                        objErrors = True
                        logging.info("getVideoFrame: Can't get %s objects points" % d_name)

                    objects_data.append({'id': int(obj_id), 'top_l': [int(obj_points[0]), int(obj_points[1])], 'bot_r': [int(obj_points[2]), int(obj_points[3])]})
            except:
                objErrors = True
                logging.info("getVideoFrame: Can't get %s objects bitmap_list" % d_name)
        
        objData = None
        if not objErrors and xml_obj:
            objData = {detector: objects_data}
        
        return objData

    def getVideoFrame(self, uuid, mode, w, h, method = "getFrame", id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
    
                error_remark = None
        
                xml_text = XML_HEADER+'<methodCall><methodName>%s</methodName><params><uuid>%s</uuid></params><id_command>getFrame%s</id_command></methodCall>' % (method, uuid, id_command)
                
                
                xml_node = parseString(xml_text)
                xml_text = xml_node.toxml()
        
                socketUnit.sendData(xml_text)
                if method=="getFrame":
                    jpeg_image = socketUnit.readData()
                else:
                    jpeg_image = None
                xml_node = socketUnit.readXml()
                
                focusfactors = []
                try:
                    xml_focusfactors = xml_node.getElementsByTagName("focusfactor")
                    for xml_focusfactor in xml_focusfactors:
                        focusfactors.append(float(xml_focusfactor.firstChild.toxml()))
                except:
                    logging.info("getFrame: Can't get focusfactors data")
                
                noisefactors = []
                try:
                    xml_noisefactors = xml_node.getElementsByTagName("noisefactor")
                    for xml_noisefactor in xml_noisefactors:
                        noisefactors.append(float(xml_noisefactor.firstChild.toxml()))
                except:
                    logging.info("getFrame: Can't get noisefactors data")  
                
                noiseStdDevs = []
                try:
                    xml_noiseStdDevs = xml_node.getElementsByTagName("noiseStdDev")
                    for xml_noiseStdDev in xml_noiseStdDevs:
                        noiseStdDevs.append(float(xml_noiseStdDev.firstChild.toxml()))
                except:
                    logging.info("getFrame: Can't get noiseStdDevs data")  
                
                histograms = []
                try:
                    xml_histograms = xml_node.getElementsByTagName("histogram")
                    for xml_histogram in xml_histograms:
                        histograms.append(xml_histogram.firstChild.toxml())
                except:
                    logging.info("getFrame: Can't get histograms data")
                    
                person_data = []
                xml_person_id = None
                try:
                    ident_data = []
                    xml_persons = xml_node.getElementsByTagName("person")
                    xml_k = None
                    xml_person_id = None
                    xml_person_name = None
                    xml_name_photo = None
                    i = 0
                    for xml_person in xml_persons:
                        xml_face = xml_person.getElementsByTagName("face")[0]
                        res_face = socketUnit.parsRes(xml_face.firstChild.toxml())
                            
                        try:
                            xml_k = xml_person.getElementsByTagName("k")[0].firstChild.toxml()
                        except:
                            logging.info("getVideoFrame: Can't get k value")
                        
                        try:
                            xml_person_id = xml_person.getElementsByTagName("person_id")[0].firstChild.toxml()
                        except:
                            pass
                        
                        try:
                            xml_person_name = xml_person.getElementsByTagName("person_name")[0].firstChild.toxml()
                        except:
                            pass
                        
                        try:
                            xml_name_photo = xml_person.getElementsByTagName("name_photo")[0].firstChild.toxml()
                            if xml_name_photo == 'none' or xml_name_photo == 'empty':
                                xml_name_photo = None
                        except:
                            logging.info("getVideoFrame: Can't get name_photo value")
                            
                        try:
                            focusfactor = focusfactors[i]
                        except:
                            focusfactor = ''
                            logging.info("getVideoFrame: Can't get focusfactor for person")
                        
                        try:
                            noisefactor = noisefactors[i]
                        except:
                            noisefactor = ''
                            logging.info("getVideoFrame: Can't get noisefactor for person")
                        
                        try:
                            noiseStdDev = noiseStdDevs[i]
                        except:
                            noiseStdDev = ''
                            logging.info("getVideoFrame: Can't get noiseStdDev for person")
        
                        ident_data.append({'face': res_face, 'k': xml_k, 'person_id': xml_person_id, 'person_name': xml_person_name, 'name_photo': xml_name_photo, 'focusfactor': focusfactor, 'noisefactor': noisefactor, 'noiseStdDev': noiseStdDev})
                        i += 1
                except:
                    logging.info("getFrame: Can't get ident data %s",  str(sys.exc_info()))
        
                #separating objects
                block_w = None
                block_h = None
                bitmap_list = []
                try:
                    xml_sepObj = xml_node.getElementsByTagName('separatingObjects')[0]
                except:
                    xml_sepObj = None
                
                sepObjErrors = False
                if xml_sepObj:
                    try:
                        xml_block = xml_sepObj.getElementsByTagName("blockSize")[0]
                    except:
                        sepObjErrors = True
                        logging.info("getVideoFrame: Can't get separating objects blockSize")
                    
                    try:
                        block_w = int(xml_block.getElementsByTagName("w")[0].firstChild.toxml())
                    except:
                        sepObjErrors = True
                        logging.info("getVideoFrame: Can't get separating objects block width")
                    
                    try:
                        block_h = int(xml_block.getElementsByTagName("h")[0].firstChild.toxml())
                    except:
                        sepObjErrors = True
                        logging.info("getVideoFrame: Can't get separating objects block height")
                    
                    try:
                        xml_data = xml_sepObj.getElementsByTagName("data")[0]
                    except:
                        sepObjErrors = True
                        logging.info("getVideoFrame: Can't get separating objects data")
                    
                    try:
                        data_lines = xml_data.getElementsByTagName("line")
                    except:
                        sepObjErrors = True
                        logging.info("getVideoFrame: Can't get separating objects data lines")
                    
                    try:
                        for line in data_lines:
                            row = []
                            for bit in line.firstChild.toxml():
                                row.append(int(bit))
                            bitmap_list.append(row)
                    except:
                        sepObjErrors = True
                        logging.info("getVideoFrame: Can't get separating objects bitmap_list")
                
                sepObjData = None
                if not sepObjErrors and xml_sepObj:
                   sepObjData = {'b_width': block_w, 'b_height': block_h, 'bitmap_list': bitmap_list}
                
                #leftthings detect
                leftObjData = self.va_detector('leftThings', xml_node, 'left_objects')
                
                #fire detect
                fireObjData = self.va_detector('fireDetect', xml_node, 'fire_objects')
                
                #smoke detect
                smokeObjData = self.va_detector('smokeDetect', xml_node, 'smoke_objects')
                
                #flash detect
                flashObjData = self.va_detector('flashDetect', xml_node, 'flash_objects')
        
                #getFrame errors
                try:
                    error_remark = xml_node.getElementsByTagName('remark')[0].firstChild.toxml()
                except:
                    pass
                    #logging.info("getFrame: Can't get remark value")
                
                frame_date = None
                try:
                    frame_date = xml_node.getElementsByTagName('date')[0].firstChild.toxml()
                except:
                    pass
                
                delay_time_frame = None
                try:
                    delay_time_frame = abs(int(xml_node.getElementsByTagName('delay_time_frame')[0].firstChild.toxml()))
                except:
                    pass
        
                data = { 'frame_date': frame_date, 'delay_time_frame': delay_time_frame }
                
                return {'success': True, 'answer': {'image': jpeg_image, 'error_remark': error_remark, 'data': data, 'person_data':  ident_data, 'sep_obj_data': sepObjData, 'left_obj_data': leftObjData, 'fire_obj_data': fireObjData, 'smoke_obj_data': smokeObjData, 'flash_obj_data': flashObjData }}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator getVideoFrame: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
    def getCameraFrameStat(self, uuid, mode, w, h, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
                
                error_remark = None
                info = None
                data = {}
                
                detectDaemonTime = 'Null'
                detectTotalTime = 'Null'
                recognitionDaemonTime = 'Null'
                recognitionTotalTime = 'Null'
                
                xml_text = XML_HEADER + '<methodCall><methodName>getFrame</methodName><params><uuid>%s</uuid><mode>%s</mode><w>%s</w><h>%s</h></params><id_command>getFrame%s</id_command></methodCall>' % (uuid, mode, w, h, id_command)
                
                xml_node = parseString(xml_text)
                xml_text = xml_node.toxml()
                
                socketUnit.sendData(xml_text)
                jpeg_image = socketUnit.readData()
                xml_node = socketUnit.readXml()
        
                try:
                    error_remark = xml_node.getElementsByTagName('remark')[0].firstChild.toxml()
                except:
                    logging.info("getFrame: Can't get remark value")
                
                try:
                    info_node = xml_node.getElementsByTagName('info')[0]
                except:
                    logging.info("getFrame: Can't get info node")
                
                try:
                    detectDaemonTime = float(info_node.getElementsByTagName('detectDaemonTime')[0].firstChild.toxml())
                    detectDaemonTime = float('%.6f' % detectDaemonTime)
                except:
                    pass
                
                try:
                    detectTotalTime = float(info_node.getElementsByTagName('detectTotalTime')[0].firstChild.toxml())
                    detectTotalTime = float('%.6f' % detectTotalTime)
                except:
                    pass
                
                try:
                    recognitionDaemonTime = float(info_node.getElementsByTagName('recognitionDaemonTime')[0].firstChild.toxml())
                    recognitionDaemonTime = float('%.6f' % recognitionDaemonTime)
                except:
                    pass
                
                try:
                    recognitionTotalTime = float(info_node.getElementsByTagName('recognitionTotalTime')[0].firstChild.toxml())
                    recognitionTotalTime = float('%.6f' % recognitionTotalTime)
                except:
                    pass   
        
                data = { 'detectDaemonTime': detectDaemonTime, 'detectTotalTime': detectTotalTime, 'recognitionDaemonTime': recognitionDaemonTime, 'recognitionTotalTime': recognitionTotalTime }
                return {'success': True, 'answer': data}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator getCameraFrameStat: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
    def getValue(self, xml_node, name):
        answer = None
        try:
            if len(xml_node.getElementsByTagName(name))>0:
                answer = xml_node.getElementsByTagName(name)[0].firstChild.toxml()
        except:
            logging.exception(str(sys.exc_info()))
        return answer
    
    def parseGraphics(self, node):
        try:
            childNodes = node.childNodes
            answer = []
            for childNode in childNodes:
                name = childNode.localName
                koeff = 1
                if name == 'memoryUsage':
                    name = 'memoryUsageMB'
                    koeff = float(1)/1024/1024;
                if len(childNode.childNodes)>0:
                    text_value = childNode.childNodes[0].toxml()
                    if name in ["time"]:
                        value = text_value.split(',')
                        
                        new_value = []
                        if len(value)>601:
                            value = value[0:601] 
                        i = 0
                        for v in value:
                            if v != "-1":
                                try:
                                    new_value.append([i, float(v)*koeff]);
                                except:
                                    pass
                            i=i+1
                    else:
                        value = text_value.split(';')
                        
                        new_value = []
                        if len(value)>601:
                            value = value[len(value)-601-1:len(value)-1] 
                        i = len(value)
                        for v in value:
                            i=i-1
                            if v != "-1":
                                try:
                                    new_value.append([i, float(v)*koeff]);
                                except:
                                    pass
                    if len(new_value)>0:
                        answer.append({'name': name, 'value': new_value})
            return answer
        except:
            return None
        
    def parseSubStatistic(self, childNode):
        answer = []
        name = childNode.localName
        if not name: return answer
        graphics = self.parseGraphics(childNode)
        if graphics is not None:
            answer.append({'name': name, 'value': graphics})
        return answer
    
    def parseStatistic(self, node):
        childNodes = node.childNodes
        answer = []
        for childNode in childNodes:
            answer.extend(self.parseSubStatistic(childNode))
        return answer
    
    def getCameraFramesStat(self, uuid, id_command = DEFAULT_ID_COMMAND):
        
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
                
                error_remark = None
                info = None
                data = {}
                
                xml_text = XML_HEADER + '<methodCall><methodName>getCameraFramesStatistics</methodName><params><uuid>%s</uuid></params><id_command>getCameraFramesStat%s</id_command></methodCall>' % (uuid, id_command) 
                
                xml_node = parseString(xml_text)
                xml_text = xml_node.toxml()
                
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()

                statistic = None
                
                error_remark = self.getValue(xml_node, 'remark')
                if error_remark:
                    return {'success': True, 'answer': statistic, 'error_remark': error_remark }
                
                param_exec = self.getValue(xml_node, 'exec')
                if param_exec and param_exec != 'ok':
                    error_remark = "Exec is not ok"
                    return {'success': True, 'answer': statistic, 'error_remark': error_remark }
                
                statistic_nodes = xml_node.getElementsByTagName('response')
                
                if len(statistic_nodes)>0:
                    statistic_node = statistic_nodes[0]
                    statistic = self.parseSubStatistic(statistic_node)
                else:
                    error_remark = "Can't get statistic node" 
                
                return {'success': True, 'answer': statistic, 'error_remark': error_remark }
            else:
                return {'success': False}
        except:
            return {'success': False}
    
    def getCameraVaStat(self, uuid, timeKind='astronomical', perSecond=1, perFrame=1, perMinute=1, id_command = DEFAULT_ID_COMMAND):
        
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
                
                error_remark = None
                info = None
                data = {}
                
                xml_text = XML_HEADER + '<methodCall><methodName>vaStatistics</methodName><params><uuid>%s</uuid><timeKind>%s</timeKind><perSecond>%s</perSecond><perFrame>%s</perFrame><perMinute>%s</perMinute></params><id_command>vaStatistics%s</id_command></methodCall>' % (uuid, timeKind, perSecond, perFrame, perMinute, id_command) 
                
                xml_node = parseString(xml_text)
                xml_text = xml_node.toxml()
                
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                statistic = None
                
                error_remark = self.getValue(xml_node, 'remark')
                if error_remark:
                    return {'success': True, 'answer': statistic, 'error_remark': error_remark }
                    
                
                param_exec = self.getValue(xml_node, 'exec')
                if param_exec and param_exec != 'ok':
                    error_remark = "Exec is not ok"
                    return {'success': True, 'answer': statistic, 'error_remark': error_remark }
                
                statistic_nodes = xml_node.getElementsByTagName('statistics')

                if len(statistic_nodes)>0:
                    statistic_node = statistic_nodes[0]
                    statistic = self.parseStatistic(statistic_node)
                else:
                    error_remark = "Can't get statistic node"
        
                return {'success': True, 'answer': statistic, 'error_remark': error_remark }
        except:
            return {'success': False}

    def getVAVersion(self, uuid, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
        
                xml_text = XML_HEADER+'<methodCall><methodName>vaVersion</methodName><params><uuid>%s</uuid></params><id_command>getVAVersion%s</id_command></methodCall>' %(uuid, id_command)
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                
                if xml_node.getElementsByTagName('exec')[0].firstChild.toxml() == 'ok':
                    return True, xml_node.getElementsByTagName('version')[0].firstChild.toxml()
                else:
                    return False, xml_node.getElementsByTagName('remark')[0].firstChild.toxml()
            else:
                return False, 'socket error'
        except:
            logging.info("Class communicator getModeScheduler: %s", str(sys.exc_info()))
            return False, str(sys.exc_info())
    
    def setModeScheduler(self, uuid, mode, id_person=0, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
        
                if id_person ==0:
                    xml_text = XML_HEADER+'<methodCall><methodName>setModeScheduler</methodName><params><uuid>%s</uuid><mode>%s</mode></params><id_command>setModeScheduler%s</id_command></methodCall>' %(uuid, mode, id_command)
                else:
                    xml_text = XML_HEADER+'<methodCall><methodName>setModeScheduler</methodName><params><uuid>%s</uuid><mode>%s</mode><id_person>%s</id_person></params><id_command>setModeScheduler%s</id_command></methodCall>' %(uuid, mode, id_person, id_command)
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
        
                return {'success': True, 'answer': socketUnit.answerIsTrue(xml_node)}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator setModeScheduler: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
        return {'success': False}
    
    def getModeScheduler(self, uuid, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
        
                xml_text = XML_HEADER+'<methodCall><methodName>getModeScheduler</methodName><params><uuid>%s</uuid></params><id_command>getModeScheduler%s</id_command></methodCall>' %(uuid, id_command)
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                return {'success': True, 'answer': int(xml_node.getElementsByTagName('mode')[0].firstChild.toxml())}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator getModeScheduler: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}

    
    def getVersion(self, id_command = DEFAULT_ID_COMMAND):
        version_info = []
        try:
            socketUnits = self.selectSocketUnit()
            if socketUnits["success"]:
                for socketUnit in socketUnits["listOfConnectUnits"]:
                    try:
                        socketUnit.connect()
              
                        xml_text = XML_HEADER+'<methodCall><methodName>version</methodName><params/><id_command>getVersion%s</id_command></methodCall>' %(id_command)
                        
                        socketUnit.sendData(xml_text)
                        xml_node = socketUnit.readXml()
                        
                        version_info.append({'host': socketUnit.host, 'port': socketUnit.port, 'version': xml_node.getElementsByTagName('version')[0].firstChild.toxml()})
                    except:
                        version_info.append({'host': socketUnit.host, 'port': socketUnit.port, 'version': None})
                return {'success': True, 'versions': version_info}
        except:
            logging.info("Class communicator getVersion: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
    def setCorrelationIdent(self, num, k, id_command = DEFAULT_ID_COMMAND):
        
        self.__connect()
        
        xml_text = XML_HEADER+'<methodCall><methodName>setCorrelationIdent</methodName><params><numcamera>%s</numcamera><k>%s</k></params><id_command>setCorrelationIdent%s</id_command></methodCall>' %(num, k, id_command)
        self.__sendData(xml_text)
        xml_node = self.__readXml()
        
        return self.__answerIsTrue(xml_node)
    
    def getCorrelationIdent(self, num, id_command = DEFAULT_ID_COMMAND):
        
        self.__connect()

        xml_text = XML_HEADER+'<methodCall><methodName>getCorrelationIdent</methodName><params><numcamera>%s</numcamera></params><id_command>getCorrelationIdent%s</id_command></methodCall>' %(num, id_command)
                
        self.__sendData(xml_text)
        xml_node = self.__readXml()
                
        return xml_node.getElementsByTagName('k')[0].firstChild.toxml()
    
    def setCaptureRectCamera(self, uuid, x, y, width, height, id_command = DEFAULT_ID_COMMAND): # add width height
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
                xml_text = XML_HEADER+'<methodCall><methodName>setCaptureRectCamera</methodName><params><uuid>%s</uuid><x>%s</x><y>%s</y><width>%s</width><height>%s</height></params><id_command>setCaptureRectCamera%s</id_command></methodCall>' %(uuid, x, y, width, height, id_command)
                
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                
                if socketUnit.answerIsTrue(xml_node):
                    return {'success': True, 'answer': xml_node.getElementsByTagName('exec')[0].firstChild.toxml()}
                else:
                    return {'success': False}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator setCaptureRectCamera: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
    def getCaptureRectCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()

                xml_text = XML_HEADER+'<methodCall><methodName>getCaptureRectCamera</methodName><params><uuid>%s</uuid></params><id_command>getCaptureRectCamera%s</id_command></methodCall>' % (uuid, id_command)
                
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                
                return {'success': True, 'answer': {'x': xml_node.getElementsByTagName('x')[0].firstChild.toxml(),
                'y': xml_node.getElementsByTagName('y')[0].firstChild.toxml(),
                'width': xml_node.getElementsByTagName('width')[0].firstChild.toxml(),
                'height': xml_node.getElementsByTagName('height')[0].firstChild.toxml(),
                }}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator getCaptureRectCamera: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
        
    def setResolutionCamera(self, uuid, width, height, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
                xml_text = XML_HEADER+'<methodCall><methodName>setResolutionCamera</methodName><params><uuid>%s</uuid><width>%s</width><height>%s</height></params><id_command>setResolutionCamera%s</id_command></methodCall>' %( uuid, width, height, id_command)
                
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                
                if socketUnit.answerIsTrue(xml_node):
                    return {'success': True, 'answer': xml_node.getElementsByTagName('exec')[0].firstChild.toxml()}
                else:
                    return {'success': False}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator setResolutionCamera: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
    
    def getResolutionCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
        
                xml_text = XML_HEADER+'<methodCall><methodName>getResolutionCamera</methodName><params><uuid>%s</uuid></params><id_command>getResolutionCamera%s</id_command></methodCall>' % (uuid, id_command)
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                
                rs = xml_node.getElementsByTagName('resol')[0].firstChild.toxml().split('*')
                resol=[]
                for r in rs:
                    params = r.split('x')
                    #w, h, f = r.split('x')
                    try:
                        w = params[0]
                    except:
                        pass
                    try:
                        h = params[1]
                    except:
                        pass
                    try:
                        f = params[2]
                    except:
                        f = 0
                    resol.append({'width': w, 'height': h, 'fps': f})
                
                width = xml_node.getElementsByTagName('width')[0].firstChild.toxml()
                height = xml_node.getElementsByTagName('height')[0].firstChild.toxml()
                resol = resol
                max_width = xml_node.getElementsByTagName('max_width')[0].firstChild.toxml()
                max_height = xml_node.getElementsByTagName('max_height')[0].firstChild.toxml()      
                return {'success': True, 'answer': {'width': width, 'height': height, 'resol': resol, 'max_width': max_width, 'max_height': max_height}}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator getResolutionCamera: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}

    
    def getCameras(self, filter_active=False, id_command = DEFAULT_ID_COMMAND):
        cameras = []
        try:
            socketUnits = self.selectSocketUnit()
            if socketUnits["success"]:
                communicator_errors_info = []
                for socketUnit in socketUnits["listOfConnectUnits"]:
                    try:
                        socketUnit.connect()
              
                        xml_text = XML_HEADER+'<methodCall><methodName>getCameras</methodName><params/><id_command>getCameras%s</id_command></methodCall>' % id_command
                        
                        xml_node = parseString(xml_text)
                        xml_text = xml_node.toxml()
                        
                        socketUnit.sendData(xml_text)
                        
                        xml_node = socketUnit.readXml()
                        xml_cameras = xml_node.getElementsByTagName('camera')
                        
                        for xml_camera in xml_cameras:
                            ip = xml_camera.getElementsByTagName('ip')[0].firstChild.toxml()
                            port = xml_camera.getElementsByTagName('port')[0].firstChild.toxml()
                            type_ = xml_camera.getElementsByTagName('type')[0].firstChild.toxml()
                            info = ip + " " + type_
                            uuid = xml_camera.getElementsByTagName('uuid')[0].firstChild.toxml()
                            active = xml_camera.getElementsByTagName('active')[0].firstChild.toxml()
                            num = xml_camera.getElementsByTagName('num')[0].firstChild.toxml()
                            try:
                                from videoclient.views import unescape
                                url = xml_camera.getElementsByTagName('url')[0].firstChild.toxml()
                                url = unescape(url)                                
                                if type_ == "URL": info = url + " " + type_
                            except: url = ""
                            cameras.append({'info': info, 'uuid': uuid, 'active': active, 'ip': ip, 'port': port, 'type': type_, 'num': num, 'com_host': socketUnit.host, 'com_port': socketUnit.port, 'com_id': socketUnit.com_id, 'url': url})
                    except:
                        communicator_errors_info.append({'host': str(socketUnit.host), 'port': str(socketUnit.port)})
                        logging.info("Communicator connection error: %s:%s: %s", str(socketUnit.host), str(socketUnit.port), str(sys.exc_info()))

                active_uuids = []
                for camera in cameras:
                    cam = models.Camera.objects.get_or_create(uuid=camera["uuid"])
                    cam = cam[0]
                    if not cam.name: cam.name = camera["info"]
                    cam.ip = camera["ip"]
                    cam.port = camera["port"]
                    cam.type = camera["type"]
                    cam.commun_id = int(camera["com_id"])
                    cam.active = True
                    cam.delete = False
                    cam.available = int(camera["active"])
                    cam.url = camera["url"]
                    cam.save()
                    active_uuids.append(camera["uuid"])
                
                #make old cameras inactive
                cams = []
                try:
                    cams = models.Camera.objects.filter(active=True).exclude(Q(uuid__in=active_uuids) | Q(type="IMPORT"))
                    for cam_ in cams:
                        cam_.delete = True
                        cam_.available = False
                        cam_.save()
                except:
                    cams = []
                    
                cameras = []
                try:
                    if filter_active:
                        cameras = models.Camera.objects.filter(active=True, available=True).exclude(type="IMPORT").order_by('delete', '-id')
                    else:
                        cameras = models.Camera.objects.filter(active=True).exclude(type="IMPORT").order_by('-available', 'delete', '-id')
                except:
                    cameras = []
            return {'success': True, 'cameras': cameras, 'communicator_errors_info': communicator_errors_info, 'disappeared_cams': cams}
        except:
            logging.info("Class communicator getCameras: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
    def foundCameras(self, count = 0, id_command = DEFAULT_ID_COMMAND):
        
        self.__connect()
        
        xml_text = XML_HEADER+'<methodCall><methodName>foundCameras</methodName><params></params><id_command>foundCameras%s</id_command></methodCall>' %id_command
        if count>0: 
            xml_text = XML_HEADER+'<methodCall><methodName>foundCameras</methodName><params><count>%s</count></params><id_command>foundCameras%s</id_command></methodCall>' %(count, id_command)

        self.__sendData(xml_text)
        
        old_time_out = self.time_out 
        self.time_out = None
        xml_node = self.__readXml()
        self.time_out = old_time_out
        
        return self.__answerIsTrue(xml_node)
    

    def setParamsScheduler(self, uuid, interval=-1, delay=-1, fd=-1, fr=-1, fl=-1, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()

                xml_text = XML_HEADER + '<methodCall><methodName>setParamsScheduler</methodName><params><uuid>%s</uuid>' %uuid
                if int(interval)>=0:
                    xml_text = xml_text+'<interval>%s</interval>' %interval
                if int(delay)>=0:
                    xml_text = xml_text+'<delay>%s</delay>' %delay
                if int(fd)>=0:
                    xml_text = xml_text+'<limit_fd>%s</limit_fd>' %fd
                if int(fr)>=0:
                    xml_text = xml_text+'<limit_fi>%s</limit_fi>' %fr
                if int(fl)>=0:
                    xml_text = xml_text+'<limit_fl>%s</limit_fl>' %fl
        
                xml_text = xml_text+'</params><id_command>setParamsScheduler%s</id_command></methodCall>' %id_command
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()    
                if socketUnit.answerIsTrue(xml_node):     
                    return {'success': True, 'answer': xml_node.getElementsByTagName('exec')[0].firstChild.toxml()}
                else:
                    return {'success': False}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator __getOption: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
        
    
    def getParamsScheduler(self, uuid, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()

                xml_text = XML_HEADER+'<methodCall><methodName>getParamsScheduler</methodName><params><uuid>%s</uuid></params><id_command>getParamsScheduler%s</id_command></methodCall>' %(uuid, id_command)
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()

                return {'success': True, 'answer': {'interval': xml_node.getElementsByTagName('interval')[0].firstChild.toxml(),
                'delay': xml_node.getElementsByTagName('delay')[0].firstChild.toxml(),
                'limit_fd': xml_node.getElementsByTagName('limit_fd')[0].firstChild.toxml(),
                'limit_fr': xml_node.getElementsByTagName('limit_fi')[0].firstChild.toxml(),
                'limit_fl': xml_node.getElementsByTagName('limit_fl')[0].firstChild.toxml(),
                }}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator getParamsScheduler: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
        
    
    def setSettingsDetectScheduler(self, form, detect='leftThings', id_command = DEFAULT_ID_COMMAND):
        self.__connect()
        
        error_remark = None

        if detect == 'background':
            d_time = (form.cleaned_data['bg_minutes'] * 60) + form.cleaned_data['bg_seconds']
            xml_text = XML_HEADER + '<methodCall><methodName>setSettingsDetectScheduler</methodName><params><numcamera>%s</numcamera><detect>%s</detect><interval>%s</interval></params><id_command>setSettingsDetectScheduler%s</id_command></methodCall>' % (form.cleaned_data['cam_id'], detect, d_time, id_command)  
        else:
            d_time = (form.cleaned_data['hour'] *  3600) + (form.cleaned_data['minutes'] * 60) + form.cleaned_data['seconds']
            xml_text = XML_HEADER+'<methodCall><methodName>setSettingsDetectScheduler</methodName><params><numcamera>%s</numcamera><detect>%s</detect><interval>%s</interval><diffColorThreshold>%s</diffColorThreshold><diffGrayThreshold>%s</diffGrayThreshold><diffMotionThreshold>%s</diffMotionThreshold><minPixelObject>%s</minPixelObject><minPixelMove>%s</minPixelMove></params><id_command>setSettingsDetectScheduler%s</id_command></methodCall>' % (form.cleaned_data['cam_id'], detect, d_time, form.cleaned_data['diffColorThreshold'], form.cleaned_data['diffGrayThreshold'], form.cleaned_data['diffMotionThreshold'],form.cleaned_data['minPixelObject'],form.cleaned_data['minPixelMove'], id_command)
        
        xml_node = parseString(xml_text)
        xml_text = xml_node.toxml()
        
        self.__sendData(xml_text)
        xml_node = self.__readXml()

        if self.__answerIsTrueLogless(xml_node):
            return {'result': True, 'error_remark': error_remark}
        else:
            try:
                error_remark = xml_node.getElementsByTagName('remark')[0].firstChild.toxml()
            except:
                logging.info("setSettingsDetectScheduler %s: Can't get remark value") % detect

            return {'result': False, 'error_remark': error_remark}
    
    def getSettingsDetectScheduler(self, num, detect='leftThings', id_command = DEFAULT_ID_COMMAND):
        self.__connect()
        
        xml_text = XML_HEADER+'<methodCall><methodName>getSettingsDetectScheduler</methodName><params><numcamera>%s</numcamera><detect>%s</detect></params><id_command>getSettingsDetectScheduler%s</id_command></methodCall>' % (num, detect, id_command)
        
        self.__sendData(xml_text)
        xml_node = self.__readXml()
        
        if detect == 'leftThings':
            interval = xml_node.getElementsByTagName('interval')[0].firstChild.toxml()
            minPixelObject = xml_node.getElementsByTagName('minPixelObject')[0].firstChild.toxml()
            diffMotionThreshold = xml_node.getElementsByTagName('diffMotionThreshold')[0].firstChild.toxml()
            diffGrayThreshold = xml_node.getElementsByTagName('diffGrayThreshold')[0].firstChild.toxml()
            minPixelMove = xml_node.getElementsByTagName('minPixelMove')[0].firstChild.toxml()
            diffColorThreshold = xml_node.getElementsByTagName('diffColorThreshold')[0].firstChild.toxml()
            return {'interval': interval, 'minPixelObject': minPixelObject, 'diffMotionThreshold': diffMotionThreshold, 'diffGrayThreshold': diffGrayThreshold, 'minPixelMove': minPixelMove, 'diffColorThreshold': diffColorThreshold}
            #return {'interval': interval}
        if detect == 'background':
            interval = xml_node.getElementsByTagName('interval')[0].firstChild.toxml()
            return {'interval': interval}
    
    def turnOnOffModeDetectScheduler(self, form, mode='on', detect='leftThings', id_command = DEFAULT_ID_COMMAND):
        error_remark = None

        self.__connect()
        if mode == 'on':
            xml_text = XML_HEADER+'<methodCall><methodName>turnOnModeDetectScheduler</methodName><params><numcamera>%s</numcamera><detect>%s</detect></params><id_command>turnOnModeDetectScheduler%s</id_command></methodCall>' % (form.cleaned_data['cam_id'], detect, id_command)  
        else:
            xml_text = XML_HEADER+'<methodCall><methodName>turnOffModeDetectScheduler</methodName><params><numcamera>%s</numcamera><detect>%s</detect></params><id_command>turnOffModeDetectScheduler%s</id_command></methodCall>' % (form.cleaned_data['cam_id'], detect, id_command)
            
        xml_node = parseString(xml_text)
        xml_text = xml_node.toxml()
        
        self.__sendData(xml_text)
        xml_node = self.__readXml()
        
        if self.__answerIsTrueLogless(xml_node):
            return {'result': True, 'error_remark': error_remark}
        else:
            try:
                error_remark = xml_node.getElementsByTagName('remark')[0].firstChild.toxml()
            except:
                if mode == 'on':
                    logging.info("turnOnModeDetectScheduler background: Can't get remark value")
                else:
                    logging.info("turnOffModeDetectScheduler background: Can't get remark value")

            return {'result': False, 'error_remark': error_remark }
    
    def getModeDetectScheduler(self, uuid, detect='leftThings', id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
                xml_text = XML_HEADER + '<methodCall><methodName>getModeDetectScheduler</methodName><params><uuid>%s</numcamera><detect>%s</detect></params><id_command>getModeDetectScheduler%s</id_command></methodCall>' % (uuid, detect, id_command)
                
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                if xml_node.getElementsByTagName('active')[0].firstChild.toxml() == 'true':
                    return {'success': True, 'answer': xml_node.getElementsByTagName('active')[0].firstChild.toxml()}
                else:
                    try:
                        error_remark = xml_node.getElementsByTagName('remark')[0].firstChild.toxml()
                    except:
                        logging.info("getModeDetectScheduler %s: remark value" % detect)
                    return {'success': False, 'reason': error_remark }
                
            else:
                return {'success': False}
        except:
            logging.info("Class communicator getModeDetectScheduler: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
        
       
    def getStatistics(self, host, port, mjpeg_port, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid=None, host=host, port=port, mjpeg_port=mjpeg_port)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
                               
                xml_text = XML_HEADER+'<methodCall><methodName>statistics</methodName><params></params><id_command>getStatistics%s</id_command></methodCall>' %(id_command)
                
                xml_node = parseString(xml_text)
                xml_text = xml_node.toxml()
                
                socketUnit.sendData(xml_text)
                
                xml_node = socketUnit.readXml()
                nodes = xml_node.getElementsByTagName('response')[0].childNodes
                
                value = dict();
                for node in nodes:
                    name = None
                    if node: name = node.localName
                    if name: 
                        value[name] = map(int, node.childNodes[0].toxml().split(','))
                        value[name].reverse()
                        #value[name] = node.toxml()
                logging.info('getStatistics: '+str(value))
                return {'success': True, 'answer': value}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator getStatistics: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
#<time>hhmmss,hhmmss</time>
#<min>500,300</min>
#<max>800,900</max>
#<avg>350, 400</avg>
#<missed>1,2</missed>
#<errors>0,0</errors>
    
    
    def addCamera(self, type, ip, mac='000000000000', port=None, num=None, user=None, psw=None, url=None, json=False, id_command = DEFAULT_ID_COMMAND):
        
        self.__connect()
        
        xml_text = XML_HEADER + '<methodCall><methodName>addCamera</methodName><params><type>%s</type><ip>%s</ip><mac>%s</mac>' %(type, ip, mac)
        if port != None:
            xml_text = xml_text+'<port>%s</port>' %port
        if num != None:
            xml_text = xml_text+'<num>%s</num>' %num
        if user != None:
            xml_text = xml_text+'<user>%s</user>' %user
        if psw != None:
            xml_text = xml_text+'<psw>%s</psw>' %psw
        if url != None:
            xml_text = xml_text+'<url>%s</url>' %url
        xml_text = xml_text+'</params><id_command>addCamera%s</id_command></methodCall>' %id_command
               
        self.__sendData(xml_text)
        
        xml_node = self.__readXml()
        
        if self.socket_timeout:
            status = False
            if json:
                answer = {"status": status}
                answer["remark"] = "Socket timeout"
                return answer
            else:
                return status
        
        status = self.__answerIsTrue(xml_node)
        if json:
            answer = {"status": status}
            if not status:
                if xml_node.getElementsByTagName('remark') and len(xml_node.getElementsByTagName('remark'))>0:
                    answer["remark"] =  xml_node.getElementsByTagName('remark')[0].firstChild.toxml()
            return answer
        else:
            return status

    
    def __getOption(self, uuid, option, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
                xml_text = XML_HEADER+'<methodCall><methodName>get%s</methodName><params><uuid>%s</uuid></params><id_command>get%s%s</id_command></methodCall>' %(option, uuid, option, id_command)
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                return {'success': True, 'answer': xml_node.getElementsByTagName('value')[0].firstChild.toxml()}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator __getOption: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
        
    
    def deleteCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
        
                xml_text = XML_HEADER+'<methodCall><methodName>deleteCamera</methodName><params><uuid>%s</uuid></params><id_command>deleteCamera%s</id_command></methodCall>' %( uuid, id_command)
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                
                #make camera inactive
                try:
                    cam = models.Camera.objects.get_or_create(uuid=uuid)
                    cam = cam[0]
                    cam.active = False
                    cam.save()
                except:
                    pass
                return {'success': True, 'answer': socketUnit.answerIsTrue(xml_node)}
            else:
               return {'success': False} 
        except:
            logging.info("Class communicator deleteCamera: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
    def startRecord(self, uuid, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
        
                #1-flv,2-mjpeg,3-mpeg
                xml_text = XML_HEADER+'<methodCall><methodName>startRecord</methodName><params><uuid>%s</uuid></params><id_command>startRecord%s</id_command></methodCall>' %( uuid, id_command)
        
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
        
                filename = None
                try:
                    filename = xml_node.getElementsByTagName('filename')[0].firstChild.toxml()
                except:
                    logging.exception(sys.exc_info())
                
                return {'success': True, 'answer': filename}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator startRecord: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
    def stopRecord(self, uuid, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
        
                xml_text = XML_HEADER+'<methodCall><methodName>stopRecord</methodName><params><uuid>%s</uuid></params><id_command>stopRecord%s</id_command></methodCall>' %( uuid, id_command)
        
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
        
                return {'success': True, 'answer': socketUnit.answerIsTrue(xml_node)}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator stopRecord: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
    
    def statusRecord(self, uuid, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
        
                xml_text = XML_HEADER+'<methodCall><methodName>statusRecord</methodName><params><uuid>%s</uuid></params><id_command>statusRecord%s</id_command></methodCall>' %( uuid, id_command)
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                
                status = None
                status = xml_node.getElementsByTagName('status')[0].firstChild.toxml()
                
                return {'success': True, 'answer': status}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator statusRecord: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
  
   
    def getBrightnessCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'BrightnessCamera', id_command)
    
    def getSaturationCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'SaturationCamera', id_command)
      
    def getSharpnessCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'SharpnessCamera', id_command)
    
    def getContrastCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'ContrastCamera', id_command)          
        
    def getQualityCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'QualityCamera', id_command)
    
    def getGammaCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'GammaCamera', id_command)
    
    def getLightHZCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'LightHZCamera', id_command)
    
    def getNightModeCamera(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'NightModeCamera', id_command)
    
    def getIlluminationMode(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'IlluminationMode', id_command)
        
    def getLowLight(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'LowLight', id_command)
    
    def getShortexposures(self, uuid, id_command = DEFAULT_ID_COMMAND):
        return self.__getOption(uuid, 'Shortexposures', id_command)        
    
    def __setOption(self, uuid, value, option, id_command = DEFAULT_ID_COMMAND):
        try:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                socketUnit = socketUnit["connect"]
                socketUnit.connect()

                xml_text = XML_HEADER+'<methodCall><methodName>set%s</methodName><params><uuid>%s</uuid><value>%s</value></params><id_command>set%s%s</id_command></methodCall>' %(option, uuid, value, option, id_command)
                
                socketUnit.sendData(xml_text)
                xml_node = socketUnit.readXml()
                if socketUnit.answerIsTrue(xml_node):     
                    return {'success': True, 'answer': xml_node.getElementsByTagName('exec')[0].firstChild.toxml()}
                else:
                    return {'success': False}
            else:
                return {'success': False}
        except:
            logging.info("Class communicator __getOption: %s", str(sys.exc_info()))
            return {'success': False, 'reason': str(sys.exc_info())}
     
    def setBrightnessCamera(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'BrightnessCamera', id_command)
    
    def setSaturationCamera(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'SaturationCamera', id_command)
      
    def setSharpnessCamera(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'SharpnessCamera', id_command)
    
    def setContrastCamera(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'ContrastCamera', id_command)          
        
    def setQualityCamera(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'QualityCamera', id_command)
    
    def setGammaCamera(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'GammaCamera', id_command)
    
    def setLightHZCamera(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'LightHZCamera', id_command)
    
    def setNightModeCamera(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'NightModeCamera', id_command)
    
    def setIlluminationMode(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'IlluminationMode', id_command)
    
    def setLowLight(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'LowLight', id_command)
    
    def setShortexposures(self, uuid, value, id_command = DEFAULT_ID_COMMAND):
        return self.__setOption(uuid, value, 'Shortexposures', id_command)
    
    
    def executeMethodByName(self, name, params):
        func = {'getFrame': self.getFrame,
                'setModeScheduler': self.setModeScheduler,
                'getModeScheduler': self.getModeScheduler,
                'setCorrelationIdent': self.setCorrelationIdent,
                'getCorrelationIdent': self.getCorrelationIdent,
                'setCaptureRectCamera': self.setCaptureRectCamera,
                'getCaptureRectCamera': self.getCaptureRectCamera,
                'setResolutionCamera': self.setResolutionCamera,
                'getResolutionCamera': self.getResolutionCamera,
                'getCameras': self.getCameras,
                'foundCameras': self.foundCameras,
                'setParamsScheduler': self.setParamsScheduler,
                'getParamsScheduler': self.getParamsScheduler,
                'addCamera': self.addCamera,
                'getBrightnessCamera': self.getBrightnessCamera,
                'getSaturationCamera': self.getSaturationCamera,
                'getSharpnessCamera': self.getSharpnessCamera,
                'getContrastCamera': self.getContrastCamera,
                'getQualityCamera': self.getQualityCamera,
                'getGammaCamera': self.getGammaCamera,
                'getLightHZCamera': self.getLightHZCamera,
                'getNightModeCamera': self.getNightModeCamera,
                'getIlluminationMode': self.getIlluminationMode,
                'getLowLight': self.getLowLight,
                'getShortexposures': self.getShortexposures,
                'setBrightnessCamera': self.setBrightnessCamera,
                'setSaturationCamera': self.setSaturationCamera,
                'setSharpnessCamera': self.setSharpnessCamera,
                'setContrastCamera': self.setContrastCamera,
                'setQualityCamera': self.setQualityCamera,
                'setGammaCamera': self.setGammaCamera,
                'setLightHZCamera': self.setLightHZCamera,
                'setNightModeCamera': self.setNightModeCamera,
                'setIlluminationMode': self.setIlluminationMode,
                'setLowLight': self.setLowLight,
                'setShortexposures': self.setShortexposures
                }
        
        if len(params) == 0:
            return func[name]()
        if len(params) == 1:
            return func[name](params[0])
        if len(params) == 2:
            return func[name](params[0], params[1])
        if len(params) == 3:
            return func[name](params[0], params[1], params[2])
        if len(params) == 4:
            return func[name](params[0], params[1], params[2], params[3])
        if len(params) == 5:
            return func[name](params[0], params[1], params[2], params[3], params[4])
        if len(params) == 6:
            return func[name](params[0], params[1], params[2], params[3], params[4], params[5])
        if len(params) == 7:
            return func[name](params[0], params[1], params[2], params[3], params[4], params[5], params[6])
        if len(params) == 8:
            return func[name](params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
        return False
    
    #universal method
    def executeCommand(self, name, params, answer_type, get_values = None, host=None, port=None, mjpeg_port=None, id_command = DEFAULT_ID_COMMAND):
        uuid = None
        params_str = ''
        for key in params.keys():
            params_str += '<%s>%s</%s>' % (str(key), str(params[key]), str(key))
            if str(key) == 'uuid':
                uuid = str(params[key])

        method = '<methodCall><methodName>%s</methodName><params>%s</params><id_command>%s%s</id_command></methodCall>' % (name, params_str, name, id_command)
        
        error_remark = None

        isSocketUnit = False
        if uuid:
            socketUnit = self.selectSocketUnit(uuid)
            if socketUnit["success"]:
                isSocketUnit = True
                socketUnit = socketUnit["connect"]
                socketUnit.connect()

        if host and port and mjpeg_port:
            socketUnit = self.selectSocketUnit(host=host, port=port, mjpeg_port=mjpeg_port)
            if socketUnit["success"]:
                isSocketUnit = True
                socketUnit = socketUnit["connect"]
                socketUnit.connect()
        
        if isSocketUnit:
                xml_text = XML_HEADER + method
                socketUnit.sendData(xml_text)
        
                xml_node = socketUnit.readXml()
                condition = None
                if answer_type == 'GetValues' and get_values:
                    try:
                        error_remark = xml_node.getElementsByTagName('remark')[0].firstChild.toxml()
                        return {'result': False, 'error_remark': error_remark }
                    except:
                        returned_values = dict()
                        
                        for i in range(0, len(get_values)):
                            temp_param = None
                            try:
                                temp_param = xml_node.getElementsByTagName(get_values[i])[0].firstChild.toxml()
                                returned_values[get_values[i]] = temp_param
                            except:
                                returned_values[get_values[i]] = None
                                logging.info("%s : Can't get '%s' value" % (name, get_values[i]))
            
                        return {'result': True, 'returned_values': returned_values }
                else:
                    if answer_type == 'IsTrue':
                        condition = socketUnit.answerIsTrueLogless(xml_node)
                        
                    if answer_type == 'IsActive':
                        condition = socketUnit.answerIsActiveLogless(xml_node)
            
                    if condition != None:
                        return {'result': condition, 'error_remark': error_remark}
                    else:
                        try:
                            error_remark = xml_node.getElementsByTagName('remark')[0].firstChild.toxml()
                        except:
                            error_remark = u'неправильный формат ответа коммуникатора'
                            logging.info("%s %s: Can't get remark value" % (name, params))
            
                        return {'result': False, 'error_remark': error_remark }
        
        return {'result': False, 'error_remark': 'communicator executeCommand internal error'}



