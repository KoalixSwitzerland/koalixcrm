# -*- coding: utf-8 -*-
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from koalixcrm.subscriptions.models import *


class AdminSubscriptionEvent(admin.TabularInline):
    model = SubscriptionEvent
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': (
                'event_date',
                'event',)
        }),
    )
    allow_add = True


class InlineSubscription(admin.TabularInline):
    model = Subscription
    extra = 1
    classes = ('collapse-open',)
    readonly_fields = ('contract',
                       'subscription_type')
    fieldsets = (
        (_('Basics'), {
            'fields': (
                'contract',
                'subscription_type')
        }),
    )
    allow_add = False


class OptionSubscription(admin.ModelAdmin):
    list_display = ('id',
                    'contract',
                    'subscription_type',)
    ordering = ('id',
                'contract',
                'subscription_type')
    search_fields = ('id',
                     'contract',)
    fieldsets = (
        (_('Basics'), {
            'fields': (
                'contract',
                'subscription_type',)
        }),
    )
    inlines = [AdminSubscriptionEvent]

    @staticmethod
    def create_invoice(queryset):
        for obj in queryset:
            invoice = obj.create_invoice()
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
        return response
    create_invoice.short_description = _("Create Invoice")

    @staticmethod
    def create_quote(queryset):
        for obj in queryset:
            invoice = obj.create_invoice()
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
        return response

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    actions = ['create_subscription_pdf', 'create_invoice']


class OptionSubscriptionType(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    ordering = ('id', )
    search_fields = ('id',)
    fieldsets = (
        (_('Basics'), {
            'fields': (
                'cancellation_period',
                'automatic_contract_extension',
                'automatic_contract_extension_reminder',
                'minimum_duration',
                'payment_interval',
                'contract_document')
        }),
    )


def create_subscription(a, request, queryset):
    for contract in queryset:
        subscription = Subscription()
        subscription.create_subscription_from_contract(crmmodels.Contract.objects.get(id=contract.id))
        response = HttpResponseRedirect('/admin/subscriptions/' + str(subscription.id))
    return response


create_subscription.short_description = _("Create Subscription")


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
