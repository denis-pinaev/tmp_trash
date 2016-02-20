import os
import tempfile
from django.core.files import File
from urllib import urlopen

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
    from settings import HTTP_HOST
    return HTTP_HOST + url
    import hashlib, time

def get_store_path(filename):
    return "%s/%s" % (filename[:2], filename[2:4])
