# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

import socket
from struct import pack, unpack
from cStringIO import StringIO
from xml.dom.minidom import parseString
from videoclient.settings import log_balancer as logging
import sys
import datetime

MAX_READ_DATA = 10
TIME_OUT = 25.0

class Balancer():
    
    host = ''
    port = 0
    login = ''
    passwd = ''
    user = ''

    sock = socket.SocketType
    connect = False
    
    def __init__(self, host, port, login, passwd, user):
        self.host = host
        self.port = port
        self.login = login
        self.passwd = passwd
        self.user = user
        self.TIME_OUT = TIME_OUT
    
    def __del__(self):
        self.__disconnect()
        
    def __readBytes(self, bytes):
        if bytes == 0:
            return ''
        buffer = StringIO()
        df = bytes
        self.sock.settimeout(self.TIME_OUT)
        while df > 0:
            if (df > 1024):
                s = self.sock.recv(1024)
            else :
                s = self.sock.recv(df)
            if len(s) == 0:
                return None
            df = df - len(s)
            buffer.write(s)
            
        res=buffer.getvalue()
        buffer.close()
        return res
    
    def __connect(self):
        try:
            if not self.connect:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                self.connect = True
        except:
            from django.utils.translation import ugettext as _
            from videoclient.monitoring.utils import saveMonitoringMessage
            params = {'host':self.host, 'port':self.port}
            saveMonitoringMessage(id = 'cs_connect_error', params = params, type='accident_components', description=_("Ошибка подключения к Управляющей системе %(host)s:%(port)s") % params, show=True)
            logging.exception("Balancer __connect: "+str(sys.exc_info()))            
    
    def open(self):
        self.__connect()
            
    def close(self):
        self.__disconnect()
        
    def __disconnect(self):
        if self.connect:
            self.sock.close()
            self.connect = False    
    
    def __toFloat(self, param):
        i = 0
        while i<len(param):
            param[i] = float(param[i])
            i=i+1
        return param
    
    def __parsRes(self, text):
        res = dict()
        res['face_string'] = text.split(',')
        res['full_face'] = text        
        
        params = self.__toFloat(text.split(','));
        
        res['face'] = [params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]]
        res['is_face'] = int(params[8])
                
        res['eye1'] = [params[9], params[10]]
        res['is_eye1'] = int(params[11])
        
        res['eye2'] = [params[12], params[13]]
        res['is_eye2'] = int(params[14])
        
        res['nouse'] = [params[15], params[16]]
        res['is_nouse'] = int(params[17])
        
        res['chin'] = [params[18], params[19]]
        res['is_chin'] = int(params[20])
        return res
    
    def __joinRes(self, params):
        float_to_str = lambda x: list(map(str, x))
        join_str = lambda x: ",".join(float_to_str(x))
        out = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (join_str(params['face']), params['is_face'], join_str(params['eye1']), params['is_eye1'], join_str(params['eye2']), params['is_eye2'], join_str(params['nouse']), params['is_nouse'], join_str(params['chin']), params['is_chin'])
        return out
    
    def __sendSize(self, size):
        spack = pack('>i', size)
        self.sock.send(spack)    
          
    def __sendData(self, data):
        self.__sendSize(len(data))
        self.sock.send(data)
        
    def __sendXml(self, data):
        logging.info("sendXml: "+str(data))
        
        try:
            xml_node = parseString(data)
            id_commands = xml_node.getElementsByTagName("id_command")
            if id_commands:
                id_command = id_commands[0].firstChild.toxml()
                new_id_command = "".join([id_command, datetime.datetime.now().isoformat()])
                data = data.replace("<id_command>%s</id_command>" % id_command, 
                                    "<id_command>%s</id_command>" % new_id_command)
        except:
            logging.exception(sys.exc_info())
        
        data = data.encode("utf-8")
        data = bytearray(data)
        self.__sendData(data)
        
    def __readSize(self):
        df = self.__readBytes(4)
        return unpack('>i', df)[0]
    
    def __readData(self):
        size = self.__readSize()
        count = 0
        while size == 0 and count < MAX_READ_DATA:
            size = self.__readSize()
            count = count + 1
        return self.__readBytes(size)
    
    def __readXml(self):
        data = self.__readData()
        logging.info("Recv xml: "+data)
        return parseString(data)
    
    def __readImages(self):
        cnt = self.__readSize()
        images = []
        i=0
        while i<cnt:
            img_file = self.__readData()
            images.append(img_file)
            i = i+1
        return images
    
    def faceDetect(self, data_image, api_version="", id_command = 'SDKBalancer'):
        
        self.__connect()

        if api_version:
            xml_file = '<methodCall><methodName>facedetect</methodName><params><login>%s</login><password>%s</password><user>%s</user><apiVersion>%s</apiVersion><cutting>0,0,2,400,400</cutting><cutting_horizontal/></params><id_command>facedetect%s</id_command></methodCall>' % (self.login, self.passwd, self.user, api_version, id_command)
        else:
            xml_file = '<methodCall><methodName>facedetect</methodName><params><login>%s</login><password>%s</password><user>%s</user><cutting>0,0,2,400,400</cutting><cutting_horizontal/></params><id_command>facedetect%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        
        self.__sendXml(xml_file)
        
        self.__sendSize(1) # Количество передаваемых картинок
        self.__sendData(data_image)        
        
        xml_node = self.__readXml()
        images = self.__readImages()

        xml_faces = xml_node.getElementsByTagName("faces")[0].childNodes
        xml_cutting = []
        xml_cuttings = xml_node.getElementsByTagName("cuttingFaces")
        if len(xml_cuttings) > 0:
            xml_cutting = xml_cuttings[0].childNodes
        
        logging.info(len(xml_cutting))
        
        out = []
        i = 0
        for xml_face in xml_faces:
            face = self.__parsRes(xml_face.firstChild.toxml())
            if i < len(xml_cutting):
                face["cutting_face"] = self.__parsRes(xml_cutting[i].firstChild.toxml())
            out.append(face)
            i += 1
                
        return (out, images)
    
    def recognize(self, data_image, limit = 10, params={}, id_command = 'SDKBalancer'):
        self.__connect()
        
        if "face" in params:
            xml_file = '<methodCall><methodName>identification</methodName><params><login>%s</login><password>%s</password><user>%s</user><face>%s</face><result_count>%d</result_count></params><id_command>recognize%s</id_command></methodCall>' % (self.login, self.passwd, self.user, self.__joinRes(params), limit, id_command)
        elif "answerType" in params:
            xml_file = '<methodCall><methodName>identification</methodName><params><login>%s</login><password>%s</password><user>%s</user><answerType>%s</answerType><result_count>%d</result_count><apiVersion>2.0</apiVersion></params><id_command>recognize%s</id_command></methodCall>' % (self.login, self.passwd, self.user, params["answerType"], limit, id_command)
        else:
            xml_file = '<methodCall><methodName>identification</methodName><params><login>%s</login><password>%s</password><user>%s</user><result_count>%d</result_count></params><id_command>recognize%s</id_command></methodCall>' % (self.login, self.passwd, self.user, limit, id_command)
        
        self.__sendXml(xml_file)
        
        self.__sendSize(1)
        self.__sendData(data_image)
        
        xml_file = self.__readXml()
        images = self.__readImages()
        
        
        xml_persons = xml_file.getElementsByTagName("person")
        
        out = []
        for xml_person in xml_persons:
            
            xml_face = xml_person.getElementsByTagName("face")[0]
            res_face = self.__parsRes(xml_face.firstChild.toxml())
            
            xml_person_id = xml_person.getElementsByTagName("person_id")
            xml_person_name = xml_person.getElementsByTagName("person_name")
            xml_name_photo = xml_person.getElementsByTagName("name_photo")
            xml_k = xml_person.getElementsByTagName("k")
            
            i=0
            res_sim = []
            while i<len(xml_person_id):
                res_sim.append({'id': xml_person_id[i].firstChild.toxml(), 
                                #'name': xml_person_name[i].firstChild.toxml(),
                                'image': xml_name_photo[i].firstChild.toxml(), 
                                'rang': float(xml_k[i].firstChild.toxml()), }) 
                i = i+1
           
            out.append((res_face, res_sim))

        return (out, images)
            
    def fanStudio(self, data_image, param, id_command = 'SDKBalancer'):
        self.__connect()
                        
        xml_file = '<methodCall><methodName>fanstudio</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>funStudio%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        xml_node = parseString(xml_file)
        if param:
            xml_params = xml_node.getElementsByTagName("params")[0]
            for proc in param:
                node_str = '<%s>%s</%s>' % (proc['name'], proc['param'], proc['name'])
                xml_params.appendChild(parseString(node_str).firstChild)
        xml_file = xml_node.toxml()
        self.__sendXml(xml_file)
        
        self.__sendSize(1)
        self.__sendData(data_image)
        
        xml_file = self.__readXml()
        images = self.__readImages()
        return images
    
    def learning(self, data_image, id, distortion = None, face=None, command='learning', res2=False, eyes=None, id_command = 'SDKBalancer'):

        self.__connect()
        
        if distortion is not None:
            xml_file = '<methodCall><methodName>%s</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_name>%s</person_name><distortion>%s</distortion><apiVersion>2.0</apiVersion></params><id_command>learning%s</id_command></methodCall>'  % (command, self.login, self.passwd, self.user, id, distortion, id_command)
        else:
            xml_file = '<methodCall><methodName>%s</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_name>%s</person_name><apiVersion>2.0</apiVersion></params><id_command>learning%s</id_command></methodCall>'  % (command, self.login, self.passwd, self.user, id, id_command)
        
        if face: 
            xml_node = parseString(xml_file)
            xml_params = xml_node.getElementsByTagName("params")[0]
            node_str = '<face>%s</face>' % face
            xml_params.appendChild(parseString(node_str).firstChild)
            xml_file = xml_node.toxml()
        if eyes:
            xml_node = parseString(xml_file)
            xml_params = xml_node.getElementsByTagName("params")[0]
            node_str = '<eyes>%s</eyes>' % eyes
            xml_params.appendChild(parseString(node_str).firstChild)
            xml_file = xml_node.toxml()
        
        self.__sendXml(xml_file)
       
        self.__sendSize(1)
        self.__sendData(data_image)

        xml_node = self.__readXml()
        xml_txt = xml_node.toxml()
        
        answer = []
        faces = xml_node.getElementsByTagName('face')
        person_ids = xml_node.getElementsByTagName('person_id')
        name_photos = xml_node.getElementsByTagName('name_photo')
        person_names = xml_node.getElementsByTagName('person_name')
        cause = None
        try:
            cause = xml_node.getElementsByTagName('cause')[0].firstChild.toxml()
        except:
            pass
        log_error = None
        try:
            log_error = xml_node.getElementsByTagName('logError')[0].firstChild.toxml()
        except:
            pass
            
        answer2 = {'cause': cause, 'log_error': log_error}
        
        i = 0
        while i<len(faces):
            face = faces[i].firstChild.toxml() if i<len(faces) and faces[i].firstChild else None
            person_id = person_ids[i].firstChild.toxml() if i<len(person_ids) and person_ids[i].firstChild else None
            name_photo = name_photos[i].firstChild.toxml() if i<len(name_photos) and name_photos[i].firstChild else None
            person_name = person_names[i].firstChild.toxml() if i<len(person_names) and person_names[i].firstChild else None
            a = {'face': face, 'perons_id': person_id, 'name_photo': name_photo, 'person_name': person_name, 'cause': cause, 'log_error': log_error}
            answer.append(a)
            i = i+1  
        
        if res2:
            return answer, answer2
        return answer
        
    def deleting(self, id, num=-1, id_command = 'SDKBalancer'):
        
        self.__connect()
        
        xml_file = ''
        
        if num<0:
            xml_file = '<methodCall><methodName>deleting</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_id>%s</person_id></params><id_command>delete%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id, id_command)
        else:
            xml_file = '<methodCall><methodName>deleting</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_id>%s</person_id><name_photo>%s</name_photo></params><id_command>delete%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id, num, id_command)

        self.__sendXml(xml_file)
        self.__sendSize(0)
        
        xml_node = self.__readXml()
        
        return xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
    
    def getPreview(self, id, num, id_command = 'SDKBalancer'):
        self.__connect()
        
        xml_file = '<methodCall><methodName>getpreview</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_id>%s</person_id><name_photo>%s</name_photo></params><id_command>getPreview%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id, num, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)
        
        xml_node = self.__readXml()
        namePerson = ''
        try:
            namePerson = xml_node.getElementsByTagName('person_name')[0].firstChild.toxml()
        except:
            pass
        
        images = self.__readImages()
        return (namePerson, images)
    
    def getPersonPhoto(self, id, num, id_command = 'SDKBalancer'):
        self.__connect()
                
        xml_file = '<methodCall><methodName>getpersonphoto</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_id>%s</person_id><name_photo>%s</name_photo></params><id_command>getPersonPhoto%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id, num, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)
        
        xml_file = self.__readXml()
        images = self.__readImages()
        
        return images
    
    def getPersonPhotoWithParams(self, id, num, id_command = 'SDKBalancer', get_info_xml = False):
        self.__connect()
                
        xml_file = '<methodCall><methodName>getpersonphoto</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_id>%s</person_id><name_photo>%s</name_photo></params><id_command>getPersonPhoto%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id, num, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)
        
        xml_file = self.__readXml()
        
        if not get_info_xml:
            params = []
            params = self.recursXml(xml_file.getElementsByTagName('methodResponse')[0])
        else:
            params = xml_file.getElementsByTagName('info')[0].toxml()
        
        images = self.__readImages()
        logging.info(str(params))
        
        return images, params  
      
        
    def getPersonPhotos(self, id, id_command = 'SDKBalancer'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>getpersonphotos</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_id>%s</person_id></params><id_command>getPersonPhotos%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)
        
        xml_node = self.__readXml()
        xml_txt = xml_node.toxml()
        
        photos = []
        if len(xml_node.getElementsByTagName('photos'))>0:
            fc = xml_node.getElementsByTagName('photos')[0].firstChild
            if fc != None:
                photos = fc.toxml().split(';')
        
        images = self.__readImages()
        
        return (photos, images)
    
    def getPersons(self, id_command = 'SDKBalancer'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>getpersons</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>getPersons%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)
        
        xml_node = self.__readXml()
        xml_txt = xml_node.toxml()
        
        ids = xml_node.getElementsByTagName('persons_ids')[0].firstChild.toxml().split(';')
        names = xml_node.getElementsByTagName('persons_names')[0].firstChild.toxml().split(';')
        photos = xml_node.getElementsByTagName('photos')[0].firstChild.toxml().split(';')
        
        return (ids, names, photos)
    
    
    def getCameraParameter(self, uuid, param = 'distortion', id_command = 'SDKBalancer'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>getcameraparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><cameraUuid>%s</cameraUuid><parameter>%s</parameter></params><id_command>getCameraParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, uuid, param, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        child = xml_node.getElementsByTagName('value')[0].firstChild
        if child:
            res = xml_node.getElementsByTagName('value')[0].firstChild.toxml().split(',')
        else:
            res = []
        
        return res
    
    def setCameraParameter(self, uuid, p1=None, p2=None, p3=None, p4=None, param = 'distortion', id_command = 'SDKBalancer'):
        
        self.__connect()
        
        if param != "distortion" or "crowd" in param:
            xml_file = '<methodCall><methodName>setcameraparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><cameraUuid>%s</cameraUuid><parameter>%s</parameter><value>%s</value></params><id_command>setCameraParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, uuid, param, p1, id_command)
        else:
            if p2 != "None":
                xml_file = '<methodCall><methodName>setcameraparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><cameraUuid>%s</cameraUuid><parameter>%s</parameter><value>%s,%s,%s,%s</value></params><id_command>setCameraParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, uuid, param, p1, p2, p3, p4, id_command)
            else:        
                xml_file = '<methodCall><methodName>setcameraparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><cameraUuid>%s</cameraUuid><parameter>%s</parameter><value>%s,%s,%s</value></params><id_command>setCameraParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, uuid, param, p1, p3, p4, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        
        return res
    
    ALL_PERAMS_FOR_TO_BASE = ['control.fd.preprocessing.min.face.side.pixels', 'minEyesDistance', 'control.fd.preprocessing.min.image.to.face.side.ratio', 'control.fd.preprocessing.max.image.to.face.side.ratio', 'control.fr.answer.type', 'control.fr.with.mirroring']
    
    def setParameter(self, value, param = 'eyes_distance', toBase="system", id_command = 'SDKBalancer'):
        
        self.__connect()
        
        if param == 'control.fd.detect.type':
            user = "system"
        else:
            user = self.user
        if param in self.ALL_PERAMS_FOR_TO_BASE:
            user = self.user
            toBase = self.user
        if toBase:
            xml_file = '<methodCall><methodName>setparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><toBase>%s</toBase><parameter>%s</parameter><value>%s</value></params><id_command>setParameter%s</id_command></methodCall>'  % (self.login, self.passwd, user, toBase, param, value, id_command)
        else:        
            xml_file = '<methodCall><methodName>setparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><parameter>%s</parameter><value>%s</value></params><id_command>setParameter%s</id_command></methodCall>'  % (self.login, self.passwd, user, param, value, id_command)        
      #  logging.info(xml_file)
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        
        return res
    
    def getParameter(self, param = 'eyes_distance', fromBase="system", id_command = 'SDKBalancer'):
        self.__connect()
        
        if param == 'control.fd.detect.type':
            user = "system"
        else:
            user = self.user
        if param in self.ALL_PERAMS_FOR_TO_BASE:            
            user = self.user
            fromBase = self.user            
                        
        xml_file = '<methodCall><methodName>getparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><parameter>%s</parameter><fromBase>%s</fromBase></params><id_command>getParameter%s</id_command></methodCall>'  % (self.login, self.passwd, user, param, fromBase, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('value')[0].firstChild.toxml()
        
        return res

    def getLeftPhotosCount(self, id_command = 'SDKBalancer'):
        try:
            self.__connect()
            
            # getLeftPhotosCount изменен на getLeftPicturesSpace по просьбе руководителя группы "Платформа"
            xml_file = '<methodCall><methodName>getLeftPhotosCount</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>getParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id_command)
            
            self.__sendXml(xml_file)
            self.__sendSize(0)
    
            xml_node = self.__readXml()
            
            res = xml_node.getElementsByTagName('count')[0].firstChild.toxml()
            
            return int(res) 
        except:
            logging.exception(str(sys.exc_info()))
        return None
    
    def getLeftPicturesSpace(self, id_command = 'SDKBalancer'):
        try:
            self.__connect()
            
            xml_file = '<methodCall><methodName>getLeftPicturesSpace</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>getParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id_command)
            
            self.__sendXml(xml_file)
            self.__sendSize(0)
    
            xml_node = self.__readXml()
            
            res = xml_node.getElementsByTagName('value')[0].firstChild.toxml()
            
            return int(res) 
        except:
            logging.exception(str(sys.exc_info()))
        return None    
    
    def deleteParameter(self, param='', toBase=""):
        if param == "" or toBase == "": return False
        
        self.__connect()
        
        xml_file = '<methodCall><methodName>removeParameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><parameter>%s</parameter><toBase>%s</toBase></params><id_command>removeParameterCommandID</id_command></methodCall>'  % (self.login, self.passwd, self.user, param, toBase)

        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        return xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
      
    def renameParameter(self, param='', new_param="", toBase=""):
        if param == "" or new_param == "" or toBase == "": return False
        
        self.__connect()
        
        xml_file = '<methodCall><methodName>renameParameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><parameter>%s</parameter><newParameter>%s</newParameter><toBase>%s</toBase></params><id_command>renameParameterSDKBalancer</id_command></methodCall>'  % (self.login, self.passwd, self.user, param, new_param, toBase)
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        return xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'

    def getPersonsPhotos(self, id_command = 'getCommandId', person_ids = []):
        self.__connect()
        person_ids = ','.join(person_ids) 
        xml_file = '<methodCall><methodName>getPersonsPhotos</methodName><params><login>%s</login><password>%s</password><user>%s</user><persons>%s</persons></params><id_command>%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, person_ids, id_command)
        self.__sendXml(xml_file)
        self.__sendSize(0)
        xml_node = self.__readXml()
        
        plist = []
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        if res:
            persons = xml_node.getElementsByTagName("persons")[0].childNodes
            i = 0
            for person in persons:
                plist.append({ "person_id": None, "photos": None, "p_num": None })
                plist[i]["person_id"] = person.getElementsByTagName('person_id')[0].childNodes[0].nodeValue
                params = person.getElementsByTagName('photos')[0].toxml()
                params = params.replace('<photos>', '')
                params = params.replace('<photos/>', '')
                params = params.replace('</photos>', '')
                plist[i]["photos"] = params
                plist[i]["p_num"] = None
                if len(params) > 0:
                    plist[i]["p_num"] = len(params.split(',')) 
                i += 1            
        return plist
    
    def getLogins(self, id_command = 'getLoginsCommandId'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>getLogins</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        logins = []
        if res:         
            params = xml_node.getElementsByTagName("login")
            for param in params:
                logins.append({"login": param.firstChild.toxml()})        
        return logins
    
    def getLoginParameters(self, uLogin=None, id_command = 'getLoginsCommandId'):
        
        self.__connect()
        if not uLogin: uLogin = self.login
                
        xml_file = '<methodCall><methodName>getLoginParameters</methodName><params><toLogin>%s</toLogin><login>%s</login><password>%s</password><user>%s</user></params><id_command>%s</id_command></methodCall>'  % (uLogin, self.login, self.passwd, self.user, id_command)
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        plist = {}
        if res:
            if (xml_node.getElementsByTagName('fullName')): plist["full_name"] = xml_node.getElementsByTagName('fullName')[0].firstChild.toxml()         
            bases = xml_node.getElementsByTagName("bases")[0].childNodes
            blist = []
            i = 0
            for base in bases:
                base = base.childNodes
                blist.append({"name": i, "params": []})
                if base[0].tagName == "baseName": blist[i]["name"] = base[0].firstChild.toxml()
                if base[1].tagName == "parameters":
                    bparams = []
                    for p in base[1].childNodes:
                        bparams.append({"name": p.tagName, "val": p.firstChild.toxml() if p.firstChild else None})
                    blist[i]["params"] = bparams
                i += 1
            plist["bases"] = blist                       
        
        return plist    
    
    def splitXmlParams(self, xml_node):
        blist = []
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        if res:
            bases = xml_node.getElementsByTagName("bases")[0].childNodes    
            i = 0
            for base in bases:
                base = base.childNodes
                if len(base) == 0:
                    continue
                blist.append({"name": i, "params": []})
                if base[0].tagName == "baseName": blist[i]["name"] = base[0].firstChild.toxml()
                if base[1].tagName == "parameters":
                    bparams = []
                    for p in base[1].childNodes:
                        bparams.append({"name": p.tagName, "val": p.firstChild.toxml() if p.firstChild else None})
                    blist[i]["params"] = bparams      
                i += 1                          
        return blist        
    
    def getAllParameters(self, id_command = 'getLoginsCommandId', return_xml=False):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>getAllParameters</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id_command)

        self.__sendXml(xml_file)
        self.__sendSize(0)

        if return_xml: return self.__readData()
        xml_node = self.__readXml()
                                 
        return self.splitXmlParams(xml_node)       
    
    def saveCameras(self, id_command = 'SDKBalancer'):
        
        self.__connect()
        
        update_value_defaultparams(name="settings_has_not_saved", value="0", create_new = True)

        xml_file = '<methodCall><methodName>savecameras</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>saveCameras%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        
        return res
    
    def configureCameras(self, id_command = 'SDKBalancer'):
       
        self.__connect()

        xml_file = '<methodCall><methodName>configurecameras</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>configureCameras%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        
        return res          

    def skinDetect(self, data_image, param, id_command = 'SDKBalancer'):
        
        self.__connect()

        xml_file = '<methodCall><methodName>skinDetect</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>skinDetect%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        xml_node = parseString(xml_file)
        if param:
            xml_params = xml_node.getElementsByTagName("params")[0]
            for proc in param:
                node_str = '<%s>%s</%s>' % (proc['name'], proc['param'], proc['name'])
                xml_params.appendChild(parseString(node_str).firstChild)
        xml_file = xml_node.toxml()
        
        self.__sendXml(xml_file)
        
        self.__sendSize(1) # Количество передаваемых картинок
        self.__sendData(data_image)        
        
        xml_node = self.__readXml()
        images = self.__readImages()

        result = xml_node.getElementsByTagName("percent")[0].firstChild.toxml()
                
        return (result, images)
    
    def dduppProc(self, data_image, brief=0, dduppDups=1, dduppMode=0, id_command = 'SDKBalancer'):
        self.__connect()

        xml_file = '<methodCall><methodName>dduppProc</methodName><params><login>%s</login><password>%s</password><user>%s</user><duppDupps>%s</duppDupps><duppMode>%s</duppMode><brief>%s</brief></params><id_command>dduppProc%s</id_command></methodCall>' % (self.login, self.passwd, self.user, dduppDups, dduppMode, brief, id_command)
       #logging.info(xml_file)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendXml(xml_file)
        
        self.__sendSize(1) # Количество передаваемых картинок
        self.__sendData(data_image)        
        
        xml_node = self.__readXml()
        images = self.__readImages()

        status = xml_node.getElementsByTagName("status")[0].firstChild.toxml()
        result = None
    #    logging.info(status)
        if status == "201 Created": result = "created"
        elif status == "200 OK":
            result = []
            """
            l = len(xml_node.getElementsByTagName("coeff"))
            if l==1:
                coeff = xml_node.getElementsByTagName("coeff")[0].firstChild.toxml()
                brief = xml_node.getElementsByTagName("brief")[0].firstChild.toxml()
                result = {"coeff": coeff, "brief": brief}
            elif l>0:                
                for i in range(l):
                    coeff = xml_node.getElementsByTagName("coeff")[i].firstChild.toxml()
                    brief = xml_node.getElementsByTagName("brief")[i].firstChild.toxml()
                    result.append({"coeff": coeff, "brief": brief})                        
            """
            xml_coeff = xml_node.getElementsByTagName("coeff")
            xml_brief = xml_node.getElementsByTagName("brief")
            xml_old_quad = xml_node.getElementsByTagName("new_quad")
            xml_new_quad = xml_node.getElementsByTagName("old_quad")        
            l = len(xml_coeff)
            """
            if l==1:
                coeff = xml_coeff[0].firstChild.toxml()
                brief = xml_brief[0].firstChild.toxml()
                old_quad = xml_old_quad[0].firstChild.toxml()
                new_quad = xml_new_quad[0].firstChild.toxml()
                result.append({"coeff": coeff, "brief": brief, "old_quad": old_quad, "new_quad": new_quad})
            el"""
            if l>0:
                for i in range(l):
                    coeff = xml_coeff[i].firstChild.toxml()
                    brief = xml_brief[i].firstChild.toxml()
                    old_quad = xml_old_quad[i].firstChild.toxml()
                    new_quad = xml_new_quad[i].firstChild.toxml()
                    result.append({"coeff": coeff, "brief": brief, "old_quad": old_quad, "new_quad": new_quad})

        return result    

    def dduppTest(self, data_image, dduppCoeff=0, dduppDups=1, dduppMode=0, id_command = 'SDKBalancer'):
        self.__connect()

        xml_file = '<methodCall><methodName>dduppTest</methodName><params><login>%s</login><password>%s</password><user>%s</user><duppCoeff>%s</duppCoeff><duppDupps>1000</duppDupps><duppMode>%s</duppMode></params><id_command>dduppTest%s</id_command></methodCall>' % (self.login, self.passwd, self.user, dduppCoeff, dduppMode, id_command)
      #  logging.info(xml_file)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendXml(xml_file)
        
        self.__sendSize(1) # Количество передаваемых картинок
        self.__sendData(data_image)        
        
        xml_node = self.__readXml()
        images = self.__readImages()

        status = xml_node.getElementsByTagName("status")[0].firstChild.toxml()
        result = []
        if status == "200 OK":
            xml_coeff = xml_node.getElementsByTagName("coeff")
            xml_brief = xml_node.getElementsByTagName("brief")
            xml_old_quad = xml_node.getElementsByTagName("new_quad")
            xml_new_quad = xml_node.getElementsByTagName("old_quad")        
            l = len(xml_coeff)
            """
            if l==1:
                coeff = xml_coeff[0].firstChild.toxml()
                brief = xml_brief[0].firstChild.toxml()
                old_quad = xml_old_quad[0].firstChild.toxml()
                new_quad = xml_new_quad[0].firstChild.toxml()
                result.append({"coeff": coeff, "brief": brief, "old_quad": old_quad, "new_quad": new_quad})
            el
            """
            if l>0:
                for i in range(l):
                    coeff = xml_coeff[i].firstChild.toxml()
                    brief = xml_brief[i].firstChild.toxml()
                    old_quad = xml_old_quad[i].firstChild.toxml()
                    new_quad = xml_new_quad[i].firstChild.toxml()
                    result.append({"coeff": coeff, "brief": brief, "old_quad": old_quad, "new_quad": new_quad})
    #    logging.info("ddupp "+str( result))
        return result

    def dduppSave(self, data_image, brief, dduppCoeff=0, dduppDups=1, dduppMode=0, id_command = 'SDKBalancer'):
        self.__connect()

        xml_file = '<methodCall><methodName>dduppSave</methodName><params><login>%s</login><password>%s</password><user>%s</user><duppDupps>20</duppDupps><duppCoeff>%s</duppCoeff><duppMode>%s</duppMode><brief>%s</brief></params><id_command>dduppSave%s</id_command></methodCall>' % (self.login, self.passwd, self.user, dduppDups, dduppCoeff, dduppMode, brief, id_command)

        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendXml(xml_file)
        
        self.__sendSize(1) # Количество передаваемых картинок
        self.__sendData(data_image)        
        
        xml_node = self.__readXml()
        images = self.__readImages()

        status = xml_node.getElementsByTagName("status")[0].firstChild.toxml()

        if status == "201 Created": return True
        return False  

    def dduppRemove(self, brief, id_command = 'SDKBalancer'):
        self.__connect()

        xml_file = '<methodCall><methodName>dduppRemove</methodName><params><login>%s</login><password>%s</password><user>%s</user><brief>%s</brief></params><id_command>dduppRemove%s</id_command></methodCall>' % (self.login, self.passwd, self.user, brief, id_command)
      #  logging.info(xml_file)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendXml(xml_file)
        
        self.__sendSize(0) # Количество передаваемых картинок
        
        xml_node = self.__readXml()
        images = self.__readImages()

        status = xml_node.getElementsByTagName("status")[0].firstChild.toxml()

        if status == "200 OK": return True
        return False

    def renamePerson(self, param, id_command = 'SDKBalancer'):
        
        self.__connect()

        xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>renamePerson</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>renamePerson%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        xml_node = parseString(xml_file)
        
        xml_params = xml_node.getElementsByTagName("params")[0]
        
        for proc in param:
            node_str = '<%s>%s</%s>' % (proc['name'], proc['param'], proc['name'])
            xml_params.appendChild(parseString(node_str).firstChild)

        xml_file = xml_node.toxml()
        
        self.__sendXml(xml_file)
        
        self.__sendSize(0) # Количество передаваемых картинок
        
        xml_node = self.__readXml()
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        
        return res
    
    def getParam(self, xml_node, param):
        data = dict()
        data[param] = None
        try:
            data[param] = xml_node.getElementsByTagName(param)[0].toxml();
        except:
            pass
        return data
    
    def recursXml(self, xml_node):
        value = None
        nodes = xml_node.childNodes
        if len(nodes)>0:
            value = dict();
            for node in nodes:
                name = node.localName                
                if (len(node.childNodes) == 1) and (node.childNodes[0].localName == None):
                    value[name] = node.childNodes[0].toxml()
                else:
                    arr = []

                    if value.has_key(name):
                        #if value[name] 
                        arr = value[name]
                    arr.append(self.recursXml(node))
                    value[name] = arr
        else:
            value = xml_node.toxml()
            
        return value
    
    
    def getSystemInfo(self, id_command = 'SDKBalancer', fullInfo = False):
        
        self.__connect()
                
        xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>getSystemInfo</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>getSystemInfo%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)                
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
                       
        if xml_node.getElementsByTagName('status')[0].firstChild.toxml() != '200 OK':
            return None;
       
        res = []
        res = self.recursXml(xml_node.getElementsByTagName('balancers')[0])
        if fullInfo:
            csV = ""
            try: csV = xml_node.getElementsByTagName('csVersion')[0].childNodes[0].toxml()
            except: None
            return res, csV 
        return res
        
    def rebootDaemon(self, balancerIp=None, balancerPort=None, daemonType=None, daemonIp=None, daemonPort=None, id_command = 'restartDaemonId'):
        
        self.__connect()
                
        xml_file = "<methodCall><methodName>restartDaemon</methodName><params><login>%s</login><password>%s</password><user>%s</user><balancerIp>%s</balancerIp><balancerPort>%s</balancerPort><daemonType>%s</daemonType><daemonIp>%s</daemonIp><daemonPort>%s</daemonPort></params><id_command>%s</id_command></methodCall>" % (self.login, self.passwd, self.user, balancerIp, balancerPort, daemonType, daemonIp, daemonPort, id_command)

        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
                       
        if xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK':
            return True;
        return False

    def getBalancerStatistics(self, balancerIp, balancerPort, id_command = 'SDKBalancer'):
        
        self.__connect()
        
        import time
        time = str(time.time())
        xml_file = '<methodCall><methodName>getBalancerStatistics</methodName><params><login>%s</login><password>%s</password><user>%s</user><balancerIp>%s</balancerIp><balancerPort>%s</balancerPort></params><id_command>getBalancerStatistics%s%s</id_command></methodCall>' % (self.login, self.passwd, self.user, balancerIp, balancerPort, id_command, time)                
        
        self.__sendXml(xml_file)
        self.__sendSize(0)
        
        xml_node = self.__readXml()
        xml_txt = xml_node.toxml()
        
        if xml_node.getElementsByTagName('status')[0].firstChild.toxml() != '200 OK':
            return None;

        balancer = xml_node.getElementsByTagName('balancer')[0]
        faces = xml_node.getElementsByTagName('faces')[0].firstChild.toxml().split(',')
        statistics = xml_node.getElementsByTagName('statistics')[0].firstChild.toxml().split(',')
        identifications = xml_node.getElementsByTagName('identifications')[0].firstChild.toxml().split(',')
        
        return (faces, statistics, identifications)


    
    def setBalancerState(self, balancerIp=None, balancerPort=None, state=None, daemonip=None, daemonport=None, type=None,  id_command = 'SDKBalancer'):
        
        self.__connect()
        
        if state:
            str_state = "true"
        else:
            str_state = "false"
        if daemonip and daemonport and type:
            xml_file = "<methodCall><methodName>setDaemonState</methodName><params><login>%s</login><password>%s</password><user>%s</user><balancerIp>%s</balancerIp><balancerPort>%s</balancerPort><daemonIp>%s</daemonIp><daemonPort>%s</daemonPort><daemonType>%s</daemonType><stateUsed>%s</stateUsed></params><id_command>setDaemonState%s</id_command></methodCall>" % (self.login, self.passwd, self.user, balancerIp, balancerPort, daemonip, daemonport, type, str_state, id_command)
        else:
            xml_file = "<methodCall><methodName>setBalancerState</methodName><params><login>%s</login><password>%s</password><user>%s</user><balancerIp>%s</balancerIp><balancerPort>%s</balancerPort><stateUsed>%s</stateUsed></params><id_command>setBalancerState%s</id_command></methodCall>" % (self.login, self.passwd, self.user, balancerIp, balancerPort, str_state, id_command)        
        #xml_file = "<methodCall><methodName>restartDaemon</methodName><params><login>%s</login><password>%s</password><user>%s</user><balancerIp>%s</balancerIp><balancerPort>%s</balancerPort><daemonType>%s</daemonType><daemonIp>%s</daemonIp><daemonPort>%s</daemonPort></params><id_command>%s</id_command></methodCall>" % (self.login, self.passwd, self.user, balancerIp, balancerPort, daemonType, daemonIp, daemonPort, id_command)

        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
                       
        if xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK':
            return True;
        return False  
        
    def correlationTest(self, coeff=0.4):
        
        self.__connect()
                
        xml_file = "<methodCall><methodName>correlationTest</methodName><params><login>%s</login><password>%s</password><user>%s</user><coeff>%s</coeff></params><id_command>correlationTestIdCommand</id_command></methodCall>" % (self.login, self.passwd, self.user, coeff)

        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
                       
        if xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK':
            return True;
        return False

    def removeCamera(self, ip, type, id_command = 'restartDaemonId'):
        try:
            self.__connect()
                    
            xml_file = "<methodCall><methodName>removeCamera</methodName><params><login>%s</login><password>%s</password><user>%s</user><cameraIp>%s</cameraIp><cameraPort>%s</cameraPort></params><id_command>removeCamera%s</id_command></methodCall>" % (self.login, self.passwd, self.user, ip, type, id_command)        
    
            self.__sendXml(xml_file)
            self.__sendSize(0)
    
            xml_node = self.__readXml()
                           
            if xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK':
                return True;
        except:
            logging.exception("removeCamera: "+str(sys.exc_info()))
        return False
    
    def concatenatePersons(self, persons = [], id_command = 'concatenatePersons'):
        try:
            self.__connect()
                    
            xml_file = "<methodCall><methodName>concatenatePersons</methodName><params><login>%s</login><password>%s</password><user>%s</user><units></units></params><id_command>removeCamera%s</id_command></methodCall>" % (self.login, self.passwd, self.user, id_command)        

            xml_node = parseString(xml_file)
            
            xml_params = xml_node.getElementsByTagName("units")[0]
            
            for person in persons:
                node_str = '<unite>%s</unite>' % (person)
                xml_params.appendChild(parseString(node_str).firstChild)
    
            xml_file = xml_node.toxml()
    
            self.__sendXml(xml_file)
            self.__sendSize(0)
    
            xml_node = self.__readXml()
                           
            if xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK':
                return int(xml_node.getElementsByTagName('person_id')[0].firstChild.toxml())
        except:
            logging.exception("removeCamera: "+str(sys.exc_info()))
        return None        
        
    def registration(self, login="", password="", user="", full_name=""):
        self.__connect()
        
        if login == "" or password == "" or full_name == "": return False

        xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>registration</methodName><params><login>%s</login><password>%s</password><user>%s</user><fullName>%s</fullName></params><id_command>getRegistrationId</id_command></methodCall>' % (login, password, user, full_name)        
      #  logging.info(xml_file)
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
                       
        if xml_node.getElementsByTagName('status')[0].firstChild.toxml() != '200 OK':
            cause = xml_node.getElementsByTagName('status')
            if len(cause)>0: return cause[0].firstChild.toxml()
            return False;
       
        return True
    
    def calculateDistortion(self, lines, width, height, id_command = 'SDKBalancer'):
        
        self.__connect()
        
        xml_file = '<methodCall><methodName>lineDistortion</methodName><params><login>%s</login><password>%s</password><user>%s</user>%s<width>%s</width><height>%s</height><depth>10</depth></params><id_command>calculateDistortion%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, lines, width, height, id_command)

        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        status = None
        try:
            status = xml_node.getElementsByTagName('status')[0].firstChild.toxml()
        except:
            status = None
        
        if status:
            if status == "ERROR":
                return {"status": "error"}
            if status == "200 OK":
                try:
                    distortion = xml_node.getElementsByTagName('value')[0].firstChild.toxml().split(',')
                    return {"status": "success", "distortion": distortion}
                except:
                    return {"status": "error"}
        else:
            return {"status": "error"}
        #logging.info("sendXml: "+str(status))
        
        return {"status": "error"}


        
#        <methodResponse>
#<response>
#<status>200 OK</status>
#<balancers>
#<balancer>
#<port>16545</port>
#<sdQueue>0</sdQueue>
#<fsQueue>0</fsQueue>
#<address>192.168.0.142</address>
#<fdQueue>0</fdQueue>
#<active>true</active>
#<frQueue>0</frQueue>
#<daemons>
#<daemon>
#<port>15000</port><address>192.168.0.233</address><active>true</active><type>Face Detection Daemon</type>
#<total_memory_bytes>1609760768</total_memory_bytes><name>GeForce GTX 480</name><device>0</device><free_memory_bytes>520617984</free_memory_bytes>
#</daemon>
#<daemon><port>16002</port><address>192.168.0.233</address><active>true</active><type>Face Recognition Daemon</type></daemon>
#<daemon><port>17000</port><address>192.168.0.61</address><active>true</active><type>Fan Studio Daemon</type></daemon>
#<daemon><port>18000</port><address>192.168.0.142</address><active>true</active><type>Skin Detection Daemon</type></daemon>
#</daemons>
#</balancer>
#<balancer>
#<port>16545</port>
#<sdQueue>-4</sdQueue><!-- отрицательное значение означает либо отсутствие демона в настройках , либо неактивность всех подключенных демонов этого типа -->
#<fsQueue>-3</fsQueue>
#<address>192.168.0.233</address>
#<fdQueue>0</fdQueue>
#<active>true</active>
#<frQueue>0</frQueue>
#<daemons>
#<daemon><port>15000</port><address>192.168.0.233</address><active>true</active><type>Face Detection Daemon</type></daemon>
#<daemon><port>16002</port><address>192.168.0.233</address><active>true</active><type>Face Recognition Daemon</type></daemon>
#</daemons>
#</balancer>
#</balancers>
#</response>
#</methodResponse>
#Загрузка...
#
#        
#        return res 


    def executeMethodByName(self, name, params):
        func = {'getCameraParameter': self.getCameraParameter,
                'setCameraParameter': self.setCameraParameter,
                'setParameter': self.setParameter,
                'getParameter': self.getParameter,
                'saveCameras': self.saveCameras,
                'configureCameras': self.configureCameras,
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

#HOST = '192.168.0.142'
#PORT = 16544
#LOGIN = 'lLogin'
#PASSWD = 'pPassword'
#USER = 'qhaira'
#b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
#image_path = './aaa3.jpg'
#file = open(image_path, "r")
#data_image = file.read()
#file.close()
#print b.getPersons();
#print b.learning(data_image, "123")
#print b.getPersonPhoto("123", 9)
#print b.getPrewiew("123", 5)
#print b.deleting("123", 5)
#print b.recognize(data_image, 3)
#CMD_AUTO = [{'name':'distortion', 'param':'-0.02,0,0,0'}, {'name':'vignetting', 'param':'0.1,0,0,0'}, {'name':'shadows', 'param':''}, {'name':'sharp', 'param':''}, {'name':'curves', 'param':''}]
#print b.fanStudio(data_image, CMD_AUTO)  
#print b.faceDetect(data_image)
#CMD_FACE = []#[{'name':'face', 'param':'138.344025,259.367126,343.975952,230.145264,373.197815,435.776978,167.565872,464.998840,1,0.084476,0.266410,1,0.927741,0.275109,1,0.501368,0.644436,0,0.501761,1.172682,0'}]
#print 'percent', b.skinDetect(data_image, CMD_FACE)[0]
#CMD_RENAME = [{'name':'person_name', 'param':'oldName'}, {'name':'value', 'param':'newName'}]
#CMD_RENAME = [{'name':'person_name', 'param':'newName'}, {'name':'person_id', 'param':'203'}]
#print 'rename result', b.renamePerson(CMD_RENAME)
# DDUPP #
#print b.dduppProc(data_image, "123")
#print b.dduppSave(data_image, "123")
#print b.dduppTest(data_image)
#print b.dduppRemove("123")