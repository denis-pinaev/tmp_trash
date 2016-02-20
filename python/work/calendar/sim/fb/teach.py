#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import floor, asin 
import logging
import os, sys
import socket
import string
import re
#import sim
from ctypes import ARRAY

#HOST = '192.168.0.55'
#PORT = 6300
HOST = '192.168.0.61'#237'
PORT = 16544
imgPath = '/home/srv/www/vhosts/uni.gale.ru/www/files/media/photos.uni/'

class QPoint:
    x = 0
    y = 0
    def __init__(self, x=0, y=0):
        self.x = x;
        self.y = y;
class Face:
    def __init__(self):  
        self.name      = ''
        self.string    = ''             
        self.kFace     = 0.0
        self.topLeft   = QPoint()
        self.topRight  = QPoint()
        self.botLeft   = QPoint()
        self.botRight  = QPoint()
        #self.faceRect  = QRect()
        self.kChin     = 0.0
        self.chin      = QPoint()
        self.kNose     = 0.0
        self.nose      = QPoint()
        self.kLeftEye  = 0.0
        self.leftEye   = QPoint()
        self.kRightEye = 0.0
        self.rightEye  = QPoint()

class Client:
    
    def __init__(self):
        pass
        
    def readBytes(self, f, bytes):
        from cStringIO import StringIO
        if bytes == 0:
            return ''
        buffer = StringIO()
        df = bytes
        while df > 0:
            if (df > 1024):
                s = f.recv(1024)
            else :
                s = f.recv(df)
            df = df - len(s)
            buffer.write(s)
            
        res=buffer.getvalue()
        buffer.close()
        #    print 'res:', res
        return res    
        
    def trainPerson(self, frame, id):
        #print '================== learning ====================='
        from xml.dom.minidom import parseString
        from struct import pack, unpack
        
        if self.connect():            
            return
        
        xml_file = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>learning</methodName><params><login>lLogin</login><password>pPassword</password><user>univer</user><person_name>%s</person_name></params><id_command>learningWithoutFace</id_command></methodCall>' % id
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()

        spack = pack('>i', len(xml_file))  
        self.socket.send(spack)         
        self.socket.send(xml_file) 
        
        spack = pack('>i', 1)
        self.socket.send(spack)
        
        spack = pack('>i', len(frame))
        self.socket.send(spack)
        self.socket.send(frame)
        
        df = self.socket.recv(4)
        size_xml = unpack('>i', df)[0]
        
        xml_file = self.readBytes(self.socket, size_xml)
        
        self.disconnect()
        
        xml_node = parseString(xml_file)
        if len(xml_node.getElementsByTagName('name_photo')) == 0 or xml_node.getElementsByTagName('name_photo')[0].firstChild == None:
            return 'error'
        else:
            photo = xml_node.getElementsByTagName('name_photo')[0].firstChild.toxml()
            while len(photo)<4:
                photo = '0%s'%(photo)
            return photo
            
        #print '====================================================' 
        
    def connect(self):   
        #print 'Connecting to server!'   
        #try:        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)               
        self.socket.connect((HOST, PORT))
        #except socket.error, message:
        #    print message 
        #    return 1
            
        #if self.sendInitialRequest():
        #    return 1
        
        return 0    
        
    def disconnect(self):
        #print 'Close connection!'
        self.socket.close()       
        
    def sendInitialRequest(self):
        #print 'Sending initial request!'                                                              
        self.socket.send("login admin")
        data = self.socket.recv(1024)
        #print 'login: ' + data
        if data != 'ok':            
            return 1
            
        self.socket.send("password lthtdj")
        data = self.socket.recv(1024)
        #print 'password: ' + data
        if data != 'ok':
            return 1
        
        return 0
        
    def parseFace(self, rect):
        face = Face()
        face.string = string.join(rect, ',')
            
        dxx = float(rect[2]) - float(rect[0])
        dyx = float(rect[6]) - float(rect[0])
        
        dxy = float(rect[3]) - float(rect[1])
        dyy = float(rect[7]) - float(rect[1])
                
        face.topLeft   = QPoint(float(rect[0]), float(rect[1]))
        face.topRight  = QPoint(float(rect[2]), float(rect[3]))
        face.botLeft   = QPoint(float(rect[6]), float(rect[7]))
        face.botRight  = QPoint(float(rect[4]), float(rect[5]))
        
        face.leftEye  = QPoint(float(rect[0]) + dxx*float(rect[9]) + dyx*float(rect[10]), float(rect[1])+ dxy*float(rect[9]) + dyy*float(rect[10]))
        face.rightEye = QPoint(float(rect[0]) + dxx*float(rect[12]) + dyx*float(rect[13]), float(rect[1])+ dxy*float(rect[12]) + dyy*float(rect[13]))
        face.nose     = QPoint(float(rect[0]) + dxx*float(rect[15]) + dyx*float(rect[16]), float(rect[1])+ dxy*float(rect[15]) + dyy*float(rect[16]))
        face.chin     = QPoint(float(rect[0]) + dxx*float(rect[18]) + dyx*float(rect[19]), float(rect[1])+ dxy*float(rect[18]) + dyy*float(rect[19]))
        
        face.kFace = float(rect[8])
        face.kLeftEye = float(rect[11])
        face.kRightEye = float(rect[14])
        face.kNose = float(rect[17])
        face.kChin = float(rect[20])
        
        return face
        
    def getFaceDetected(self, frame): 
        self.faces = []        
        
        #print '================== detection =====================' 
        if self.connect():            
            return self.faces
        self.socket.send("action facedetect")
        data = self.socket.recv(1024)
        #print 'facedetect: ' + data
        if data != 'ok':
            return self.faces
                    
        self.socket.send("image size %s" % str(len(frame)))
        data = self.socket.recv(1024)
        #print 'size: ' + data
        if data != 'ok':
            return self.faces
        
        self.socket.send(frame)
        data = self.socket.recv(1024)
        #print 'image: ' + data 
        if data != 'ok':
            return self.faces
        
        self.socket.send("get result")
        data = self.socket.recv(1024)
        data = data.replace('\x00', '')
        if data == '':
            return self.faces
        #print 'result: ' + data
        
        rect = data.split(',')
        face = self.parseFace(rect)

        self.disconnect()
        #print '====================================================' 

        return face  


