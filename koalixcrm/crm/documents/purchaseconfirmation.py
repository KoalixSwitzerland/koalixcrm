# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.documents.salesdocument import SalesDocumentTextParagraph
from koalixcrm.crm.documents.salesdocument import SalesDocumentPostalAddress
from koalixcrm.crm.documents.salesdocument import SalesDocumentPhoneAddress
from koalixcrm.crm.documents.salesdocument import SalesDocumentEmailAddress
from koalixcrm.crm.documents.salesdocumentposition import SalesDocumentInlinePosition
from koalixcrm.crm.documents.salesdocument import SalesDocument
from koalixcrm.crm.product.product import Product
from koalixcrm.crm.views import export_pdf

import koalixcrm.crm.documents.pdfexport
import koalixcrm.crm.documents.calculations


class PurchaseConfirmation(SalesDocument):
    derived_from_quote = models.ForeignKey("Quote", blank=True, null=True)

    def create_purchase_confirmation(self, calling_model):
        """Checks which model was calling the function. Depending on the calling
        model, the function sets up a purchase confirmation. On success, the
        purchase confirmation is saved.
        At the moment only the koalixcrm.crm.documents.contract.Contract and
        koalixcrm.crm.documents.quote.Quote are allowed to call this function"""

        self.staff = calling_model.staff
        if type(calling_model) == koalixcrm.crm.documents.contract.Contract:
            self.contract = calling_model
            self.customer = calling_model.default_customer
            self.currency = calling_model.default_currency
            self.description = calling_model.description
            self.template_set = calling_model.default_template_set.purchase_confirmation_template
            self.discount = 0
        elif type(calling_model) == koalixcrm.crm.documents.quote.Quote:
            self.derived_from_quote = calling_model
            self.copy_sales_document(calling_model)

        self.date_of_creation = date.today().__str__()
        self.save()

    def create_pdf(self):
        self.last_print_date = datetime.now()
        self.save()
        return koalixcrm.crm.documents.pdfexport.PDFExport.create_pdf(self)

    def __str__(self):
        return _("Purchase Confirmation") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Purchase Confirmation')
        verbose_name_plural = _('Purchase Confirmations')


class OptionPurchaseConfirmation(admin.ModelAdmin):
    list_display = (
    'id', 'description', 'contract', 'customer', 'currency', 'staff',
    'last_calculated_price', 'last_calculated_tax', 'last_pricing_date', 'last_modification',
    'last_modified_by', 'last_print_date')
    list_display_links = ('id', )
    list_filter = ('customer', 'contract', 'staff', 'currency', 'last_modification')
    ordering = ('id',)
    search_fields = ('contract__id', 'customer__name', 'currency__description')
    fieldsets = (
        (_('Basics'), {
            'fields': ('contract', 'description', 'customer', 'currency', 'discount',
                       'external_reference', 'template_set' )
        }),
    )
    save_as = True
    inlines = [SalesDocumentInlinePosition, SalesDocumentTextParagraph,
               SalesDocumentPostalAddress, SalesDocumentPhoneAddress,
               SalesDocumentEmailAddress]

    def response_add(self, request, obj, post_url_continue=None):
        new_obj = self.after_saving_model_and_related_inlines(request, obj)
        return super(OptionPurchaseConfirmation, self).response_add(request, new_obj)

    def response_change(self, request, obj):
        new_obj = self.after_saving_model_and_related_inlines(request, obj)
        return super(OptionPurchaseConfirmation, self).response_add(request, new_obj)

    def after_saving_model_and_related_inlines(self, request, obj):
        try:
            koalixcrm.crm.documents.calculations.Calculations.calculate_document_price(obj, date.today())
            self.message_user(request, "Successfully calculated Prices")
        except Product.NoPriceFound as e:
            self.message_user(request, "Unsuccessfull in updating the Prices " + e.__str__(), level=messages.ERROR)
        return obj

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

    def create_pdf(self, request, queryset):
        for obj in queryset:
            response = export_pdf(self, request, obj, "/admin/crm/purchaseconfirmation/")
            return response

    create_pdf.short_description = _("Create PDF of Purchase Confirmation")

    actions = ['create_pdf']