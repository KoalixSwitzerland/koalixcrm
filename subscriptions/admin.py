# -*- coding: utf-8 -*-
import os
from django import forms
from django.core.urlresolvers import reverse
from datetime import date
from crm.models import *
from crm.admin import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from subscriptions.models import *

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
   list_display = ('id', 'defaultcustomer','defaultcurrency','subscriptiontype' , 'startdate', 'cancelingdate', 'staff', 'lastmodification', 'lastmodifiedby')
   list_display_links = ('id', )       
   list_filter    = ('defaultcustomer', 'subscriptiontype')
   ordering       = ('id', 'defaultcustomer', 'subscriptiontype')
   search_fields  = ('id', 'defaultcustomer')
   fieldsets = (
      (_('Basics'), {
         'fields': ('defaultcustomer','defaultcurrency','subscriptiontype' , 'startdate', 'cancelingdate', 'staff',)
      }),
   )
   inlines = [AdminSubscriptionEvent]
   
   def createInvoice(self, request, queryset):
      for obj in queryset:
         invoice = obj.createInvoice()
         response = HttpResponseRedirect('/admin/crm/invoice/'+str(invoice.id))
      return response
      
   def save_model(self, request, obj, form, change):
     if (change == True):
       obj.lastmodifiedby = request.user
     else:
       obj.lastmodifiedby = request.user
       obj.staff = request.user
     obj.save()
   createInvoice.short_description = _("Create Invoice")

   actions = ['createSubscriptionPDF', 'createInvoice']


class OptionSubscriptionType(admin.ModelAdmin):
   list_display = ('id', 'title','defaultunit', 'tax', 'accoutingProductCategorie')
   list_display_links = ('id', )       
   list_filter    = ('title', )
   ordering       = ('id', 'title',)
   search_fields  = ('id', 'title')
   fieldsets = (
      (_('Basics'), {
         'fields': ('productNumber', 'title', 'description', 'defaultunit', 'tax', 'accoutingProductCategorie', 'cancelationPeriod', 'automaticContractExtension', 'automaticContractExtensionReminder', 'minimumDuration', 'paymentIntervall', 'contractDocument')
      }),
   )
   inlines = [ProductPrice, ProductUnitTransform]
   
admin.site.register(Subscription, OptionSubscription)
admin.site.register(SubscriptionType, OptionSubscriptionType)