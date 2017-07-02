# -*- coding: utf-8 -*-
from crm.models import *
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from filebrowser.sites import site
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/koalixcrm/media'}),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/admin'}),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
