# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

import socket
from struct import pack, unpack
from cStringIO import StringIO
from xml.dom.minidom import parseString
import logging
MAX_READ_DATA = 10

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
#        if bytes == 0:
#            return ''
        buffer = StringIO()
        df = bytes
        while df > 0:
            if (df > 1024):
                s = self.sock.recv(1024)
            else :
                s = self.sock.recv(df)
            df = df - len(s)
            buffer.write(s)
            
        res=buffer.getvalue()
        buffer.close()
        #    print 'res:', res
        return res
    
    def __connect(self):
        if not self.connect:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    
    def joinRes(self, params):
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
        
    def __readSize(self):
        df = self.sock.recv(4)
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
        logging.info(data)
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
    
    def faceDetect(self, data_image, returnImage = False,  id_command = 'SDKBalancer'):
        
        self.__connect()
        
        xml_file = ''
        if not returnImage:
            xml_file = '<methodCall><methodName>facedetect</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>facedetect%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        else:
            xml_file = '<methodCall><methodName>facedetect</methodName><params><login>%s</login><password>%s</password><user>%s</user><cutting>0,0,2,400,400</cutting></params><id_command>facedetect%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendData(xml_file)
        
        self.__sendSize(1) # Количество передаваемых картинок
        self.__sendData(data_image)        
        
        xml_node = self.__readXml()
        images = self.__readImages()

        xml_node = xml_node.getElementsByTagName("faces")[0]
        xml_faces = xml_node.childNodes
        
        out = []
        for xml_face in xml_faces:
            out.append(self.__parsRes(xml_face.firstChild.toxml()))
                
        return (out, images)
    
    def faceDetect2(self, data_image, returnImage = False,  id_command = 'SDKBalancer'):
        
        self.__connect()
        
        xml_file = ''
        if not returnImage:
            xml_file = '<methodCall><methodName>facedetect</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>facedetect%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        else:
            xml_file = '<methodCall><methodName>facedetect</methodName><params><login>%s</login><password>%s</password><user>%s</user><cutting>0,0,2,400,400</cutting></params><id_command>facedetect%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendData(xml_file)
        
        self.__sendSize(1) # Количество передаваемых картинок
        self.__sendData(data_image)        
        
        xml_node = self.__readXml()
        images = self.__readImages()

        xml_node = xml_node.getElementsByTagName("faces")[0]
        xml_faces = xml_node.childNodes
        
        out = []
        for xml_face in xml_faces:
            out.append(xml_face.firstChild.toxml())
                
        return (out, images)
    
    def compare(self, data_image1, data_image2, id_command = 'SDKBalancer'):
        self.__connect()
        
        xml_file = '<methodCall><methodName>correlationTwoPhotos</methodName><params><login>%s</login><password>%s</password><user>%s</user></params><id_command>compare%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id_command)
        logging.info(xml_file)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendData(xml_file)
        self.__sendSize(2)
        self.__sendData(data_image1)
        self.__sendData(data_image2)
        
        xml_file = self.__readXml()
        images = self.__readImages()
        
        xml_coeff = xml_file.getElementsByTagName("coeff")
        xml_face1 = xml_file.getElementsByTagName("face1")
        xml_face2 = xml_file.getElementsByTagName("face2")
        
        out = ['0','','']
        
        if(len(xml_coeff)>0):
            out[0] = xml_coeff[0].firstChild.toxml()
        if(len(xml_face1)>0):
            out[1] = xml_face1[0].firstChild.toxml()
        if(len(xml_face2)>0):
            out[2] = xml_face2[0].firstChild.toxml()

        return (out, images)
            
    def recognize(self, data_image, limit = 10, params={}, id_command = 'SDKBalancer'):
        self.__connect()
        
        if "face" in params:
            xml_file = '<methodCall><methodName>identification</methodName><params><login>%s</login><password>%s</password><user>%s</user><face>%s</face><result_count>%d</result_count></params><id_command>recognize%s</id_command></methodCall>' % (self.login, self.passwd, self.user, self.__joinRes(params), limit, id_command)
        else:
            xml_file = '<methodCall><methodName>identification</methodName><params><login>%s</login><password>%s</password><user>%s</user><result_count>%d</result_count></params><id_command>recognize%s</id_command></methodCall>' % (self.login, self.passwd, self.user, limit, id_command)
        logging.info(xml_file)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
