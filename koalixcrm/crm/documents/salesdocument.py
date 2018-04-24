# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin, messages
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.purpose import *
from koalixcrm.globalSupportFunctions import xstr
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.documents.salesdocumentposition import SalesDocumentPosition, SalesDocumentInlinePosition
from koalixcrm.djangoUserExtension.models import TextParagraphInDocumentTemplate, UserExtension
from koalixcrm.crm.product.product import Product
from koalixcrm.crm.exceptions import TemplateSetMissingInContract
import koalixcrm.crm.documents.calculations
import koalixcrm.crm.documents.pdfexport


class TextParagraphInSalesDocument(models.Model):
    sales_document = models.ForeignKey("SalesDocument")
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
        return str(self.id)


class SalesDocument(models.Model):
    contract = models.ForeignKey("Contract", verbose_name=_('Contract'))
    external_reference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    last_pricing_date = models.DateField(verbose_name=_("Pricing Date"), blank=True, null=True)
    last_calculated_price = models.DecimalField(max_digits=17, decimal_places=2,
                                                verbose_name=_("Price without Tax "), blank=True, null=True)
    last_calculated_tax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Tax"),
                                            blank=True, null=True)
    customer = models.ForeignKey("Customer", verbose_name=_("Customer"))
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relscstaff", null=True)
    currency = models.ForeignKey("Currency", verbose_name=_("Currency"), blank=False, null=False)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    custom_date_field = models.DateTimeField(verbose_name=_("Custom Date/Time"), blank=True, null=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    last_modified_by = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"), related_name="db_lstscmodified", null=True,
                                         blank="True")
    template_set = models.ForeignKey("djangoUserExtension.DocumentTemplate", verbose_name=_("Referred Template"), null=True,
                                     blank=True)
    derived_from_sales_document = models.ForeignKey("SalesDocument", blank=True, null=True)
    last_print_date = models.DateTimeField(verbose_name=_("Last printed"), blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Sales Document')
        verbose_name_plural = _('Sales Documents')

    @staticmethod
    def objects_to_serialize(object_to_create_pdf):
        from koalixcrm.crm.contact.contact import PostalAddressForContact
        from koalixcrm.crm.contact.postaladdress import PostalAddress
        from koalixcrm.crm.product.currency import Currency
        from koalixcrm.crm.contact.contact import Contact
        from django.contrib import auth
        position_class = koalixcrm.crm.documents.salesdocumentposition.SalesDocumentPosition
        objects = list(type(object_to_create_pdf).objects.filter(id=object_to_create_pdf.id))
        objects += list(koalixcrm.crm.documents.salesdocument.SalesDocument.objects.filter(id=object_to_create_pdf.id))
        if isinstance(object_to_create_pdf, koalixcrm.crm.documents.purchaseorder.PurchaseOrder):
            objects += list(Contact.objects.filter(id=object_to_create_pdf.supplier.id))
            objects += list(PostalAddressForContact.objects.filter(person=object_to_create_pdf.supplier.id))
            for address in list(PostalAddressForContact.objects.filter(person=object_to_create_pdf.supplier.id)):
                objects += list(PostalAddress.objects.filter(id=address.id))
        else:
            objects += list(Contact.objects.filter(id=object_to_create_pdf.customer.id))
            objects += list(PostalAddressForContact.objects.filter(person=object_to_create_pdf.customer.id))
            for address in list(PostalAddressForContact.objects.filter(person=object_to_create_pdf.customer.id)):
                objects += list(PostalAddress.objects.filter(id=address.id))
        objects += list(TextParagraphInSalesDocument.objects.filter(sales_document=object_to_create_pdf.id))
        objects += list(Currency.objects.filter(id=object_to_create_pdf.currency.id))
        objects += SalesDocumentPosition.add_positions(position_class, object_to_create_pdf)
        objects += list(auth.models.User.objects.filter(id=object_to_create_pdf.staff.id))
        objects += UserExtension.objects_to_serialize(object_to_create_pdf)
        return objects

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

    def create_pdf(self, template_set):
        self.last_print_date = datetime.now()
        self.save()
        return koalixcrm.crm.documents.pdfexport.PDFExport.create_pdf(self, template_set)

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
    sales_document = models.ForeignKey("SalesDocument")

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Sales Documents')
        verbose_name_plural = _('Postal Address For Sales Documents')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class EmailAddressForSalesDocument(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    sales_document = models.ForeignKey("SalesDocument")

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Sales Documents')
        verbose_name_plural = _('Email Address For Sales Documents')

    def __str__(self):
        return str(self.email)


class PhoneAddressForSalesDocument(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    sales_document = models.ForeignKey("SalesDocument")

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
            'fields': (
            'prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode',
            'town', 'state', 'country', 'purpose')
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
    list_display = ('id', 'description', 'contract', 'customer', 'currency',
                    'staff', 'last_modified_by', 'last_calculated_price',
                    'last_calculated_tax', 'last_pricing_date',
                    'last_modification', 'last_print_date')
    list_display_links = ('id',)
    list_filter = ('customer', 'contract', 'currency', 'staff', 'last_modification')
    ordering = ('-id',)
    search_fields = ('contract__id', 'customer__name', 'currency__description')

    fieldsets = (
        (_('Sales Contract'), {
            'fields': ('contract', 'description', 'customer', 'currency', 'discount',
                       'staff', 'external_reference', 'template_set', 'custom_date_field')
        }),
    )
    save_as = True
    inlines = [SalesDocumentInlinePosition, SalesDocumentTextParagraph,
               SalesDocumentPostalAddress, SalesDocumentPhoneAddress,
               SalesDocumentEmailAddress]

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        obj.custom_date_field = date.today().__str__()
        return super(OptionSalesDocument, self).response_add(request, obj)

    def response_change(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionSalesDocument, self).response_change(request, obj)

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

    def create_quote(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self, request, obj,
                                           koalixcrm.crm.documents.quote.Quote,
                                           ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_quote.short_description = _("Create Quote")

    def create_invoice(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self, request, obj,
                                           koalixcrm.crm.documents.invoice.Invoice,
                                           ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_invoice.short_description = _("Create Invoice")

    def create_purchase_confirmation(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self, request, obj,
                                           koalixcrm.crm.documents.purchaseconfirmation.PurchaseConfirmation,
                                           ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_purchase_confirmation.short_description = _("Create Purchase Confirmation")

    def create_delivery_note(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self, request, obj,
                                           koalixcrm.crm.documents.deliverynote.DeliveryNote,
                                           ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_delivery_note.short_description = _("Create Delivery note")

    def create_payment_reminder(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self, request, obj,
                                           koalixcrm.crm.documents.paymentreminder.PaymentReminder,
                                           ("/admin/crm/"+obj.__class__.__name__.lower()+"/"))
            return response

    create_payment_reminder.short_description = _("Create Payment Reminder")

    def create_purchase_order(self, request, queryset):
        from koalixcrm.crm.views.newdocument import CreateNewDocumentView
        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(self, request, obj,
                                           koalixcrm.crm.documents.purchaseorder.PurchaseOrder,
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

