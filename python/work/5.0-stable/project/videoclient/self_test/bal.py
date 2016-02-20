# -*- encoding: utf-8 -*-

import socket
from struct import pack, unpack
from cStringIO import StringIO
from xml.dom.minidom import parseString
import logging
import sys

import time

log_self_test = logging.getLogger('kpp.slog_self_test')

MAX_READ_DATA = 10
TIME_OUT = 40.0

def checkFloatParam( results, xml_node, name):
    xml_times = xml_node.getElementsByTagName(name)
    if len(xml_times) == 0:
        return
    xml_time = xml_times[0]
    time = float(xml_time.firstChild.toxml())
    results[name] = time
#    print name, time

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
    
    def __del__(self):
        self.__disconnect()
        
    def __readBytes(self, bytes):
        if bytes == 0:
            return ''
        buffer = StringIO()
        df = bytes
        self.sock.settimeout(TIME_OUT)
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
        #    print 'res:', res
        return res
    
    def __connect(self):
        if not self.connect:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            log_self_test.info((self.host, self.port))
            self.sock.connect((self.host, self.port))
            self.connect = True
            
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
        
        params = self.__toFloat(text.split(','));
        
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
        data = data.encode("utf-8")
        #print data
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
        log_self_test.info(data)
#        print data
        return parseString(data)
    
    def __readImages(self):
        log_self_test.info("readImages")
        cnt = self.__readSize()
        log_self_test.info(cnt)
        images = []
        i=0
        while i<cnt:
            img_file = self.__readData()
            images.append(img_file)
            i = i+1
        return images
    
    def faceDetect(self, data_image, id_command = 'SDKBalancer'):
        
        self.__connect()
        addFocus = 'false'
        addNoise = 'false'
        addStdDev = 'false'
        addHisto = 'false'
        deep = 0
        xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>facedetect</methodName><params><fdAngle>0</fdAngle><eyes_distance>0</eyes_distance><fdPreprocessingMinFaceSidePixels>0</fdPreprocessingMinFaceSidePixels><statistics/><addNoiseFactor>%s</addNoiseFactor><addFocusFactor>%s</addFocusFactor><addNoiseStdDev>%s</addNoiseStdDev><addHistogram>%s</addHistogram><detectType>light</detectType><login>%s</login><password>%s</password><user>%s</user><deep_level>%s</deep_level></params><id_command>facedetectCommandID</id_command></methodCall>' % ( addNoise, addFocus, addStdDev, addHisto, self.login, self.passwd, self.user, deep)
#        xml_file = '<methodCall><methodName>facedetect</methodName><params><login>%s</login><password>%s</password><user>%s</user><detectType>light</detectType></params><id_command>facedetect%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        log_self_test.info(xml_file)
        self.__sendXml(xml_file)
        log_self_test.info("send xml")
        self.__sendSize(1) # Количество передаваемых картинок
        log_self_test.info("send count picture")
        self.__sendData(data_image)
        log_self_test.info("send data")
        
        xml_doc = self.__readXml()
        log_self_test.info("read xml")
        images = self.__readImages()
        log_self_test.info("read images")
        
        res = xml_doc.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        result = {}        
        xml_node = xml_doc.getElementsByTagName("info")[0]
        checkFloatParam( result, xml_node, "detectDaemonTime")
        checkFloatParam( result, xml_node, "detectTotalTime")
        checkFloatParam( result, xml_node, "detectDaemonTimeProc")
        checkFloatParam( result, xml_node, "detectDaemonTimeCS")
        
        if not res: return ([], images, result)
        
        xml_node = xml_doc.getElementsByTagName("faces")[0]
        xml_faces = xml_node.childNodes
        log_self_test.info("xml")
        out = []
        for xml_face in xml_faces:
            out.append(self.__parsRes(xml_face.firstChild.toxml()))
        log_self_test.info("for xml")
        
                                                                                                                                                                                                                        
        return (out, images, result)         
    
    def recognize(self, data_image, limit = 10, params={}, id_command = 'SDKBalancer'):
        timework = time.time()
        self.__connect()
        
        addFocus = 'false'
        addNoise = 'false'
        addStdDev = 'false'
        addHisto = 'false'
        deep = 0
        """
        if "face" in params:
            xml_file = '<methodCall><methodName>identification</methodName><params><login>%s</login><password>%s</password><user>%s</user><face>%s</face><detectType>light</detectType><result_count>%d</result_count></params><id_command>recognize%s</id_command></methodCall>' % (self.login, self.passwd, self.user, self.__joinRes(params), limit, id_command)
        else:
            xml_file = '<methodCall><methodName>identification</methodName><params><login>%s</login><password>%s</password><user>%s</user><detectType>light</detectType><result_count>%d</result_count></params><id_command>recognize%s</id_command></methodCall>' % (self.login, self.passwd, self.user, limit, id_command)
        """
