#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from videoclient import utils
from videoclient.views import initBalancer, JsonResponse, tester, render_to_response_ex
import logging
import sys
from turnstilesSDK import TurnstilesSDK
from videoclient.configuration.turnstiles.models import Turnstile, TurnstileCamera
from videoclient.communicator.models import Camera
from videoclient.communicator import Communicator
from django.contrib.auth.decorators import permission_required

def getCameras():
    c = Communicator()
    res_cameras = c.getCameras()#filter_active=True)
    c.close()
    del c
    return res_cameras

def checkActivity(turns):
    td = getTurnsArray(turns)
    sdk = TurnstilesSDK(td)
    new_turns = sdk.searchTurnstiles()
    i = 0
    was_changes = False
    while i<len(td):
        nturn = new_turns[0]
        if td[i]["id"] == nturn["id"]:
            #print nturn["id"], nturn["active"]
            if not turns[i].ip == nturn["address"]:
                was_changes = True
                turns[i].ip = nturn["address"]
            if not turns[i].active == nturn["active"]:
                #td[i]["active"] = td[i]["id"] < 3#TEST!!! DELETE
                was_changes = True
                turns[i].active = nturn["active"]# = td[i]["active"]
            new_turns.remove(nturn)
            if was_changes: turns[i].save()
        i = i+1
    return td, new_turns

def getTurnsArray(turns):
    td = []
    for turn in turns:
        td.append({"id":turn.turn_id, "address":turn.ip, "active":turn.active, "enable":turn.enable, "name":turn.name, "description":turn.description})
    return td

def updateTurnstilesCameras(td, turnscamera):
    curr_id = -1
    turn = None
    for tc in turnscamera:
        tid = tc.turnstile.turn_id
        if not curr_id == tid:
            curr_id = tid
            for turn in td:
                if turn["id"] == tid: break;
        if turn:
            if not turn.has_key("cameras"):
                turn["cameras"] = []
            #turn["cameras"].append({"inside":tc.inside, "uuid":tc.camera.uuid})
            turn["cameras"].append({"inside":tc.inside, "camera":tc.camera})
    return td

@tester
@permission_required('user_perms.perm_settings')
def turnstiles_list(request):
    data = dict()
    getCameras()
    data.update(utils.getDefaultParams(request, 'turnstiles'))
    turns = Turnstile.objects.all().order_by("turn_id")
    td, new_turns = checkActivity(turns)
    turnscamera = TurnstileCamera.objects.all().order_by('turnstile')
    td = updateTurnstilesCameras(td, turnscamera)
    data["turns"] = td
    data["new_turns"] = new_turns
    #return JsonResponse(data)
    return render_to_response_ex(request, "turnstiles.html", data)

@tester
@permission_required('user_perms.perm_settings')
def turnstile_edit(request):
    data = dict()
    data.update(utils.getDefaultParams(request, 'turnstiles'))
    if request.REQUEST.has_key("id"):
        if request.REQUEST.has_key("cameras_in") and request.REQUEST.has_key("cameras_out"): turnstile_settings(request)
        tid = int(request.REQUEST["id"])
        turn = Turnstile.objects.filter(turn_id = tid)
        td = getTurnsArray(turn)
        turnscamera = TurnstileCamera.objects.filter(turnstile__turn_id = tid)
        td = updateTurnstilesCameras(td, turnscamera)
        turnscamera = TurnstileCamera.objects.all()
        if len(td)>0:
            data["turn"] = td[0]
            camerasbase = Camera.objects.all().order_by("active").reverse()
            cameras = []
            for camera in camerasbase:
                is_free = True
                if True:#td[0].has_key("cameras"):
                    #1 camera for all turnstiles
                    for ucam in turnscamera:
                        if ucam.camera.uuid == camera.uuid:
                    #1 camera for 1 turnstile 
                    #for ucam in td[0]["cameras"]:
                    #    if ucam["camera"].uuid == camera.uuid:
                            is_free = False
                            break
                if is_free:
                    cameras.append(camera)
            data["cameras"] = cameras
            
    #return JsonResponse(data)
    return render_to_response_ex(request, "turnstile_form.html", data)

