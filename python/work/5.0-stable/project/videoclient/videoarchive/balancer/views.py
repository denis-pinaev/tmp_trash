# Create your views here.
from videoarchive.balancer import models
from videoclient.settings import log_videoarchive as logging

def initBalancer():
    logging.info(models.Balancer.objects.filter(active = True).count())
    if models.Balancer.objects.filter(active = True).count()>0:
        bal = models.Balancer.objects.filter(active=True)[0]
        HOST = bal.host
        PORT = bal.port
        LOGIN = bal.login
        PASSWD = bal.passwd
        USER = bal.user
        return HOST, PORT, LOGIN, PASSWD, USER
    return '', '', '', ''
