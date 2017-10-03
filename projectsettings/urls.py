"""test_koalixcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls.static import *
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from filebrowser.sites import FileBrowserSite
from django.core.files.storage import DefaultStorage

site = FileBrowserSite(name="filebrowser", storage=DefaultStorage())
customsite = FileBrowserSite(name='custom_filebrowser', storage=DefaultStorage())
customsite.directory = "media/uploads/"


admin.autodiscover()

urlpatterns = [
    url(r'^admin/filebrowser/', customsite.urls),
    url(r'^admin/', admin.site.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

