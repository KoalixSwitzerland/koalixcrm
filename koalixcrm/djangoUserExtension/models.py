# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from filebrowser.fields import FileBrowseField
from koalixcrm import crm
from koalixcrm.djangoUserExtension.const.purpose import *
from koalixcrm.crm.const.purpose import *
from koalixcrm.globalSupportFunctions import xstr
from koalixcrm.crm.exceptions import *


class UserExtension(models.Model):
    user = models.ForeignKey("auth.User", blank=False, null=False)
    defaultTemplateSet = models.ForeignKey("TemplateSet")
    defaultCurrency = models.ForeignKey("crm.Currency")

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('User Extention')
        verbose_name_plural = _('User Extentions')

    def __str__(self):
        return xstr(self.id) + ' ' + xstr(self.user.__str__())


class DocumentTemplate(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100, blank=True, null=True)
    xsl_file = FileBrowseField(verbose_name=_("XSL File"), max_length=200)
    fop_config_file = FileBrowseField(verbose_name=_("FOP Configuration File"), blank=True, null=True,
                                           max_length=200)
    logo = FileBrowseField(verbose_name=_("Logo for the PDF generation"), blank=True, null=True, max_length=200)

    def get_fop_config_file(self):
        if self.fop_config_file:
            return self.fop_config_file
        else:
            raise TemplateFOPConfigFileMissing(_("Fop Config File missing in Document Template"+str(self)))

    def get_xsl_file(self):
        if self.xsl_file:
            return self.xsl_file
        else:
            raise TemplateXSLTFileMissing(_("XSL Template missing in Document Template"+str(self)))

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Document template')
        verbose_name_plural = _('Document templates')

    def __str__(self):
        return xstr(self.id) + ' ' + xstr(self.title.__str__())


class InvoiceTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Invoice template')
        verbose_name_plural = _('Invoice templates')


class QuoteTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Quote template')
        verbose_name_plural = _('Quote templates')


class DeliveryNoteTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Delivery note template')
        verbose_name_plural = _('Delivery note templates')


class PaymentReminderTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Payment reminder template')
        verbose_name_plural = _('Payment reminder templates')


class PurchaseOrderTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Purchase order template')
        verbose_name_plural = _('Purchase order templates')


class PurchaseConfirmationTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Purchase confirmation template')
        verbose_name_plural = _('Purchase confirmation templates')


class ProfitLossStatementTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Profit loss statement template')
        verbose_name_plural = _('Profit loss statement templates')


class BalanceSheetTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Balance sheet template')
        verbose_name_plural = _('Balance sheet templates')


class TemplateSet(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    invoice_template = models.ForeignKey("InvoiceTemplate", blank=True, null=True)
    quote_template = models.ForeignKey("QuoteTemplate", blank=True, null=True)
    delivery_note_template = models.ForeignKey("DeliveryNoteTemplate", blank=True, null=True)
    payment_reminder_template =models.ForeignKey("PaymentReminderTemplate", blank=True, null=True)
    purchase_confirmation_template = models.ForeignKey("PurchaseConfirmationTemplate", blank=True, null=True)
    purchase_order_template = models.ForeignKey("PurchaseOrderTemplate", blank=True, null=True)
    profit_loss_statement_template = models.ForeignKey("ProfitLossStatementTemplate", blank=True, null=True)
    balance_sheet_statement_template = models.ForeignKey("BalanceSheetTemplate", blank=True, null=True)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Templateset')
        verbose_name_plural = _('Templatesets')

    def __str__(self):
        return xstr(self.id) + ' ' + xstr(self.title)

    def get_template_set(self, required_template_set):
        mapping_class_to_templates = {"Invoice": self.invoice_template,
                                      "Quote": self.quote_template,
                                      "DeliveryNote": self.delivery_note_template,
                                      "PaymentReminder": self.payment_reminder_template,
                                      "PurchaseConfirmation": self.purchase_confirmation_template,
                                      "PurchaseOrder": self.purchase_order_template,
                                      "ProfitLossStatement": self.profit_loss_statement_template,
                                      "BalanceSheet": self.balance_sheet_statement_template}
        try:
            if mapping_class_to_templates[required_template_set]:
                return mapping_class_to_templates[required_template_set]
            else:
                raise TemplateMissingInTemplateSet("The TemplateSet does not contain a template for " +
                                         required_template_set)
        except KeyError:
            raise IncorrectUseOfAPI("")

class UserExtensionPostalAddress(crm.contact.postaladdress.PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __str__(self):
        return xstr(self.name) + ' ' + xstr(self.prename)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Postal Address for User Extention')
        verbose_name_plural = _('Postal Address for User Extention')


class UserExtensionPhoneAddress(crm.contact.phoneaddress.PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __str__(self):
        return xstr(self.phone)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Phonenumber for User Extention')
        verbose_name_plural = _('Phonenumber for User Extention')


class UserExtensionEmailAddress(crm.contact.emailaddress.EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __str__(self):
        return xstr(self.email)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Email Address for User Extention')
        verbose_name_plural = _('Email Address for User Extention')


class TextParagraphInDocumentTemplate(models.Model):
    document_template = models.ForeignKey(DocumentTemplate)
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=2, choices=PURPOSESTEXTPARAGRAPHINDOCUMENTS)
    text_paragraph = models.TextField(verbose_name=_("Text"), blank=False, null=False)

    class Meta:
        app_label = "crm"
        verbose_name = _('TextParagraphInDocumentTemplate')
        verbose_name_plural = _('TextParagraphInDocumentTemplates')

    def __str__(self):
        return str(self.id)