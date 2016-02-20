# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

import threading
import socket
import sys, os
import string
from struct import pack, unpack
from cStringIO import StringIO
from xml.dom.minidom import parseString
from django.http import HttpResponse
from stringold import replace
from PIL import Image
from sim.models import *
from sim import util, settings

FS_HOST = settings.FS_HOST
FS_PORT = settings.FS_PORT
FS_LOGIN = settings.FS_LOGIN
FS_PASSWD = settings.FS_PASSWD
FS_USER = settings.FS_USER

class FanStudio():

    def readBytes(self, f, bytes):
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
    
    def face_detect(self, file_in, viewer, upload_file):
        out_codes = []
        
        image = Image.open(file_in)
        size_x, size_y = image.size 
        index_image = 0
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((FS_HOST, FS_PORT))

        xml_file = '<?xml version="1.0" encoding="UTF-8"?><request><login>%s</login><password>%s</password><type>facedetect</type><params><user>%s</user></params></request>' % (FS_LOGIN, FS_PASSWD, FS_USER)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()

        file = open(file_in, "r")
        data_file = file.read()
        spack = pack('>i', len(xml_file)) + pack('>i', len(data_file))
        s.send(spack)#send size
        s.send(xml_file)#send XML
        s.send(data_file)#send file
        
        df = s.recv(4)
        size_xml = unpack('>i', df)[0]
        
        df = s.recv(4)
        size_image = unpack('>i', df)[0]
        
        xml_file = self.readBytes(s, size_xml)
        img_file = self.readBytes(s, size_image)
            
        xml_node = parseString(xml_file)    
        xml_node = xml_node.getElementsByTagName("lines")[0]
        xml_lines = xml_node.childNodes        
        
        buffer = StringIO() # Убрать потом
        
        buffer.write('%s' % xml_file)
               
        for xml_line in xml_lines:
            text = xml_line.toxml()
            params = text.split(',')
            
            is_x = True
            x_min=10000
            x_max=0
            y_min=10000
            y_max=0
            
            i=0
            for param in params:
                if param.count('=') > 0:
                    param = param.split('=')[1]
                    
                param = int(param.split('.')[0])        
                    
                if is_x:
                    if param<x_min:
                        x_min = param
                    elif param>x_max:
                        x_max = param     
                else:
                    if param<y_min:
                        y_min = param
                    elif param>y_max:
                        y_max = param
                      
                is_x = not is_x    
                i = i+1
                if i==8:
                    break
            
            x_min_new = x_min - (x_max-x_min)/2 #Увеличиваем захват, берем больше фона
            if x_min_new<0:
                x_min_new=0
            x_max = x_max+x_min-x_min_new
            if x_max>size_x:
                x_max=size_x
            x_min=x_min_new                
            x_max = x_min+(x_max-x_min)/3*3
                                   
            if float(x_max-x_min)/3 > float(y_max-y_min)/4:
               add_len = (float(x_max-x_min)/3*4-(y_max-y_min))
               y_min = y_min-add_len/2
               y_max = y_max+add_len/2
               
               if y_min<0:
                   y_max = y_max-y_min
                   y_min=0
               
               if y_max>size_y:
                   y_max=size_y                    
                     
                     
            img1 = image.crop((x_min, y_min, x_max, y_max))
            size = 120, 160
            img1.thumbnail(size)
            index_image = index_image + 1
            code = gen_tmp_code()

            from sim.util import *
            import os.path
            dir_out = "%stmp/%s/" % (settings.MEDIA_ROOT, get_store_path(code))
            file_out = "%stmp/%s/%s" % (settings.MEDIA_ROOT, get_store_path(code), code)
            tmp_file = file_out+"_tmp"
            #file_out = settings.MEDIA_ROOT+"tmp/tmp"
            #loader = util.FileLoader(file_out)
            if not os.path.lexists( dir_out):
                os.makedirs( dir_out)
                                            

            f = open(tmp_file, 'w')
            img1.save(f, "JPEG")
            f.close()
            f = open(tmp_file, 'r')

            img2 = TmpImage(code = code, user = viewer)
            img2.image.save(code, File(f))
            img2.save()
            
            f.close()
            os.remove(tmp_file)


                        
            out = {}
            out['code'] = code
            
            out['url'] = util.get_absolute(img2.image.url, False)
            
            out_codes.append(out)
         
        return out_codes
    
    
    def recognize(self, file_in):
        out_codes = []
        
        image = Image.open(file_in)
        size_x, size_y = image.size 
        index_image = 0
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((FS_HOST, FS_PORT))
        
        xml_file = '<?xml version="1.0" encoding="UTF-8"?><request><login>%s</login><password>%s</password><type>recognize</type><params><user>%s</user></params></request>' % (FS_LOGIN, FS_PASSWD, FS_USER)
        xml_node = parseString(xml_file)
        xml_file = xml_node.toxml()
        
        file = open(file_in, "r")
        data_file = file.read()
        spack = pack('>i', len(xml_file)) + pack('>i', len(data_file))
        s.send(spack)#send size
        s.send(xml_file)#send XML
        s.send(data_file)#send file
        
        df = s.recv(4)
        size_xml = unpack('>i', df)[0]
        
        df = s.recv(4)
        size_image = unpack('>i', df)[0]
        
        xml_file = self.readBytes(s, size_xml)
        img_file = self.readBytes(s, size_image)
        xml_file = parseString(xml_file)
        xml_element = xml_file.getElementsByTagName("find")[0]
        
        text = xml_element.firstChild.toxml()

        return text
                

def test( request):
    f = FanStudio()
    str = f.face_detect('/home/dmitry/workspace/test/src/test/3.jpg') 
    print(str)
    return HttpResponse(str)   
