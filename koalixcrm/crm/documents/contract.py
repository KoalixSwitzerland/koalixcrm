# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.plugin import *
from koalixcrm.crm.contact.phone_address import PhoneAddress
from koalixcrm.crm.contact.email_address import EmailAddress
from koalixcrm.crm.contact.postal_address import PostalAddress
from koalixcrm.crm.documents.invoice import Invoice
from koalixcrm.crm.documents.quote import Quote
from koalixcrm.crm.documents.purchase_order import PurchaseOrder
from koalixcrm.global_support_functions import xstr
from koalixcrm.crm.const.purpose import *
from koalixcrm.crm.documents.invoice import InlineInvoice
from koalixcrm.crm.documents.quote import InlineQuote
from koalixcrm.crm.reporting.generic_project_link import InlineGenericProjectLink
from koalixcrm.crm.exceptions import *
from koalixcrm.djangoUserExtension.models import UserExtension
import koalixcrm.crm.documents.calculations
import koalixcrm.crm.documents.pdf_export
from rest_framework import serializers


class PostalAddressForContract(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contracts')
        verbose_name_plural = _('Postal Address For Contracts')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class PhoneAddressForContract(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contracts')
        verbose_name_plural = _('Phone Address For Contracts')

    def __str__(self):
        return str(self.phone)


class EmailAddressForContract(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contracts')
        verbose_name_plural = _('Email Address For Contracts')

    def __str__(self):
        return str(self.email)


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


class Contract(models.Model):
    id = models.BigAutoField(primary_key=True)
    staff = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              limit_choices_to={'is_staff': True},
                              verbose_name=_("Staff"),
                              related_name="db_relcontractstaff",
                              blank=True,
                              null=True)
    description = models.TextField(verbose_name=_("Description"))
    default_customer = models.ForeignKey("Customer",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Default Customer"),
                                         null=True,
                                         blank=True)
    default_supplier = models.ForeignKey("Supplier",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Default Supplier"),
                                         null=True,
                                         blank=True)
    default_currency = models.ForeignKey("Currency",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Default Currency"),
                                         blank=False,
                                         null=False)
    default_template_set = models.ForeignKey("djangoUserExtension.TemplateSet",
                                             on_delete=models.CASCADE,
                                             verbose_name=_("Default Template Set"),
                                             null=True,
                                             blank=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         related_name="db_contractlstmodified")

    class Meta:
        app_label = "crm"
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    def get_template_set(self, calling_model):
        if self.default_template_set:
            required_template_set = str(type(calling_model).__name__)
            return self.default_template_set.get_template_set(required_template_set)
        else:
            raise TemplateSetMissingInContract("The Contract has no Default Template Set selected")

    def create_from_reference(self, calling_model, staff):
        staff_user_extension = UserExtension.get_user_extension(staff.id)
        self.default_customer = calling_model
        self.default_currency = staff_user_extension.defaultCurrency
        self.default_template_set = staff_user_extension.defaultTemplateSet
        self.last_modified_by = staff
        self.staff = staff
        self.save()
        return self

    def create_invoice(self):
        invoice = Invoice()
        invoice.create_from_reference(self)
        return invoice

    def create_quote(self):
        quote = Quote()
        quote.create_from_reference(self)
        return quote

    def create_purchase_order(self):
        purchase_order = PurchaseOrder()
        purchase_order.create_from_reference(self)
        return purchase_order

    def __str__(self):
        return _("Contract") + " " + str(self.id)


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
               InlineInvoice,
               InlineGenericProjectLink]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("contractInlines"))

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


class ContractJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contract
        fields = ('id',
                  'description')
