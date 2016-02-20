from __future__ import with_statement
import socket
import os
import string
import sys
import threading
from wizer.faces import conf
from wizer.faces.util import gen_filename
from wizer import settings
import logging, traceback, pprint


def parse_results( string):
    sarr = string.split(',')
    del sarr[9:] #last "," - empty element
    results = map(float, sarr)
    return results

def process( path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((conf.FD_HOST, conf.FD_PORT))

    s.send("login " + conf.FD_LOGIN)
    data = s.recv(self.MAX_RES)
    if data != self.OK:
        raise RuntimeError(data)

    s.send("password " + conf.FD_PASSWD)
    data = s.recv(self.MAX_RES)
    if data != self.OK:
        raise RuntimeError(data)

    command_detect = "action facedetect"
    if is_mask:
        command_detect = "action skindetect"
    s.send( command_detect)

    data = s.recv(self.MAX_RES)
    if data != self.OK:
        raise RuntimeError( data)
 
    file = open(path, "r")
    data_file = file.read()
    file.close()

    s.send( "image size " + str(len(data_file)))
    data = s.recv(self.MAX_RES)
    if data != self.OK:
        raise RuntimeError(data)

    s.send( data_file)
    data = s.recv(self.MAX_RES)
    if data != self.OK:
        raise RuntimeError(data)

    command_detect = "get result"
    s.send(command_detect)

    result = s.recv(self.MAX_RES)
    source_mask = None

    s.close()

    return self.parse_results(result)
