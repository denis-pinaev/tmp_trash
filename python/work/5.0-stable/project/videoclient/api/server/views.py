from api.views import json_response
import datetime

@json_response
def get_server_time(request):
    answer = dict()
    answer["status"] = True
    time_now = datetime.datetime.now()
    answer["server_time"] = str(time_now.strftime("%H:%M:%S"))
    return answer 
