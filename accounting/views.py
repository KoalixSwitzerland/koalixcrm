# -*- coding: utf-8 -*-
from os import path
from accounting.models import *
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from subprocess import *

def createBalanceSheetPDF(modelAdmin, request, calculationunitid):
  try:
   accountingPeriod = AccountingPeriod.objects.get(id=calculationunitid)
   pdf = accountingPeriod.createBalanceSheetPDF(request.user)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response
  except (TemplateSetMissing, UserExtensionMissing, CalledProcessError), e:
   if type(e) == UserExtensionMissing:
      response = HttpResponseRedirect('/admin/accounting/accountingperiod/')
      modelAdmin.message_user(request, _("User Extension Missing"))
   elif type(e) == TemplateSetMissing:
      response = HttpResponseRedirect('/admin/accounting/accountingperiod/')
      modelAdmin.message_user(request, _("Templateset Missing"))
   elif type(e) ==CalledProcessError:
      response = HttpResponseRedirect('/admin/accounting/accountingperiod/')
      modelAdmin.message_user(request, e.output)
   else:
      raise Http404
   return response

def createProfitLossStatementPDF(modelAdmin, request, calculationunitid):
  try:
   accountingPeriod = AccountingPeriod.objects.get(id=calculationunitid)
   pdf = accountingPeriod.createProfitLossStatementPDF(request.user)
   response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
   response['Content-Length'] = path.getsize(pdf)
   return response
  except (TemplateSetMissing, UserExtensionMissing, CalledProcessError), e:
   if type(e) == UserExtensionMissing:
      response = HttpResponseRedirect('/admin/accounting/accountingperiod/')
      modelAdmin.message_user(request, _("User Extension Missing"))
   elif type(e) == TemplateSetMissing:
      response = HttpResponseRedirect('/admin/accounting/accountingperiod/')
      modelAdmin.message_user(request, _("Templateset Missing"))
   elif type(e) ==CalledProcessError:
      response = HttpResponseRedirect('/admin/accounting/accountingperiod/')
      modelAdmin.message_user(request, e.output)
   else:
      raise Http404
   return response
