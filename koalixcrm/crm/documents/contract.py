# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.documents.invoice import Invoice
from koalixcrm.crm.documents.quote import Quote
from koalixcrm.crm.documents.purchaseorder import PurchaseOrder
from koalixcrm.globalSupportFunctions import xstr
from koalixcrm.crm.const.purpose import *

class Contract(models.Model):
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relcontractstaff", null=True)
    description = models.TextField(verbose_name=_("Description"))
    defaultcustomer = models.ForeignKey("Customer", verbose_name=_("Default Customer"), null=True, blank=True)
    defaultSupplier = models.ForeignKey("Supplier", verbose_name=_("Default Supplier"), null=True, blank=True)
    defaultcurrency = models.ForeignKey("Currency", verbose_name=_("Default Currency"), blank=False, null=False)
    default_template_set = models.ForeignKey("djangoUserExtension.TemplateSet", verbose_name=_("Default Template Set"), null=False, blank=False)
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_contractlstmodified")

    class Meta:
        app_label = "crm"
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    def create_invoice(self):
        invoice = Invoice()
        invoice.create_invoice(self)
        return invoice

    def create_quote(self):
        quote = Quote()
        quote.create_quote(self)
        return quote

    def createPurchaseOrder(self):
        purchaseorder = PurchaseOrder()
        purchaseorder.contract = self
        purchaseorder.description = self.description
        purchaseorder.discount = 0
        purchaseorder.currency = self.defaultcurrency
        purchaseorder.supplier = self.defaultSupplier
        purchaseorder.status = 'C'
        purchaseorder.dateofcreation = date.today().__str__()
        # TODO: today is not correct it has to be replaced
        purchaseorder.save()
        return purchaseorder

    def __str__(self):
        return _("Contract") + " " + str(self.id)


class PostalAddressForContract(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(Contract)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contracts')
        verbose_name_plural = _('Postal Address For Contracts')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class PhoneAddressForContract(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(Contract)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contracts')
        verbose_name_plural = _('Phone Address For Contracts')

    def __str__(self):
        return str(self.phone)


class EmailAddressForContract(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(Contract)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contracts')
        verbose_name_plural = _('Email Address For Contracts')

    def __str__(self):
        return str(self.email)