#        print params
        if "eyes" in params:
            xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>identification</methodName><params><eye>%s</eye><fdAngle>0</fdAngle><eyes_distance>0</eyes_distance><fdPreprocessingMinFaceSidePixels>0</fdPreprocessingMinFaceSidePixels><statistics/><addNoiseFactor>%s</addNoiseFactor><addFocusFactor>%s</addFocusFactor><addNoiseStdDev>%s</addNoiseStdDev><addHistogram>%s</addHistogram><detectType>light</detectType><login>%s</login><password>%s</password><user>%s</user><deep_level>%s</deep_level><result_count>1</result_count></params><id_command>identificationCommandID</id_command></methodCall>' % (params["eyes"], addNoise, addFocus, addStdDev, addHisto, self.login, self.passwd, self.user, deep)
        else:
            xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>identification</methodName><params><fdAngle>0</fdAngle><eyes_distance>0</eyes_distance><fdPreprocessingMinFaceSidePixels>0</fdPreprocessingMinFaceSidePixels><statistics/><addNoiseFactor>%s</addNoiseFactor><addFocusFactor>%s</addFocusFactor><addNoiseStdDev>%s</addNoiseStdDev><addHistogram>%s</addHistogram><detectType>light</detectType><login>%s</login><password>%s</password><user>%s</user><deep_level>%s</deep_level><result_count>1</result_count></params><id_command>identificationCommandID</id_command></methodCall>' % ( addNoise, addFocus, addStdDev, addHisto, self.login, self.passwd, self.user, deep)

#        print(xml_file)
        self.__sendXml(xml_file)
        
        self.__sendSize(1)
#        log_self_test.info(len(data_image))
        self.__sendData(data_image)
        
        xml_doc = self.__readXml()
        images = self.__readImages()
