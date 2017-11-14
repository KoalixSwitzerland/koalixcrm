# -*- coding: utf-8 -*-

from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.purpose import *
from koalixcrm.globalSupportFunctions import xstr
from koalixcrm.crm.documents.salescontractposition import SalesContractPosition
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress


class SalesContract(models.Model):
    contract = models.ForeignKey("Contract", verbose_name=_('Contract'))
    externalReference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=_("Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2,
                                              verbose_name=_("Price without Tax "), blank=True, null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Tax"),
                                            blank=True, null=True)
    customer = models.ForeignKey("Customer", verbose_name=_("Customer"))
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relscstaff", null=True)
    currency = models.ForeignKey("Currency", verbose_name=_("Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_lstscmodified", null=True,
                                       blank="True")
    template_set = models.ForeignKey("djangoUserExtension.TemplateSet", verbose_name=_("Default Supplier"), null=True,
                                     blank=True)

    last_print_date = models.DateTimeField(verbose_name=_("Last printed"), blank=True, null=True)

    def recalculate_prices(self, pricingDate):
        """Performs a price recalculation on the SalesContract.
        The calculated price is stored in the lastCalculatedPrice and lastCalculatedTax.
        The date when the price was calculated is stored in lastPricingDate

        Args:
            no arguments

        Returns:
            1 (Boolean) when passed
            0 (Boolean) when failed

        Raises:
            Can trow Product.NoPriceFound when Product Price could not be found"""

        price = 0
        tax = 0
        positions = SalesContractPosition.objects.filter(contract=self.id)
        if positions.exists():
            for position in positions:
                price += position.recalculate_prices(pricingDate, self.customer, self.currency)
                tax += position.recalculateTax(self.currency)
            if isinstance(self.discount, Decimal):
                price = int(price * (1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                tax = int(tax * (1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
        self.lastCalculatedPrice = price
        self.lastCalculatedTax = tax
        self.lastPricingDate = pricingDate
        self.save()
        return 1

    class Meta:
        app_label = "crm"
        verbose_name = _('Sales Contract')
        verbose_name_plural = _('Sales Contracts')

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