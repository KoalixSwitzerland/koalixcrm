from rest_framework import serializers

from koalixcrm.djangoUserExtension.models.document_template import InvoiceTemplate
from koalixcrm.djangoUserExtension.models.document_template import QuoteTemplate
from koalixcrm.djangoUserExtension.models.document_template import DeliveryNoteTemplate
from koalixcrm.djangoUserExtension.models.document_template import PaymentReminderTemplate
from koalixcrm.djangoUserExtension.models.document_template import PurchaseOrderTemplate
from koalixcrm.djangoUserExtension.models.document_template import PurchaseConfirmationTemplate
from koalixcrm.djangoUserExtension.models.document_template import ProfitLossStatementTemplate
from koalixcrm.djangoUserExtension.models.document_template import BalanceSheetTemplate
from koalixcrm.djangoUserExtension.models.document_template import MonthlyProjectSummaryTemplate
from koalixcrm.djangoUserExtension.models.document_template import WorkReportTemplate


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


class OptionQuoteTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = QuoteTemplate
        fields = ('id',
                  'title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionDeliveryNoteTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = DeliveryNoteTemplate
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


class OptionPurchaseConfirmationTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = PurchaseConfirmationTemplate
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
