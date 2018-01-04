# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.purpose import *
from koalixcrm.globalSupportFunctions import xstr
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
    template_set = models.ForeignKey("djangoUserExtension.TemplateSet", verbose_name=_("Referred Template Set"), null=True,
                                     blank=True)

    last_print_date = models.DateTimeField(verbose_name=_("Last printed"), blank=True, null=True)

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


class TextParagraphInSalesContract(models.Model):
    sales_contract = models.ForeignKey("SalesContract")
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=2, choices=PURPOSESTEXTPARAGRAPHINDOCUMENTS)
    text_paragraph = models.TextField(verbose_name=_("Text"), blank=False, null=False)

    class Meta:
        app_label = "crm"
        verbose_name = _('TextParagraphInSalesContract')
        verbose_name_plural = _('TextParagraphsInSalesContract')

    def __str__(self):
        return str(self.id)