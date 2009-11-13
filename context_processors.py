from dinette.models import Ftopics, SiteConfig


def get_announcement(request):
    try:
       ancount =  Ftopics.objects.filter(announcement_flag = True).count()       
       if(ancount > 0 ) :
             announcement = Ftopics.objects.filter(announcement_flag = True).latest()
             return {'announcement': announcement,'ancount':ancount}
             
       return {'ancount':ancount}
    except Ftopics.DoesNotExist:
       return {}
    
def get_site_config(request):
    try:
        config = SiteConfig.objects.get(id = 1)
        return {'config': config}
    except SiteConfig.DoesNotExist:
        return {}
    
