# -*- coding: utf-8 -*-
from os import path
from django.http import Http404
from crm.models import *
from django.http import HttpResponse
from exceptions import TemplateSetMissing
from exceptions import UserExtensionMissing
from django.core.servers.basehttp import FileWrapper
from django.utils.translation import ugettext as _

def createQuotePDF(request, quoteid):
  try:
   quote = Quote.objects.get(id=quoteid)
   pdf = quote.createPDF(purchaseconfirmation=False)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response
  except (TemplateSetMissing, UserExtensionMissing), e:
    raise Http404
   
def createPurchaseConfirmationPDF(request, quoteid):
  try:
   quote = Quote.objects.get(id=quoteid)
   pdf = quote.createPDF(purchaseconfirmation=True)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response
  except (TemplateSetMissing, UserExtensionMissing), e:
    raise Http404
   
def createInvoicePDF(request, invoiceid):
  try:
    invoice = Invoice.objects.get(id=invoiceid)
    pdf = invoice.createPDF(deliveryorder=False)
    response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
    response['Content-Length'] = path.getsize(pdf)
    return response
  except (TemplateSetMissing, UserExtensionMissing), e:
    raise Http404
  
def createDeliveryOrderPDF(request, invoiceid):
  try:
    invoice = Invoice.objects.get(id=invoiceid)
    pdf = invoice.createPDF(deliveryorder=True)
    response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
    response['Content-Length'] = path.getsize(pdf)
    return response
  except (TemplateSetMissing, UserExtensionMissing), e:
    raise Http404
 
def createPurchaseOrderPDF(request, purchaseorderid):
  try:
    purchaseorder = PurchaseOrder.objects.get(id=purchaseorderid)
    response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
    response['Content-Length'] = path.getsize(pdf)
    return response
  except (TemplateSetMissing, UserExtensionMissing), e:
    raise Http404
   
def selectaddress(invoiceid):
  invoice = Invoice.objects.get(id=invoiceid)
  address = invoice.contract
  
def test(self, request, queryset):
  for obj in queryset:
      invoice = obj.createInvoice()
      self.message_user(request, _("Invoice created"))
      response = HttpResponseRedirect('/admin/crm/invoice/'+str(invoice.id))
  return response
test.short_description = _("Test")
  
   