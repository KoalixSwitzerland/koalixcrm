# -*- coding: utf-8 -*-
from os import path
from accounting.models import *
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

def createBalanceSheetPDF(request, calculationunitid):
   calculationUnit = AccountingCalculationUnit.objects.get(id=calculationunitid)
   pdf = calculationUnit.createBalanceSheetPDF()
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response