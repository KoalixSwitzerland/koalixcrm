# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.global_support_functions import xstr
from koalixcrm.core.exceptions import *


class TemplateSet(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=100)
    invoice_template = models.ForeignKey("InvoiceTemplate",
                                         on_delete=models.CASCADE,
                                         blank=True,
                                         null=True)
    quotation_template = models.ForeignKey("QuotationTemplate",
                                           on_delete=models.CASCADE,
                                           blank=True,
                                           null=True)
    despatch_advice_template = models.ForeignKey("DespatchAdviceTemplate",
                                                 on_delete=models.CASCADE,
                                                 blank=True, null=True)
    payment_reminder_template = models.ForeignKey("PaymentReminderTemplate",
                                                  on_delete=models.CASCADE,
                                                  blank=True,
                                                  null=True)
    sales_order_template = models.ForeignKey("SalesOrderTemplate",
                                             on_delete=models.CASCADE,
                                             blank=True, null=True)
    purchase_order_template = models.ForeignKey("PurchaseOrderTemplate",
                                                on_delete=models.CASCADE,
                                                blank=True,
                                                null=True)
    profit_loss_statement_template = models.ForeignKey("ProfitLossStatementTemplate",
                                                       on_delete=models.CASCADE,
                                                       blank=True, null=True)
    balance_sheet_statement_template = models.ForeignKey("BalanceSheetTemplate",
                                                         on_delete=models.CASCADE,
                                                         blank=True,
                                                         null=True)
    monthly_project_summary_template = models.ForeignKey("MonthlyProjectSummaryTemplate",
                                                         on_delete=models.CASCADE,
                                                         blank=True,
                                                         null=True)
    work_report_template = models.ForeignKey("WorkReportTemplate",
                                             on_delete=models.CASCADE,
                                             blank=True,
                                             null=True)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Template-set')
        verbose_name_plural = _('Template-sets')

    def __str__(self):
        return xstr(self.id) + ' ' + xstr(self.title)

    def get_template_set(self, required_template_set):
        mapping_class_to_templates = {"Invoice": self.invoice_template,
                                      "Quotation": self.quotation_template,
                                      "DespatchAdvice": self.despatch_advice_template,
                                      "PaymentReminder": self.payment_reminder_template,
                                      "SalesOrder": self.sales_order_template,
                                      "PurchaseOrder": self.purchase_order_template,
                                      "ProfitLossStatement": self.profit_loss_statement_template,
                                      "BalanceSheet": self.balance_sheet_statement_template,
                                      "MonthlyProjectSummaryTemplate": self.monthly_project_summary_template,
                                      "WorkReport": self.work_report_template}
        try:
            if mapping_class_to_templates[required_template_set]:
                return mapping_class_to_templates[required_template_set]
            else:
                raise TemplateMissingInTemplateSet("The TemplateSet does not contain a template for " +
                                                   required_template_set)
        except KeyError:
            raise IncorrectUseOfAPI("")


class OptionTemplateSet(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title',
                       'invoice_template',
                       'quotation_template',
                       'despatch_advice_template',
                       'payment_reminder_template',
                       'sales_order_template',
                       'purchase_order_template',
                       'profit_loss_statement_template',
                       'balance_sheet_statement_template',
                       'monthly_project_summary_template',
                       'work_report_template')
        }),
    )
