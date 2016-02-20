import os
from balancer import Balancer

FS_HOST = '192.168.0.55'
FS_PORT = 16544
FS_LOGIN = 'lLogin'
FS_PASSWD = 'pPassword'
FS_USER = 'babyboom'

def recognize(file_in):
    file = open(file_in, "r")
    data_file = file.read()
    file.close()
    b = Balancer(FS_HOST, FS_PORT, FS_LOGIN, FS_PASSWD, FS_USER)
    res = b.recognize(data_file, 100)[0][0][1]
#    res = b.getPersons()
    b.close()
    del b
    return res

def compare(file_path1, file_path2):
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

#print recognize("1.jpg")
print compare("1.jpg", "j.jpg")
