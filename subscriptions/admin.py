# -*- coding: utf-8 -*-

from django.contrib import admin
from django.http import HttpResponseRedirect

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


class InlineSubscription(admin.TabularInline):
    model = Subscription
    extra = 1
    classes = ('collapse-open',)
    readonly_fields = ('contract', 'subscriptiontype')
    fieldsets = (
        (trans('Basics'), {
            'fields': ('contract', 'subscriptiontype')
        }),
    )
    allow_add = False


class OptionSubscription(admin.ModelAdmin):
    list_display = ('id', 'contract', 'subscriptiontype', )
    ordering = ('id', 'contract', 'subscriptiontype')
    search_fields = ('id', 'contract', )
    fieldsets = (
        (trans('Basics'), {
            'fields': ('contract', 'subscriptiontype',)
        }),
    )
    inlines = [AdminSubscriptionEvent]

    def create_invoice(request, queryset):
        for obj in queryset:
            invoice = obj.create_invoice()
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
            return response

    @staticmethod
    def create_quote(request, queryset):
        for obj in queryset:
            invoice = obj.create_invoice()
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
            return response

    def save_model(self, request, obj, form, change):
        if change:
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()

    create_invoice.short_description = trans("Create Invoice")

    actions = ['createSubscriptionPDF', 'create_invoice']


class OptionSubscriptionType(admin.ModelAdmin):
    list_display = ('id', 'title', 'defaultunit', 'tax', 'accoutingProductCategorie')
    list_display_links = ('id', )
    list_filter = ('title', )
    ordering = ('id', 'title',)
    search_fields = ('id', 'title')
    fieldsets = (
        (trans('Basics'), {
            'fields': ('productNumber', 'title', 'description', 'defaultunit', 'tax', 'accoutingProductCategorie',
                       'cancelationPeriod', 'automaticContractExtension', 'automaticContractExtensionReminder',
                       'minimumDuration', 'paymentIntervall', 'contractDocument')
        }),
    )


def create_subscription(a, request, queryset):
    for contract in queryset:
        subscription = Subscription()
        subscription.create_subscription_from_contract(Contract.objects.get(id=contract.id))
        response = HttpResponseRedirect('/admin/subscriptions/' + str(subscription.id))
        return response


create_subscription.short_description = trans("Create Subscription")


class KoalixcrmPluginInterface(object):
    contractInlines = [InlineSubscription]
    contractActions = [create_subscription]
    invoiceInlines = []
    invoiceActions = []
    quoteInlines = []
    quoteActions = []
    customerInlines = []
    customerActions = []


admin.site.register(Subscription, OptionSubscription)
admin.site.register(SubscriptionType, OptionSubscriptionType)