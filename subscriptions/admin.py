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
   list_filter    = ('customer', 'subscriptiontype')
   ordering       = ('id', 'customer', 'subscriptiontype')
   search_fields  = ('id', 'customer')
   fieldsets = (
      (_('Basics'), {
         'fields': ('customer','subscriptiontype' , 'startdate', 'cancelingdate', 'staff', 'lastmodification', 'lastmodifiedby')
      }),
   )
   inlines = [SubscriptionEvent]
   
   def createInvoice(self, request, queryset):
      for obj in queryset:
         invoice = obj.createInvoice()
         response = HttpResponseRedirect('/admin/crm/invoice/'+str(invoice.id))
      return response
   createInvoice.short_description = _("Create Invoice")

   actions = ['createSubscriptionPDF', 'createInvoice']
   
class OptionSubscriptionType(Product):
   list_display = ('id', 'title',)
   list_display_links = ('id', )       
   list_filter    = ('title', )
   ordering       = ('id', 'title',)
   search_fields  = ('id', 'title')
   fieldsets = (
      (_('Basics'), {
         'fields': ('title', 'description' , 'cancelationPeriod', 'automaticContractExtension', 'automaticContractExtensionReminder', 'minimumDuration', 'paymentIntervall', 'contractDocument')
      }),
   )
   
admin.site.register(Subscription, OptionSubscription)
admin.site.register(SubscriptionType, OptionSubscriptionType)