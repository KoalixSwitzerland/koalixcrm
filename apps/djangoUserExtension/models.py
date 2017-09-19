# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from filebrowser.fields import FileBrowseField
from apps.crm import models as crmmodels
from apps.djangoUserExtension.const.purpose import *


class XSLFile(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100, blank=True, null=True)
    xslfile = FileBrowseField(verbose_name=_("XSL File"), max_length=200)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('XSL File')
        verbose_name_plural = _('XSL Files')

    def __str__(self):
        return str(self.id) + ' ' + self.title


class UserExtension(models.Model):
    user = models.ForeignKey('auth.User')
    defaultTemplateSet = models.ForeignKey('TemplateSet')
    defaultCurrency = models.ForeignKey('crm.Currency')

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('User Extention')
        verbose_name_plural = _('User Extentions')

    def __str__(self):
        return str(self.id) + ' ' + self.user.__str__()


class TemplateSet(models.Model):
    organisationname = models.CharField(verbose_name=_("Name of the Organisation"), max_length=200)
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    invoiceXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Invoice"),
                                       related_name="db_reltemplateinvoice")
    quoteXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Quote"), related_name="db_reltemplatequote")
    purchaseorderXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Purchaseorder"),
                                             related_name="db_reltemplatepurchaseorder")
    purchaseconfirmationXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Purchase Confirmation"),
                                                    related_name="db_reltemplatepurchaseconfirmation")
    deilveryorderXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Deilvery Order"),
                                             related_name="db_reltemplatedeliveryorder")
    profitLossStatementXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Profit Loss Statement"),
                                                   related_name="db_reltemplateprofitlossstatement")
    balancesheetXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Balancesheet"),
                                            related_name="db_reltemplatebalancesheet")
    logo = FileBrowseField(verbose_name=_("Logo for the PDF generation"), blank=True, null=True, max_length=200)
    bankingaccountref = models.CharField(max_length=60, verbose_name=_("Reference to Banking Account"), blank=True,
                                         null=True)
    addresser = models.CharField(max_length=200, verbose_name=_("Addresser"), blank=True, null=True)
    fopConfigurationFile = FileBrowseField(verbose_name=_("FOP Configuration File"), blank=True, null=True,
                                           max_length=200)
    footerTextsalesorders = models.TextField(verbose_name=_("Footer Text On Salesorders"), blank=True, null=True)
    headerTextsalesorders = models.TextField(verbose_name=_("Header Text On Salesorders"), blank=True, null=True)
    headerTextpurchaseorders = models.TextField(verbose_name=_("Header Text On Purchaseorders"), blank=True, null=True)
    footerTextpurchaseorders = models.TextField(verbose_name=_("Footer Text On Purchaseorders"), blank=True, null=True)
    pagefooterleft = models.CharField(max_length=40, verbose_name=_("Page Footer Left"), blank=True, null=True)
    pagefootermiddle = models.CharField(max_length=40, verbose_name=_("Page Footer Middle"), blank=True, null=True)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Templateset')
        verbose_name_plural = _('Templatesets')

    def __str__(self):
        return str(self.id) + ' ' + self.title


class UserExtensionPostalAddress(crmmodels.PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __str__(self):
        return self.name + ' ' + self.prename

    class Meta:
        app_label = "djangoUserExtension"
        # app_label_koalix = _('Djang User Extention')
        verbose_name = _('Postal Address for User Extention')
        verbose_name_plural = _('Postal Address for User Extention')


class UserExtensionPhoneAddress(crmmodels.PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __str__(self):
        return self.phone

    class Meta:
        app_label = "djangoUserExtension"
        # app_label_koalix = _('Djang User Extention')
        verbose_name = _('Phonenumber for User Extention')
        verbose_name_plural = _('Phonenumber for User Extention')


class UserExtensionEmailAddress(crmmodels.EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __str__(self):
        return self.email

    class Meta:
        app_label = "djangoUserExtension"
        # app_label_koalix = _('Djang User Extention')
        verbose_name = _('Email Address for User Extention')
        verbose_name_plural = _('Email Address for User Extention')
