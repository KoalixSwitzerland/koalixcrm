# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _

from filebrowser.fields import FileBrowseField

from koalixcrm.djangoUserExtension.user_extension.text_paragraph import InlineTextParagraph
from koalixcrm.global_support_functions import xstr
from koalixcrm.crm.exceptions import *


class DocumentTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=100,
                             blank=True,
                             null=True)
    xsl_file = FileBrowseField(verbose_name=_("XSL File"),
                               max_length=200)
    fop_config_file = FileBrowseField(verbose_name=_("FOP Configuration File"),
                                      blank=True,
                                      null=True,
                                      max_length=200)
    logo = FileBrowseField(verbose_name=_("Logo for the PDF generation"),
                           blank=True,
                           null=True,
                           max_length=200)

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


class MonthlyProjectSummaryTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Monthly project summary template')
        verbose_name_plural = _('Monthly project summary templates')


class WorkReportTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Work report template')
        verbose_name_plural = _('Work report templates')


class OptionDocumentTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title',
                       'xsl_file',
                       'fop_config_file',
                       'logo')
        }),
    )
    inlines = [InlineTextParagraph]

