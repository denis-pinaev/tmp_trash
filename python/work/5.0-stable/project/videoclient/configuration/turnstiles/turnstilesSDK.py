import socket
import sys
class TurnstilesSDK:
    
    COMMAND_SEARCH = 'h'
    COMMAND_STATUS = 's'
    COMMAND_OPEN_IN = 'in'
    COMMAND_OPEN_OUT = 'out'
    COMMAND_CHANGE_IP = 'ipchange'
    
    STATUS_RESPONSE = 'h:id'
    STATUS_CLOSED = 'c'
    STATUS_OPENED_IN = 'in'
    STATUS_OPENED_OUT = 'out'
    STATUS_ERROR = 'error'
    
    data = dict()
    DEVICE_PORT = 50000
    CONNECTION_TIMEOUT = 1
    CONNECTION_TYPE = "UDP"#"TCP"#"UDP"
    
    
    def __init__(self, turns=None):
        if turns:
            nturns = []
            for t in turns:
                nturns.append(t)
            self.data = {"turns":nturns} 
        else:
            self.clear()
    
    def __save_data(self):
        if "turns" in self.data: return
        self.clear()
        
    def __get_data(self):
        if "turns" in self.data: return
        self.clear()
        
    def __searchTurnstiles(self):
        new_turns = []
        x = ('<broadcast>', self.DEVICE_PORT)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(self.CONNECTION_TIMEOUT)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(self.COMMAND_SEARCH, x)
        except:
            return new_turns
        
        try:
            while True:
                (buf, address) = s.recvfrom(2048)
                if self.STATUS_RESPONSE in buf:#True:#buf == self.STATUS_RESPONSE:
                    if not len(buf):
                        break
                    id = ord(buf.split(self.STATUS_RESPONSE)[1])
                    new_turns.append({"address":address[0],"id":id})
                    #print "Received from %s: %s" % (address, buf)
        except:
            s.close()
            return new_turns
        
        s.close()
        return new_turns
    
    def __sendCommand(self, turn_id, command):
        response = self.STATUS_ERROR
        turns = self.data["turns"]
        for turn in turns:
            if turn_id == turn["id"] :
                try:
                    if self.CONNECTION_TYPE == "TCP":
                        #print("TCP connect")
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#tcp
                        s.settimeout(self.CONNECTION_TIMEOUT)
                        s.connect((turn["address"], self.DEVICE_PORT))#tcp
                        s.send(command)#tcp
                    else:
                        #print("UDP connect")
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#udp
                        s.settimeout(self.CONNECTION_TIMEOUT)
                        s.sendto(command, (turn["address"], self.DEVICE_PORT))#udp
                except:
                    return self.STATUS_ERROR
                
                try:
                    #print "sent", (command, (turn["address"], self.DEVICE_PORT))
                    response = s.recv(1024)
                    #(response, address) = s.recvfrom(2048)
                except:
                    response = self.STATUS_ERROR
                    
                s.close()
                break
        return response
    
    def __updateTurnstiles(self, new_turns):
        turns = self.data["turns"]
        for turn in turns:
            was_address = False
            for nturn in new_turns:
                if turn["id"] == nturn["id"]:
                    turn["active"] = True
                    turn["status"] = self.STATUS_CLOSED
                    turn["address"] = nturn["address"]
                    new_turns.remove(nturn)
                    was_address = True
                    break
            if not was_address:
                turn["active"] = False
        for nturn in new_turns:
            turns.append({"address":nturn["address"], "active":True, "status":self.STATUS_CLOSED, "id":nturn["id"]})
        self.__save_data()
        
    def __setTurnParam(self, id, param, value):
        was_id = False
        for turn in self.data["turns"]:
            if turn["id"] == id:
                turn[param] = value
                was_id = True
        self.__save_data()
        return was_id
    
    def __convertAddress(self, address):
        response = ""
        address_ar = address.split(".")
        if len(address_ar) == 4:
            response = "%s%s%s%s" % (chr(int(address_ar[0])),chr(int(address_ar[1])),chr(int(address_ar[2])),chr(int(address_ar[3])))
        return response
        
    
    
    
    def setTurnstile(self, turn):
        try:
            self.data = {"turns":[{'active': True, 'status': 'c', 'id': turn.turn_id, 'address': turn.ip}]}
        except:
            self.clear()
    
    def getTurnstiles(self):
        self.__get_data()
        if "turns" in self.data and len(self.data["turns"])>0: return self.data["turns"]
        return self.searchTurnstiles()
    
    def clear(self):
        self.data = {"turns":[]}
        self.__save_data()
        
    def searchTurnstiles(self):
        self.__get_data()
        new_turns = self.__searchTurnstiles()
        self.__updateTurnstiles(new_turns)
        return self.data["turns"]
    
    def sendCommand(self, id, command):
        self.__get_data()
        response = self.__sendCommand(id, command)
        if response == self.STATUS_ERROR:
            self.__setTurnParam(id, "active", False)
        else:
            self.__setTurnParam(id, "active", True)
        return response
            
    def changeIP(self, id, address, DNS=None, gateway=None):
        self.__get_data()
        command = "%s%s" % (self.COMMAND_CHANGE_IP, self.__convertAddress(address))
        if DNS:
            command = "%s%s" % (command, self.__convertAddress(DNS))
            if gateway: command = "%s%s" % (command, self.__convertAddress(gateway))
        elif gateway:
            command = "%s%s%s" % (command, self.__convertAddress("0.0.0.0"), self.__convertAddress(gateway))
            
        response = self.__sendCommand(id, command)
        if not response == self.STATUS_ERROR:
            self.__setTurnParam(id, "address", address)
        return response
    
''' 
#turns example: {"turns":[{'active': True, 'status': 'c', 'id': 1, 'address': '192.168.0.142'}]}
print "Start"
trns = [{'active': True, 'status': 'c', 'id': 0, 'address': '192.168.0.147'}, {'active': True, 'status': 'c', 'id': 2, 'address': '192.168.0.143'}]
turns = TurnstilesSDK(trns)
trns = turns.searchTurnstiles()
print trns
#if len(trns) > 0:
#    print turns.sendCommand(trns[0]["id"], TurnstilesSDK.COMMAND_OPEN_IN)
#if len(trns) > 1:
#    print turns.sendCommand(trns[1]["id"], TurnstilesSDK.COMMAND_OPEN_OUT)
    #print turns.changeIP(trns[0]["id"], "192.168.0.142")
    #print turns.changeIP(trns[0]["id"], "192.168.0.142", "192.168.0.143")
    #print turns.changeIP(trns[0]["id"], "192.168.0.142", "192.168.0.143", "192.168.0.144")
    #print turns.changeIP(trns[0]["id"], "192.168.0.142", None, "192.168.0.144")
print "Finish"
'''