# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse

from crm.models import *
from crp.models import *
from django.utils.translation import ugettext as _

from django.contrib import admin

class OptionBooking(admin.ModelAdmin):
   list_display = ('fromAccount', 'toAccount', 'amount', 'bookingDate', 'staff')
   fieldsets = ((_('Basic'), {'fields' : ('fromAccount', 'toAccount', 'amount', 'bookingDate', 'staff', 'description', 'bookingReference')}),)
   save_as = True

   def save_model(self, request, obj, form, change):
      obj.staff = request.user
      obj.lastmodifiedby = request.user
      obj.save()

class OptionAccount(admin.ModelAdmin):
   list_display = ('accountNumber', 'accountType', 'title')
   list_display_links = ('accountNumber', 'accountType', 'title')
   fieldsets = ((_('Basic'), {'fields': ('accountNumber', 'accountType', 'title' )}),)
   save_as = True

class InlineAccountUsage(admin.TabularInline):
   model = AccountUsage
   extra = 1
   classes = ('collapse-open',)
   fieldsets = ((_('Basic'), {'fields': ('account', 'valueAtStartOfBusinessYear')}),)
   allow_add = True

class OptionCRPCalculationUnit(admin.ModelAdmin):
   list_display = ('title', 'allEarnings', 'allSpendings', 'allActivas', 'allPassivas', 'begin', 'end')
   list_display_links = ('title', 'begin', 'end')
   fieldsets = (
      (_('Basics'), {
         'fields': ('title', 'allEarnings', 'allSpendings', 'allActivas', 'allPassivas', 'begin', 'end')
      }),
   )
   save_as = True
   inlines = [InlineAccountUsage]   
   
admin.site.register(Account, OptionAccount)
admin.site.register(Booking, OptionBooking)
admin.site.register(CRPCalculationUnit, OptionCRPCalculationUnit)
