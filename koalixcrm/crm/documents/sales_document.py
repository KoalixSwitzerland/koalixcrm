# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin, messages
from django.utils.translation import gettext as _
from koalixcrm.crm.const.purpose import *
from koalixcrm.global_support_functions import xstr, make_date_utc
from koalixcrm.crm.contact.phone_address import PhoneAddress
from koalixcrm.crm.contact.email_address import EmailAddress
from koalixcrm.crm.contact.postal_address import PostalAddress
from koalixcrm.crm.documents.sales_document_position import SalesDocumentPosition, SalesDocumentInlinePosition
from koalixcrm.djangoUserExtension.models import TextParagraphInDocumentTemplate, UserExtension
from koalixcrm.crm.product.product_type import ProductType
from koalixcrm.crm.exceptions import TemplateSetMissingInContract
import koalixcrm.crm.documents.calculations
from koalixcrm.crm.documents.pdf_export import PDFExport


class TextParagraphInSalesDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    sales_document = models.ForeignKey("SalesDocument", on_delete=models.CASCADE)
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=2, choices=PURPOSESTEXTPARAGRAPHINDOCUMENTS)
    text_paragraph = models.TextField(verbose_name=_("Text"), blank=False, null=False)

    def create_paragraph(self, default_paragraph, sales_document):
        self.sales_document = sales_document
        self.purpose = default_paragraph.purpose
        self.text_paragraph = default_paragraph.text_paragraph
        self.save()
        return

    class Meta:
        app_label = "crm"
        verbose_name = _('Text Paragraph In Sales Document')
        verbose_name_plural = _('Text Paragraphs In Sales Documents')

    def __str__(self):
        return self.id.__str__()


class SalesDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    contract = models.ForeignKey("Contract",
                                 on_delete=models.CASCADE,
                                 verbose_name=_('Contract'))
    external_reference = models.CharField(verbose_name=_("External Reference"),
                                          max_length=100,
                                          blank=True)
    discount = models.DecimalField(max_digits=5,
                                   decimal_places=2,
                                   verbose_name=_("Discount"),
                                   blank=True,
                                   null=True)
    description = models.CharField(verbose_name=_("Description"),
                                   max_length=100,
                                   blank=True,
                                   null=True)
    last_pricing_date = models.DateField(verbose_name=_("Pricing Date"),
                                         blank=True,
                                         null=True)
    last_calculated_price = models.DecimalField(max_digits=17,
                                                decimal_places=2,
                                                verbose_name=_("Price without Tax "),
                                                blank=True,
                                                null=True)
    last_calculated_tax = models.DecimalField(max_digits=17,
                                              decimal_places=2,
                                              verbose_name=_("Tax"),
                                              blank=True,
                                              null=True)
    customer = models.ForeignKey("Customer",
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Customer"))
    staff = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              limit_choices_to={'is_staff': True},
                              blank=True,
                              verbose_name=_("Staff"),
                              related_name="db_relscstaff",
                              null=True)
    currency = models.ForeignKey("Currency", on_delete=models.CASCADE, verbose_name=_("Currency"),
                                 blank=False, null=False)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    custom_date_field = models.DateField(verbose_name=_("Custom Date"),
                                         blank=True,
                                         null=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         related_name="db_lstscmodified",
                                         null=True,
                                         blank="True")
    template_set = models.ForeignKey("djangoUserExtension.DocumentTemplate",
                                     on_delete=models.CASCADE,
                                     verbose_name=_("Referred Template"),
                                     null=True,
                                     blank=True)
    derived_from_sales_document = models.ForeignKey("SalesDocument",
                                                    on_delete=models.CASCADE,
                                                    blank=True,
                                                    null=True)
    last_print_date = models.DateTimeField(verbose_name=_("Last printed"),
                                           blank=True,
                                           null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Sales Document')
        verbose_name_plural = _('Sales Documents')

    def serialize_to_xml(self):
        from koalixcrm.crm.models import PostalAddressForContact
        from koalixcrm.crm.models import Currency
        from koalixcrm.crm.models import PurchaseOrder
        from koalixcrm.crm.models import SalesDocument
        from koalixcrm.crm.models import SalesDocumentPosition
        from koalixcrm.crm.models import Contact
        from django.contrib import auth
        objects = [self, ]
        position_class = SalesDocumentPosition
        objects += list(SalesDocument.objects.filter(id=self.id))
        if isinstance(self, PurchaseOrder):
            objects += list(Contact.objects.filter(id=self.supplier.id))
            objects += list(PostalAddressForContact.objects.filter(person=self.supplier.id))
            for address in list(PostalAddressForContact.objects.filter(person=self.supplier.id)):
                objects += list(PostalAddress.objects.filter(id=address.id))
        else:
            objects += list(Contact.objects.filter(id=self.customer.id))
            objects += list(PostalAddressForContact.objects.filter(person=self.customer.id))
            for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
                objects += list(PostalAddress.objects.filter(id=address.id))
        objects += list(TextParagraphInSalesDocument.objects.filter(sales_document=self.id))
        objects += list(Currency.objects.filter(id=self.currency.id))
        objects += SalesDocumentPosition.add_positions(position_class, self)
        objects += list(auth.models.User.objects.filter(id=self.staff.id))
        objects += UserExtension.objects_to_serialize(self, self.staff)
        main_xml = PDFExport.write_xml(objects)
        return main_xml

    def is_complete_with_price(self):
        """ Checks whether the SalesContract is completed with a price, in case the
        SalesContract was not completed or the price calculation was not performed,
        the method returns false"""

        if self.last_pricing_date and self.last_calculated_price:
            return True
        else:
            return False

    def create_sales_document(self, calling_model):
        self.staff = calling_model.staff
        if isinstance(calling_model, koalixcrm.crm.documents.contract.Contract):
            self.contract = calling_model
            self.customer = calling_model.default_customer
            self.currency = calling_model.default_currency
            self.description = calling_model.description
            self.discount = 0
        elif isinstance(calling_model, SalesDocument):
            self.derived_from_sales_document = calling_model
            self.contract = calling_model.contract
            self.customer = calling_model.customer
            self.currency = calling_model.currency
            self.description = calling_model.description
            self.discount = calling_model.discount

    def attach_text_paragraphs(self):
        default_paragraphs = TextParagraphInDocumentTemplate.objects.filter(document_template=self.template_set)
        for default_paragraph in list(default_paragraphs):
            invoice_paragraph = TextParagraphInSalesDocument()
            invoice_paragraph.create_paragraph(default_paragraph, self)

    def attach_sales_document_positions(self, calling_model):
        if isinstance(calling_model, SalesDocument):
            sales_document_positions = SalesDocumentPosition.objects.filter(sales_document=calling_model.id)
            for sales_document_position in list(sales_document_positions):
                new_position = SalesDocumentPosition()
                new_position.create_position(sales_document_position, self)

    def create_pdf(self, template_set, printed_by):
        self.last_print_date = make_date_utc(datetime.now())
        self.save()
        return koalixcrm.crm.documents.pdf_export.PDFExport.create_pdf(self, template_set, printed_by)

    def get_template_set(self):
        if self.template_set:
            return self.template_set
        else:
            raise TemplateSetMissingInContract((_("Template Set missing in Sales Document" + str(self))))

    def get_fop_config_file(self, template_set):
        template_set = self.get_template_set()
        return template_set.get_fop_config_file()

    def get_xsl_file(self, template_set):
        template_set = self.get_template_set()
        return template_set.get_xsl_file()

    def __str__(self):
        return _("Sales Contract") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)


