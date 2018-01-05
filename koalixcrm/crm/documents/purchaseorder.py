# -*- coding: utf-8 -*-

from datetime import *
from decimal import Decimal

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _

from koalixcrm.plugin import *
from koalixcrm.crm.const.status import *
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.documents.salescontractposition import Position
from koalixcrm.crm.const.purpose import *
from koalixcrm.globalSupportFunctions import xstr
import koalixcrm.crm.documents.pdfexport


class PurchaseOrderPosition(Position):
    contract = models.ForeignKey("PurchaseOrder", verbose_name=_("Contract"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Purchaseorder Position')
        verbose_name_plural = _('Purchaseorder Positions')

    def __str__(self):
        return _("Purchaseorder Position") + ": " + str(self.id)


class PurchaseOrderInlinePosition(admin.TabularInline):
    model = PurchaseOrderPosition
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': (
            'position_number', 'quantity', 'unit', 'product', 'description', 'overwrite_product_price',
            'position_price_per_unit', 'sent_on')
        }),
    )
    allow_add = True


class PostalAddressForPurchaseOrder(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey("PurchaseOrder")

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contracts')
        verbose_name_plural = _('Postal Address For Contracts')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class PurchaseOrderPostalAddress(admin.StackedInline):
    model = PostalAddressForPurchaseOrder
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


class PhoneAddressForPurchaseOrder(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey("PurchaseOrder")

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contracts')
        verbose_name_plural = _('Phone Address For Contracts')

    def __str__(self):
        return str(self.phone)


class PurchaseOrderPhoneAddress(admin.TabularInline):
    model = PhoneAddressForPurchaseOrder
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class EmailAddressForPurchaseOrder(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey("PurchaseOrder")

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contracts')
        verbose_name_plural = _('Email Address For Contracts')

    def __str__(self):
        return str(self.email)


class PurchaseOrderEmailAddress(admin.TabularInline):
    model = EmailAddressForPurchaseOrder
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class PurchaseOrder(models.Model):
    contract = models.ForeignKey("Contract", verbose_name=_("Contract"))
    external_reference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True, null=True)
    supplier = models.ForeignKey("Supplier", verbose_name=_("Supplier"))
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    last_pricing_date = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    last_calculated_price = models.DecimalField(max_digits=17, decimal_places=2,
                                                verbose_name=_("Last Calculted Price With Tax"), blank=True, null=True)
    last_calculated_tax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"),
                                              blank=True, null=True)
    status = models.CharField(max_length=1, choices=PURCHASEORDERSTATUS)
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relpostaff", null=True)
    currency = models.ForeignKey("Currency", verbose_name=_("Currency"), blank=False, null=False)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    last_modified_by = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"), related_name="db_polstmodified")
    last_print_date = models.DateTimeField(verbose_name=_("Last printed"), blank=True, null=True)

    def recalculatePrices(self, pricingDate):
        price = 0
        tax = 0
        try:
            positions = PurchaseOrderPosition.objects.filter(contract=self.id)
            if isinstance(positions, PurchaseOrderPosition):
                if isinstance(self.discount, Decimal):
                    price = int(positions.recalculatePrices(pricingDate, self.customer, self.currency) * (
                    1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    tax = int(positions.recalculateTax(self.currency) * (
                    1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                else:
                    price = positions.recalculatePrices(pricingDate, self.customer, self.currency)
                    tax = positions.recalculateTax(self.currency)
            else:
                for position in positions:
                    if isinstance(self.discount, Decimal):
                        price += int(position.recalculate_prices(pricingDate, self.customer, self.currency) * (
                        1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                        tax += int(position.recalculateTax(self.currency) * (
                        1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    else:
                        price += position.recalculate_prices(pricingDate, self.customer, self.currency)
                        tax += position.recalculateTax(self.currency)
            self.last_calculated_price = price
            self.last_calculated_tax = tax
            self.last_pricing_date = pricingDate
            self.save()
            return 1
        except PurchaseOrder.DoesNotExist as e:
            print("ERROR " + e.__str__())
            print("Der Fehler trat beim File: " + self.sourcefile + " / Cell: " + listOfLines[0][
                                                                                  listOfLines[0].find("cell ") + 4:
                                                                                  listOfLines[0].find(
                                                                                      "(cellType ") - 1] + " auf!")
            exit()
            return 0

    def createPDF(self):
        self.last_print_date = datetime.now()
        self.save()
        return koalixcrm.crm.documents.pdfexport.PDFExport.createPDF(self)


    class Meta:
        app_label = "crm"
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Order')

    def __str__(self):
        return _("Purchase Order") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)



class OptionPurchaseOrder(admin.ModelAdmin):
    list_display = (
    'id', 'description', 'contract', 'supplier', 'status', 'currency', 'staff', 'last_modified_by',
    'last_calculated_price', 'last_calculated_tax', 'last_pricing_date', 'last_modification', 'last_print_date')
    list_display_links = ('id',)
    list_filter = ('supplier', 'contract', 'staff', 'status', 'currency', 'last_modification')
    ordering = ('id',)
    search_fields = ('contract__id', 'supplier__name', 'currency_description')

    fieldsets = (
        (_('Basics'), {
            'fields': ('contract', 'description', 'supplier', 'currency', 'status', 'external_reference')
        }),
    )

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionPurchaseOrder, self).response_add(request, obj)

    def response_change(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(request, new_object)
        return super(OptionPurchaseOrder, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, request, obj):
        try:
            Calculations.calculate_document_price(obj, date.today())
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

    def recalculatePrices(self, request, queryset):
        for obj in queryset:
            self.after_saving_model_and_related_inlines(request, obj)
        return;

    recalculatePrices.short_description = _("Recalculate Prices")

    def createPurchseOrderPDF(self, request, queryset):
        for obj in queryset:
            response = export_pdf(self, request, obj, "/admin/crm/purchaseorder/")
            return response

    createPurchseOrderPDF.short_description = _("Create PDF of Purchase Order")

    actions = ['createPurchseOrderPDF']
    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("purchaseOrderActions"))

    save_as = True
    inlines = [PurchaseOrderInlinePosition, PurchaseOrderPostalAddress, PurchaseOrderPhoneAddress,
               PurchaseOrderEmailAddress]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("purchaseOrderInlines"))


class InlinePurchaseOrder(admin.TabularInline):
    model = PurchaseOrder
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = (
    'description', 'contract', 'supplier', 'external_reference', 'status', 'last_pricing_date', 'last_calculated_price')
    fieldsets = (
        (_('Basics'), {
            'fields': ('description', 'contract', 'supplier', 'external_reference', 'status')
        }),
        (_('Advanced (not editable)'), {
            'classes': ('collapse',),
            'fields': ('last_pricing_date', 'last_calculated_price')
        }),
    )
    allow_add = False

