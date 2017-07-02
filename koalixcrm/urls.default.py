# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import *
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from filebrowser.sites import FileBrowserSite
from crm.views import *
from accounting.views import *
from django.core.files.storage import DefaultStorage

site = FileBrowserSite(name="filebrowser", storage=DefaultStorage())
customsite = FileBrowserSite(name='custom_filebrowser', storage=DefaultStorage())
customsite.directory = "uploads/"


admin.autodiscover()

urlpatterns = [
    url(r'^admin/filebrowser/', customsite.urls),
    url(r'^admin/', admin.site.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
