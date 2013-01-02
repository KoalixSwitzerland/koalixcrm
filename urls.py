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
    (r'^export/quote/(?P<quoteid>\d+)/$', 'crm.views.createQuotePDF'),
    (r'^export/purchaseconfirmation/(?P<quoteid>\d+)/$', 'crm.views.createPurchaseConfirmationPDF'),
    (r'^export/invoice/(?P<invoiceid>\d+)/$', 'crm.views.createInvoicePDF'),
    (r'^export/deilveryorder/(?P<invoiceid>\d+)/$', 'crm.views.createDeliveryOrderPDF'),
    (r'^export/purchaseorder/(?P<purhcaseorderid>\d+)/$', 'crm.views.createPurchaseOrderPDF'),

    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