#        print xml_file
        
        self.__sendData(xml_file)
        
        self.__sendSize(1)
        self.__sendData(data_image)
        
        xml_file = self.__readXml()
        images = self.__readImages()
        
#        print xml_file.toxml()
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
                try:
                    name = ''
                    if(xml_person_name and len(xml_person_name)>i and xml_person_name[i].firstChild):
                        name = xml_person_name[i].firstChild.toxml()
                    res_sim.append({
                                'id': xml_person_id[i].firstChild.toxml(), 
                                'name': name,
                                'image': xml_name_photo[i].firstChild.toxml(), 
                                'rang': float(xml_k[i].firstChild.toxml()), 
                    }) 
                except:
                    None;
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
        
        self.__sendData(xml_file)
        
        self.__sendSize(1)
        self.__sendData(data_image)
        
        xml_file = self.__readXml()
        images = self.__readImages()
        return images
    
    def learning(self, data_image, id, id_command = 'SDKBalancer'):
        
        self.__connect()
        
        xml_file = '<methodCall><methodName>learning</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_name>%s</person_name></params><id_command>learning%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id, id_command)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendData(xml_file)
       
        self.__sendSize(1)
        self.__sendData(data_image)

        xml_node = self.__readXml()
        
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
            
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        self.__sendData(xml_file)
        self.__sendSize(0)
        
        xml_node = self.__readXml()
        
        return xml_node.getElementsByTagName('status')[0].firstChild.toxml() == '200 OK'
    
    def getPreview(self, id, num, id_command = 'SDKBalancer'):
        self.__connect()
        
        xml_file = '<methodCall><methodName>getpreview</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_id>%s</person_id><name_photo>%s</name_photo></params><id_command>getPreview%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id, num, id_command)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendData(xml_file)
        self.__sendSize(0)
        
        xml_node = self.__readXml()
        namePerson = xml_node.getElementsByTagName('person_name')[0].firstChild.toxml()
        
        images = self.__readImages()
        return (namePerson, images)
    
    def getPersonPhoto(self, id, num, id_command = 'SDKBalancer'):
        self.__connect()
                
        xml_file = '<methodCall><methodName>getpersonphoto</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_id>%s</person_id><name_photo>%s</name_photo></params><id_command>getPersonPhoto%s</id_command></methodCall>' % (self.login, self.passwd, self.user, id, num, id_command)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendData(xml_file)
        self.__sendSize(0)
        
        xml_file = self.__readXml()
        images = self.__readImages()
        
        return images    
        
    def getPersonPhotos(self, id, id_command = 'SDKBalancer'):
        
        self.__connect()
                
        xml_file = '<methodCall><methodName>getpersonphotos</methodName><params><login>%s</login><password>%s</password><user>%s</user><person_id>%s</person_id></params><id_command>getPersonPhotos%s</id_command></methodCall>'  % (self.login, self.passwd, self.user, id, id_command)
        
        self.__sendData(xml_file)
        self.__sendSize(0)
        
        xml_node = self.__readXml()
        
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
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        self.__sendData(xml_file)
        self.__sendSize(0)

        xml_node = self.__readXml()
        
        ids = xml_node.getElementsByTagName('persons_ids')[0].firstChild.toxml().split(';')
        names = xml_node.getElementsByTagName('persons_names')[0].firstChild.toxml().split(';')
        photos = xml_node.getElementsByTagName('photos')[0].firstChild.toxml().split(';')
        
        return (ids, names, photos)    
        

#HOST = '192.168.0.237'
#PORT = 6544
#LOGIN = 'lLogin'
#PASSWD = 'pPassword'
#USER = 'haira'
#b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
#image_path = '/home/dmitry/workspace/test/src/test/j.jpg'
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
