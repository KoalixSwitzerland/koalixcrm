# -*- coding: utf-8 -*-
from crm.models import *
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/koalixcrm/media'}),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^export/quote/(?P<quoteid>\d+)/$', 'crm.views.createQuotePDF'),
    (r'^export/invoice/(?P<invoiceid>\d+)/$', 'crm.views.createInvoicePDF'),
    (r'^export/balancesheet/(?P<calculationunitid>\d+)/$', 'accounting.views.createBalanceSheetPDF'),
    (r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),

)
