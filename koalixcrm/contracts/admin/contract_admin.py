# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.plugin import *
from koalixcrm.contracts.models.contract import (
    PostalAddressForContract,
    PhoneAddressForContract,
    EmailAddressForContract,
)
from koalixcrm.contracts.admin.quote_admin import InlineQuote
from koalixcrm.contracts.admin.invoice_admin import InlineInvoice
import koalixcrm.contracts.models.quote
import koalixcrm.contracts.models.invoice
import koalixcrm.contracts.models.purchase_confirmation
import koalixcrm.contracts.models.delivery_note
import koalixcrm.contracts.models.payment_reminder
import koalixcrm.contracts.models.purchase_order


class ContractPostalAddress(admin.StackedInline):
    model = PostalAddressForContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('prefix',
                       'pre_name',
                       'name',
                       'address_line_1',
                       'address_line_2',
                       'address_line_3',
                       'address_line_4',
                       'zip_code',
                       'town',
                       'state',
                       'country',
                       'purpose'),
        }),
    )
    allow_add = True


class ContractPhoneAddress(admin.TabularInline):
    model = PhoneAddressForContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class ContractEmailAddress(admin.TabularInline):
    model = EmailAddressForContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email',
                       'purpose',)
        }),
    )
    allow_add = True


class OptionContract(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'default_customer',
                    'default_supplier',
                    'staff',
                    'default_currency',
                    'date_of_creation',
                    'last_modification',
                    'last_modified_by')
    list_display_links = ('id',)
    list_filter = ('default_customer',
                   'default_supplier',
                   'staff',
                   'default_currency')
    ordering = ('id', )
    search_fields = ('id',
                     'contract')
    fieldsets = (
        (_('Basics'), {
            'fields': ('description',
                       'default_customer',
                       'staff',
                       'default_supplier',
                       'default_currency',
                       'default_template_set')
        }),
    )
    inlines = [ContractPostalAddress,
               ContractPhoneAddress,
               ContractEmailAddress,
               InlineQuote,
               InlineInvoice]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("contractInlines"))

    def create_quote(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contract_object_management.models.quote.Quote,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_quote.short_description = _("Create Quote")

    def create_invoice(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contract_object_management.models.invoice.Invoice,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_invoice.short_description = _("Create Invoice")

    def create_purchase_confirmation(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contract_object_management.models.purchase_confirmation.PurchaseConfirmation,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_purchase_confirmation.short_description = _("Create Purchase Confirmation")

    def create_delivery_note(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contract_object_management.models.delivery_note.DeliveryNote,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_delivery_note.short_description = _("Create Delivery note")

    def create_payment_reminder(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contract_object_management.models.payment_reminder.PaymentReminder,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_payment_reminder.short_description = _("Create Payment Reminder")

    def create_purchase_order(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contract_object_management.models.purchase_order.PurchaseOrder,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_purchase_order.short_description = _("Create Purchase Order")

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    actions = ['create_quote',
               'create_invoice',
               'create_purchase_order']
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("contractActions"))
