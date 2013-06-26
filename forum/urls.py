from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^forum/', include('dinette.urls')),
    (r'^accounts/', include('socialauth.urls')),

    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG or getattr(settings, 'SERVE_MEDIA', False):
    urlpatterns += patterns(
        'django.views.static',
        (r'^site_media/(?P<path>.*)$', 'serve', 
            { 
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True
            }
        ),
    )
