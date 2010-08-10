from django import  template
from django.contrib.sites.models import Site

from dinette.models import Ftopics, SiteConfig, NavLink

register = template.Library()

class BaseDinetteNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        tokens = token.contents.split()
        if len(tokens) == 3:
            if tokens[1] != "as":
                 raise template.TemplateSyntaxError("Second argument in %r must be 'as'" % tokens[0])
            return cls(
                        as_varname=tokens[2]
                        )
        else:
            return cls()

class GetAnnouncementNode(BaseDinetteNode):
    def __init__(self, as_varname='announcement'):
        self.as_varname = as_varname

    def render(self, context):
        try:
            ancount = Ftopics.objects.filter(announcement_flag=True).count()
            if(ancount > 0):
                announcement = Ftopics.objects.filter(announcement_flag=True).latest()
                context[self.as_varname] = announcement
                return ''
        except Ftopics.DoesNotExist:
            return ''

@register.tag
def get_announcement(parser, token):
    return GetAnnouncementNode.handle_token(parser, token)

class GetNavLinksNode(BaseDinetteNode):
    def __init__(self, as_varname='nav_links'):
        self.as_varname = as_varname

    def render(self, context):
        context[self.as_varname] = NavLink.objects.all()
        return ''

@register.tag
def get_forumwide_links(parser, token):
    return GetNavLinksNode.handle_token(parser, token)

@register.simple_tag
def get_site_name():
    try:
        config = SiteConfig.objects.get(id=1)
        return config.name
    except SiteConfig.DoesNotExist:
        return ''

@register.simple_tag
def get_site_tag_line():
    try:
        config = SiteConfig.objects.get(id=1)
        return config.tag_line
    except SiteConfig.DoesNotExist:
        return ''
    
@register.simple_tag
def get_main_site_name():
    try:
        name = Site.objects.get_current().name
        return name
    except:
        return ''

@register.simple_tag
def get_main_site_domain():
    try:
        domain = Site.objects.get_current().domain
        return domain
    except:
        return ''