@tester
@permission_required('user_perms.perm_settings')
def turnstile_settings(request):
    if request.REQUEST.has_key("id"):
        tid = int(request.REQUEST["id"])
        turn = Turnstile.objects.filter(turn_id = tid)
        if len(turn) == 1:
            turn = turn[0]
            if request.REQUEST.has_key("name") and request.REQUEST["name"] and not request.REQUEST["name"] == turn.name:
                turn.name = request.REQUEST["name"]
                turn.save()
            if request.REQUEST.has_key("description") and request.REQUEST["description"] and not request.REQUEST["description"] == turn.description:
                turn.description = request.REQUEST["description"]
                turn.save()
            if request.REQUEST.has_key("cameras_in") and request.REQUEST.has_key("cameras_out"):
                cameras_in = request.REQUEST["cameras_in"].split(',') if request.REQUEST["cameras_in"] else []
                cameras_out = request.REQUEST["cameras_out"].split(',') if request.REQUEST["cameras_out"] else []
                
                cameras_new = []
                for cam in cameras_in:
                    cameras_new.append({"id":cam, "inside":True})
                for cam in cameras_out:
                    cameras_new.append({"id":cam, "inside":False})

                camerasb = TurnstileCamera.objects.filter(turnstile__turn_id=tid)
                cameras = []
                for tc in camerasb:
                    cameras.append(tc)

                for cam in cameras_new:
                    need_add = True
                    for tc in cameras:
                        if int(cam["id"]) == int(tc.camera.id):
                            need_add = False
                            if not tc.inside == cam["inside"]:
                                tc.inside = cam["inside"]
                                tc.save()
                            cameras.remove(tc)
                            break
                    if need_add and cam["id"]:
                        camera = Camera.objects.filter(id=cam["id"])
                        if len(camera)>0:
                            camera = camera[0]
                            TurnstileCamera.objects.create(turnstile=turn,camera=camera,inside=cam["inside"])
                          
                for tc in cameras:
                    tc.delete()
                        
                 
    #for p in request.REQUEST: print p, request.REQUEST[p] 
    #return turnstile_edit(request)

@tester
@permission_required('user_perms.perm_settings')
def turnstile_command(request):
    data = {"status":False}
    if request.REQUEST.has_key("command"):
        data["command"] = request.REQUEST["command"] 
        data["param"] = request.REQUEST["param"]
        try:
            if data["command"] == "delete":
                tids = data["param"].split(',')
                data["deleted"] = []
                for tid in tids:
                    turn = Turnstile.objects.filter(turn_id=tid)
                    if turn.count()>0:
                        turn = turn[0]
                        data["deleted"].append(turn.turn_id)
                        data["deleted"].append(turn.ip)
                        turn.delete()#TEST!!!!!!
                data["status"] = True
            elif data["command"] == "on" or data["command"] == "off":
                tid = data["param"]
                turn = Turnstile.objects.filter(turn_id=tid)
                if turn.count()>0: turn = turn[0]
                turn.enable = data["command"] == "on"
                turn.save()
                data["status"] = True
            elif data["command"] == "add":
                param = data["param"].split(',')
                i = 0
                data["added"] = []
                while i < len(param):
                    tid = param[i]
                    tip = param[i+1]
                    turn = Turnstile.objects.filter(turn_id=tid)
                    if turn.count() == 0:
                        Turnstile.objects.create(turn_id=int(tid), ip=tip)
                        data["added"].append(tid)
                        data["added"].append(tip)
                    i = i + 2
                data["status"] = True
            elif data["command"] == "new":
                turns = Turnstile.objects.all().order_by("turn_id")
                new_turns = checkActivity(turns)[1]
                data["new_turns"] = new_turns
                data["status"] = True
        except: None
    return JsonResponse(data)
