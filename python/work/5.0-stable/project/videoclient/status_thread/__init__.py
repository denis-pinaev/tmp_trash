import threading
from status_thread import models as stModels
import json

def clear():
    stModels.Status.objects.all().delete()

class StatusThread(threading.Thread):
    
    def __init__(self):
        self.thread = stModels.Status.objects.create(percent = 0, answer="{}")
        self.value = 0
        self.percent = 0
        self.max_value = 100
        threading.Thread.__init__(self)
        
    def getThreadId(self):
        return self.thread.id
    
    def getStatus(self):
        return self.thread.persent
    
    def getAnswer(self):
        return self.thread.answer
    
    def setPercent(self, percent):
        if self.percent != percent:
            self.percent = percent
            self.thread.percent = percent
            self.thread.save()
            
    def setMaxValue(self, max_value):
        self.max_value = max_value
        percent = self.value*100/self.max_value
        self.setPercent(percent)
    
    def setValue(self, value):
        self.value = value
        percent = self.value*100/self.max_value
        self.setPercent(percent)
        
    def setRunning(self):
        self.thread.setRunning()
    
    def setFinished(self):
        self.thread.setFinished()    
    
    def setAnswer(self, answer):
        if isinstance(answer, dict):
            answer = json.dumps(answer)
        else:
            answer = str(answer)
        self.thread.answer = answer
        self.thread.save()
            
        
    
    