#coding=utf-8
from videoclient import models #Turnstile, TurnstileCamera
from turnstilesSDK import TurnstilesSDK
import logging

def sendEnterForCamera(uuid, time_opened=None):
    turnstile_cameras = models.TurnstileCamera.objects.filter(camera__uuid = uuid)
    answer = True
    for turnstile in turnstile_cameras:
        try:
            turns = TurnstilesSDK()
            turns.setTurnstile(turnstile.turnstile)
            comand_open_in = TurnstilesSDK.COMMAND_OPEN_IN
            if time_opened:
                comand_open_in += '_' + chr(time_opened)
            if turnstile.inside: #TODO сделать обработку ошибки
                if TurnstilesSDK.STATUS_OPENED_IN != turns.sendCommand(turnstile.turnstile.turn_id, comand_open_in):
                    answer = False
            else:
                if TurnstilesSDK.STATUS_OPENED_OUT != turns.sendCommand(turnstile.turnstile.turn_id, TurnstilesSDK.COMMAND_OPEN_OUT):
                    answer = False
        except:
            logging.exception("")
            answer = False
    return answer
             
        