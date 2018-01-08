# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.purpose import *
from koalixcrm.globalSupportFunctions import xstr
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.documents.salescontractposition import SalesContractPosition
from koalixcrm.djangoUserExtension.models import TextParagraphInDocumentTemplate
from django.http import HttpResponseRedirect
from django.contrib import messages
from koalixcrm.plugin import *
from koalixcrm.crm.views import export_pdf
from koalixcrm.crm.documents.salescontractposition import SalesContractInlinePosition
from koalixcrm.crm.product.product import Product
import koalixcrm.crm.documents.calculations


class TextParagraphInSalesContract(models.Model):
    sales_contract = models.ForeignKey("SalesContract")
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=2, choices=PURPOSESTEXTPARAGRAPHINDOCUMENTS)
    text_paragraph = models.TextField(verbose_name=_("Text"), blank=False, null=False)

    def create_paragraph(self, default_paragraph, sales_contract):
        self.sales_contract = sales_contract
        self.purpose = default_paragraph.purpose
        self.text_paragraph = default_paragraph.text_paragraph
        self.save()
        return

    class Meta:
        app_label = "crm"
        verbose_name = _('TextParagraphInSalesContract')
        verbose_name_plural = _('TextParagraphsInSalesContract')

    def __str__(self):
        return str(self.id)


class SalesContract(models.Model):
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
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    last_modified_by = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"), related_name="db_lstscmodified", null=True,
                                         blank="True")
    template_set = models.ForeignKey("djangoUserExtension.DocumentTemplate", verbose_name=_("Referred Template"), null=True,
                                     blank=True)
    derived_from_sales_contract = models.ForeignKey("SalesContract", blank=True, null=True)
    last_print_date = models.DateTimeField(verbose_name=_("Last printed"), blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Sales Contract')
        verbose_name_plural = _('Sales Contracts')

    def is_complete_with_price(self):
        """ Checks whether the SalesContract is completed with a price, in case the
        SalesContract was not completed or the price calculation was not performed,
        the method returns false"""

        if self.last_pricing_date and self.last_calculated_price:
            return True
        else:
            return False

    def create_sales_contract(self, calling_model):
        self.staff = calling_model.staff
        if isinstance(calling_model, koalixcrm.crm.documents.contract.Contract):
            self.contract = calling_model
            self.customer = calling_model.default_customer
            self.currency = calling_model.default_currency
            self.description = calling_model.description
            self.template_set = calling_model.default_template_set.invoice_template
            self.discount = 0
        elif isinstance(calling_model, SalesContract):
            self.derived_from_sales_contract = calling_model
            self.contract = calling_model.contract
            self.customer = calling_model.customer
            self.currency = calling_model.currency
            self.discount = calling_model.discount
            self.description = calling_model.description

    def attach_text_paragraphs(self, calling_model):
        if isinstance(calling_model, koalixcrm.crm.documents.contract.Contract):
            invoice_template = calling_model.default_template_set.invoice_template
            default_paragraphs = TextParagraphInDocumentTemplate.objects.filter(document_template=invoice_template)
            for default_paragraph in list(default_paragraphs):
                invoice_paragraph = TextParagraphInSalesContract()
                invoice_paragraph.create_paragraph(default_paragraph, self)
        elif isinstance(calling_model, SalesContract):
            sales_contract_positions = SalesContractPosition.objects.filter(contract=calling_model.id)
            for sales_contract_position in list(sales_contract_positions):
                new_position = SalesContractPosition()
                new_position.create_position(sales_contract_position, self)
            contract = koalixcrm.crm.documents.contract.Contract.objects.filter(id=calling_model.contract.id)
            invoice_template = contract[0].default_template_set.invoice_template
            default_paragraphs = TextParagraphInDocumentTemplate.objects.filter(document_template=invoice_template)
            for default_paragraph in list(default_paragraphs):
                invoice_paragraph = TextParagraphInSalesContract()
                invoice_paragraph.create_paragraph(default_paragraph, self)

    def create_quote(self):
        quote = koalixcrm.crm.documents.quote.Quote()
        quote.create_quote(self)
        return quote

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

    def create_payment_reminder(self):
        payment_reminder = koalixcrm.crm.documents.paymentreminder.PaymentReminder()
        payment_reminder.create_payment_reminder(self)
        return payment_reminder

    def create_pdf(self):
        self.last_print_date = datetime.now()
        self.save()
        return koalixcrm.crm.documents.pdfexport.PDFExport.create_pdf(self)

    def get_fop_config_file(self):
        return self.template_set.fop_config_file

    def get_xsl_file(self):
        return self.template_set.xsl_file

    def __str__(self):
        return _("Sales Contract") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)


class PostalAddressForSalesContract(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey("SalesContract")

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contracts')
        verbose_name_plural = _('Postal Address For Contracts')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class EmailAddressForSalesContract(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey("SalesContract")

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contracts')
        verbose_name_plural = _('Email Address For Contracts')

    def __str__(self):
        return str(self.email)


class PhoneAddressForSalesContract(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey("SalesContract")

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contracts')
        verbose_name_plural = _('Phone Address For Contracts')

    def __str__(self):
        return str(self.phone)


class SalesContractTextParagraph(admin.StackedInline):
    model = TextParagraphInSalesContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('text_paragraph', 'purpose', )
        }),
    )
    allow_add = True


class SalesContractPostalAddress(admin.StackedInline):
    model = PostalAddressForSalesContract
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


class SalesContractPhoneAddress(admin.TabularInline):
    model = PhoneAddressForSalesContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class SalesContractEmailAddress(admin.TabularInline):
    model = EmailAddressForSalesContract
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class OptionSalesContract(admin.ModelAdmin):
    list_display = ('id', 'description', 'contract', 'customer', 'currency',
                    'staff', 'last_modified_by', 'last_calculated_price',
                    'last_calculated_tax', 'last_pricing_date',
                    'last_modification', 'last_print_date')
    list_display_links = ('id',)
    list_filter = ('customer', 'contract', 'currency', 'staff', 'last_modification')
    ordering = ('id',)
    search_fields = ('contract__id', 'customer__name', 'currency__description')

    fieldsets = (
        (_('Sales Contract'), {
            'fields': ('contract', 'description', 'customer', 'currency', 'discount',
                       'staff', 'external_reference', 'template_set')
        }),
    )
    save_as = True
    inlines = [SalesContractInlinePosition, SalesContractTextParagraph,
               SalesContractPostalAddress, SalesContractPhoneAddress,
               SalesContractEmailAddress]

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionSalesContract, self).response_add(request, obj)

    def response_change(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionSalesContract, self).response_change(request, obj)

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

    create_pdf.short_description = _("Create PDF")

    actions = ['create_purchase_confirmation','create_invoice',
               'create_delivery_note', 'create_pdf']
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteActions"))
