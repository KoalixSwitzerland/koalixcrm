# -*- coding: utf-8 -*-
from crm.models import *
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/koalixcrm/media'}),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^export/quote/(?P<quoteid>\d+)/$', 'crm.views.createQuotePDF'),
    (r'^export/purchaseconfirmation/(?P<quoteid>\d+)/$', 'crm.views.createPurchaseConfirmationPDF'),
    (r'^export/invoice/(?P<invoiceid>\d+)/$', 'crm.views.createInvoicePDF'),
    (r'^export/deilveryorder/(?P<invoiceid>\d+)/$', 'crm.views.createDeliveryOrderPDF'),
    (r'^export/purchaseorder/(?P<purhcaseorderid>\d+)/$', 'crm.views.createPurchaseOrderPDF'),
    (r'^export/balancesheet/(?P<calculationunitid>\d+)/$', 'accounting.views.createBalanceSheetPDF'),
    (r'^export/profitlossstatement/(?P<calculationunitid>\d+)/$', 'accounting.views.createProfitLossStatementPDF'),
    (r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),

)
