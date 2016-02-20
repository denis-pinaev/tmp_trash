from django import template
from django.utils import translation
from django.shortcuts import get_object_or_404
import datetime
from django.template import Context, loader
from videoclient import models
from videoclient import settings
from videoarchive import models as aModels
import sys
from videoclient.settings import log_videoarchive as logging

register = template.Library()

LIMIT = 15

@register.filter
def checkUrl(value=""):    
    try:       
        if value.find("http://") != 0: return "http://"+value
        return value
    except: 
        return value 

@register.filter
def sygnal_name(value=""):    
    try:       
        s = aModels.Signals.objects.filter(str_id=value)
        if s.count()>0:
            return s[0].name
        return value
    except: 
        return value 

@register.filter
def person_name(value=0):
    try:
        from videoclient.models import PersonId
        p = PersonId.objects.filter(bal_id=value)
        if p.count()>0:
            return "%s %s %s" % (p[0].person.first_name, p[0].person.last_name, p[0].person.middle_name)
        return value
    except: 
        return value 

@register.filter
def ftrans(code="", value=""):
    tr = []
    try:
        tr.append(unicode(value))
    except: tr.append(value)
    return TransNode("trans", tr, code).render([])


@register.filter
def age_of(value):
    if value:
        dy = datetime.datetime.now().year - value.year
        dm = datetime.datetime.now().month - value.month
        if dm<0: return dy-1
        elif dm>0: return dy
        else:
            dd = datetime.datetime.now().day - value.day
            if dd<0: return dy-1 
        return dy
    else: return 0 

@register.filter
def mul(value, arg):
    return value*arg

@register.filter
def tostr(value):
    return str(value)

@register.filter
def toint(value):
    return int(value)

@register.filter
def div(value, arg):
    return int(value)/int(arg)

@register.filter
def fdiv(value, arg):
    try:
        res = float(value)/float(arg)
        return res
    except:
        logging.exception("templatetags fdiv: "+str(sys.exc_info()))
    return ""

@register.filter
def int_div(value, arg):
    return int(int(value)/(arg))

@register.filter
def sub(value, arg):
    res = value-arg
    if res < 0:
        res = 0
    return res

@register.filter
def odd(value):
    if value%2 == 1:
        return True
    else:
        return False

@register.filter
def pParam(value, arg):
    from videoarchive.utils import checkDataParamValue
    return checkDataParamValue(value, arg)
    
@register.filter
def ttime(value):
    param = int(value)
    if param/3600 > 0: return "%02d:%02d:%02d" % (param/3600, param%3600/60, param%60)
    return "%02d:%02d" %(param/60, param%60)

@register.filter
def item(value):
    return (value-1)*LIMIT+1

@register.filter
def last(value):
    res = (value-2)*LIMIT+1
    if res<1:
        res = 1
    return res

@register.filter
def next(value, allpages):
    res = (value)*LIMIT+1
    max = (allpages-1)*LIMIT+1
    if res>max:
        res = max
    return res

@register.filter
def radio(value, index):
    res = ''
    if value == None:
        res = 'disabled="disabled"'
    elif str(value) == str(index):
        res = 'checked="checked"'
    return res

@register.filter
def is_correct_capture(value, resolution):
    i = len(resolution)-1
    res = i
    #while i>0 and (value['width']>resolution[i]['width'] or value['height']>resolution[i]['height']):
    while i>=0:
        if int(value['width'])<=int(resolution[i]['width']) and int(value['height'])<=int(resolution[i]['height']):
            res = i
        i = i-1
    return res


#@register.tag
#def trans(parser, token):
#    return trans_and_help(parser, token)

@register.tag
def help(parser, token):
    return trans_and_help(parser, token)

def trans_and_help(parser, token):
    params=[]
    try:
        token_params = token.split_contents()
        i = 1
        while i<len(token_params):
            params.append(token_params[i][1:-1])
            i = i+1
    except ValueError:
        msg = '%r tag requires a single argument' % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return TransNode(token_params[0], params)

@register.tag
def blocktrans(parser, token):
    params=[]
    nodelist = None
    try:
        nodelist = parser.parse(('endblocktrans',))
        parser.delete_first_token()
    except ValueError:
        msg = '%r tag requires a single argument' % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return TransNode("trans", params, nodelist = nodelist)


class TransNode(template.Node):

    def __init__(self, group, params=[], nodelist=None):
        self.group = group
        self.params = params
        self.nodelist = nodelist
                
    def getTranslate(self, str):
        str = ' '.join(str.split())
        answer = str
        language = translation.get_language()
        cur_language = language
        if models.Language.objects.all().filter(name = language).count()>0:
            language = get_object_or_404( models.Language, name = language)
        else:
            return answer
        
        group = self.group
        if models.Group.objects.all().filter(title = group).count()>0:
            group = get_object_or_404( models.Group, title = group)
        else:
            return answer
        
        if models.Translation.objects.all().filter(group = int(group.id), phrase = str, language = int(language.id), active = True).count()>0:
            trans = get_object_or_404( models.Translation, group = int(group.id), phrase = str, language = int(language.id), active = True)
            from django.utils.html import conditional_escape
            from django.utils.safestring import mark_safe
            answer = mark_safe(conditional_escape(trans.translate))
        else:
            if models.Translation.objects.all().filter(group = int(group.id), phrase = str, language = int(language.id), active = False).count()>0:
                pass
            else:
                import videoarchive.settings as vaSettings
                if cur_language != vaSettings.LANGUAGE_CODE or self.group == 'help':
                    models.Translation.objects.create(group = group, phrase = str, language = language, active = False, translate="")
                    
            return answer
        return answer
    
    def getTranslateAll(self):
        out = '';
        i = 0
        while i<len(self.params):
            trans = self.getTranslate(self.params[i])
            if i>0 and len(trans)>0 and len(out)>0:
                out = out + ' '
            out = out + trans
            i = i+1
        return out

    def render(self, context):
        if self.nodelist:
            self.params = []
            self.params.append(self.nodelist.render(context))
        return self.getTranslateAll()

@register.tag
def spinbox(parser, token):
    params=[]
    try:
        token_params = token.split_contents()
        i = 1
        while i<len(token_params):
            if token_params[i][:1] == '"' :
                value = token_params[i][1:-1]
            else:
                value = token_params[i]
            params.append(value)
            i = i+1
    except ValueError:
        msg = '%r tag requires a single argument' % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return SpinBoxNode(token_params)


class SpinBoxNode(template.Node):

    def __init__(self, params):
        self.params = params

    def render(self, context):
        
        self.params.pop(0)
        i = 0
        while i<len(self.params):
            if self.params[i][:1] == '"' :
                self.params[i] = self.params[i][1:-1]
            else:
                param = self.params[i]
                value_s = param.split('.')
                value = context
                for v in value_s:
                    if value is not None:
                        try:
                            value = value[v]
                        except:
                            value = v
                            break
                    else:
                        break
                self.params[i] = value
            i = i+1
        
        onclick = None
        if len(self.params)>7:
            onclick = self.params[7]
        
        spinbox = loader.get_template('spinbox.html')  
        c = Context({
                 'id': self.params[0],
                 'name': self.params[1],
                 'value': self.params[2],
                 'width': self.params[3],
                 'min': self.params[4],
                 'max': self.params[5],
                 'step': self.params[6],
                 'onclick' : onclick
                 })
        
        return spinbox.render(c)
    
@register.filter
def truncchar(value, arg):
    if len(value) <= arg:
        return value
    else:
        return value[:arg] + '...'     