#        print 'xml_doc=',xml_doc.toxml()
        xml_persons = xml_doc.getElementsByTagName("person")
        
        out = []
        for xml_person in xml_persons:
            
            xml_face = xml_person.getElementsByTagName("face")[0]
            res_face = None
            if xml_face != None:
                if xml_face.firstChild != None:
                    res_face = self.__parsRes(xml_face.firstChild.toxml())
            
            xml_person_id = xml_person.getElementsByTagName("person_id")
            xml_person_name = xml_person.getElementsByTagName("person_name")
            xml_name_photo = xml_person.getElementsByTagName("name_photo")
            xml_k = xml_person.getElementsByTagName("k")
            
            i=0
            res_sim = []
            while i<len(xml_person_id):
                if xml_person_id[i].firstChild:
                   res_sim.append({'id': xml_person_id[i].firstChild.toxml() if xml_person_id[i].firstChild else None, 
                                'name': xml_person_name[i].firstChild.toxml() if xml_person_name[i].firstChild else None,
                                'image': xml_name_photo[i].firstChild.toxml() if xml_name_photo[i].firstChild else None, 
                                'rang': float(xml_k[i].firstChild.toxml()) if xml_k[i].firstChild else 0, }) 
                i = i+1
           
            out.append((res_face, res_sim))

        result = {"scriptTime": time.time()-timework}
        xml_node = xml_doc.getElementsByTagName("info")[0]
        checkFloatParam( result, xml_node, "detectDaemonTime")
        checkFloatParam( result, xml_node, "detectTotalTime")
        checkFloatParam( result, xml_node, "detectDaemonTimeProc")
        checkFloatParam( result, xml_node, "detectDaemonTimeCS")
        checkFloatParam( result, xml_node, "recognitionDaemonTime")
        checkFloatParam( result, xml_node, "recognitionDaemonTimeProc")
        checkFloatParam( result, xml_node, "recognitionTotalTime")
        checkFloatParam( result, xml_node, "recognitionDaemonTimeCS")
        return (out, images, result)

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
    
    def learning(self, data_image, id, params={}, id_command = 'SDKBalancer'):
        log_self_test.info("learning")
        log_self_test.info(id)
        self.__connect()
         
        if "face" in params:
            xml_file = '<methodCall><methodName>learning</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_name>%s</person_name><face>%s</face><detectType>light</detectType></params><id_command>learning%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id, self.__joinRes(params), id_command)
        else:
            xml_file = '<methodCall><methodName>learning</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_name>%s</person_name><minBoundCoeffForLearn>0</minBoundCoeffForLearn><maxBoundCoeffForLearn>1</maxBoundCoeffForLearn><detectType>light</detectType></params><id_command>learning%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id, id_command)      
        print(xml_file)
        self.__sendXml(xml_file)
       
        self.__sendSize(1)
        self.__sendData(data_image)

        xml_node = self.__readXml()
        xml_txt = xml_node.toxml()
