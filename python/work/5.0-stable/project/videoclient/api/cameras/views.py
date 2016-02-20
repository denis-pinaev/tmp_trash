from api.views import json_response, getDictFromListModel, getDictFromItemModel
from videoclient import models
from videoclient.communicator import Communicator
from videoclient.communicator import models as comModels
from videoclient.views import initBalancer
from videoclient.balancer import Balancer

@json_response
def add(request):
    answer = dict()
    
    params = request.REQUEST
    if 'id' not in params and ('host' not in params or 'port' not in params):
        answer["error"] = "id or host:port in params not found"
        return answer
        
    if 'camera_type' not in params:
        answer["error"] = "camera_ype in params not found"
        return answer
    
    if 'camera_url' not in params:
        if 'camera_ip' not in params:
            answer["error"] = "camera_ip in params not found"
            return answer
    
    id = params['id'] if 'id' in params else None
    camera_type = params["camera_type"] if "camera_type" in params else None
    camera_ip = params["camera_ip"] if "camera_ip" in params else None
    camera_mac = params["camera_mac"] if "camera_mac" in params else '000000000000'
    camera_port = params["camera_port"] if "camera_port" in params else None
    camera_num = params["camera_num"] if "camera_num" in params else None
    camera_user = params["camera_user"] if "camera_user" in params else None
    camera_psw = params["camera_psw"] if "camera_psw" in params else None
    camera_url = params["camera_url"] if "camera_url" in params else None
    params = {"type":camera_type, "ip":camera_ip, "mac":camera_mac, "port":camera_port, "num":camera_num, "user":camera_user, "psw":camera_psw, "url":camera_url}
    
    host = None
    port = None
    mjpeg_port = None
    try:
        if id is not None: communicator = comModels.Communicator.objects.get(id=id)        
        else: communicator = comModels.Communicator.objects.get(host=params['host'], port=params['port'])
        host = communicator.host
        port = communicator.port
        mjpeg_port = communicator.mjpeg_port
    except:
        return {"status": False, "error": "incorrect_communicator"}
        
    c = Communicator()
    result = c.executeCommand("addCamera", params, "IsTrue", host=host, port=port, mjpeg_port=mjpeg_port)
    
    answer['status'] = result["result"]
    if not result["result"]:
        if "error_remark" in result: answer['error'] = result["error_remark"]        

    return answer

def getCameraDetectors(uuid, b, c):
    detects = dict()
    if True:
                try:
                    detects["Identification"] = False
                    detects["faceDetect"] = False
                    res_cam_mode = c.getModeScheduler(uuid)
                    if res_cam_mode["success"]:
                        if res_cam_mode["answer"] == -1: return False, dict()
                        elif res_cam_mode["answer"] == 1: detects["faceDetect"] = True
                        elif res_cam_mode["answer"] == 2:
                            detects["Identification"] = True 
                            detects["faceDetect"] = True                        
    
                    from videoclient.utils import get_value_defaultparams
                    if int(get_value_defaultparams("show_videoanalitycs")):
                        detects["detectCrowd"] = False
                        try:
                            #detects["detectCrowd"] = b.getParameter("control.detector.crowd.need.alert")
                            detects["isOnCrowd"] = b.getCameraParameter(uuid, "crowdNeedAlert")[0]
                            if detects["detectCrowd"] == "true":
                                detects["detectCrowd"] = True
                            else:
                                detects["detectCrowd"] = False
                        except:
                            detects["detectCrowd"] = False
    
                        detects_list = ["leftThings", "smokeDetect", "fireDetect", "flashDetect"]
                        for detect in detects_list:
                            detects[detect] = False
                            try:
                                answer = c.executeCommand('getModeDetectScheduler', {'uuid': uuid, 'detect': detect}, 'IsActive')
                                detects[detect] = answer["result"]
                            except:
                                logging.info("api_cameralist_detects: getModeDetectScheduler is failed: " + str(sys.exc_info()))
                        
                except:
                    pass
    return True, detects

@json_response
def list(request):
    answer = dict()

    params = request.REQUEST

    c = Communicator()
    cameras = c.getCameras(filter_active=True)

    if cameras["success"]:
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        
        cameras = cameras["cameras"]
        result = []
        for camera in cameras:
            cam = getDictFromItemModel(camera)
            if cam["active"]: 
                turn, detects = getCameraDetectors(cam["uuid"], b, c)
                cam["turn"] = turn
                cam["detects"] = detects
            else: cam["detects"] = []
            result.append(cam)
        answer["cameras"] = result
        answer["status"] = True
        
        b.close()
        del b

    c.close()
    del c

    return answer

@json_response
def saved_cameras(request):
    answer = dict()
    m_lists = comModels.Camera.objects.all()
    d_lists = getDictFromListModel(m_lists) 
    answer["cameras"] = d_lists
    answer["status"] = True    
    return answer

@json_response
def delete(request):
    answer = dict()
    
    params = request.REQUEST
   
    if 'uuid' not in params:
        answer["error"] = "uuid not found"
        return answer
    uuid = params['uuid']
        
    c = Communicator()
    c.deleteCamera(uuid)
    c.close()
    del c
    
    answer["status"] = True
    return answer

@json_response
def detect(request):
    result = {'status': False}
    detects = ["leftThings", "smokeDetect", "fireDetect", "flashDetect", "faceDetect", "Identification", "detectCrowd"]
    turns = ["on", "off"]
    uuid = request.REQUEST.get("uuid", None)
    turn = request.REQUEST.get("turn", None)
    detect = request.REQUEST.get("detect", None)

    if not turn in turns: return {"status": False, "error": "incorrect_turn_value"}
    elif not detect in detects: return {"status": False, "error": "incorrect_detect_value"}
    elif comModels.Camera.objects.filter(uuid=uuid).count()==0: return {"status": False, "error": "incorrect_uuid_value"}
    turn = turn == "on"
    if detect == "faceDetect":
        c = Communicator()
        answer = c.executeMethodByName("setModeScheduler", [uuid, 1 if turn else 0])
        result = {'status': answer["success"]}
    elif detect == "Identification":
        c = Communicator()
        answer = c.executeMethodByName("setModeScheduler", [uuid, 2 if turn else 1])
        result = {'status': answer["success"]}
    elif detect == "detectCrowd":
        HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
        c = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
        res = c.executeMethodByName("setParameter", ["true" if turn else "false", "control.detector.crowd.need.alert"])
        result = {'status': res}
    elif detect in detects:
        turn = "turnOnModeDetectScheduler" if turn else "turnOffModeDetectScheduler"
        c = Communicator()
        answer = c.executeCommand(turn, {"detect": detect, "uuid": uuid}, "IsTrue")
        result = {'status': answer["result"]}
        if not answer["result"]:
            if "error_remark" in answer: result['error'] = answer["error_remark"]
    else: return result        
    c.close()
    del c
    return result

@json_response
def turn(request):
    result = {'status': False}
    turns = ["on", "off"]
    uuid = request.REQUEST.get("uuid", None)
    turn = request.REQUEST.get("turn", None)

    if not turn in turns: return {"status": False, "error": "incorrect_turn_value"}
    elif comModels.Camera.objects.filter(uuid=uuid).count()==0: return {"status": False, "error": "incorrect_uuid_value"}

    turn = turn == "on"
    c = Communicator()
    answer = c.executeMethodByName("setModeScheduler", [uuid, 0 if turn else -1])
    result = {'status': answer["success"]}
    c.close()
    del c
    return result
