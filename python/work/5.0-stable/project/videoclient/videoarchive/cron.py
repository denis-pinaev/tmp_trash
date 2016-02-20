from videoarchive import settings
from videoclient.settings import log_videoarchive as logging
import sys
from videoarchive.django_cron import cronScheduler, Job
from videoarchive import models
from videoarchive import utils
 

class CheckTasks(Job):

    run_every = int(utils.getParamFromBase(settings.CRON_DELAY_FOR_PROCESS))

#    def __init__(self, *args, **kwargs):
#        self.run_every = int(utils.getParamFromBase(settings.CRON_DELAY_FOR_PROCESS))
#        VcSettings.log_videoarchive.info("Init cron run_every = "+str(self.run_every))
#        Job.__init__(self, *args, **kwargs)
    
               
    def job(self):
 #       self.run_every = int(utils.getParamFromBase(settings.CRON_DELAY_FOR_PROCESS))
        logging.info("Run cron run_every = "+str(self.run_every))
        utils.checkTasks()
       
try:   
    cronScheduler.register(CheckTasks)
except:
    logging.exception("CheckTasks: "+str(sys.exc_info()))    

