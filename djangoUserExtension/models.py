# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField

from const.purpose import *
from crm.models import PostalAddress, PhoneAddress, EmailAddress


class XSLFile(models.Model):
    title = models.CharField(verbose_name=trans("Title"), max_length=100, blank=True, null=True)
    xslfile = FileBrowseField(verbose_name=trans("XSL File"), max_length=200)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = trans('XSL File')
        verbose_name_plural = trans('XSL Files')

    def __unicode__(self):
        return str(self.id) + ' ' + self.title


class UserExtension(models.Model):
    user = models.ForeignKey('auth.User')
    defaultTemplateSet = models.ForeignKey('TemplateSet')
    defaultCurrency = models.ForeignKey('crm.Currency')

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = trans('User Extension')
        verbose_name_plural = trans('User Extensions')

    def __unicode__(self):
        return str(self.id) + ' ' + self.user.__unicode__()


class TemplateSet(models.Model):
    organisationname = models.CharField(verbose_name=trans("Name of the Organisation"), max_length=200)
    title = models.CharField(verbose_name=trans("Title"), max_length=100)
    invoiceXSLFile = models.ForeignKey(XSLFile, verbose_name=trans("XSL File for Invoice"),
                                       related_name="db_reltemplateinvoice")
    quoteXSLFile = models.ForeignKey(XSLFile, verbose_name=trans("XSL File for Quote"),
                                     related_name="db_reltemplatequote")
    purchaseorderXSLFile = models.ForeignKey(XSLFile, verbose_name=trans("XSL File for Purchaseorder"),
                                             related_name="db_reltemplatepurchaseorder")
    purchaseconfirmationXSLFile = models.ForeignKey(XSLFile, verbose_name=trans("XSL File for Purchase Confirmation"),
                                                    related_name="db_reltemplatepurchaseconfirmation")
    deilveryorderXSLFile = models.ForeignKey(XSLFile, verbose_name=trans("XSL File for Deilvery Order"),
                                             related_name="db_reltemplatedeliveryorder")
    profitLossStatementXSLFile = models.ForeignKey(XSLFile, verbose_name=trans("XSL File for Profit Loss Statement"),
                                                   related_name="db_reltemplateprofitlossstatement")
    balancesheetXSLFile = models.ForeignKey(XSLFile, verbose_name=trans("XSL File for Balancesheet"),
                                            related_name="db_reltemplatebalancesheet")
    logo = FileBrowseField(verbose_name=trans("Logo for the PDF generation"), blank=True, null=True, max_length=200)
    bankingaccountref = models.CharField(max_length=60, verbose_name=trans("Reference to Banking Account"), blank=True,
                                         null=True)
    addresser = models.CharField(max_length=200, verbose_name=trans("Addresser"), blank=True, null=True)
    fopConfigurationFile = FileBrowseField(verbose_name=trans("FOP Configuration File"), blank=True, null=True,
                                           max_length=200)
    footerTextsalesorders = models.TextField(verbose_name=trans("Footer Text On Salesorders"), blank=True, null=True)
    headerTextsalesorders = models.TextField(verbose_name=trans("Header Text On Salesorders"), blank=True, null=True)
    headerTextpurchaseorders = models.TextField(verbose_name=trans("Header Text On Purchaseorders"), blank=True,
                                                null=True)
    footerTextpurchaseorders = models.TextField(verbose_name=trans("Footer Text On Purchaseorders"), blank=True,
                                                null=True)
    pagefooterleft = models.CharField(max_length=40, verbose_name=trans("Page Footer Left"), blank=True, null=True)
    pagefootermiddle = models.CharField(max_length=40, verbose_name=trans("Page Footer Middle"), blank=True, null=True)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = trans('Templateset')
        verbose_name_plural = trans('Templatesets')

    def __unicode__(self):
        return str(self.id) + ' ' + self.title


class UserExtensionPostalAddress(PostalAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __unicode__(self):
        return self.name + ' ' + self.prename

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = trans('Postal Address for User Extention')
        verbose_name_plural = trans('Postal Address for User Extention')


class UserExtensionPhoneAddress(PhoneAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __unicode__(self):
        return self.phone

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = trans('Phonenumber for User Extention')
        verbose_name_plural = trans('Phonenumber for User Extention')


class UserExtensionEmailAddress(EmailAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __unicode__(self):
        return self.email

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = trans('Email Address for User Extention')
        verbose_name_plural = trans('Email Address for User Extention')
