import os
import tempfile
from django.core.files import File
from urllib import urlopen
import settings
import logging

class FileLoader(object):
    def __init__(self, url):
	self.fileno, self.path = tempfile.mkstemp()
        f = open(self.path, 'w+b')
        f.write(urlopen(url).read())
        f.close()
        f = open(self.path, 'rb')
        self.File = File(f)
    def __del__(self):
        os.remove(self.path)


def get_absolute(url):
#    logging.info("absolute")
#    logging.info(url)
    if url.find(settings.MEDIA_URL)==0: url = url[len(settings.MEDIA_URL):]
    elif url.find(settings.MEDIA_ROOT)==0: url = url[len(settings.MEDIA_ROOT):]
    if url.find(settings.STORE_IMG)==0: url = url[len(settings.STORE_IMG):]
    elif url.find(settings.TMP_IMG)==0: url = url[len(settings.TMP_IMG):]
#    logging.info(url)
    return settings.HTTP_HOST + str(settings.MEDIA_URL[1:] if settings.MEDIA_URL.find("/")==0 else settings.MEDIA_URL) + url

def get_store_path(filename):
    return "%s/%s" % (filename[:2], filename[2:4])
