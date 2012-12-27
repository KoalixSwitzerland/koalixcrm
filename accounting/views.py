# -*- coding: utf-8 -*-
from os import path
from accounting.models import *
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

def createBalanceSheetPDF(request, calculationunitid):
  try:
   accountingPeriod = AccountingPeriod.objects.get(id=quoteid)
   pdf = accountingPeriod.createBalanceSheetPDF(request.user)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response
  except (TemplateSetMissing, UserExtensionMissing), e:
    raise Http404

def createProfitLossStatementPDF(request, calculationunitid):
  try:
   accountingPeriod = AccountingPeriod.objects.get(id=quoteid)
   pdf = accountingPeriod.createProfitLossStatementPDF(request.user)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response
  except (TemplateSetMissing, UserExtensionMissing), e:
    raise Http404
