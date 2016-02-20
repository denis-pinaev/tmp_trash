#!/usr/bin/env python

# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

from threading import Thread
import socket
import sys, os
import json
import datetime
import random
import shutil
import time
import re
import logging
LOCAL_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join( LOCAL_DIR, '../'))

from bal import Balancer
import loggers

log_self_test = logging.getLogger('kpp.slog_self_test')
if not hasattr(log_self_test, 'vFHandle'):
    PROJECT_ROOT = os.path.join(LOCAL_DIR, '../../../')
    all_loggers = loggers.LoggingConfig(PROJECT_ROOT, DEBUG=True)
    log_self_test = all_loggers.getSelfTestLogger()

#HOST = '192.168.0.236'
LOGIN = 'lLogin'
PASSWD = 'pPassword'
#USER = 'oxion_lightdefault'
USER = 'test_FRFD'

DAEMON = 'FR'



import sys
params = sys.argv[1:]
if len(params)>0:
    INPUT_DIR = os.path.join(params[0], 'faces/')
    FACES_RESAULT = os.path.join(params[0], 'resault.json')
else:
    INPUT_DIR = './faces/'
    FACES_RESAULT = './resault.json'
if len(params)>=3:    
    MAX_ITERATION = int(params[1])
    MAX_THREAD = int(params[2])
else:
    MAX_ITERATION = 2
    MAX_THREAD = 2
    
if len(params)>=5:    
    HOST = str(params[3])
    PORT = int(params[4])
else:    
    HOST = '192.168.0.55'
    PORT = 16544
    
stat_params = ["detectDaemonTime", "detectTotalTime", "detectDaemonTimeProc", "detectDaemonTimeCS", "recognitionDaemonTime", "recognitionDaemonTimeProc", "recognitionTotalTime", "recognitionDaemonTimeCS", "scriptTime"]
stat_min = {}
stat_max = {}
stat_time = {}
for p in stat_params:
    stat_min[p] = 1000
    stat_max[p] = 0
    stat_time[p] = 0
#cface = 0
tST = 0
cimage = 0
learnimage = 0

def get_format_file(fname):
    try:
        ref = re.compile(".*\.([^.]+)$")
        m = ref.match(fname)
        if (m and m.group(1)):
            return m.group(1).lower()
        return ""
    except:
#        print sys.exc_info()
        return ""

def parse_txt_data(data_txt):
    d1 = data_txt[12].split(" ")
    d2 = data_txt[15].split(" ")
    return "%s,%s,%s,%s" % (d1[0], d1[1].replace("\r\n", ""), d2[0], d2[1].replace("\r\n", ""))

def  get_faces(file_name):
    try:
        format = get_format_file(file_name)
        txt_file = "%stxt" % (file_name[:-len(format)])
        if os.path.exists(txt_file):
            file = open(txt_file, "r")
            data_txt = file.readlines()
            file.close()
            return {"eyes": parse_txt_data(data_txt)}
    except: print sys.exc_info()
    return {}

def get_detect(file_name, c=1, ti=-1):
    global cface, cimage, tST, stat_params, stat_max, stat_time, learnimage
    j = 0
    for i in xrange(c):
        #print file_name
        file = open(file_name, "r")
        data_image = file.read()
        file.close()

        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        try:
            if DAEMON == "FR" :
                t1 = time.time()
                r = b.recognize(data_image, params=get_faces(file_name))
                t2 = time.time()
            else:
                t1 = time.time()
                r = b.faceDetect(data_image)
                t2 = time.time()
        except:
            print(sys.exc_info())
            continue
#        cface += len(r[0])
        t = t2-t1
        tST += t
#        if r[2].get('recognitionDaemonTimeProc', 0) == 0: continue
        cimage += 1
        #print r[2].get('detectDaemonTime', 0), r[2].get('detectDaemonTimeProc', 0), r[2].get('detectDaemonTimeCS', 0), r[2].get('detectTotalTime', 0), r[2].get('recognitionDaemonTime', 0), r[2].get('recognitionDaemonTimeProc', 0), r[2].get('recognitionDaemonTimeCS', 0), r[2].get('recognitionTotalTime', 0), t
        for p in stat_params:
            t = r[2].get(p, 0)
            if t:
                stat_time[p] += t
                stat_max[p] = max(stat_max[p], t)
                stat_min[p] = min(stat_min[p], t)
        j += 1
        b.close()

