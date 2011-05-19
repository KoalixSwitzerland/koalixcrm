# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from crm.models import *
from accounting.models import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect

class AccountingPeriodBooking(admin.TabularInline):
   model = Booking
   extra = 1
   classes = ('collapse-open',)
   fieldsets = (
      ('Basics', {
         'fields': ('fromAccount', 'toAccount', 'description', 'amount', 'bookingDate', 'staff', 'bookingReference',)
      }),
   )
   allow_add = True

class OptionBooking(admin.ModelAdmin):
   list_display = ('fromAccount', 'toAccount', 'amount', 'bookingDate', 'staff')
   fieldsets = ((_('Basic'), {'fields' : ('fromAccount', 'toAccount', 'amount', 'bookingDate', 'staff', 'description', 'bookingReference', 'accountingPeriod')}),)
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

class OptionAccountingPeriod(admin.ModelAdmin):
   list_display = ('title', 'begin', 'end')
   list_display_links = ('title', 'begin', 'end')
   fieldsets = (
      (_('Basics'), {
         'fields': ('title', 'begin', 'end')
      }),
   )
   inlines = [AccountingPeriodBooking, ]
   save_as = True
   
   def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for instance in instances :
      if (change == True):
        instance.lastmodifiedby = request.user
      else:
        instance.lastmodifiedby = request.user
        instance.staff = request.user
      instance.save()
   
   def createBalanceSheetPDF(self, request, queryset):
      for obj in queryset:
         response = HttpResponseRedirect('/export/balancesheet/'+str(obj.id))
         return response
   createBalanceSheetPDF.short_description = _("Create PDF of Balance Sheet")
   
   def createProfitLossStatement(self, request, queryset):
      for obj in queryset:
         response = HttpResponseRedirect('/export/profitlossstatement/'+str(obj.id))
         return response
   createProfitLossStatement.short_description = _("Create PDF of Profit Loss Statement Sheet")
   
   actions = ['createBalanceSheetPDF', 'createProfitLossStatement']
            
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
admin.site.register(AccountingPeriod, OptionAccountingPeriod)
