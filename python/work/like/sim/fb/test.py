#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import string
import re

imgPath = '/home/srv/www/vhosts/like.gale.ru/www/files/media/photos.like2/'

def getAllImagesId(idName):
    imageFiles = []
    path = imgPath+idName
    for f in os.listdir(path):
        filename = "%s/%s" % (path, f)
        if os.path.isdir(filename):
            continue
        if re.search(".jpg", filename):
            imageFiles.append(f)
    return imageFiles

print(getAllImagesId("Aaho_Shahi"))
