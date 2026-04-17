# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.plugin import *
from koalixcrm.contracts.models.contract import (
    PostalAddressForContract,
    PhoneAddressForContract,
    EmailAddressForContract,
)
from koalixcrm.contracts.admin.quotation_admin import InlineQuotation
from koalixcrm.contracts.admin.invoice_admin import InlineInvoice
from koalixcrm.contracts.admin.credit_note_admin import InlineCreditNote
import koalixcrm.contracts.models.quotation
import koalixcrm.contracts.models.credit_note
import koalixcrm.contracts.models.invoice
import koalixcrm.contracts.models.sales_order
import koalixcrm.contracts.models.despatch_advice
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
               InlineQuotation,
               InlineInvoice,
               InlineCreditNote]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("contractInlines"))

    def create_quotation(self, request, queryset):
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.quotation.Quotation,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_quotation.short_description = _("Create Quotation")

    def create_invoice(self, request, queryset):
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.invoice.Invoice,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_invoice.short_description = _("Create Invoice")

    def create_sales_order(self, request, queryset):
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.sales_order.SalesOrder,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_sales_order.short_description = _("Create Sales Order")

    def create_despatch_advice(self, request, queryset):
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.despatch_advice.DespatchAdvice,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_despatch_advice.short_description = _("Create Despatch Advice")

    def create_payment_reminder(self, request, queryset):
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.payment_reminder.PaymentReminder,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_payment_reminder.short_description = _("Create Payment Reminder")

    def create_purchase_order(self, request, queryset):
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.purchase_order.PurchaseOrder,
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

    def create_credit_note(self, request, queryset):
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.credit_note.CreditNote,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_credit_note.short_description = _("Create Credit Note")

    actions = ['create_quotation',
               'create_invoice',
               'create_purchase_order',
               'create_credit_note']
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("contractActions"))
