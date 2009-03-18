from django.conf.urls.defaults import *
from django.conf import settings



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
     (r'^forum/', include('dinette.urls')),                           
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),    
     (r'^admin/(.*)', admin.site.root),
     
     
)



if settings.DEBUG:    
    urlpatterns += patterns('',
            url(r'^appmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )


