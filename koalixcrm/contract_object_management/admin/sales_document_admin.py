# -*- coding: utf-8 -*-

from datetime import *
from django.contrib import admin, messages
from django.utils.translation import gettext as _
from koalixcrm.contract_object_management.models.sales_document import (
    TextParagraphInSalesDocument,
    PostalAddressForSalesDocument,
    EmailAddressForSalesDocument,
    PhoneAddressForSalesDocument,
)
from koalixcrm.contract_object_management.models.sales_document_position import SalesDocumentPosition
from koalixcrm.contract_object_management.admin.sales_document_position_admin import SalesDocumentInlinePosition
from koalixcrm.products.models.product_type import ProductType
import koalixcrm.contract_object_management.models.calculations


class SalesDocumentTextParagraph(admin.StackedInline):
    model = TextParagraphInSalesDocument
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('text_paragraph', 'purpose', )
        }),
    )
    allow_add = True


class SalesDocumentPostalAddress(admin.StackedInline):
    model = PostalAddressForSalesDocument
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
                       'purpose')
        }),
    )
    allow_add = True


class SalesDocumentPhoneAddress(admin.TabularInline):
    model = PhoneAddressForSalesDocument
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class SalesDocumentEmailAddress(admin.TabularInline):
    model = EmailAddressForSalesDocument
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class OptionSalesDocument(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'contract',
                    'customer',
                    'currency',
                    'staff',
                    'last_modified_by',
                    'last_calculated_price',
                    'last_calculated_tax',
                    'last_pricing_date',
                    'last_modification',
                    'last_print_date')
    list_display_links = ('id',)
    list_filter = ('customer',
                   'contract',
                   'currency',
                   'staff',
                   'last_modification')
    ordering = ('-id',)
    search_fields = ('contract__id',
                     'customer__name',
                     'currency__description')

    fieldsets = (
        (_('Sales Contract'), {
            'fields': ('contract',
                       'description',
                       'customer',
                       'currency',
                       'discount',
                       'staff',
                       'external_reference',
                       'template_set',
                       'custom_date_field')
        }),
    )
    save_as = True
    inlines = [SalesDocumentInlinePosition, SalesDocumentTextParagraph,
               SalesDocumentPostalAddress, SalesDocumentPhoneAddress,
               SalesDocumentEmailAddress]

    def response_add(self, request, obj, post_url_continue=None):
        new_obj = self.after_saving_model_and_related_inlines(request, obj)
        new_obj.custom_date_field = date.today().__str__()
        return super(OptionSalesDocument, self).response_add(request=request,
                                                             obj=new_obj,
                                                             post_url_continue=post_url_continue)

    def response_change(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionSalesDocument, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, request, obj):
        try:
            koalixcrm.contract_object_management.models.calculations.Calculations.calculate_document_price(obj, date.today())
            self.message_user(request, "Successfully calculated Prices")
        except (ProductType.NoPriceFound, SalesDocumentPosition.NoPriceFound) as e:
            self.message_user(request, "Unsuccessful in updating the Prices " + e.__str__(), level=messages.ERROR)
        return obj

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

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

    def create_pdf(self, request, queryset):
        from koalixcrm.crm.views.pdfexport import PDFExportView
        for obj in queryset:
            response = PDFExportView.export_pdf(self,
                                                request,
                                                obj,
                                                ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"),
                                                obj.template_set)
            return response

    create_pdf.short_description = _("Create PDF")

    def create_project(self, request, queryset):
        from koalixcrm.crm.views.create_task import CreateTaskView
        for obj in queryset:
            response = CreateTaskView.create_project(self,
                                                     request,
                                                     obj,
                                                     ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_project.short_description = _("Create Project")