class PostalAddressForSalesDocument(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    sales_document = models.ForeignKey("SalesDocument", on_delete=models.CASCADE)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Sales Documents')
        verbose_name_plural = _('Postal Address For Sales Documents')

    def __str__(self):
        return xstr(self.pre_name) + ' ' + xstr(self.name) + ' ' + xstr(self.address_line_1)


class EmailAddressForSalesDocument(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    sales_document = models.ForeignKey("SalesDocument", on_delete=models.CASCADE)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Sales Documents')
        verbose_name_plural = _('Email Address For Sales Documents')

    def __str__(self):
        return str(self.email)


class PhoneAddressForSalesDocument(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    sales_document = models.ForeignKey("SalesDocument", on_delete=models.CASCADE)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Sales Documents')
        verbose_name_plural = _('Phone Address For Sales Documents')

    def __str__(self):
        return str(self.phone)


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
            koalixcrm.crm.documents.calculations.Calculations.calculate_document_price(obj, date.today())
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
                                                                 koalixcrm.crm.documents.quote.Quote,
                                                                 ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_quote.short_description = _("Create Quote")

    def create_invoice(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.crm.documents.invoice.Invoice,
                                                                 ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_invoice.short_description = _("Create Invoice")

    def create_purchase_confirmation(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.crm.documents.purchase_confirmation.PurchaseConfirmation,
                                                                 ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_purchase_confirmation.short_description = _("Create Purchase Confirmation")

    def create_delivery_note(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.crm.documents.delivery_note.DeliveryNote,
                                                                 ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_delivery_note.short_description = _("Create Delivery note")

    def create_payment_reminder(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.crm.documents.payment_reminder.PaymentReminder,
                                                                 ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_payment_reminder.short_description = _("Create Payment Reminder")

    def create_purchase_order(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self,
                                                                 request,
                                                                 obj,
                                                                 koalixcrm.crm.documents.purchase_order.PurchaseOrder,
                                                                 ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_purchase_order.short_description = _("Create Purchase Order")

    def create_pdf(self, request, queryset):
        from koalixcrm.crm.views.pdfexport import PDFExportView
        for obj in queryset:
            response = PDFExportView.export_pdf(self,
                                                request,
                                                obj,
                                                ("/admin/crm/"+obj.__class__.__name__.lower()+"/"),
                                                obj.template_set)
            return response

    create_pdf.short_description = _("Create PDF")

    def create_project(self, request, queryset):
        from koalixcrm.crm.views.create_task import CreateTaskView
        for obj in queryset:
            response = CreateTaskView.create_project(self,
                                                     request,
                                                     obj,
                                                     ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_project.short_description = _("Create Project")
