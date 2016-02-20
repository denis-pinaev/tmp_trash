#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from videoclient.views import render_to_response_ex, tester
from utils import getDefaultParams, REVISION, VERSION, check_rule ,get_value_defaultparams
import logging,sys
from django.contrib.auth.decorators import permission_required, login_required
from videoclient.models import DefaultParams

@tester
@permission_required('user_perms.perm_setup')
def setup(request):
    data = dict()
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.REQUEST.has_key('period_storage_data'):
        try:
            period_storage_data = request.POST['period_storage_data']
            if str(period_storage_data).isdigit() and int(period_storage_data)>0:
                dp = DefaultParams.objects.get_or_create(name="period_storage_data")
                dp[0].value = period_storage_data
                dp[0].save() 
                return HttpResponse(True)
            return HttpResponse(False)
        except:
            logging.exception('setup: set period_storage_data '+str(sys.exc_info()))
            return HttpResponse(False)
    
    distr_version = None
    try:
        from videoclient import settings
        f = open(settings.VERSION_FILE, 'r+b')
        distr_version = f.read()
        f.close()
    except:
        logging.exception(str(sys.exc_info())) 
    data = {'version': VERSION, 'select_page': 'setup', 'user': request.user.username, 'distr_version': distr_version,}
    data['period']=get_value_defaultparams("period_storage_data")

    data.update(getDefaultParams(request, 'setup', ""))
    data["admin"] = check_rule(request)
    return render_to_response_ex(request, "setup.html", data)