#coding=utf-8

from django.db import models
import json

STATE_PENDING = "pending"
STATE_RUNNING = "running"
STATE_FINISHED = "finished"

class Status(models.Model):
    STATE_CHOICES = (
        (0, STATE_PENDING),
        (1, STATE_RUNNING),
        (2, STATE_FINISHED),
    )
    percent = models.IntegerField()
    state = models.IntegerField(choices=STATE_CHOICES, default=0)
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_update = models.DateTimeField(auto_now=True, auto_now_add=True)
    answer = models.TextField()
            
    def setRunning(self):
        self.state = 1
        self.save()
    
    def setFinished(self):
        self.state = 2
        self.save()

    def setPercent(self, percent):
        self.percent = percent
        self.save()
        
    def setAnswer(self, answer):
        if isinstance(answer, dict):
            answer = json.dumps(answer)
        else:
            answer = str(answer)
        self.answer = answer
        self.save()
    
    