# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

import threading
import socket
import sys, os
import md5

#HOST = '127.0.0.1'
HOST = '10.0.1.1'
#PORT = 9110
PORT = 9100

login = "admin"
password = "lthtdj"

def get_similar( fname):
    data = ""
#    try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT)) 

    s.send("login "+login)
    data = s.recv(1024)

    s.send("password "+password)
    data = s.recv(1024)

    s.send("action similar")
    data = s.recv(1024)

    file = open(fname, "r")
    data_file = file.read()
    s.send("image size "+str(len(data_file)))
    data = s.recv(1024)
	
    s.send(data_file)
    data = s.recv(1024)
	
    s.send("get result")
    data = s.recv(1024)
	
    s.close()
#    except:
#	return ""

    return data
    
print get_similar(''.join( [os.path.dirname(os.path.abspath(__file__)), '/1.jpg']))