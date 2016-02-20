import datetime
from videoclient.views import logout

class SessionIdleTimeout(object):
    """Middleware class to timeout a session after a specified time period.
    """
    
    SESSION_IDLE_TIMEOUT = 1200
    
    def process_request(self, request):
        if request.user.is_authenticated():
            now = datetime.datetime.now()
            if request.session.has_key('last_activity') and (now - request.session['last_activity']).seconds > self.SESSION_IDLE_TIMEOUT:
                logout(request)
            else:
                request.session['last_activity'] = now
        return None