#        print xml_txt
        
        if (len(xml_node.getElementsByTagName('person_id'))>0):
            return {'id':xml_node.getElementsByTagName('person_id')[0].firstChild.toxml(),
                    'photo_name':xml_node.getElementsByTagName('name_photo')[0].firstChild.toxml(),
                    'person_name':xml_node.getElementsByTagName('person_name')[0].firstChild.toxml(),}
        
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
    
    
    def getCameraParameter(self, source, type, param = 'distortion', id_command = 'SDKBalancer'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>getcameraparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><source>%s</source><type>%s</type><parameter>%s</parameter></params><id_command>getCameraParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, source, type, param, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('value')[0].firstChild.toxml().split(',')
        
        return res
    
    def setCameraParameter(self, source, type, p1, p2, p3, p4, param = 'distortion', id_command = 'SDKBalancer'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>setcameraparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><source>%s</source><type>%s</type><parameter>%s</parameter><value>%s,%s,%s,%s</value></params><id_command>setCameraParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, source, type, param, p1, p2, p3, p4, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        
        return res
    
    def setParameter(self, value, param = 'eyes_distance', id_command = 'SDKBalancer'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>setparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><parameter>%s</parameter><value>%s</value></params><id_command>setParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, param, value, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        
        return res
    
    def getParameter(self, param = 'eyes_distance', id_command = 'SDKBalancer'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>getparameter</methodName><params><login>%s</login><password>%s</password><user>%s</user><parameter>%s</parameter></params><id_command>getParameter%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, param, id_command)
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('value')[0].firstChild.toxml()
        
        return res    
    
    def saveCameras(self, id_command = 'SDKBalancer'):
       
        self.__connect()

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
    
    def dduppProc(self, data_image, brief=0, dduppDups=1, dduppMode=0, report=0, id_command = 'SDKBalancer'):
        self.__connect()

        xml_file = '<methodCall><methodName>dduppProc</methodName><params><login>%s</login><password>%s</password><user>%s</user><duppDupps>%s</duppDupps><duppLoose>2</duppLoose><duppFlips>1</duppFlips><duppCw90s>1</duppCw90s><duppCrops>6</duppCrops><duppMode>%s</duppMode><brief>%s</brief><report>%s</report></params><id_command>dduppProc%s</id_command></methodCall>' % (self.login, self.passwd, self.user, dduppDups, dduppMode, brief, report, id_command)
        log_self_test.info(xml_file)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendXml(xml_file)
        
        self.__sendSize(1) # Количество передаваемых картинок
        self.__sendData(data_image)
        
        xml_node = self.__readXml()
        images = self.__readImages()

        status = xml_node.getElementsByTagName("status")[0].firstChild.toxml()
        result = None
        log_self_test.info(status)
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

        return (result, images)    

    def dduppTest(self, data_image, dduppCoeff=0.5, dduppDups=1, dduppMode=0, dduppLoose=2, dduppDupps=10, report=0, id_command = 'SDKBalancer'):
        self.__connect()

        xml_file = '<methodCall><methodName>dduppTest</methodName><params><login>%s</login><password>%s</password><user>%s</user><duppCoeff>%s</duppCoeff><duppDupps>%s</duppDupps><duppFlips>1</duppFlips><duppCw90s>1</duppCw90s><duppLoose>%s</duppLoose><duppMode>%s</duppMode><duppReport>%s</duppReport></params><id_command>dduppTest%s</id_command></methodCall>' % (self.login, self.passwd, self.user, dduppCoeff, dduppDupps, dduppLoose, dduppMode, report, id_command)
        log_self_test.info(xml_file)
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
                known_brief = []
                for i in range(l):
                    coeff = xml_coeff[i].firstChild.toxml()
                    brief = xml_brief[i].firstChild.toxml()
                    old_quad = xml_old_quad[i].firstChild.toxml()
                    new_quad = xml_new_quad[i].firstChild.toxml()                    
                    if not brief in known_brief:                 
                        result.append({"coeff": coeff, "brief": brief, "old_quad": old_quad, "new_quad": new_quad, "count":1})       
                        known_brief.append(brief)
                    else: 
                        f = filter(lambda x: x["brief"]==brief, result)    
                        f[0]["count"] += 1
                        
        log_self_test.info("ddupp "+str( result))
        return (result, images)

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
        log_self_test.info(xml_file)
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
    
    
    def getSystemInfo(self, id_command = 'SDKBalancer'):
        
        self.__connect()
                
        xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>getSystemInfo</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>getSystemInfo%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)                
        
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
                       
        if xml_node.getElementsByTagName('status')[0].firstChild.toxml() != '200 OK':
            return None;
       
        res = []
        res = self.recursXml(xml_node.getElementsByTagName('balancers')[0])
        return res
        
    def registration(self, login="", password="", user="", full_name=""):
        self.__connect()
        
        if login == "" or password == "" or full_name == "": return False

        xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>registration</methodName><params><login>%s</login><password>%s</password><user>%s</user><fullName>%s</fullName></params><id_command>getRegistrationId</id_command></methodCall>' % (login, password, user, full_name)        
        log_self_test.info(xml_file)
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
                       
        if xml_node.getElementsByTagName('status')[0].firstChild.toxml() != '200 OK':
            cause = xml_node.getElementsByTagName('status')
            if len(cause)>0: return cause[0].firstChild.toxml()
            return False;
       
        return True
    
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
        log_self_test.info(xml_file)
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
    
    def getAllParameters(self, id_command = 'getLoginsCommandId'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>getAllParameters</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id_command)
        log_self_test.info(xml_file)
        self.__sendXml(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        res = xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
        blist = []
        if res:
            bases = xml_node.getElementsByTagName("bases")[0].childNodes    
            i = 0
            for base in bases:
                base = base.childNodes
                blist.append({"name": i, "params": []})
                log_self_test.info(base[0].firstChild.toxml())
                if base[0].tagName == "baseName": blist[i]["name"] = base[0].firstChild.toxml()
                if base[1].tagName == "parameters":
                    bparams = []
                    for p in base[1].childNodes:
                        bparams.append({"name": p.tagName, "val": p.firstChild.toxml() if p.firstChild else None})
                    blist[i]["params"] = bparams      
                i += 1                          
        return blist                 
        
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