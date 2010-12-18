# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from crm.models import *
from accounting.models import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect

class OptionBooking(admin.ModelAdmin):
   list_display = ('fromAccount', 'toAccount', 'amount', 'bookingDate', 'staff')
   fieldsets = ((_('Basic'), {'fields' : ('fromAccount', 'toAccount', 'amount', 'bookingDate', 'staff', 'description', 'bookingReference', 'accountingCalculationUnit')}),)
   save_as = True

   def save_model(self, request, obj, form, change):
      if (change == True):
        obj.lastmodifiedby = request.user
      else:
        obj.lastmodifiedby = request.user
        obj.staff = request.user
      obj.save()
   
class OptionAccount(admin.ModelAdmin):
   list_display = ('accountNumber', 'accountType', 'title', 'isopenreliabilitiesaccount', 'isopeninterestaccount', 'isProductInventoryActiva', 'isACustomerPaymentAccount')
   list_display_links = ('accountNumber', 'accountType', 'title')
   fieldsets = ((_('Basic'), {'fields': ('accountNumber', 'accountType', 'title', 'isopenreliabilitiesaccount', 'isopeninterestaccount', 'isProductInventoryActiva', 'isACustomerPaymentAccount')}),)
   save_as = True

class OptionAccountingCalculationUnit(admin.ModelAdmin):
   list_display = ('title', 'begin', 'end')
   list_display_links = ('title', 'begin', 'end')
   fieldsets = (
      (_('Basics'), {
         'fields': ('title', 'begin', 'end')
      }),
   )
   save_as = True
   
   def createBalanceSheetPDF(self, request, queryset):
      for obj in queryset:
         response = HttpResponseRedirect('/export/balancesheet/'+str(obj.id))
         return response
   createBalanceSheetPDF.short_description = _("Create PDF of Balance Sheet")
   
   actions = ['createBalanceSheetPDF',]
            
class OptionProductCategorie(admin.ModelAdmin):
   list_display = ('title', 'profitAccount', 'lossAccount')
   list_display_links = ('title', 'profitAccount', 'lossAccount')
   fieldsets = (
      (_('Basics'), {
         'fields': ('title', 'profitAccount', 'lossAccount')
      }),
   )
   save_as = True
   
admin.site.register(Account, OptionAccount)
admin.site.register(Booking, OptionBooking)
admin.site.register(ProductCategorie, OptionProductCategorie)
admin.site.register(AccountingCalculationUnit, OptionAccountingCalculationUnit)
