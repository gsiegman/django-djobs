from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^admindocs/', include('django.contrib.admindocs.urls')),
    (r'^', include('djobs.urls')),
    (r'^site_media/(?P<path>.*)$', 
     'django.views.static.serve', 
     {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
    ),
)