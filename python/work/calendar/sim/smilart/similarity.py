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
from sim.smilart.balancer import Balancer
from sim import fb
from sim.settings import FS_HOST, FS_PORT, FS_LOGIN, FS_PASSWD, FS_USER, face_size


class Similarity():

    def readBytes(self, f, bytes):
#        if bytes == 0:
#            return ''
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
        
        image = Image.open(file_in)
        size_x, size_y = image.size 
        
        file = open(file_in, "r")
        data_file = file.read()
        file.close()
        
        #b = Balancer(FS_HOST, FS_PORT, FS_LOGIN, FS_PASSWD, FS_USER)
        bal = Balancer(FS_HOST, FS_PORT, FS_LOGIN, FS_PASSWD, FS_USER)
        faces, images = bal.faceDetect(data_file)
                
        i=0
        out_codes = []
        while i<len(faces):
            x_min = int(min((faces[i]['face'][0], faces[i]['face'][2], faces[i]['face'][4], faces[i]['face'][6])))
            y_min = int(min((faces[i]['face'][1], faces[i]['face'][3], faces[i]['face'][5], faces[i]['face'][7])))
            x_max = int(max((faces[i]['face'][0], faces[i]['face'][2], faces[i]['face'][4], faces[i]['face'][6])))
            y_max = int(max((faces[i]['face'][1], faces[i]['face'][3], faces[i]['face'][5], faces[i]['face'][7])))
            i = i+1
            
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
#            size = 120, 160
            if face_size: img1.thumbnail(face_size)
            code = gen_tmp_code()

            from sim.util import *
            import os.path
            dir_out = "%s%stmp/%s/" % (settings.MEDIA_ROOT, settings.TMP_IMG, get_store_path(code))
            file_out = "%s%stmp/%s/%s" % (settings.MEDIA_ROOT, settings.TMP_IMG, get_store_path(code), code)
            tmp_file = file_out+"_tmp"
            
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
            
            out['url'] = util.get_absolute(img2.image.url)
#            out['url'] = util.get_absolute(fb.views.get_preview( "", img2.image.url, (120, 160)))
            
            out_codes.append(out)
        bal.close()
        del bal
        return out_codes
    
    
    def recognize(self, file_in, limit=100):
        
        file = open(file_in, "r")
        data_file = file.read()
        file.close()
        
        b = Balancer(FS_HOST, FS_PORT, FS_LOGIN, FS_PASSWD, FS_USER)
        #!!!
        res = b.recognize(data_file, limit)[0][0][1]
        b.close()
        del b
        return res
    
    def getNameById(self, id, name):
        bal = Balancer(FS_HOST, FS_PORT, FS_LOGIN, FS_PASSWD, FS_USER)
        res = bal.getPreview(id, name)[0]
        bal.close()
        del bal
        return res
        
    def comparePhotos(self, file_path1, file_path2):
        file = open(file_path1, "r")
        data_file1 = file.read()
        file.close()
        
        file = open(file_path2, "r")
        data_file2 = file.read()
        file.close()
        
        b = Balancer(FS_HOST, FS_PORT, FS_LOGIN, FS_PASSWD, FS_USER)
        res = b.compare(data_file1, data_file2)[0][0]
        b.close()
        del b
        return res
                

def test( request):
    f = FanStudio()
    str = f.face_detect('/home/dmitry/workspace/test/src/test/3.jpg') 
    print(str)
    return HttpResponse(str)   
