from __future__ import annotations

from rest_framework import serializers

from koalixcrm.djangoUserExtension.models.document_template import (
    BalanceSheetTemplate,
    DespatchAdviceTemplate,
    InvoiceTemplate,
    MonthlyProjectSummaryTemplate,
    PaymentReminderTemplate,
    ProfitLossStatementTemplate,
    PurchaseOrderTemplate,
    QuotationTemplate,
    SalesOrderTemplate,
    WorkReportTemplate,
)


class OptionDocumentTemplateJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False, read_only=True)
    xsl_file = serializers.FileField(read_only=True)
    fop_config_file = serializers.FileField(read_only=True)
    logo = serializers.FileField(read_only=True)


class OptionInvoiceTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = InvoiceTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionQuotationTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = QuotationTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionDespatchAdviceTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = DespatchAdviceTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionPaymentReminderTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = PaymentReminderTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionPurchaseOrderTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = PurchaseOrderTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionSalesOrderTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = SalesOrderTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionProfitLossStatementTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = ProfitLossStatementTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionBalanceSheetTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = BalanceSheetTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = MonthlyProjectSummaryTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionWorkReportTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = WorkReportTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')
