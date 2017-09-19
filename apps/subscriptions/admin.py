# -*- coding: utf-8 -*-
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from apps.subscriptions.models import *


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


class InlineSubscription(admin.TabularInline):
    model = Subscription
    extra = 1
    classes = ('collapse-open',)
    readonly_fields = ('contract', 'subscriptiontype')
    fieldsets = (
        (_('Basics'), {
            'fields': ('contract', 'subscriptiontype')
        }),
    )
    allow_add = False


class OptionSubscription(admin.ModelAdmin):
    list_display = ('id', 'contract', 'subscriptiontype',)
    ordering = ('id', 'contract', 'subscriptiontype')
    search_fields = ('id', 'contract',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('contract', 'subscriptiontype',)
        }),
    )
    inlines = [AdminSubscriptionEvent]

    @staticmethod
    def createInvoice(queryset):
        for obj in queryset:
            invoice = obj.createInvoice()
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
        return response

    @staticmethod
    def createQuote(queryset):
        for obj in queryset:
            invoice = obj.createInvoice()
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
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
    list_display = ('id', 'title', 'defaultunit', 'tax', 'accoutingProductCategorie')
    list_display_links = ('id',)
    list_filter = ('title',)
    ordering = ('id', 'title',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('productNumber', 'title', 'description', 'defaultunit', 'tax', 'accoutingProductCategorie',
                       'cancelationPeriod', 'automaticContractExtension', 'automaticContractExtensionReminder',
                       'minimumDuration', 'paymentIntervall', 'contractDocument')
        }),
    )


def createSubscription(a, request, queryset):
    for contract in queryset:
        subscription = Subscription()
        subscription.createSubscriptionFromContract(crmmodels.Contract.objects.get(id=contract.id))
        response = HttpResponseRedirect('/admin/subscriptions/' + str(subscription.id))
    return response


createSubscription.short_description = _("Create Subscription")


class KoalixcrmPluginInterface(object):
    contractInlines = [InlineSubscription]
    contractActions = [createSubscription]
    invoiceInlines = []
    invoiceActions = []
    quoteInlines = []
    quoteActions = []
    customerInlines = []
    customerActions = []


admin.site.register(Subscription, OptionSubscription)
admin.site.register(SubscriptionType, OptionSubscriptionType)
