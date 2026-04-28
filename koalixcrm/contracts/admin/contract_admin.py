# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.utils.translation import gettext as _

import koalixcrm.contracts.models.credit_note
import koalixcrm.contracts.models.despatch_advice
import koalixcrm.contracts.models.invoice
import koalixcrm.contracts.models.payment_reminder
import koalixcrm.contracts.models.purchase_order
import koalixcrm.contracts.models.quotation
import koalixcrm.contracts.models.sales_order
from koalixcrm.contracts.admin.credit_note_admin import InlineCreditNote
from koalixcrm.contracts.admin.invoice_admin import InlineInvoice
from koalixcrm.contracts.admin.quotation_admin import InlineQuotation
from koalixcrm.contracts.models.contract import (
    ContractAddressAssignment,
    ContractEmailAssignment,
    ContractPhoneAssignment,
)
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.plugin import *

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.forms import ModelForm
    from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

    from koalixcrm.contracts.models.contract import Contract


class ContractPostalAddress(admin.StackedInline):
    model = ContractAddressAssignment
    extra = 1
    classes = ['collapse']
    raw_id_fields = ('address',)
    fieldsets = (
        ('Basics', {
            'fields': ('address',
                       'purpose',
                       'is_primary',
                       'valid_from',
                       'valid_to'),
        }),
    )
    allow_add = True


class ContractPhoneAddress(admin.TabularInline):
    model = ContractPhoneAssignment
    extra = 1
    classes = ['collapse']
    raw_id_fields = ('phone_number',)
    fieldsets = (
        ('Basics', {
            'fields': ('phone_number', 'purpose', 'is_primary',)
        }),
    )
    allow_add = True


class ContractEmailAddress(admin.TabularInline):
    model = ContractEmailAssignment
    extra = 1
    classes = ['collapse']
    raw_id_fields = ('email',)
    fieldsets = (
        ('Basics', {
            'fields': ('email',
                       'purpose',
                       'is_primary',)
        }),
    )
    allow_add = True


class OptionContract(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'buyer_party',
                    'supplier_party',
                    'staff',
                    'default_currency',
                    'date_of_creation',
                    'last_modification',
                    'last_modified_by')
    list_display_links = ('id',)
    list_filter = ('workspace',
                   'buyer_party',
                   'supplier_party',
                   'staff',
                   'default_currency')
    ordering = ('id', )
    search_fields = ('id',
                     'contract')
    fieldsets = (
        (_('Basics'), {
            'fields': ('description',
                       'buyer_party',
                       'staff',
                       'supplier_party',
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

    def create_quotation(self, request: HttpRequest, queryset: QuerySet[Contract]) -> HttpResponse | HttpResponseRedirect | None:
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.quotation.Quotation,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_quotation.short_description = _("Create Quotation")

    def create_invoice(self, request: HttpRequest, queryset: QuerySet[Contract]) -> HttpResponse | HttpResponseRedirect | None:
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.invoice.Invoice,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_invoice.short_description = _("Create Invoice")

    def create_sales_order(self, request: HttpRequest, queryset: QuerySet[Contract]) -> HttpResponse | HttpResponseRedirect | None:
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.sales_order.SalesOrder,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_sales_order.short_description = _("Create Sales Order")

    def create_despatch_advice(self, request: HttpRequest, queryset: QuerySet[Contract]) -> HttpResponse | HttpResponseRedirect | None:
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.despatch_advice.DespatchAdvice,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_despatch_advice.short_description = _("Create Despatch Advice")

    def create_payment_reminder(self, request: HttpRequest, queryset: QuerySet[Contract]) -> HttpResponse | HttpResponseRedirect | None:
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.payment_reminder.PaymentReminder,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_payment_reminder.short_description = _("Create Payment Reminder")

    def create_purchase_order(self, request: HttpRequest, queryset: QuerySet[Contract]) -> HttpResponse | HttpResponseRedirect | None:
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.contracts.models.purchase_order.PurchaseOrder,
                                                                 ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_purchase_order.short_description = _("Create Purchase Order")

    def save_model(self, request: HttpRequest, obj: Contract, form: ModelForm, change: bool) -> None:
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    def create_credit_note(self, request: HttpRequest, queryset: QuerySet[Contract]) -> HttpResponse | HttpResponseRedirect | None:
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
