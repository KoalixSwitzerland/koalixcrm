# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.crm.documents.salescontract import SalesContract
from django.contrib import messages
from koalixcrm.plugin import *
from koalixcrm.crm.views import export_pdf
from koalixcrm.crm.documents.salescontract import SalesContractTextParagraph
from koalixcrm.crm.documents.salescontract import SalesContractPostalAddress
from koalixcrm.crm.documents.salescontract import SalesContractPhoneAddress
from koalixcrm.crm.documents.salescontract import SalesContractEmailAddress
from koalixcrm.crm.documents.salescontractposition import SalesContractInlinePosition
from koalixcrm.crm.product.product import Product
import koalixcrm.crm.documents.calculations
import koalixcrm.crm.documents.invoice
import koalixcrm.crm.documents.pdfexport


class Quote(SalesContract):
    valid_until = models.DateField(verbose_name=_("Valid until"))
    status = models.CharField(max_length=1, choices=QUOTESTATUS, verbose_name=_('Status'))

    def create_invoice(self):
        invoice = koalixcrm.crm.documents.invoice.Invoice()
        invoice.create_invoice(self)
        return invoice

    def create_purchase_confirmation(self):
        purchase_confirmation = koalixcrm.crm.documents.purchaseconfirmation.PurchaseConfirmation()
        purchase_confirmation.create_purchase_confirmation(self)
        return purchase_confirmation

    def create_delivery_note(self):
        delivery_note = koalixcrm.crm.documents.deliverynote.DeliveryNote()
        delivery_note.create_delivery_note(self)
        return delivery_note

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

    def create_pdf(self):
        self.last_print_date = datetime.now()
        self.save()
        return koalixcrm.crm.documents.pdfexport.PDFExport.create_pdf(self)

    def __str__(self):
        return _("Quote") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')


class OptionQuote(admin.ModelAdmin):
    list_display = (
    'id', 'description', 'contract', 'customer', 'currency', 'valid_until', 'status', 'staff', 'last_modified_by',
    'last_calculated_price', 'last_calculated_tax', 'last_pricing_date', 'last_modification', 'last_print_date')
    list_display_links = ('id',)
    list_filter = ('customer', 'contract', 'currency', 'staff', 'status', 'last_modification')
    ordering = ('id',)
    search_fields = ('contract__id', 'customer__name', 'currency__description')

    fieldsets = (
        (_('Basics'), {
            'fields': ('contract', 'description', 'customer', 'currency', 'discount',
                       'valid_until', 'staff', 'status', 'external_reference', 'template_set')
        }),
    )
    save_as = True
    inlines = [SalesContractInlinePosition, SalesContractTextParagraph,
               SalesContractPostalAddress, SalesContractPhoneAddress,
               SalesContractEmailAddress]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteInlines"))

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionQuote, self).response_add(request, obj)

    def response_change(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionQuote, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, request, obj):
        try:
            koalixcrm.crm.documents.calculations.Calculations.calculate_document_price(obj, date.today())
            self.message_user(request, "Successfully calculated Prices")
        except Product.NoPriceFound as e:
            self.message_user(request, "Unsuccessful in updating the Prices " + e.__str__(), level=messages.ERROR)
        return obj

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    def create_invoice(self, request, queryset):
        for obj in queryset:
            invoice = obj.create_invoice()
            self.message_user(request, _("Invoice created"))
            response = HttpResponseRedirect('/admin/crm/invoice/' + str(invoice.id))
        return response

    create_invoice.short_description = _("Create Invoice")

    def create_purchase_confirmation(self, request, queryset):
        for obj in queryset:
            purchase_confirmation = obj.create_purchase_confirmation()
            self.message_user(request, _("Purchase confirmation created"))
            response = HttpResponseRedirect('/admin/crm/purchaseconfirmation/' + str(purchase_confirmation.id))
        return response

        create_purchase_confirmation.short_description = _("Create Purchase confirmation")

    def create_delivery_note(self, request, queryset):
        for obj in queryset:
            delivery_note = obj.create_delivery_note()
            self.message_user(request, _("Delivery note created"))
            response = HttpResponseRedirect('/admin/crm/deliverynote/' + str(delivery_note.id))
        return response

    create_delivery_note.short_description = _("Create Delivery note")

    def create_pdf(self, request, queryset):
        for obj in queryset:
            response = export_pdf(self, request, obj, "/admin/crm/quote/")
            return response

    create_pdf.short_description = _("Create PDF of Quote")

    actions = ['create_purchase_confirmation','create_invoice',
               'create_delivery_note', 'create_pdf']
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteActions"))


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
