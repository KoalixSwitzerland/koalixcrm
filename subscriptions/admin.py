# -*- coding: utf-8 -*-
import os
from django import forms
from django.core.urlresolvers import reverse
from datetime import date
from crm.models import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper

class AdminSubscriptionEvent(admin.TabularInline):
   model = SubscriptionEvent
   extra = 1
   classes = ('collapse-open',)
   fieldsets = (
      ('Basics', {
         'fields': ('eventdate', 'event',)
      }),
   )
   allow_add = True

class OptionSubscription(admin.ModelAdmin):
   list_display = ('id', 'customer','subscriptiontype' , 'startdate', 'cancelingdate', 'staff', 'lastmodification', 'lastmodifiedby')
   list_display_links = ('id', )       
   list_filter    = ('customer', 'startdate', 'staff', 'defaultcurrency')
   ordering       = ('id', 'defaultcustomer', 'defaultcurrency')
   search_fields  = ('id','contract', 'defaultcurrency__description')
   fieldsets = (
      (_('Basics'), {
         'fields': ('description', 'defaultcustomer', 'defaultSupplier', 'defaultcurrency')
      }),
   )
   inlines = [SubscriptionEvent, ContractPhoneAddress, ContractEmailAddress, InlineQuote, InlineInvoice, InlinePurchaseOrder]

   def save_model(self, request, obj, form, change):
     if (change == True):
       obj.lastmodifiedby = request.user
     else:
       obj.lastmodifiedby = request.user
       obj.staff = request.user
     obj.save()
   actions = ['createContract', 'createInvoice', 'createQuote']