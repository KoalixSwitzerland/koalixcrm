# -*- coding: utf-8 -*-

from datetime import *
from django.contrib import admin, messages
from django.utils.translation import gettext as _
from koalixcrm.contracts.models.commercial_document import (
    TextParagraphInCommercialDocument,
    PostalAddressForCommercialDocument,
    EmailAddressForCommercialDocument,
    PhoneAddressForCommercialDocument,
)
from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition
from koalixcrm.contracts.admin.commercial_document_position_admin import CommercialDocumentInlinePosition
from koalixcrm.contracts.admin.commercial_document_media_admin import CommercialDocumentMediaInline
from koalixcrm.products.models.product_type import ProductType
import koalixcrm.contracts.models.calculations


class CommercialDocumentTextParagraph(admin.StackedInline):
    model = TextParagraphInCommercialDocument
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('text_paragraph', 'purpose', )
        }),
    )
    allow_add = True


class CommercialDocumentPostalAddress(admin.StackedInline):
    model = PostalAddressForCommercialDocument
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


class CommercialDocumentPhoneAddress(admin.TabularInline):
    model = PhoneAddressForCommercialDocument
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class CommercialDocumentEmailAddress(admin.TabularInline):
    model = EmailAddressForCommercialDocument
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class OptionCommercialDocument(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'contract',
                    'party',
                    'currency',
                    'staff',
                    'last_modified_by',
                    'last_calculated_price',
                    'last_calculated_tax',
                    'last_pricing_date',
                    'last_modification',
                    'last_print_date')
    list_display_links = ('id',)
    list_filter = ('party',
                   'contract',
                   'currency',
                   'staff',
                   'last_modification')
    ordering = ('-id',)
    search_fields = ('contract__id',
                     'party__display_name',
                     'currency__description')

    fieldsets = (
        (_('Sales Contract'), {
            'fields': ('contract',
                       'description',
                       'party',
                       'currency',
                       'discount',
                       'staff',
                       'external_reference',
                       'template_set',
                       'custom_date_field')
        }),
    )
    save_as = True
    inlines = [CommercialDocumentInlinePosition, CommercialDocumentTextParagraph,
               CommercialDocumentPostalAddress, CommercialDocumentPhoneAddress,
               CommercialDocumentEmailAddress, CommercialDocumentMediaInline]

    def response_add(self, request, obj, post_url_continue=None):
        new_obj = self.after_saving_model_and_related_inlines(request, obj)
        new_obj.custom_date_field = date.today().__str__()
        return super(OptionCommercialDocument, self).response_add(request=request,
                                                             obj=new_obj,
                                                             post_url_continue=post_url_continue)

    def response_change(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionCommercialDocument, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, request, obj):
        try:
            koalixcrm.contracts.models.calculations.Calculations.calculate_document_price(obj, date.today())
            self.message_user(request, "Successfully calculated Prices")
        except (ProductType.NoPriceFound, CommercialDocumentPosition.NoPriceFound) as e:
            self.message_user(request, "Unsuccessful in updating the Prices " + e.__str__(), level=messages.ERROR)
        return obj

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()

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

    def create_pdf(self, request, queryset):
        from koalixcrm.core.views.pdfexport import PDFExportView
        for obj in queryset:
            response = PDFExportView.export_pdf(self,
                                                request,
                                                obj,
                                                ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"),
                                                obj.template_set)
            return response

    create_pdf.short_description = _("Create PDF")

    def create_pdf_async(self, request, queryset):
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        queued = 0
        for obj in queryset:
            if not obj.template_set:
                self.message_user(
                    request,
                    _("Template-set missing for %(doc)s") % {"doc": obj},
                    level=messages.ERROR,
                )
                continue
            PDFExportProcess.objects.create(
                source_model=obj.__class__.__name__,
                source_id=obj.id,
                template_set=obj.template_set,
                triggered_by=request.user,
            )
            queued += 1
        if queued:
            self.message_user(
                request,
                _("%(count)d PDF export job(s) queued. Check PDF Export Processes for status.") % {"count": queued},
                level=messages.SUCCESS,
            )

    create_pdf_async.short_description = _("Create PDF")

    def create_project(self, request, queryset):
        from koalixcrm.reporting.views.create_task import CreateTaskView
        for obj in queryset:
            response = CreateTaskView.create_project(self,
                                                     request,
                                                     obj,
                                                     ("/admin/contract_object_management/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_project.short_description = _("Create Project")
