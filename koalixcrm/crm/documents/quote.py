# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.plugin import *
from koalixcrm.crm.documents.salescontract import SalesContract, OptionSalesContract


class Quote(SalesContract):
    valid_until = models.DateField(verbose_name=_("Valid until"))
    status = models.CharField(max_length=1, choices=QUOTESTATUS, verbose_name=_('Status'))

    def create_quote(self, calling_model):
        self.discount = 0
        self.contract = calling_model
        self.staff = calling_model.staff
        self.customer = calling_model.default_customer
        self.currency = calling_model.default_currency
        self.template_set = calling_model.default_template_set.quote_template
        self.status = 'I'
        self.valid_until = date.today().__str__()
        self.date_of_creation = date.today().__str__()
        self.save()

    def __str__(self):
        return _("Quote") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')


class OptionQuote(OptionSalesContract):
    list_display = OptionSalesContract.list_display + ('valid_until', 'status',)
    list_filter = OptionSalesContract.list_filter + ('status',)
    ordering = OptionSalesContract.ordering
    search_fields = OptionSalesContract.search_fields
    fieldsets = OptionSalesContract.fieldsets + (
        (_('Quote specific'), {
            'fields': ( 'valid_until', 'status', )
        }),
    )

    save_as = OptionSalesContract.save_as
    inlines = OptionSalesContract.inlines

    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteInlines"))


class InlineQuote(admin.TabularInline):
    model = Quote
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = (
    'description', 'contract', 'customer', 'valid_until', 'status', 'last_pricing_date', 'last_calculated_price',
    'last_calculated_tax',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('description', 'contract', 'customer', 'valid_until', 'status')
        }),
        (_('Advanced (not editable)'), {
            'classes': ('collapse',),
            'fields': ('last_pricing_date', 'last_calculated_price', 'last_calculated_tax',)
        }),
    )
    allow_add = False
