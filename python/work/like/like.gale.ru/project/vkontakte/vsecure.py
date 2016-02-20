import hashlib
import time
import urllib, urllib2

SEND_NOTIFICATION = "secure.sendNotification"
SAVE_APP_STATUS = "secure.saveAppStatus"
GET_APP_BALANCE = "secure.getAppBalance"
GET_BALANCE = "secure.getBalance"
ADD_VOTES = "secure.addVotes"
WITHDRAW_VOTES = "secure.withdrawVotes"
TRANSFER_VOTES = "secure.transferVotes"
GET_TRANSACTION_HISTORY = "secure.getTransactionsHistory"

# rux
API_ID = 1510688
API_SECRET = "DxI2mwQQlbMt5OIPt8pC"
# Soltino
#API_ID = 1518465
#API_SECRET = "m19wWwp963LbhwD816tW"

API_URL = "http://api.vkontakte.ru/api.php"
API_VERSION = "2.0"
API_DATA_FORMAT = "JSON"

class VSDataProvider():
    def generateSignature(self,params):
	data = sorted( params.items(), key = lambda x: x[0])
        signature_data = "".join([str(p[0]) + "=" + str(p[1]) for p in data])
	signature_data += API_SECRET
        return hashlib.md5(signature_data).hexdigest()
	
    def sendRequest(self,  method, **kwargs):
	import random, json
	params = {
	    'method': method, 
	    'random': str(random.randint(1, 32767)),
	    'api_id': str(API_ID),
	    'format': API_DATA_FORMAT,
	    'timestamp':str(int(time.time())),
	    'v':API_VERSION}
	params.update(kwargs)
	params.update( {"sig": self.generateSignature(params)})	
	enc_params = urllib.urlencode(params)
	req = urllib2.Request( API_URL)
	fd = urllib2.urlopen( req, enc_params)
	return json.load( fd)

def check_auth(viewer_id, auth_key):
#    return auth_key == hashlib.md5( str(API_ID) + '_' + str(viewer_id) + '_' + API_SECRET).hexdigest()
    return True    

def get_user_balance( viewer):
    data = VSDataProvider().sendRequest( GET_BALANCE, uid=viewer)
    try:
	return data['response']
    except:
	return None
    
def withdraw( viewer, amount):
    data = VSDataProvider().sendRequest( WITHDRAW_VOTES, uid=viewer, votes=amount)
    return data
    
    



















