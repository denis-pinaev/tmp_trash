#coding=utf-8
import logging
import sys
import json

def getClassByName(module, class_name):
    try:
        imported_module_object = __import__(module)
        kls = getattr(imported_module_object, class_name)  
        return kls
    except:
        logging.exception("getClassByName: class="+class_name+' error:'+str(sys.exc_info()))
    return False

def getDictFromString(string):
    result = {}  
    if string:        
        try:
            d = json.loads(string)
        except:
            logging.exception("getDictFromString: string="+string+' error:'+str(sys.exc_info()))
            d = {}        
        for i in d:
            result[str(i)]= d[i]
    return result