# -*- coding: utf-8 -*-
from os import path
from django.http import Http404
from crm.models import *
from django.http import HttpResponse
from exceptions import TemplateSetMissing
from exceptions import UserExtentionMissing
from django.core.servers.basehttp import FileWrapper

def createQuotePDF(request, quoteid):
  try:
   quote = Quote.objects.get(id=quoteid)
   pdf = quote.createPDF(purchaseconfirmation=False)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response
  except (TemplateSetMissing, UserExtentionMissing), e:
    raise Http404
   
def createPurchaseConfirmationPDF(request, quoteid):
  try:
   quote = Quote.objects.get(id=quoteid)
   pdf = quote.createPDF(purchaseconfirmation=True)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response
  except (TemplateSetMissing, UserExtentionMissing), e:
    raise Http404
   
def createInvoicePDF(request, invoiceid):
  try:
    invoice = Invoice.objects.get(id=invoiceid)
    pdf = invoice.createPDF(deliveryorder=False)
    response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
    response['Content-Length'] = path.getsize(pdf)
    return response
  except (TemplateSetMissing, UserExtentionMissing), e:
    raise Http404
  
def createDeliveryOrderPDF(request, invoiceid):
  try:
    invoice = Invoice.objects.get(id=invoiceid)
    pdf = invoice.createPDF(deliveryorder=True)
    response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
    response['Content-Length'] = path.getsize(pdf)
    return response
  except (TemplateSetMissing, UserExtentionMissing), e:
    raise Http404
 
def createPurchaseOrderPDF(request, purchaseorderid):
  try:
    purchaseorder = PurchaseOrder.objects.get(id=purchaseorderid)
    response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
    response['Content-Length'] = path.getsize(pdf)
    return response
  except (TemplateSetMissing, UserExtentionMissing), e:
    raise Http404
   
def selectaddress(invoiceid):
  invoice = Invoice.objects.get(id=invoiceid)
  address = invoice.contract
   