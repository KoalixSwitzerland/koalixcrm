# -*- coding: utf-8 -*-
from os import path
from accounting.models import *
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

def createBalanceSheetPDF(request, calculationunitid):
   calculationUnit = AccountingCalculationUnit.objects.get(id=calculationunitid)
   pdf = calculationUnit.createBalanceSheetPDF(request.user)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response
   
def createProfitLossStatementPDF(request, calculationunitid):
   calculationUnit = AccountingCalculationUnit.objects.get(id=calculationunitid)
   pdf = calculationUnit.createProfitLossStatementPDF(request.user)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response