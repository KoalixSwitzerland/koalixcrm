# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.djangoUserExtension.models.text_paragraph import InlineTextParagraph
from koalixcrm.global_support_functions import xstr
from koalixcrm.core.exceptions import *
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm_utils.s3_storage import TemplateFileStorage


class DocumentTemplate(WorkspaceScopedModel):
    title = models.CharField(verbose_name=_("Title"),
                             max_length=100,
                             blank=True,
                             null=True)
    xsl_file = models.FileField(verbose_name=_("XSL File"),
                                storage=TemplateFileStorage,
                                upload_to="xsl/",
                                max_length=200)
    fop_config_file = models.FileField(verbose_name=_("FOP Configuration File"),
                                       storage=TemplateFileStorage,
                                       upload_to="fop_config/",
                                       blank=True,
                                       null=True,
                                       max_length=200)
    logo = models.FileField(verbose_name=_("Logo for the PDF generation"),
                            storage=TemplateFileStorage,
                            upload_to="logos/",
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


class QuotationTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Quotation template')
        verbose_name_plural = _('Quotation templates')


class DespatchAdviceTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Despatch advice template')
        verbose_name_plural = _('Despatch advice templates')


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


class SalesOrderTemplate(DocumentTemplate):
    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Sales order template')
        verbose_name_plural = _('Sales order templates')


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


class OptionDocumentTemplate(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    list_filter = ('workspace',)
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

