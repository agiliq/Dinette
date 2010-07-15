from django import  template
from dinette.models import Ftopics, SiteConfig, NavLink

register = template.Library()

@register.simple_tag
def get_announcement():
    try:
        ancount = Ftopics.objects.filter(announcement_flag=True).count()
        if(ancount > 0):
            announcement = Ftopics.objects.filter(announcement_flag=True).latest()
            return {'announcement': announcement, 'ancount': ancount}

        return {'ancount': ancount}

    except Ftopics.DoesNotExist:
        return {}

@register.simple_tag
def get_site_config():
    try:
        config = SiteConfig.objects.get(id=1)
        return {'config': config}
    except SiteConfig.DoesNotExist:
        return {}

@register.simple_tag
def get_forumwide_links():
    try:
        return {"dinette_nav_links": NavLink.objects.all()}
    except:
        return {}