images = []
client = Client()
logfile = imgPath+'log.txt'

def testAll(images, id):
    for f in images:
        print f
        if f.count('noface'): continue
        with open(f,'r') as img:
            data = img.read()
            img.close()
            retFile = client.trainPerson(data, id)
            newpath = f[:-8]
            oldname = f[-8:-4]
            if retFile == 'error':
                retFile = '%s%s'%(oldname,'_noface_0x0')
	    newpath = '%s%s%s'%(newpath,retFile,'.jpg')
	    printStr = 'ok'
            if not retFile == oldname:
        	os.rename(f, newpath)
		printStr = '%s%s%s%s'%('rename ',oldname, ' to ', retFile)
	    print printStr
	    if logfile:
		log = open(logfile, 'a+')
		log.write('%s : %s%s'%(f,printStr,'\n'))
		log.close()
        
def bufAll(path):
    for f in os.listdir( path):
        if len(f) != 8:
            continue
        filename = "%s/%s" % (path, f)
        if os.path.isdir(filename):
            bufAll(filename)
            continue
        images.append( filename)

def learnPerson(person_id):
    global images
    images = []
    path = imgPath + person_id
    bufAll(path)
    images.sort()
    testAll(images, person_id)
    
def learnAllPersons(start = 0):
    path = imgPath
    counter = start
    for id in sorted(os.listdir(path))[start:]:
        if logfile:
	    log = open(logfile, 'a+')
	    print('%s : %s'%(str(counter),id))
	    log.write('%s : %s%s'%(str(counter),id,'\n'))
	    log.close()
	counter+=1
        learnPerson(id)
    
learnAllPersons(0)
#learnPerson('Yuri__Kutsenko')