def get_stat(file_dir, ti=-1, max_thread = MAX_THREAD, max_iteration = MAX_ITERATION):
    lst = os.listdir(file_dir)
    m = len(lst)
    i = 0
    global t_all, tDT, tDTP, tTT, cimage
    while i<m:
        file_name = os.path.join(file_dir, lst[i])
        i += 1
#        if cimage >= 3: break
        if os.path.isdir(file_name): continue
        if get_format_file(file_name) in ("jpg", "png"):
            get_detect(file_name, max_iteration, ti)


def get_format_file(fname):
    try:
        ref = re.compile(".*\.([^.]+)$")
        m = ref.match(fname)
        if (m and m.group(1)):
            return m.group(1).lower()
        return ""
    except:
#        print sys.exc_info()
        return ""

def test_dir(file_dir, nxt=True, ti=-1, max_thread = MAX_THREAD, max_iteration = MAX_ITERATION):
    get_stat(file_dir, ti, max_thread = max_thread, max_iteration = max_iteration)
#    lst = os.listdir(file_dir)
#    m = len(lst)
#    i = 0
#    while i<m:
#        file_name = os.path.join(file_dir, lst[i])
#        if nxt: test_dir(file_name, False, max_thread = max_thread, max_iteration = max_iteration)
#        else: get_stat(file_name, ti, max_thread = max_thread, max_iteration = max_iteration)
#        i += 1

class TestThread(Thread):
    dr = ""
    fls = False
    ti = -1
    max_thread = 0
    max_iteration = 0

    def __init__( self, dr, fls, ti, max_thread = MAX_THREAD, max_iteration = MAX_ITERATION):
        Thread.__init__(self)
        self.dr = dr
        self.fls = fls
        self.ti = ti
        self.max_thread = max_thread
        self.max_iteration = max_iteration

    def run(self):
        test_dir(self.dr, self.fls, self.ti, max_thread = self.max_thread, max_iteration = self.max_iteration)
        
def testingFaces(faces = 3, max_thread = MAX_THREAD, max_iteration = MAX_ITERATION, daemon= DAEMON):
    res = dict()
    global cface, cimage, tST, stat_params, stat_min, stat_max, stat_time, learnimage, DAEMON
    DAEMON = daemon
    stat_min = {}
    stat_max = {}
    stat_time = {}
    for p in stat_params:
        stat_min[p] = 1000
        stat_max[p] = 0
        stat_time[p] = 0
    #cface = 0
    tST = 0
    cimage = 0
    learnimage = 0
    
    t11 = time.time()
    
    threads = []
    for ti in xrange(max_thread):
        tr = TestThread(os.path.join(INPUT_DIR, "%s/"%faces), False, ti, max_thread = max_thread, max_iteration = max_iteration)
        tr.start()
        threads.append(tr)
    
    for thread in threads: thread.join()
    
    t11 =  time.time()-t11
    f = open(FACES_RESAULT, 'w+b')
    res["host"] = HOST
    res["port"] = PORT
    res["faces"] = faces
    res["all_time"] = t11*1000
    res["time_to_1_img"] = t11/cimage*1000
    res["count_all_img"] = cimage
    res["max_iteration"] = max_iteration
    res["max_thread"] = max_thread
    for p in stat_params:
        res[p] = [stat_time[p]/cimage*1000, stat_min[p]*1000, stat_max[p]*1000]
    
    res["avg1"] = tST/cimage*1000
    res["learnimage"] = learnimage
    return res        

def startTesting(max_thread = MAX_THREAD, max_iteration = MAX_ITERATION): 
    f = open(FACES_RESAULT, 'w+b')
    f.write('[]')
    f.close()
    res = []
    #res.append(testingFaces(3, max_thread, max_iteration, 'FD'))
    res.append(testingFaces(3, max_thread, max_iteration, 'FR'))
    #res.append(testingFaces(5, max_thread, max_iteration, 'FD'))
    res.append(testingFaces(5, max_thread, max_iteration, 'FR'))
    f = open(FACES_RESAULT, 'w+b')
    f.write(json.dumps(res))
    f.close()

startTesting(max_thread = MAX_THREAD, max_iteration = MAX_ITERATION)