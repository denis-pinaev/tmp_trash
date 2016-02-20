from django import template
#from django.utils import translation
#from django.shortcuts import get_object_or_404
from django.template import Context, loader
from control_settings import config
register = template.Library()

LIMIT = 15

@register.filter
def get_size(value):
    l = len(value)
    if l>config.text_length: return config.max_text_width
    return config.min_text_width

"""
@register.tag
def trans(parser, token):
    return trans_and_help(parser, token)

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


class TransNode(template.Node):

    def __init__(self, group, params):
        self.group = group
        self.params = params
        
    def getTranslate(self, str):
        answer = str
        language = translation.get_language()
        cur_language = language
        if Language.objects.all().filter(name = language).count()>0:
            language = get_object_or_404( Language, name = language)
        else:
            return answer
        
        group = self.group
        if Group.objects.all().filter(title = group).count()>0:
            group = get_object_or_404( Group, title = group)
        else:
            return answer
        
        if Translation.objects.all().filter(group = int(group.id), phrase = str, language = int(language.id), active = True).count()>0:
            trans = get_object_or_404( Translation, group = int(group.id), phrase = str, language = int(language.id), active = True)
            #answer = trans.translate.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
            from django.utils.html import conditional_escape
            from django.utils.safestring import mark_safe
            answer = mark_safe(conditional_escape(trans.translate))
        else:
            if Translation.objects.all().filter(group = int(group.id), phrase = str, language = int(language.id), active = False).count()>0:
                pass
            else:
                import videoclient.settings
                if cur_language != videoclient.settings.LANGUAGE_CODE or self.group == 'help':
                    Translation.objects.create(group = group, phrase = str, language = language, active = False, translate="")
                    
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
        return self.getTranslateAll()
"""

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
    return SpinBoxNode(params)


class SpinBoxNode(template.Node):

    def __init__(self, params):
        self.params = params

    def get_val(self, context={}, param=""):         
        value_s = param.split('.')        
        value = context        
        for v in value_s:
            if value is not None:
                if v in value: value = value[v]
                else: return v
            else:
                break
        return value        

    def render(self, context):
       
        val = []
        for param in self.params:
            val.append(self.get_val(context, param))
        
        onclick = None
        if len(self.params)>7:
            onclick = self.params[7]
        
        spinbox = loader.get_template('control_settings_spinbox.html')  
        c = Context({
                 'id': val[0],
                 'name': val[1],
                 'value': val[2],
                 'width': val[3],
                 'min': val[4],
                 'max': val[5],
                 'step': val[6],
                 'onclick' : onclick
                 })
        return spinbox.render(c)
