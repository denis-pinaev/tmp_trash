#coding=utf-8
import logging
from django.shortcuts import render_to_response
from views import initBalancer
from balancer import Balancer
from utils import get_value_defaultparams, delete_value_defaultparams

class StreamSmilartMiddleware(object):
    
    kwargs = []
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        self.kwargs=view_kwargs

    def process_response(self, request, response):
        if "document_root" not in self.kwargs:
            response['Pragma'] = 'no-cache'
            response['Cache-Control'] = 'no-cache must-revalidate proxy-revalidate'
            
            HOST, PORT, LOGIN, PASSWD, USER = initBalancer()
            b = Balancer(HOST, PORT, LOGIN, PASSWD, USER)
            
            df_value = get_value_defaultparams("control.fd.detect.type")
            # В случае если df_value не равен None и не равен 0
            if df_value:
                cs_value = None
                try:
                    # TODO уменьшить таймаут до 1-2 сек
                    # но не обязательно, т.к. проверка прараметра будет не на каждый запрос.
                    cs_value = b.getParameter("control.fd.detect.type")
                except:
                    logging.exception("")
                    
                if cs_value is not None: 
                    if df_value != cs_value:
                        # TODO убрать костыль с проверками, или организовать его через список разрешенных urls
                        if "/admin/" not in request.path and "/set_default_params/" not in request.path and "/execute_method_balancer/" not in request.path:
                            return render_to_response("loader_converting_database.html", {})
                    else:
                        delete_value_defaultparams("control.fd.detect.type")
        return response