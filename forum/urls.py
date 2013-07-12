from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^forum/', include('dinette.urls')),
    (r'^accounts/', include('accounts.urls')),

    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
