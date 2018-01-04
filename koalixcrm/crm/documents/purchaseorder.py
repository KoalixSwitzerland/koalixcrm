# -*- coding: utf-8 -*-

from datetime import *
from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.documents.salescontractposition import Position
from koalixcrm.crm.const.purpose import *
from koalixcrm.globalSupportFunctions import xstr

import koalixcrm.crm.documents.pdfexport


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


class PurchaseOrderPosition(Position):
    contract = models.ForeignKey("PurchaseOrder", verbose_name=_("Contract"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Purchaseorder Position')
        verbose_name_plural = _('Purchaseorder Positions')

    def __str__(self):
        return _("Purchaseorder Position") + ": " + str(self.id)


class PostalAddressForPurchaseOrder(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey("PurchaseOrder")

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contracts')
        verbose_name_plural = _('Postal Address For Contracts')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class PhoneAddressForPurchaseOrder(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey("PurchaseOrder")

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contracts')
        verbose_name_plural = _('Phone Address For Contracts')

    def __str__(self):
        return str(self.phone)


class EmailAddressForPurchaseOrder(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey("PurchaseOrder")

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contracts')
        verbose_name_plural = _('Email Address For Contracts')

    def __str__(self):
        return str(self.email)